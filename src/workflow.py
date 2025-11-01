from langgraph.graph import StateGraph, END
from agents.architecture_agent import architecture_agent
from agents.arch_judge_agent import judge_architecture_agent
from agents.skeleton_agent import skeleton_agent
from agents.skeleton_judge_agent import judge_skeleton_agent
from agents.code_agent import code_agent
from agents.code_judge_agent import judge_code_agent

def route_arch_judge(state: dict) -> str:
    return "skeleton" if state.get("arch_decision") else "architecture"

def route_skeleton_judge(state: dict) -> str:
    return "code" if state.get("skeleton_decision") else "skeleton"

def route_code_judge(state: dict) -> str:
    return END if state.get("code_decision") else "code"

def build_graph():
    builder = StateGraph(dict)

    builder.add_node("architecture", architecture_agent)
    builder.add_node("arch_judge", judge_architecture_agent)
    
    builder.add_node("skeleton", skeleton_agent)
    builder.add_node("skeleton_judge", judge_skeleton_agent)
    builder.add_node("code", code_agent)
    builder.add_node("code_judge", judge_code_agent)

    builder.set_entry_point("architecture")
    builder.add_edge("architecture", "arch_judge")
    builder.add_conditional_edges("arch_judge", route_arch_judge)

    builder.add_edge("skeleton", "skeleton_judge")
    builder.add_conditional_edges("skeleton_judge", route_skeleton_judge)
    
    builder.add_edge("code", "code_judge")
    builder.add_conditional_edges("code_judge", route_code_judge)

    return builder.compile()
