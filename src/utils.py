from langchain_deepseek import ChatDeepSeek
from langchain_openai import ChatOpenAI
from logger import get_logger
import re
import os
import json
from typing import List, Dict, Union

logger = get_logger()


os.environ["OPENAI_API_KEY"] = ''
llm = ChatOpenAI(model_name="gpt-4o", temperature=0, top_p=1.0)

def log_input(x):
    if hasattr(x, "to_string"):
        content = x.to_string()
    elif hasattr(x, "content"):
        content = x.content
    else:
        content = str(x)
    # logger.info(f"[Prompt Input]:\n{content}")
    return x

def log_output(x):
    if hasattr(x, "to_string"):
        content = x.to_string()
    elif hasattr(x, "content"):
        content = x.content
    else:
        content = str(x)
    # logger.info(f"[Prompt Output]:\n{content}")
    return x

def extract_mermaid(text: str) -> str:
    # 保证 text 是字符串
    if hasattr(text, "to_string"):
        text = text.to_string()
    elif hasattr(text, "content"):
        text = text.content
    else:
        text = str(text)
    match = re.search(r"(```mermaid[\s\S]+?```)", text)
    return match.group(1).strip() if match else "no mermaid diagram found"

def get_coding_plan(code_file_DAG: Dict) -> List:
    def dfs(node):
        if node in gold_plan:
            return
        if node not in code_file_DAG or len(code_file_DAG[node]) == 0:
            gold_plan.append(node)
        else:
            for child in code_file_DAG[node]:
                dfs(child)
            if node not in gold_plan:
                gold_plan.append(node)

    gold_plan = []
    
    for k,v in code_file_DAG.items():
        if k in gold_plan:
            continue
        dfs(k)
    
    return gold_plan


def extract_code_block(text) -> str:
    if hasattr(text, "to_string"):
        text = text.to_string()
    elif hasattr(text, "content"):
        text = text.content
    else:
        text = str(text)
    match = re.search(r"```(?:\w+)?\s*([\s\S]*?)\s*```", text.strip(), flags=re.IGNORECASE| re.DOTALL)
    return match.group(1) if match else ""

def clean_history(input_dict):
    history = input_dict.get("history", [])
    cleaned = "\n\n".join([msg.content for msg in history if hasattr(msg, "content")])
    input_dict["history"] = cleaned
    return input_dict