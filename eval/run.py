import json
from app.retriever import Retriever

def recall_at_k(retrieved, relevant, k):
    return 1.0 if any(r in relevant for r in retrieved[:k]) else 0.0

def reciprocal_rank(retrieved, relevant):
    for i, r in enumerate(retrieved, start=1):
        if r in relevant:
            return 1.0 / i
    return 0.0

def main(k=5, gold_path="eval/gold.jsonl"):
    print("Đang nạp model embedding (lần đầu tải về nên hơi lâu)...")
    r = Retriever()
    print("Nạp xong, bắt đầu chấm điểm...")
    gold = [json.loads(l) for l in open(gold_path, encoding="utf-8")]
    recalls, rrs = [], []
    for ex in gold:
        ids = [d["id"] for d, _ in r.search(ex["question"], k=k)]
        recalls.append(recall_at_k(ids, ex["relevant_ids"], k))
        rrs.append(reciprocal_rank(ids, ex["relevant_ids"]))
    print(f"Recall@{k}: {sum(recalls)/len(recalls):.3f}")
    print(f"MRR:       {sum(rrs)/len(rrs):.3f}")

if __name__ == "__main__":
    main()