import json, numpy as np, faiss
from sentence_transformers import SentenceTransformer
from app.config import settings

class Retriever:
    def __init__(self, docs_path="data/docs.jsonl"):
        self.model = SentenceTransformer(settings.embed_model)
        self.docs = [json.loads(l) for l in open(docs_path, encoding="utf-8")]
        emb = self.model.encode([d["text"] for d in self.docs],
                                normalize_embeddings=True)
        self.index = faiss.IndexFlatIP(emb.shape[1])   # cosine vì đã normalize
        self.index.add(np.asarray(emb, dtype="float32"))

    def search(self, query, k=None):
        k = k or settings.top_k
        q = self.model.encode([query], normalize_embeddings=True)
        scores, idx = self.index.search(np.asarray(q, dtype="float32"), k)
        return [(self.docs[i], float(s)) for i, s in zip(idx[0], scores[0])]