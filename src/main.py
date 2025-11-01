from workflow import build_graph
import os
import json
from logger import get_logger
import argparse


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=str, required=False, default="CodeProjectEval")
    args = parser.parse_args()
    dataset = args.dataset
    
    app = build_graph()

    base_dir = '../datasets'
    dataset_dir = os.path.join(base_dir, dataset)
    
    repo_list = os.listdir(dataset_dir)
    try:
        repo_list.remove('.pytest_cache') 
        repo_list.remove('test_script.py') 
    except:
        pass
    repo_list.sort()
    
    os.makedirs(f'../{dataset}_outputs', exist_ok=True)
    log_path = f'../{dataset}_outputs/test_log.log'
    logger = get_logger(log_path)
    
    for repo_name in repo_list:
        logger.info(f"Processing repository: {repo_name}")
        os.makedirs(f'../{dataset}_outputs/{repo_name}/tmp_files', exist_ok=True)
        repo_dir = os.path.join(dataset_dir, repo_name)
        repo_config = json.load(open(os.path.join(repo_dir, "config.json"), "r"))
        
        code_file_DAG = repo_config['code_file_DAG'] if 'code_file_DAG' in repo_config else []
        
        requirement = open(os.path.join(repo_dir, repo_config['PRD']), "r").read()
        if dataset == 'DevBench':
            uml_class = open(os.path.join(repo_dir, repo_config['UML_class']), "r").read()
            uml_sequence = open(os.path.join(repo_dir, repo_config['UML_sequence']), "r").read()
        if dataset == 'CodeProjectEval':
            for i in repo_config['UML']:
                if 'pyreverse' in i:
                    uml_class = open(os.path.join(repo_dir, i), "r").read()
                    break
            uml_sequence = ""
        arch_design = open(os.path.join(repo_dir, repo_config['architecture_design']), "r").read()

        final_state = app.invoke({"user_input": requirement, "uml_class": uml_class, "uml_sequence": "", "arch_design": arch_design, 
                                    "repo_name": repo_name, "code_file_DAG": code_file_DAG, "repo_dir": f'../{dataset}_outputs/{repo_name}', "dataset": dataset},
                                    config={"recursion_limit": 50})

        