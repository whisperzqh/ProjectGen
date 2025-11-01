from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI
from langchain_deepseek import ChatDeepSeek
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import ChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.messages import AIMessage, HumanMessage
from agents.skeleton_agent import MAX_SKELETON_ITER
from prompts import *
import os
from logger import get_logger
from utils import *
import logging
import re
import py_compile

logger = get_logger()

arch_judge_memory = ConversationBufferMemory(
    memory_key="history", input_key="architecture", return_messages=True
)


def parse_judge_output(text: str) -> dict:
    result = {}
    patterns = {
        "feedback": {
            "directory_structure_matching": r"Directory Structure Matching:\s*(.*)",
            "interface_and_call_relationship_matching": r"Interface & Call Relationship Matching:\s*(.*)"
        },
        "final_score": r"Final Score:\s*\**(\d+)\**"
    }

    result["feedback"] = {}
    for fb_key, fb_pattern in patterns["feedback"].items():
        match = re.search(fb_pattern, text, re.IGNORECASE)
        if match:
            result["feedback"][fb_key] = match.group(1).strip()
        else:
            result["feedback"][fb_key] = ""

    match = re.search(patterns["final_score"], text, re.IGNORECASE)
    if match:
        result["final_score"] = int(match.group(1))
    else:
        result["final_score"] = 0

    return result

postprocess_runnable = RunnableLambda(parse_judge_output)


def write_skeleton_to_files(latest_skeleton, repo_dir):
    written_files = []
    if isinstance(latest_skeleton, str):
        try:
            skeleton_data = json.loads(latest_skeleton)
        except Exception:
            return False, []
    else:
        skeleton_data = latest_skeleton
    for item in skeleton_data:
        file_path = os.path.join(repo_dir, item["path"])
        
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(item["skeleton"])
        except Exception as e:
            logger.error(f"Error writing file {file_path}: {e}")
        written_files.append(file_path)
    return True, written_files


def remove_written_files(written_files):
    for f in written_files:
        try:
            os.remove(f)
        except Exception:
            pass


def check_python_compile(repo_dir):
    error_msgs = []
    all_pass = True
    for root, dirs, files in os.walk(repo_dir):
        for fname in files:
            if fname.endswith(".py"):
                fpath = os.path.join(root, fname)
                try:
                    py_compile.compile(fpath, doraise=True)
                except py_compile.PyCompileError as e:
                    all_pass = False
                    error_msgs.append(f"{fpath}:\n{e.msg}")
    return all_pass, error_msgs


def get_session_history(session_id: str):
    return ChatMessageHistory()

log_prompt_runnable = RunnableLambda(log_input)
log_output_runnable = RunnableLambda(log_output)

judge_skeleton_chain = RunnableWithMessageHistory(
    check_skeleton_prompt | log_prompt_runnable | llm | log_output_runnable | StrOutputParser() | postprocess_runnable,
    get_session_history=get_session_history,
    input_messages_key="skeleton",             
    history_messages_key="history",        
)

def judge_skeleton_agent(state: dict) -> dict:
    dataset = state["dataset"]
    repo_name = state["repo_name"]
    code_file_DAG = state["code_file_DAG"]
    repo_dir = state["repo_dir"]
    latest_arch = state["latest_arch"]
    latest_skeleton = state["latest_skeleton"]
    file_nodes_sorted = state["file_nodes_sorted"]
    steps = state["skeleton_steps"]
    session_id = "skeleton_judge_agent"
    
    logger.info(f"==========SKELETON CHECK IN STEP {steps}===========")
    
    write_ok, written_files = write_skeleton_to_files(latest_skeleton, repo_dir)
    if not write_ok:
        feed_back = "Skeleton JSON parsing failed."
        logger.info(f"[decision]: False")
        logger.info(f"[feedback]: {feed_back}")
        return {
            **state,
            "repo_name": repo_name,
            "repo_dir": repo_dir,
            "code_file_DAG": code_file_DAG,
            "file_nodes_sorted": file_nodes_sorted,
            "skeleton_decision": False,
            "skeleton_feedback": feed_back,
            "latest_skeleton": latest_skeleton,
            "skeleton_steps": steps,
            "dataset": dataset
        }

    compile_ok, compile_errors = check_python_compile(repo_dir)
    remove_written_files(written_files)
    if not compile_ok:
        feed_back = "Skeleton failed the Python compilation check. Please correct the syntax error.\n"
        feed_back += "\n".join(compile_errors)
        logger.info(f"[decision]: False")
        logger.info(f"[feedback]: {feed_back}")
        return {
            **state,
            "repo_name": repo_name,
            "repo_dir": repo_dir,
            "code_file_DAG": code_file_DAG,
            "file_nodes_sorted": file_nodes_sorted,
            "skeleton_decision": False,
            "skeleton_feedback": feed_back,
            "latest_skeleton": latest_skeleton,
            "skeleton_steps": steps,
            "dataset": dataset
        }
    

    result = judge_skeleton_chain.invoke(
        {"skeleton": latest_skeleton, "architecture": latest_arch},
        config={"configurable": {"session_id": session_id}}
    )

    feed_back = f"Final Score: {result['final_score']}\n"
    feed_back += "\n".join([f"{k}: {v}" for k, v in result["feedback"].items()])
    pass_score = 8
    if result["final_score"] >= pass_score:
        decision = True
    else:
        decision = False
    
    if steps >= MAX_SKELETON_ITER:
        decision = True  
        feed_back = "Maximum skeleton iterations reached, forcing approval.\n" + feed_back
        

    logger.info(f"[decision]: {decision}")
    logger.info(f"[feedback]: {feed_back}")

    return {
        **state,
        "repo_name": repo_name,
        "repo_dir": repo_dir,
        "code_file_DAG": code_file_DAG,
        "file_nodes_sorted": file_nodes_sorted,
        "skeleton_decision": decision,
        "skeleton_feedback": feed_back,
        "latest_skeleton": latest_skeleton,
        "skeleton_steps": steps,
        "dataset": dataset
    }