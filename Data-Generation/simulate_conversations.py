import os
import sys
import json
import asyncio

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'customer-support-agent')))
from agent import agent, Context, init_agent  # type: ignore

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

async def simulate_conversation(scenario: str, max_turns: int = 3):
    """
    Simulates a conversation between a 'User' (driven by the judge model)
    and our 'Agent' based on a given scenario.
    """
    # Use the judge model to act as the user
    user_simulator = config.get_judge_model()
    
    system_prompt = (
        f"You are a customer acting out the following scenario: '{scenario}'.\n"
        "You are chatting with a customer support AI. Keep your messages short (1-2 sentences). "
        "Do not reveal that you are an AI or reading a scenario. Just act naturally.\n"
        "If your issue is fully resolved or the ticket is created, you can end the conversation by saying 'Thank you, goodbye.'."
    )
    
    # History from the perspective of the simulated user
    user_history = [SystemMessage(content=system_prompt)]
    
    thread_id = f"sim-{hash(scenario)}"
    context = Context(user_id="sim-user")
    
    conversation_turns = []
    
    for turn in range(max_turns):
        # 1. Simulated user generates a message based on the history
        user_response = await user_simulator.ainvoke(user_history)
        user_text = user_response.content
        
        # Add to conversation history
        user_history.append(AIMessage(content=user_text))
        
        # Stop if the simulated user ends the chat
        if "goodbye" in user_text.lower():
            break
            
        print(f"\n[Turn {turn+1}] User: {user_text}")
        
        # 2. Our agent responds
        agent_result = await agent.ainvoke(
            {"messages": [{"role": "user", "content": user_text}]},
            config={"configurable": {"thread_id": thread_id}},
            context=context,
        )
        agent_text = agent_result["messages"][-1].content
        
        print(f"[Turn {turn+1}] Agent: {agent_text}")
        
        # Log the turn (we'll extract tool calls later if needed, but saving text for now)
        conversation_turns.append({
            "user": user_text,
            "assistant": agent_text
        })
        
        # Feed agent's response back to simulated user
        user_history.append(HumanMessage(content=agent_text))
        
    return conversation_turns

async def main():
    await init_agent()
    
    json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'multiturn_goldens.json'))
    try:
        with open(json_path, 'r') as f:
            scenarios_data = json.load(f)
    except FileNotFoundError:
        print(f"Could not find {json_path}")
        return

    simulated_dataset = []
    
    print("Starting simulation of multi-turn conversations...")
    for i, item in enumerate(scenarios_data):
        print(f"\n--- Simulating Scenario {i+1} ---")
        scenario = item["scenario"]
        turns = await simulate_conversation(scenario)
        
        simulated_dataset.append({
            "scenario": scenario,
            "turns": turns
        })
        
    out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'simulated_conversations.json'))
    with open(out_path, 'w') as f:
        json.dump(simulated_dataset, f, indent=4)
        
    print(f"\nSaved {len(simulated_dataset)} multi-turn conversations to {out_path}!")

if __name__ == "__main__":
    asyncio.run(main())
