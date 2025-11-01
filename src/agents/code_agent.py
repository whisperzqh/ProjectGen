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
import os
import json
from typing import List, Dict, Union
import re
from utils import *
from json_repair import repair_json
from memory_manager.code_memory import get_session_history
from extract_api import extract_api
import difflib
from build_dependency_graph import reorder_skeleton_by_topo


MAX_CODE_ITER = 10
logger = get_logger()

def extract_code_json(text):
    # 保证 text 是字符串
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

    logger.info(f"Extracted JSON: {parsed_json}")
    logger.info(f"Type of Extracted JSON: {type(parsed_json)}")
    return parsed_json


log_prompt_runnable = RunnableLambda(log_input)
log_output_runnable = RunnableLambda(log_output)
extract_code_block_runnable = RunnableLambda(lambda x: extract_code_block(x))
extract_code_json_runnable = RunnableLambda(lambda x: extract_code_json(x))

def parse_sketch_output(output: str) -> list[dict]:
    if hasattr(output, "to_string"):
        content = output.to_string()
    elif hasattr(output, "content"):
        content = output.content
    else:
        content = str(output)
    try:
        if "```" in content:
            match = re.search(r"```(?:json)?\s*([\s\S]+?)\s*```", content)
            if match:
                content = match.group(1)

        parsed = json.loads(content)
        if isinstance(parsed, list):
            parsed_sorted = sorted(parsed, key=lambda x: x.get("generation_order", float("inf")))
            return parsed_sorted
        else:
            logger.warning("Parsed JSON is not a list.")
            return []
    except Exception as e:
        logger.error(f"Failed to parse JSON from sketch output: {e}")
        return []
    
parse_sketch_output_runnable = RunnableLambda(parse_sketch_output)


def save_file_output_to_jsonl(path: str, file_content: str, jsonl_path: str = "generated_files.jsonl"):
    if hasattr(file_content, "to_string"):
        content = file_content.to_string()
    elif hasattr(file_content, "content"):
        content = file_content.content
    else:
        content = str(file_content)
        
    if "```" in content:
        match = re.search(r"```(?:python)?\s*([\s\S]+?)\s*```", content)
        if match:
            content = match.group(1)
        
    record = {
        "path": path,
        "content": content.strip()
    }

    with open(jsonl_path, "w", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def extract_first_list(response: str):
    if hasattr(response, "to_string"):
        response = response.to_string()
    elif hasattr(response, "content"):
        response = response.content
    else:
        response = str(response)
    match = re.search(r"\[.*?\]", response, re.S)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            return []
    return []

extract_list_runnable = RunnableLambda(extract_first_list)

clean_history_runnable = RunnableLambda(clean_history)


code_chain = RunnableWithMessageHistory(
    code_prompt | log_prompt_runnable | llm | log_output_runnable | extract_code_block_runnable,
    get_session_history=get_session_history,
    input_messages_key="step",
    history_messages_key="history"
)


iter_code_chain = RunnableWithMessageHistory(
    clean_history_runnable | iter_code_prompt | log_prompt_runnable | llm | log_output_runnable | extract_code_json_runnable,
    get_session_history=get_session_history,
    input_messages_key="step",
    history_messages_key="history"
)

def code_agent(state: dict) -> dict:
    dataset = state["dataset"]
    repo_name = state["repo_name"]
    repo_dir = state["repo_dir"]
    latest_skeleton = state["latest_skeleton"]
    latest_code = state.get("latest_code", "")
    code_file_DAG = state["code_file_DAG"]
    file_nodes_sorted = state["file_nodes_sorted"]
    steps = state.get("code_steps", 0)
    feedback = state.get("code_feedback", "")
    test_status = state.get("test_status", {})
    session_id = f"code_agent_{repo_name}"
    
    steps+=1
    logger.info(f"==========CODE GENERATION IN STEP {steps}===========")
    
    
    if steps == 1:
        full_code = []

        logger.info(f"[code generation] Getting generation order.")
        
        try:
            latest_skeleton = reorder_skeleton_by_topo(latest_skeleton)
        except Exception as e:
            logger.error(f"Error in reordering skeleton by topo: {e}")
        
        for file_item in latest_skeleton:
            if file_item["path"].endswith(".py"):
                logger.info(f"[code generation] Processing file: {file_item['path']}")
                context = []
                if len(full_code) > 5:
                    for item in full_code[:-5]:
                        api_info = extract_api(item["code"], item["path"])
                        context.append({"path": item["path"], "code": api_info})
                    context.extend(full_code[-5:])
                else:
                    context = full_code
                
                result = code_chain.invoke(
                    {"file_item": file_item, "context": context},
                    config={"configurable": {"session_id": session_id, "step": steps}}
                )
                file_item["code"] = result
                full_code.append({"path": file_item["path"], "code": result})

                
        
        memory = get_session_history(session_id)
        memory.save_context(
            {"latest_skeleton": latest_skeleton, "test_status": test_status, "step": steps},
            {"result": full_code}
        )

    else:
        get_files_to_update_chain = RunnableWithMessageHistory(
            get_files_to_update_prompt | log_prompt_runnable | llm | log_output_runnable | extract_list_runnable,
            get_session_history=get_session_history,
            input_messages_key="feedback",
            history_messages_key="history"
        )
        
        files_to_update = get_files_to_update_chain.invoke(
            {"feedback": feedback, "context": latest_code},
            config={"configurable": {"session_id": "none"}}
        )
        
        context = []
        files_to_update_set = set(files_to_update) if files_to_update else set()
        for file_item in latest_code:
            if file_item["path"] not in files_to_update_set:
                api_info = extract_api(file_item["code"], file_item["path"])
                context.append({"path": file_item["path"], "code": api_info})

        full_code = []
        diff_code = []
        for file_item in latest_code:
            if files_to_update and file_item["path"] in files_to_update_set:
                logger.info(f"[code iteration] Processing file: {file_item['path']}")
                memory = get_session_history(session_id)
                history_str = memory.load_memory_variables({"feedback": feedback})["history"]
   
                result = iter_code_chain.invoke(
                    {"file_item": file_item, "feedback": feedback, "context": context, "history_str": history_str},
                    config={"configurable": {"session_id": session_id, "step": steps, "feedback": feedback}}
                )
       
                if isinstance(result, list) and len(result) > 0:
                    diff = difflib.unified_diff(
                        file_item["code"].splitlines(), 
                        result[0]["code"].splitlines(),
                        fromfile=file_item["path"], 
                        tofile=file_item["path"],
                    )
                    diff_code.append({"path": file_item["path"], "diff": "\n".join(diff)})
                    file_item = result[0]
                else:
                    diff_code.append({"path": file_item["path"], "diff": "No valid diff"})
                
            full_code.append({"path":file_item["path"], "code": file_item["code"]})
            context.append({"path":file_item["path"], "code": extract_api(file_item["code"], file_item["path"])})
            
        memory = get_session_history(session_id)
        memory.save_context(
            {"latest_code": latest_code, "feedback": feedback, "test_status": test_status, "step": steps},
            {"result": full_code, "diff_code": diff_code}
        )
    
    latest_code = full_code
    with open(f"{repo_dir}/tmp_files/generated_code_{steps}.jsonl", "w", encoding="utf-8") as f:
        for item in full_code:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")


    return {
        **state,
        "latest_code": latest_code,
        "code_steps": steps,
        "test_status": test_status,
        "dataset": dataset
    }
