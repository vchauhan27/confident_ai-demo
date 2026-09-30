import sys
import os
from langchain_core.messages import HumanMessage, AIMessage
from deepteam.test_case import RTTurn

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "customer-support-agent")))
import agent as research_agent # type: ignore
from guardrail import check_input, check_output # type: ignore
graph = research_agent.agent
Context = research_agent.Context

from deepteam import red_team
from deepteam.vulnerabilities import (
    Bias, Toxicity, Fairness,
    Misinformation, Hallucination,
    PersonalSafety, Ethics
)
from deepteam.attacks.single_turn import PromptInjection, Roleplay
from deepteam.attacks.multi_turn import CrescendoJailbreaking

async def model_callback(input: str, turns: list[RTTurn] | None = None) -> RTTurn:
    input_res = check_input(input)
    if not input_res["allowed"]:
        return RTTurn(
            role="assistant",
            content="Input blocked by guardrails:\n" + str(input_res.get("message", ""))
        )

    history = []
    for turn in (turns or []):
        if turn.role == "user":
            history.append(HumanMessage(content=turn.content))
        elif turn.role == "assistant":
            history.append(AIMessage(content=turn.content))
            
    history.append(HumanMessage(content=input))
    state = {"messages": history}
    
    result = await graph.ainvoke(
        state,  # type: ignore
        config={"configurable": {"thread_id": "red-team-session"}},
        context=Context(user_id="red-team-user"),
    )
    
    last_msg = result["messages"][-1]
    output_text = str(last_msg.content)

    output_res = check_output(input, output_text)
    if not output_res["allowed"]:
        return RTTurn(
            role="assistant",
            content="Output blocked by guardrails:\n" + str(output_res.get("message", ""))
        )

    return RTTurn(
        role="assistant",
        content=output_text
    )

if __name__ == "__main__":
    diagnostics_vulnerabilities = [
        Bias(),
        Toxicity(),
        Fairness(),
        Misinformation(),
        Hallucination(),
        PersonalSafety(),
        Ethics()
    ]

    import sys, os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from config import get_attacker_model, get_redteam_judge_model
    
    risk_assessment = red_team(
        simulator_model=get_attacker_model(),
        evaluation_model=get_redteam_judge_model(),
        model_callback=model_callback,  # type: ignore
        target_purpose="AI Customer Support Agent that is responsible, safe, and accurate.",
        vulnerabilities=diagnostics_vulnerabilities,
        attacks=[PromptInjection(), Roleplay(), CrescendoJailbreaking()],
        attacks_per_vulnerability_type=1,
    )  # type: ignore

    risk_assessment.save(to="./deepteam-results/")

    import os, glob
    list_of_files = glob.glob('./deepteam-results/*.json')
    if list_of_files:
        latest_file = max(list_of_files, key=os.path.getctime)
        new_name = "./deepteam-results/responsible_results.json"
        if os.path.exists(new_name) and latest_file != os.path.abspath(new_name).replace('\\\\', '/'):
            try: os.remove(new_name)
            except: pass
        if latest_file != new_name and not latest_file.endswith("responsible_results.json"):
            os.rename(latest_file, new_name)
