from agent import setup_llm, create_agent
from agent_tools import get_function_list
from ui import AgentDirUI

def main():
    # Setup LLM
    setup_llm()
    
    # Create agent
    agent = create_agent(get_function_list)
    
    # Run UI
    AgentDirUI(agent).run()

if __name__ == '__main__':
    main()