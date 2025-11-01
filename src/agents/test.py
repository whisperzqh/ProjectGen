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

def parse_pytest_summary(output: str):
    """
    Parse pytest output to extract number of passed, failed, and total tests.
    Works even if some categories are missing.
    """
    passed = failed = skipped = 0

    matches = re.findall(r"(\d+)\s+(passed|failed|skipped)", output)
    for count, label in matches:
        count = int(count)
        if label == "passed":
            passed = count
        elif label == "failed":
            failed = count
        elif label == "skipped":
            skipped = count

    return {"passed": passed, "failed": failed, "skipped": skipped}

class Test:
    def __init__(self, src_path, tgt_path, logger=None):
        self.src_path = src_path
        self.tgt_path = tgt_path
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
        self.env_vars = self.config.get("env_vars", {})
    
    def copy_files(self, file_path):
        if not file_path:
            return
        tgt_full_path = os.path.join(self.tgt_path, file_path)
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

        rc = process.poll()
        return "\n".join(outputs), rc

    def check_tests(self, path, language, test_mode):
        passed = 0
        total = 0
        if language == "python":
            env = os.environ.copy()
            env["PYTHONPATH"] = path
            if self.env_vars:
                for k, v in self.env_vars.items():
                    env[k] = v
            process = subprocess.Popen(
                ["pytest", "--cov=.", test_mode],
                cwd=path, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
        else:
            if test_mode == "unit_tests":
                process = subprocess.Popen(self.unit_tests_command, shell=True, cwd=path, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            elif test_mode == "check_tests":
                process = subprocess.Popen(self.check_tests_command, shell=True, cwd=path, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
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
            m_total = re.search(r"collected (\d+) items", check_output)
            if m_total:
                total = int(m_total.group(1))
            stats = parse_pytest_summary(check_output)
            passed = stats["passed"]
        except subprocess.TimeoutExpired:
            check_output = "check_tests function has timed out."
        return check_output, passed, total

    def test(self, path, language):
        self.setup_implementation()
        check_test_output, passed, total = self.check_tests(path, language, "check_tests")
        test_output = f"[check test] Passed {passed} out of {total} test cases.\n{check_test_output}"

        # test_msg = "**[Evaluation results]**\n\n"
        # test_msg += test_output
        # if self.logger:
        #     self.logger.info(test_msg)

        return test_output, passed, total
