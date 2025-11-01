import ast
import json
from pathlib import Path
from collections import defaultdict, deque
from typing import List, Dict


def get_py_files_from_skeleton(skeleton):
    py_files = [item for item in skeleton if item["path"].endswith(".py")]
    return py_files

def extract_imports_from_source(source: str, file_path: str = "<string>"):
    try:
        tree = ast.parse(source, filename=file_path)
    except SyntaxError:
        print(f"Skip files with syntax errors: {file_path}")
        return set(), True 

    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for n in node.names:
                imports.add(n.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module)
    return imports, False

def path_to_module(path: str):
    return Path(path).with_suffix('').as_posix().replace('/', '.')


def build_dependency_graph(py_files):
    file_to_module = {item["path"]: path_to_module(item["path"]) for item in py_files}
    graph = defaultdict(set)
    syntax_errors = []

    for item in py_files:
        path = item["path"]
        source = item["skeleton"]

        imports, has_error = extract_imports_from_source(source, file_path=path)
        if has_error:
            syntax_errors.append(path)
            continue

        for imported_module in imports:
            for other_path, other_module in file_to_module.items():
                if imported_module == other_module or imported_module.startswith(other_module + "."):
                    graph[path].add(other_path)

        graph.setdefault(path, set())

    return graph, syntax_errors


def topological_sort(graph, syntax_errors):
    indegree = {node: 0 for node in graph}
    for node, deps in graph.items():
        for dep in deps:
            indegree[dep] = indegree.get(dep, 0) + 1

    queue = deque([n for n, d in indegree.items() if d == 0])
    order = []

    while queue:
        node = queue.popleft()
        order.append(node)
        for dep in graph.get(node, []):
            indegree[dep] -= 1
            if indegree[dep] == 0:
                queue.append(dep)

    for f in syntax_errors:
        if f not in order:
            order.append(f)

    remaining = set(graph.keys()) - set(order)
    if remaining:
        print("Warning: circular dependencies detected:", remaining)
        order.extend(remaining)

    return order

def reorder_skeleton_by_topo(skeleton: List[Dict]) -> List[Dict]:
    py_files = get_py_files_from_skeleton(skeleton)
    graph, syntax_errors = build_dependency_graph(py_files)

    order = topological_sort(graph, syntax_errors)
    path_to_item = {item["path"]: item for item in skeleton}
    reordered = []
    used_paths = set()
    for path in order:
        if path in path_to_item:
            reordered.append(path_to_item[path])
            used_paths.add(path)
    
    for item in skeleton:
        if item["path"] not in used_paths:
            reordered.append(item)
    
    return reordered
