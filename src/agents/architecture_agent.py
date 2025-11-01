from langchain.chains import LLMChain
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
from json_repair import repair_json
from deepdiff import DeepDiff
from memory_manager.arch_memory import get_session_history

MAX_ARCH_ITER = 3

logger = get_logger()

def extract_arch_json(text, output_file) -> bool:
    if hasattr(text, "to_string"):
        text = text.to_string()
    elif hasattr(text, "content"):
        text = text.content
    else:
        text = str(text)
    try:
        cleaned = re.search(r"```json\s*(.*?)\s*```", text.strip(), flags=re.IGNORECASE| re.DOTALL)
        if cleaned:
            parsed_json = json.loads(cleaned.group(1))
        else:
            parsed_json = []
    except json.JSONDecodeError as e:
        try:
            repaired = repair_json(cleaned)
            parsed_json = json.loads(repaired)
        except Exception as e:
            return []

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(parsed_json, f, indent=2, ensure_ascii=False)

    return parsed_json


log_prompt_runnable = RunnableLambda(log_input)
log_output_runnable = RunnableLambda(log_output)
clean_history_runnable = RunnableLambda(clean_history)


def architecture_agent(state: dict) -> dict:
    dataset = state["dataset"]
    repo_name = state["repo_name"]
    repo_dir = state["repo_dir"]
    prd = state["user_input"]
    uml_class = state["uml_class"]
    uml_sequence = state["uml_sequence"]
    arch_design = state["arch_design"]
    code_file_DAG = state["code_file_DAG"]
    steps = state.get("arch_steps", 0)
    latest_arch = state.get("latest_arch", "")
    feedback = state.get("arch_feedback", "")
    session_id = f"architecture_agent_{repo_name}"  
    
    steps += 1
    logger.info(f"==========ARCHITECTURE GENERATION IN STEP {steps}===========")
    
    arch_json_path = f"{repo_dir}/tmp_files/architecture_{steps}.json"
    extract_json_runnable = RunnableLambda(lambda x: extract_arch_json(x, arch_json_path))


    if steps == 1:
        ssat_chain = RunnableWithMessageHistory(
            ssat_prompt | log_prompt_runnable | llm | log_output_runnable | extract_json_runnable,
            get_session_history=get_session_history,
            input_messages_key="prd",
            history_messages_key="history"
        )
        
        result = ssat_chain.invoke(
                {"prd": prd, "uml_class": uml_class, "uml_sequence": uml_sequence, "arch_design": arch_design, "step": steps},
                config={"configurable": {"session_id": session_id, "step": steps}}
            )
        
        memory = get_session_history(session_id)
        inputs = {
            "prd": prd,
            "uml_class": uml_class,
            "uml_sequence": uml_sequence,
            "arch_design": arch_design,
            "step": steps
        }
        memory.save_context(inputs, {"result": result})
        
    else:
        memory = get_session_history(session_id)
        history_str = memory.load_memory_variables({"feedback": feedback})["history"]

        iter_arch_chain = RunnableWithMessageHistory(
            clean_history_runnable | iter_arch_prompt | log_prompt_runnable | llm | log_output_runnable | extract_json_runnable,
            get_session_history=get_session_history,
            input_messages_key="latest_arch",
            history_messages_key="history"
        )
        
        result = iter_arch_chain.invoke(
            {"prd": prd, "uml_class": uml_class, "uml_sequence": uml_sequence, "arch_design": arch_design, "latest_arch": latest_arch, "feedback": feedback, "step": steps, "history_str": history_str},
            config={"configurable": {"session_id": session_id, "step": steps, "feedback": feedback}}
        )
        
        if result != None:
            arch_diff = json.dumps(DeepDiff(latest_arch, result, ignore_order=True), indent=2, default=str)
            
        memory = get_session_history(session_id) 
        inputs = {
            "prd": prd,
            "uml_class": uml_class,
            "uml_sequence": uml_sequence,
            "arch_design": arch_design,
            "latest_arch": latest_arch,
            "feedback": feedback,
            "step": steps
        }
        memory.save_context(inputs, {"result": result, "arch_diff": arch_diff if result != None else None})
        
    latest_arch = result
    

    return {
        **state,
        "repo_name": repo_name,
        "repo_dir": repo_dir,
        "requirement": prd,
        "uml_class" : uml_class,
        "uml_sequence" : uml_sequence,
        "arch_design" : arch_design,
        "code_file_DAG": code_file_DAG,
        "latest_arch": latest_arch,
        "arch_steps": steps,
        "dataset": dataset
    }
