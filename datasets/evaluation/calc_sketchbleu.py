import json

from codebleu.codebleu import calc_repobleu
from pathlib import Path
import argparse
from loguru import logger
from tokenize import tokenize, NUMBER, STRING, NAME, OP
from io import BytesIO
import csv
import os


def list_py_files(root: Path, exclude_names=("acceptance_tests", "unit_tests", "check_tests", "examples", "test", "docs")):
    files = []
    if not root.exists():
        return files
    exclude = set(n.lower() for n in exclude_names)
    for p in root.rglob("*.py"):
        if any(part.lower() in exclude for part in p.parts):
            continue
        files.append(p)
    return files


def tokenize_code(code):
    """Tokenize source code and return the list of tokens."""
    tokens = []
    try:
        for tok in tokenize(BytesIO(code.encode("utf-8")).readline):
            if tok.type == 57:  # TokenInfo.NEWLINE is 57 in Python 3.8
                tokens.append("\n")
            elif tok.type == 58:  # TokenInfo.INDENT is 58 in Python 3.8
                tokens.append("    ")
            elif tok.type == 59:  # TokenInfo.DEDENT is 59 in Python 3.8
                pass
            else:
                tokens.append(tok.string)
    except:
        pass
    return tokens


if __name__ == "__main__":
    ref = '../CodeProjectEval'
    pred = '../../CodeProjectEval_outputs'

    repo_list = [d for d in os.listdir(pred) if os.path.isdir(os.path.join(pred, d))]
    
    
    with open(f'{pred}/sketchbleu.jsonl', 'a') as f:
        for repo in repo_list:
            repo_pred = f'{pred}/{repo}'
            repo_ref = f'{ref}/{repo}'
            repo_name = repo
            res = calc_repobleu(
                [Path(repo_ref)], [Path(repo_pred)], "python", tokenizer=tokenize_code
            )
            logger.info(f"{repo}: {res}")
            
            ref_py_files = list_py_files(Path(repo_ref))
            pred_py_files = list_py_files(Path(repo_pred))

            print("ref files:", ref_py_files)
            print("pred files:", pred_py_files)
            

            logger.info(res)
            
            item = {
                "repo": repo_name,
                "ref_len": len(ref_py_files),
                "pred_len": len(pred_py_files),
                "bleu": res,
                "ref_py_files": str(ref_py_files),
                "pred_py_files": str(pred_py_files),
            }
            f.write(json.dumps(item) + "\n")