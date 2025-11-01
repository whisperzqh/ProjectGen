from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_deepseek import ChatDeepSeek
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import ChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from agents.code_agent import MAX_CODE_ITER
from prompts import *
from logger import get_logger
import os
import json
import subprocess
from agents.test import Test
from utils import *
from json_repair import repair_json

logger = get_logger()


def extract_fix_json(text) -> bool:
    if hasattr(text, "to_string"):
        text = text.to_string()
    elif hasattr(text, "content"):
        text = text.content
    else:
        text = str(text)
        
    start = text.find('[')
    if start == -1:
        return []
    bracket_count = 0
    for i in range(start, len(text)):
        if text[i] == '[':
            bracket_count += 1
        elif text[i] == ']':
            bracket_count -= 1

        if bracket_count == 0:
            end = i + 1
            json_str = text[start:end]
            try:
                return json.loads(json_str)
            except json.JSONDecodeError as e:
                try:
                    repaired = repair_json(json_str)
                    return json.loads(repaired)
                except Exception as e:
                    logger.error(f"Failed to parse or repair JSON: {e}")
                    return []
    return []


def write_code_to_files(latest_code, repo_dir):
    written_files = []
    if isinstance(latest_code, str):
        try:
            code_data = json.loads(latest_code)
        except Exception:
            return False, []
    else:
        code_data = latest_code
    for item in code_data:
        file_path = os.path.join(repo_dir, item["path"])
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(item["code"])
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


def get_session_history(session_id: str):
    return ChatMessageHistory()

log_prompt_runnable = RunnableLambda(log_input)
log_output_runnable = RunnableLambda(log_output)
extract_json_runnable = RunnableLambda(lambda x: extract_fix_json(x))


judge_code_chain = RunnableWithMessageHistory(
    check_code_prompt | log_prompt_runnable | llm | log_output_runnable | extract_json_runnable,
    get_session_history=get_session_history,
    input_messages_key="error_log",             
    history_messages_key="history",       
)


def judge_code_agent(state: dict) -> dict: 
    dataset = state["dataset"]
    repo_name = state["repo_name"]
    repo_dir = state["repo_dir"]
    latest_code = state["latest_code"]
    steps = state["code_steps"]
    test_status = state.get("test_status", {})
    session_id = "code_judge_agent"

    def run_pytest_and_collect(repo_name, repo_dir):
        t = Test(f"../datasets/{dataset}/{repo_name}", repo_dir, logger=logger)
        test_output, passed, total = t.test(repo_dir, "python")
        return test_output, passed, total

    logger.info(f"==========CODE CHECK IN STEP {steps}===========")

    write_ok, written_files = write_code_to_files(latest_code, repo_dir)
    if not write_ok:
        feedback = "Code JSON parsing failed."
        logger.info(f"[decision]: False")
        logger.info(f"[feedback]: {feedback}")
        return {
            **state,
            "code_decision": False,
            "code_feedback": feedback,
            "code_steps": steps,
        }

    test_output, passed, total = run_pytest_and_collect(repo_name, repo_dir)
    test_status[f"step_{steps}"]= f"passed {passed} out of {total}"
    
    if passed == total and total > 0:
        feedback = "All unit tests passed.\n"
        code_decision = True
        logger.info(f"[decision]: True")
        logger.info(f"[feedback]: {feedback}")
        code_decision = True
    else:
        result = judge_code_chain.invoke(
            {"error_log": test_output},
            config={"configurable": {"session_id": session_id}}
        )
        
        feedback = f"Code failed the unit tests. Only pass {passed} out of {total} test cases.\n\nHere are some suggestions:\n\n"
        feedback += json.dumps(result, indent=2, ensure_ascii=False)
        code_decision = False
        logger.info(f"[decision]: False")
        logger.info(f"[feedback]: {feedback}")
        
        if steps >= MAX_CODE_ITER:
            feedback = "Maximum CODE iterations reached, forcing approval.\n"
            code_decision = True

        

    return {
        **state,
        "code_decision": code_decision,
        "code_feedback": feedback,
        "test_status": test_status,
        "code_steps": steps,
        "dataset": dataset
    }


