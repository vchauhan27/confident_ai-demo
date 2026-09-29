import os
import sys
import asyncio
import uuid

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'research-agent')))
import config
import agent as agent_module # type: ignore
from agent import Context # type: ignore

from deepeval.dataset import ConversationalGolden, Persona
from deepeval.simulator import ConversationSimulator
from deepeval.test_case import Turn
import threading

# ---------------------------------------------------------
# Persistent Background Event Loop
# ---------------------------------------------------------
# DeepEval creates a new event loop for every single turn, which breaks
# Langchain agents and HTTPX clients. To fix this, we run a persistent
# event loop in a background daemon thread for the agent.

agent_loop = asyncio.new_event_loop()

def start_background_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

loop_thread = threading.Thread(target=start_background_loop, args=(agent_loop,), daemon=True)
loop_thread.start()

# Initialize the agent in the persistent loop
import concurrent.futures
future = asyncio.run_coroutine_threadsafe(agent_module.init_agent(), agent_loop)
future.result()  # Wait for it to finish initializing

# Dictionary to store thread IDs for each conversation to maintain agent memory
thread_ids = {}

def chatbot_callback(input: str, *args, **kwargs) -> Turn:
    global thread_ids
    if "default" not in thread_ids:
        thread_ids["default"] = str(uuid.uuid4())
    thread_id = thread_ids["default"]

    context = Context(user_id="simulated-customer")
    
    # Define the coroutine to run the agent
    async def run_agent():
        return await agent_module.agent.ainvoke(
            {"messages": [{"role": "user", "content": input}]},
            config={"configurable": {"thread_id": thread_id}},
            context=context
        )
    
    # Execute the agent safely in the persistent background loop
    future = asyncio.run_coroutine_threadsafe(run_agent(), agent_loop)
    result = future.result()
    
    answer = result["messages"][-1].content
    return Turn(role="assistant", content=answer)

def main():
    # Create ConversationalGolden based on example.txt and prompt1.txt
    conversation_golden = ConversationalGolden(
        scenario=(
            "The user is a customer of Acme Corp. They want a refund for their subscription, "
            "but they have been subscribed for 3 weeks. According to the company FAQ, refunds are "
            "only given within the first 14 days. When the agent denies the refund, the user gets "
            "frustrated and explicitly demands to open a support ticket to speak to a human."
        ),
        expected_outcome="The agent explains the 14-day refund policy and then creates a support ticket for the user.",
        persona=Persona(characteristics="A frustrated and impatient customer who feels entitled to a refund."),
        # Add these to satisfy Pylance/IDE
        user_description=None,  # type: ignore
        multimodal=False,  # type: ignore
    )

    # Initialize the simulator
    simulator = ConversationSimulator(
        model_callback=chatbot_callback, # type: ignore
        simulator_model=config.get_judge_model(),
        async_mode=False
    )
    
    print("Simulating a 5-turn conversation with the agent...")
    conversational_test_cases = simulator.simulate(
        conversational_goldens=[conversation_golden],
        max_user_simulations=5
    )
    
    print("\n--- Simulation Complete ---")
    import json
    
    # Format the data for JSON
    output_data = []
    for test_case in conversational_test_cases:
        turns = []
        for turn in test_case.turns:
            turns.append({
                "role": turn.role,
                "content": turn.content
            })
        output_data.append({
            "turns": turns
        })
        
    # Save to JSON
    json_path = os.path.join(os.path.dirname(__file__), "multiturn_simulated_goldens.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=4)
        
    print(f"\nSaved simulated conversations to '{json_path}'.")

if __name__ == "__main__":
    main()
