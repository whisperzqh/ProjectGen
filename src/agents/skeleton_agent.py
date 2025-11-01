from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableWithMessageHistory
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import ChatMessageHistory
from langchain_openai import ChatOpenAI
from langchain_deepseek import ChatDeepSeek
from prompts import *
from logger import get_logger
from utils import *
import logging
import os
import re
import json
from deepdiff import DeepDiff
from memory_manager.skeleton_memory import get_session_history
MAX_SKELETON_ITER=3

logger = get_logger()

log_prompt_runnable = RunnableLambda(log_input)
log_output_runnable = RunnableLambda(log_output)
extract_code_block_runnable = RunnableLambda(lambda x: extract_code_block(x))
clean_history_runnable = RunnableLambda(clean_history)


skeleton_chain = RunnableWithMessageHistory(
    skeleton_prompt | log_prompt_runnable | llm | log_output_runnable | extract_code_block_runnable,
    get_session_history=get_session_history,
    input_messages_key="step",
    history_messages_key="history"
)

iter_arch_chain = RunnableWithMessageHistory(
    clean_history_runnable | iter_skeleton_prompt | log_prompt_runnable | llm | log_output_runnable | extract_code_block_runnable,
    get_session_history=get_session_history,
    input_messages_key="step",
    history_messages_key="history"
)


def skeleton_agent(state: dict) -> dict:
    dataset = state["dataset"]
    repo_name = state["repo_name"]
    repo_dir = state["repo_dir"]
    code_file_DAG = state["code_file_DAG"]
    latest_arch = state["latest_arch"]
    latest_skeleton = state.get("latest_skeleton", [])
    steps = state.get("skeleton_steps", 0)
    feedback = state.get("skeleton_feedback", "")
    session_id = f"skeleton_agent_{repo_name}" 
    
    steps += 1
    logger.info(f"==========SKELETON GENERATION IN STEP {steps}===========")
    

    file_nodes = []
    if isinstance(latest_arch, str):
        try:
            architecture = json.loads(latest_arch)
        except Exception as e:
            logger.error(f"latest_arch is not valid JSON: {e}")
            return state
    else:
        architecture = latest_arch

    for module in architecture:
        module_name = module.get("name", "")
        module_desc = module.get("description", "")
        files = module.get("files", [])
        for file_item in files:
            file_nodes.append({
                "file": file_item,
                "module": {
                    "name": module_name,
                    "description": module_desc
                }
            })

    file_nodes_sorted = file_nodes

    if steps == 1:
        context, inputs = [], []
        for file_item in file_nodes_sorted:
            logger.info(f"[skeleton generation] Processing file: {file_item['file']['path']}")
            result = skeleton_chain.invoke(
                {"file_item": file_item, "context": context, "step": steps},
                config={"configurable": {"session_id": session_id, "step": steps}}
            )
            file_item["skeleton_code"] = result
            context.append({"path":file_item["file"]["path"], "skeleton": result})
        
        memory = get_session_history(session_id)
        memory.save_context(
            {"step": steps},
            {"result": context}
        )
        
        
    else:
        memory = get_session_history(session_id)
        history_str = memory.load_memory_variables({"feedback": feedback})["history"]
        context = []
        for file_item in file_nodes_sorted:
            logger.info(f"[skeleton generation] Processing file: {file_item['file']['path']}")
            result = iter_arch_chain.invoke(
                {"previous_skeleton": latest_skeleton, "file_item": file_item, "context": context, "feedback": feedback, "step": steps, "history_str": history_str},
                config={"configurable": {"session_id": session_id, "step": steps, "feedback": feedback}}
            )
            file_item["skeleton_code"] = result
            context.append({"path":file_item["file"]["path"], "skeleton": result})
        
        if context != []:
            skeleton_diff = json.dumps(DeepDiff(latest_skeleton, context, ignore_order=True), indent=2, default=str)
            # logger.info(f"[skeleton diff]:\n{skeleton_diff}")
        
        memory = get_session_history(session_id)
        memory.save_context(
            {"step": steps, "previous_skeleton": latest_skeleton, "feedback": feedback},
            {"result": context, "skeleton_diff": skeleton_diff if context != [] else ""}
        )
        
    latest_skeleton = context
    
    with open(f"{repo_dir}/tmp_files/skeleton_{steps}.json", "w", encoding="utf-8") as f:
        json.dump(latest_skeleton, f, indent=2, ensure_ascii=False)

    

    return {
        **state,
        "repo_name": repo_name,
        "repo_dir": repo_dir,
        "code_file_DAG": code_file_DAG,
        "file_nodes_sorted": file_nodes_sorted,
        "latest_arch": latest_arch,
        "latest_skeleton": latest_skeleton,
        "skeleton_steps": steps,
        "dataset": dataset
    }
