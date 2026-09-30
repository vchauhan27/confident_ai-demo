import os
import sys
import logging
logging.basicConfig(level=logging.ERROR)
from deepeval.synthesizer import Synthesizer
from deepeval.synthesizer.types import Evolution
from deepeval.synthesizer.config import (
    ContextConstructionConfig, 
    EvolutionConfig,
    ConversationalStylingConfig
)

# Add the parent directory to sys.path to import config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import get_judge_model, get_embedding_model

def main():
    # Initialize context construction config
    context_config = ContextConstructionConfig(
        embedder=get_embedding_model(),
        critic_model=get_judge_model(),
        chunk_size=256,
        chunk_overlap=50,
        max_contexts_per_document=2,
        context_quality_threshold=0.0
    )

    # Initialize evolution config to determine complexity
    evolution_config = EvolutionConfig(
        num_evolutions=1, # Reduced from 3 to 1 to significantly speed up generation
        evolutions={
            Evolution.REASONING: 0.3,
            Evolution.MULTICONTEXT: 0.3,
            Evolution.COMPARATIVE: 0.1,
            Evolution.IN_BREADTH: 0.3,
        }
    )

    # Load the agent's prompt to guide the synthetic generation
    prompt_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'customer-support-agent', 'prompt1.txt'))
    with open(prompt_path, 'r') as f:
        agent_prompt = f.read()

    # Multi-turn specific config for conversational styling using the agent's prompt
    conversational_styling_config = ConversationalStylingConfig(
        scenario_context=f"The agent is a customer support agent. Here are its instructions and tools: {agent_prompt}. The user should ask questions or make requests that require the agent to use its tools (like creating tickets or recalling facts).",
        conversational_task="Test the agent's ability to use its specific tools and follow its rules in a multi-turn conversation.",
        participant_roles="A customer with an issue and an AI customer support agent.",
    )

    # Initialize the Synthesizer for multi-turn
    synthesizer = Synthesizer(
        model=get_judge_model(),
        evolution_config=evolution_config,
        conversational_styling_config=conversational_styling_config,
        async_mode=False # Keep false to avoid rate limits
    )
    
    # Path to the specific example.txt document
    example_doc_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'customer-support-agent', 'data', 'example.txt'))
    document_paths = [example_doc_path]
    
    print(f"Generating synthetic multi-turn (conversational) test cases from {example_doc_path}...")
    
    # Generate conversational goldens from the documents
    conversational_goldens = synthesizer.generate_conversational_goldens_from_docs(
        document_paths=document_paths,
        max_goldens_per_context=1,
        context_construction_config=context_config,
        # Set to True to include an expected outcome based on the multi-turn interaction
        include_expected_outcome=True
    )
    
    print(f"Successfully generated {len(conversational_goldens)} conversational goldens.")
    
    # Save the generated multi-turn goldens
    synthesizer.save_as(
        file_type='json',
        directory="./",
        file_name="multiturn_goldens"
    )
    print("Conversational goldens have been saved as 'multiturn_goldens.json' in the current directory.")

if __name__ == "__main__":
    main()
