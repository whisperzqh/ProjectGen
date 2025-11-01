import ast
import inspect

def extract_api(source: str, file_path: str = "<string>") -> str:
    
    try:
        tree = ast.parse(source, filename=file_path)
    except SyntaxError as e:
        print(f"Syntax error while parsing {file_path}: {e}")
        return ""

    result = []

    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            sig = get_signature(node)
            ret_type = get_return_type(node)
            result.append(f"def {sig}:\n    \"\"\"returns: {ret_type}\"\"\"\n")

        elif isinstance(node, ast.ClassDef):
            result.append(f"class {node.name}:\n")
            for sub in node.body:
                if isinstance(sub, ast.FunctionDef):
                    sig = get_signature(sub)
                    ret_type = get_return_type(sub)
                    result.append(f"    def {sig}:\n        \"\"\"returns: {ret_type}\"\"\"\n")

    return "\n".join(result)


def get_signature(func: ast.FunctionDef) -> str:
    args = []
    for a in func.args.args:
        if a.annotation:
            arg_str = f"{a.arg}: {ast.unparse(a.annotation)}"
        else:
            arg_str = a.arg
        args.append(arg_str)
    return f"{func.name}({', '.join(args)})"

def get_return_type(func: ast.FunctionDef) -> str:
    if func.returns:
        return ast.unparse(func.returns)
    else:
        return infer_return_type(func)

def infer_return_type(func: ast.FunctionDef) -> str:
    for node in ast.walk(func):
        if isinstance(node, ast.Return) and node.value is not None:
            if isinstance(node.value, ast.Constant):
                return type(node.value.value).__name__
            elif isinstance(node.value, ast.Name):
                return "UnknownVariable"
            elif isinstance(node.value, ast.Call):
                if isinstance(node.value.func, ast.Name):
                    return f"{node.value.func.id}()"
    return "None"
