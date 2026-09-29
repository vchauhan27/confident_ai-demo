import os
from dotenv import load_dotenv
from pydantic import SecretStr

load_dotenv()

embedding_model = "baai/bge-m3" 

def get_agent_model():

    from langchain_openrouter import ChatOpenRouter
    return ChatOpenRouter(
        model="qwen/qwen-2.5-7b-instruct",
        temperature=0.3,
        api_key=SecretStr(os.getenv("OPENROUTER_API_KEY", ""))
    )

    # from langchain_google_genai import ChatGoogleGenerativeAI
    # return ChatGoogleGenerativeAI(
    #     model="gemini-flash-lite-latest",
    #     temperature=0.3,
    # )

def get_guardrail_model():

    from deepeval.models import OpenRouterModel
    return OpenRouterModel(
        model="openai/gpt-oss-safeguard-20b",
        api_key=os.environ.get("OPENROUTER_API_KEY"),
        temperature=0    
    )

def get_judge_model(): 

    from deepeval.models import OpenRouterModel
    return OpenRouterModel(
        model="openai/gpt-oss-120b",
        api_key=os.environ.get("OPENROUTER_API_KEY"),
        temperature=0    
    )

    # from deepeval.models import GeminiModel
    # return GeminiModel(
    #     model="gemini-3.1-flash-lite",
    #     temperature=0,
    # )

def get_jev_client():
    from typesafe_sdk import TypeSafeClient
    return TypeSafeClient(
        api_key=os.environ.get("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api",
        timeout=30.0,  
    )

def get_jev_model_name():
    return "typesafe/jev-1.13"

def get_attacker_model():
    from deepeval.models import OpenRouterModel
    return OpenRouterModel(
        model="openai/gpt-oss-120b",
        api_key=os.environ.get("OPENROUTER_API_KEY"),
        temperature=0.7    
    )

def get_redteam_judge_model():
    # DeepTeam's built-in vulnerabilities require a standard generative LLM 
    # to evaluate their internal prompts. Jev (TypeSafeModel) cannot be passed 
    # as the evaluation_model here because it only supports bounded questions.
   
    # from deepeval.models import GeminiModel
    # return GeminiModel(
    #     model="gemini-3.1-flash-lite",
    #     temperature=0,
    from deepeval.models import OpenRouterModel
    return OpenRouterModel(
        model="openai/gpt-oss-120b",
        api_key=os.environ.get("OPENROUTER_API_KEY"),
        temperature=0    
    ) 

def get_embedding_model():
    from deepeval.models.base_model import DeepEvalBaseEmbeddingModel
    from langchain_openai import OpenAIEmbeddings

    class OpenRouterEmbeddings(OpenAIEmbeddings):
        pass

    langchain_embedder = OpenRouterEmbeddings(
        model=embedding_model,
        base_url="https://openrouter.ai/api/v1",
        api_key=os.environ.get("OPENROUTER_API_KEY"),  # type: ignore
        check_embedding_ctx_length=False
    )

    class CustomEmbedder(DeepEvalBaseEmbeddingModel):
        def __init__(self, model):
            self.model = model
        def load_model(self):
            return self.model
        def embed_text(self, text: str) -> list[float]:
            return self.model.embed_query(text)
        def embed_texts(self, texts: list[str]) -> list[list[float]]:
            return self.model.embed_documents(texts)
        async def a_embed_text(self, text: str) -> list[float]:
            return await self.model.aembed_query(text)
        async def a_embed_texts(self, texts: list[str]) -> list[list[float]]:
            return await self.model.aembed_documents(texts)
        def get_model_name(self):
            return embedding_model

    return CustomEmbedder(langchain_embedder)
