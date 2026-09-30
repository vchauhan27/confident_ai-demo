import os
import sys
import logging
logging.basicConfig(level=logging.ERROR)
from deepeval.synthesizer import Synthesizer
from deepeval.synthesizer.types import Evolution
from deepeval.synthesizer.config import ContextConstructionConfig, EvolutionConfig

# Add the parent directory to sys.path to import config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import get_judge_model, get_embedding_model

def main():
    # Initialize the configs
    context_config = ContextConstructionConfig(
        embedder=get_embedding_model(),
        critic_model=get_judge_model(),
        chunk_size=256,
        chunk_overlap=50,
        max_contexts_per_document=2,
        context_quality_threshold=0.0
    )

    evolution_config = EvolutionConfig(
        num_evolutions=3,
        evolutions={
            Evolution.REASONING: 0.3,
            Evolution.MULTICONTEXT: 0.3,
            Evolution.COMPARATIVE: 0.1,
            Evolution.IN_BREADTH: 0.3,
        }
    )

    # Initialize the Synthesizer with custom judge model and evolution config
    synthesizer = Synthesizer(
        model=get_judge_model(),
        evolution_config=evolution_config,
        async_mode=False
    )
    
    # Path to the specific example.txt document
    example_doc_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'customer-support-agent', 'data', 'example.txt'))
    document_paths = [example_doc_path]
    
    print(f"Generating 2 synthetic test cases from {example_doc_path}...")
    
    # Generate goldens from the documents
    goldens = synthesizer.generate_goldens_from_docs(
        document_paths=document_paths,
        max_goldens_per_context=1,
        context_construction_config=context_config
    )
    
    print(f"Successfully generated {len(goldens)} goldens.")
    
    # Save the generated goldens
    synthesizer.save_as(
        file_type='json',
        directory="./",
        file_name="singleturn_goldens"
    )
    print("Goldens have been saved as a JSON file in the current directory.")

if __name__ == "__main__":
    main()
