import os
import dspy
def setup_llm():
    """Set up and configure the language model."""
    llm = dspy.LM(model="gemini/gemini-2.0-flash", api_key=os.getenv("GEMINI_API_KEY"))
    dspy.configure(lm=llm)
    return llm

class AgentDIR(dspy.Signature):
    """Organize text files with categories documented by managing file operations."""
    input_task = dspy.InputField()
    result = dspy.OutputField(desc="Success message indicating the operation performed.")

def create_agent(tools_function):
    """Create and return a ReAct agent with the specified tools."""
    return dspy.ReAct(AgentDIR, tools=tools_function(), max_iters=20)
