import dspy
from agent_tools import get_function_list
import os

llm = dspy.LM("gemini/gemini-2.0-flash",api_key="AIzaSyAiwilF3zyQT1BR27GvpbbX07tsedeXdKg")
dspy.configure(lm=llm)

class AgentDIR(dspy.Signature):
    """Organize text files with categories documented. by managing file operations."""
    input_task = dspy.InputField()
    result = dspy.OutputField(desc="Success message indicating the operation performed.")


if __name__ == '__main__':
    working_directory = "./Test_Environment"
    os.makedirs(working_directory, exist_ok=True)
    os.chdir(working_directory)
    task = "organize all file in the directory"
    Agent_Module = dspy.ReAct(AgentDIR,tools=get_function_list() ,max_iters=20)

    result = Agent_Module(input_task=task)
    print(result)
