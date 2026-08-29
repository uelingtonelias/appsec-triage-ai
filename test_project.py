import requests
import pandas as pd
import numpy as np

from git import Repo
from rich.console import Console
from pydantic import BaseModel

print("Requests OK")
print("Pandas OK")
print("Numpy OK")
print("GitPython OK")
print("Rich OK")
print("Pydantic OK")

try:
    import tree_sitter
    print("Tree-Sitter OK")
except Exception as e:
    print("Tree-Sitter ERROR:", e)

try:
    import chromadb
    print("ChromaDB OK")
except Exception as e:
    print("ChromaDB ERROR:", e)

try:
    from sentence_transformers import SentenceTransformer
    print("SentenceTransformers OK")
except Exception as e:
    print("SentenceTransformers ERROR:", e)

print("\nAll tests completed.")