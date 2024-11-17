from .rag.main import rag_ai_app
from .pubmed.main import pubmed_ai


interactive_config = {"rag": [rag_ai_app]}
interactive_config["pubmed"] = [pubmed_ai]
