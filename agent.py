from tools import web_search, calculator, math_solver, document_qa
from config import master_prompt_concluder
import json
import time   
import streamlit as st
from tools import get_openai_response


def run_concluder_agent(query):
    # Collect tool names and descriptions dynamically
    tool_map = {
        "web_search": web_search,
        "calculator": calculator,
        "math_solver": math_solver,
        "document_qa": document_qa,
    }
    tool_descriptions = "\n".join([
        f"Tool: name: {name}, description: {func.__doc__.strip()}"
        for name, func in tool_map.items()
    ])
    agent_prompt = master_prompt_concluder.replace("[Your full list of 4 tools]", tool_descriptions)
    full_prompt = agent_prompt + f"\n\nUser Query: \"{query}\""

    st.write(f"Planning for query: {query}\n")
    # Step 1: Get the plan from OpenAI
    plan_json = get_openai_response(full_prompt)
    try:
        plan_text = plan_json.strip().replace("``````", "")
        plan = json.loads(plan_text)
    except Exception as e:
        st.write(f"Failed to parse LLM plan! Error: {e} Plan was:\n{plan_json}")
        return None

    st.write("✅ Plan Created:")
    st.write(json.dumps(plan, indent=2))
    step_results = {}
    answer = None

    for step in plan:
        tool_name = step["tool_name"]
        step_number = step["step"]
        tool_input = step["input"]

        # Fill any [result from step N] placeholders
        for ref_step, result in step_results.items():
            tool_input = tool_input.replace(f"[result from step {ref_step}]", result)

        st.write(f"\nExecuting Step {step_number}: Tool: {tool_name}, Input: '{tool_input}'")
        if tool_name == "final_answer":
            answer = tool_input
            break

        tool_func = tool_map.get(tool_name)
        if tool_func:
            result = tool_func(tool_input)
            st.write(f"Step {step_number} Result: {result}")
            step_results[step_number] = result
        else:
            st.write(f"Unknown tool: {tool_name}")
            step_results[step_number] = f"(Unknown tool {tool_name})"
        time.sleep(0.2)

    # Fill any placeholders in the final answer
    if answer:
        for ref_step, result in step_results.items():
            answer = answer.replace(f"[result from step {ref_step}]", result)
        st.write(f"\n🏁 Final Answer: {answer}")
        return answer
    st.write("\n⚠️ No final answer could be produced.")
    return None
