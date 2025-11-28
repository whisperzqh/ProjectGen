import subprocess
import os
import json
import shutil
import logging
import re


def output_process(process):
    outputs = list()
    while True:
        output = process.stdout.readline()
        if not output and process.poll() is not None:
            break
        if output:
            print(output.strip().decode())
            outputs.append(output.strip().decode())
    return outputs

class Test:
    def __init__(self, src_path, tgt_path, test_mode, logger=None):
        self.src_path = src_path
        self.tgt_path = tgt_path
        self.test_mode = test_mode
        with open(os.path.join(self.src_path, "config.json"), "r") as f:
            self.config = json.load(f)
        self.usage_examples = self.config["usage_examples"]
        self.required_files = self.config["required_files"]
        self.unit_tests_path = self.config["unit_tests"]
        self.unit_tests_command = self.config["unit_test_script"]
        self.dependencies = self.config["dependencies"]
        self.logger = logger
        self.check_tests_path = self.config["check_tests"]
        self.check_tests_command = self.config["check_test_script"]
    
    def copy_files(self, file_path):
        tgt_full_path = os.path.join(self.tgt_path, file_path)
        print(f"Copying {file_path} to {tgt_full_path}")
        if os.path.exists(tgt_full_path):
            if os.path.isdir(tgt_full_path):
                shutil.rmtree(tgt_full_path)
            else:
                os.remove(tgt_full_path)
        os.makedirs(os.path.dirname(tgt_full_path), exist_ok=True)
        process = subprocess.Popen(["cp", "-r", os.path.join(self.src_path, file_path), tgt_full_path], stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)

    def setup_implementation(self):
        self.copy_files(self.unit_tests_path)
        self.copy_files(self.check_tests_path)
        if type(self.usage_examples) is list:
            for example in self.usage_examples:
                self.copy_files(example)
        elif self.usage_examples != '':
            self.copy_files(self.usage_examples)
        for file in self.required_files:
            self.copy_files(file)
        if "setup_shell_script" in self.config.keys() and self.config["setup_shell_script"] != "":
            self.copy_files(self.config["setup_shell_script"])
            process = subprocess.Popen(["sh", self.config["setup_shell_script"]], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=self.tgt_path)
            while True:
                output = process.stdout.readline()
                if not output and process.poll() is not None:
                    break
                if output:
                    print(output.strip().decode())
    
    def setup_tests(self, path, language):
        if language == "python":
            process = subprocess.Popen(["pip", "install", "-r", self.dependencies], cwd=path, stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT)
            output_process(process)
        
    def check_commands(self, filename, cwd):
        process = subprocess.Popen(["conda", "run", "-n", "myenv", "sh", filename], cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        outputs = list()
        while True:
            output = process.stdout.readline()
            if not output and process.poll() is not None:
                break
            if output:
                print(output.strip().decode())
                outputs.append(output.strip().decode())

        # exit code
        rc = process.poll()
        return "\n".join(outputs), rc

    def check_tests(self, path, language, test_mode):
        if language == "python":
            env = os.environ.copy()
            env["PYTHONPATH"] = path
            process = subprocess.Popen(
                ["pytest", "--cov=.", test_mode],
                cwd=path, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
        else:
            if test_mode == "unit_tests":
                process = subprocess.Popen(self.unit_tests_command, shell=True, cwd=path, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            elif test_mode == "check_tests":
                process = subprocess.Popen(self.check_tests_command, shell=True, cwd=path, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            else:
                process = subprocess.Popen(self.acceptance_tests_command, shell=True, cwd=path, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        try:
            outputs = list()
            while True:
                output = process.stdout.readline()
                if not output and process.poll() is not None:
                    break
                if output:
                    print(output.strip().decode())
                    outputs.append(output.strip().decode())
            check_output = '\n'.join(outputs)
        except subprocess.TimeoutExpired:
            check_output = "check_tests function has timed out."
        return check_output

    def test(self, path, language):
        self.setup_implementation()
        check_output = self.check_tests(path, language, self.test_mode)
        return check_output

if __name__ == "__main__":
    dataset_dir = '../CodeProjectEval'
    output_dir = '../../CodeProjectEval_outputs'

    repo_list = [d for d in os.listdir(output_dir) if os.path.isdir(os.path.join(output_dir, d))]

    for repo_name in repo_list:
        repo_dir = os.path.join(output_dir, repo_name)
        print(repo_dir)
        t = Test(f"{dataset_dir}/{repo_name}", repo_dir, "unit_tests")
        test_output = t.test(repo_dir, "python")
        f = open(f"{repo_dir}/unit_test_results.txt", "w")
        f.write(test_output)
        f.close()