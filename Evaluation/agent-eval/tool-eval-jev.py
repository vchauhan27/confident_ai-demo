import os
import sys
import json
import uuid
import asyncio

# Setup paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'research-agent')))

import config
import agent as agent_module  # type: ignore
from deepeval.test_case import LLMTestCase, ToolCall, SingleTurnParams
from deepeval import evaluate
from deepeval.metrics import JevEval
from deepeval.metrics.jev_eval import Noul, Score, Choice
from deepeval.models.system_one.typesafe_model import TypeSafeModel

async def run_agent_and_get_test_case(input_text, expected_tools):
    await agent_module.init_agent()
    # Run the agent in an isolated thread
    result = await agent_module.agent.ainvoke(
        {"messages": [{"role": "user", "content": input_text}]},
        config={"configurable": {"thread_id": str(uuid.uuid4())}}
    )
    
    output_text = result["messages"][-1].content
    tools_called = []
    
    # First, collect all tool outputs by their tool_call_id
    tool_outputs = {}
    for msg in result["messages"]:
        if hasattr(msg, 'tool_call_id') and msg.tool_call_id:
            tool_outputs[msg.tool_call_id] = msg.content

    # Then extract tools_called and attach their outputs
    for msg in result["messages"]:
        if hasattr(msg, 'tool_calls') and msg.tool_calls:
            for tc in msg.tool_calls:
                output = tool_outputs.get(tc.get('id'))
                tools_called.append(
                    ToolCall(
                        name=tc['name'], 
                        input_parameters=tc['args'],
                        output=output
                    )
                )
                
    return LLMTestCase(
        input=input_text,
        actual_output=output_text,
        expected_tools=expected_tools,
        tools_called=tools_called
    )

async def main():
    json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'Data-Generation', 'multiturn_goldens.json'))
    test_cases = []
    
    print("Running Agent to extract Tool Calls...")
    with open(json_path, 'r') as f:
        agent_data = json.load(f)
        for item in agent_data:
            # We expect the agent to search the knowledge base for these factual questions
            expected_tools = [ToolCall(name="search_knowledge_base", input_parameters={})]
            tc = await run_agent_and_get_test_case(item["scenario"], expected_tools)
            test_cases.append(tc)
            
    print("\nEvaluating Jev Tool Faithfulness...")
    
    tool_faithfulness_jev = JevEval(
        name="Tool Faithfulness",
        system_one_model=TypeSafeModel(
            model="typesafe/jev-1.13",
            api_key=os.environ.get("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api",
        ),
        evaluation_params=[
            SingleTurnParams.INPUT,
            SingleTurnParams.ACTUAL_OUTPUT,
            SingleTurnParams.TOOLS_CALLED,
        ],
        questions=[
            Noul(
                "Every fact and figure in actual_output appears in the output "
                "of a tool in tools_called.",
                weight=2,
            ),
            Noul(
                "actual_output reports every value returned in tools_called accurately."
            ),
            Score(
                "How much of actual_output is grounded in tools_called?",
                levels=[
                    "Fabricated",
                    "Mostly fabricated",
                    "Mostly grounded",
                    "Fully grounded",
                ],
            ),
            Choice(
                "What did actual_output do with information the tools did not return?",
                options={
                    "left_it_out": 1.0,
                    "flagged_it_as_unknown": 1.0,
                    "hedged_it": 0.5,
                    "stated_it_as_fact": 0.0,
                    "nothing_missing": None,
                },
            ),
        ],
        include_reason=True,
    )
    
    evaluate(test_cases, [tool_faithfulness_jev]) # type: ignore

if __name__ == "__main__":
    asyncio.run(main())
