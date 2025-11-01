from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI
from langchain_deepseek import ChatDeepSeek
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.messages import AIMessage, HumanMessage
from agents.architecture_agent import MAX_ARCH_ITER
from prompts import *
import os
from logger import get_logger
from utils import *
import logging
import re

logger = get_logger()

arch_judge_memory = ConversationBufferMemory(
    memory_key="history", input_key="architecture", return_messages=True
)

def parse_judge_output(text: str) -> dict:
    result = {}
    patterns = {
        "feedback": {
            "requirement_coverage": r"Requirement Coverage:\s*(.*)",
            "consistency_with_provided_information": r"Consistency with Provided Information:\s*(.*)",
            "interface_consistency": r"Interface Consistency:\s*(.*)",
            "dependency_relations": r"Dependency Relations:\s*(.*)",
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

def get_session_history(session_id: str):
    return ChatMessageHistory()

log_prompt_runnable = RunnableLambda(log_input)
log_output_runnable = RunnableLambda(log_output)

judge_arch_chain = RunnableWithMessageHistory(
    check_arch_prompt | log_prompt_runnable | llm | log_output_runnable | StrOutputParser() | postprocess_runnable,
    get_session_history=get_session_history,
    input_messages_key="architecture",        
    history_messages_key="history",      
)

def judge_architecture_agent(state: dict) -> dict:
    dataset = state["dataset"]
    repo_name = state["repo_name"]
    code_file_DAG = state["code_file_DAG"]
    repo_dir = state["repo_dir"]
    latest_arch = state["latest_arch"]
    requirement = state["requirement"]
    uml_class = state["uml_class"]
    uml_sequence = state["uml_sequence"]
    arch_design = state["arch_design"]
    steps = state["arch_steps"]
    session_id = "arch_judge_agent"
    
    logger.info(f"==========ARCHITECTURE CHECK IN STEP {steps}===========")
    
    if latest_arch is None or latest_arch == "":
        decision = False
        feed_back = "No valid architecture generated in the previous step. Please ensure the output is strictly valid JSON."
    
    else:
        result = judge_arch_chain.invoke(
            {"requirement": requirement, "uml_class": uml_class, "uml_sequence": uml_sequence, "arch_design": arch_design, "architecture": latest_arch},
            config={"configurable": {"session_id": session_id}}
        )

        feed_back = f"Final Score: {result['final_score']}\n"
        feed_back += "\n".join([f"- {k.upper()}: {v}" for k, v in result["feedback"].items()])

        pass_score = 8
        if result["final_score"] >= pass_score:
            decision = True
        else:
            decision = False
        
        if steps >= MAX_ARCH_ITER:
            decision = True  
            feed_back = "Maximum architecture iterations reached, forcing approval.\n" + feed_back
            

    logger.info(f"[decision]: {decision}")
    logger.info(f"[feedback]: {feed_back}")

    return {
        **state,
        "repo_name": repo_name,
        "repo_dir": repo_dir,
        "code_file_DAG": code_file_DAG,
        "arch_decision": decision,
        "arch_feedback": feed_back,
        "requirement": requirement,
        "latest_arch": latest_arch,
        "arch_steps": steps,
        "dataset": dataset
    }