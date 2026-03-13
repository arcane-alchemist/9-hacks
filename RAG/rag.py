"""RAG module: ChromaDB setup and graph-based retrieval."""

import os
import json
import random
from pathlib import Path
import chromadb
from chromadb.config import Settings
from config import TOP_K_CHUNKS, STATUTE_FILES_DIR

class RAGSystem:
    """RAG system with hand-coded statute relationship graph."""
    
    def __init__(self):
        """Initialize RAG system with ChromaDB and statute graph."""
        self.gemini_enabled = False
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        if gemini_api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=gemini_api_key)
                self.genai = genai
                self.gemini_enabled = True
            except ImportError:
                pass
        
        if not self.gemini_enabled:
            print("⚠️ Warning: GEMINI_API_KEY not set. Using dummy embeddings strictly for Groq testing.")

        # Initialize ChromaDB in-memory
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection(
            name="statutes",
            metadata={"hnsw:space": "cosine"}
        )
        
        # Load statute relationship graph (hand-coded knowledge)
        self.statute_graph = self._load_statute_graph()
        self.loaded = False
    
    def _load_statute_graph(self) -> dict:
        """Load the hand-coded statute relationship graph."""
        graph_path = Path("data/statute_graph.json")
        
        if not graph_path.exists():
            print("⚠️  statute_graph.json not found. Graph expansion disabled.")
            return {}
        
        try:
            with open(graph_path, "r", encoding="utf-8") as f:
                graph_data = json.load(f)
            return graph_data
        except Exception as e:
            print(f"⚠️  Error loading statute graph: {e}")
            return {}
    
    def _get_embedding(self, text: str, task_type: str) -> list[float]:
        """Get actual embedding or random fallback for testing."""
        if self.gemini_enabled:
            result = self.genai.embed_content(
                model="models/gemini-embedding-001",
                content=text,
                task_type=task_type
            )
            return result['embedding']
        else:
            # Dummy embedding for testing architecture without crashing
            return [random.uniform(-1, 1) for _ in range(768)]

    def load_statutes(self):
        """Load statute chunks from files and embed them."""
        statute_dir = Path(STATUTE_FILES_DIR)
        
        if not statute_dir.exists():
            return
        
        statute_files = sorted(statute_dir.glob("*.txt"))
        if not statute_files:
            return
        
        print(f"Loading {len(statute_files)} statute chunks...")
        documents, metadatas, ids = [], [], []
        
        for idx, file_path in enumerate(statute_files):
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
            if not content:
                continue
            
            document_id = file_path.stem
            documents.append(content)
            metadatas.append({"filename": file_path.name, "source": document_id})
            ids.append(document_id)
        
        if documents:
            embeddings = [self._get_embedding(doc, "retrieval_document") for doc in documents]
            
            self.collection.add(
                documents=documents,
                embeddings=embeddings,
                metadatas=metadatas,
                ids=ids
            )
            self.loaded = True
    
    def _expand_with_graph(self, seed_ids: list[str]) -> list[str]:
        if not self.statute_graph or "statute_relationships" not in self.statute_graph:
            return seed_ids
        
        relationship_map = self.statute_graph["statute_relationships"]
        expanded_ids = set(seed_ids)
        
        for seed_id in seed_ids:
            if seed_id in relationship_map:
                node = relationship_map[seed_id]
                if "related" in node:
                    expanded_ids.update(node["related"])
        return list(expanded_ids)
    
    def retrieve(self, query: str) -> list[dict]:
        if not self.loaded and not self.collection.count():
            return []
        
        query_embedding = self._get_embedding(query, "retrieval_query")
        
        seed_count = min(2, TOP_K_CHUNKS)
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=seed_count
        )
        
        seed_ids = []
        seed_chunks = []
        
        if results and results["documents"] and len(results["documents"]) > 0:
            docs = results["documents"][0]
            distances = results["distances"][0] if results["distances"] else []
            metadatas = results["metadatas"][0] if results["metadatas"] else []
            
            for i, doc in enumerate(docs):
                source = metadatas[i].get("filename", "unknown") if i < len(metadatas) else "unknown"
                chunk_id = Path(source).stem
                seed_ids.append(chunk_id)
                seed_chunks.append({
                    "content": doc,
                    "source": source,
                    "distance": float(distances[i]) if i < len(distances) else 0.0
                })
        
        expanded_ids = self._expand_with_graph(seed_ids)
        retrieved_chunks = seed_chunks.copy()
        
        # Pull extra documents from DB if needed
        return retrieved_chunks
