import json
from app.tools.vnstock_tool import build_record

TICKERS = ["FPT", "HPG", "VNM", "MWG", "VCB"]
YEAR = "2024"

def record_to_docs(r):
    """Biến 1 FinancialRecord thành list doc {id, text}. Bỏ qua trường None."""
    docs = []
    if r.revenue_bn is not None:
        docs.append({
            "id": f"{r.ticker.lower()}_revenue_{r.period}",
            "text": f"Doanh thu thuần của {r.ticker} năm {r.period} là {r.revenue_bn:,.0f} tỷ đồng.",
        })
    if r.net_profit_bn is not None:
        docs.append({
            "id": f"{r.ticker.lower()}_net_profit_{r.period}",
            "text": f"Lợi nhuận sau thuế của {r.ticker} năm {r.period} là {r.net_profit_bn:,.0f} tỷ đồng.",
        })
    if r.total_assets_bn is not None:
        docs.append({
            "id":f"{r.ticker.lower()}_total_assets_{r.period}",
            "text":f"Tổng tài sản của {r.ticker} năm {r.period} là {r.total_assets_bn:,.0f} tỷ đồng."
        })
    if r.eps is not None:
        docs.append({
            "id": f"{r.ticker.lower()}_eps_{r.period}",
            "text": f"Lãi cơ bản trên cổ phiếu (EPS) của {r.ticker} năm {r.period} là {r.eps:,.0f} đồng.",
        })
    if r.equity_bn is not None:
        docs.append({
            "id": f"{r.ticker.lower()}_equity_{r.period}",
            "text": f"Vốn chủ sở hữu của {r.ticker} năm {r.period} là {r.equity_bn:,.0f} tỷ đồng.",
        })

    if r.total_liabilities_bn is not None:
        docs.append({
            "id": f"{r.ticker.lower()}_total_liabilities_{r.period}",
            "text": f"Tổng nợ phải trả của {r.ticker} năm {r.period} là {r.total_liabilities_bn:,.0f} tỷ đồng.",
        })
    return docs

def main():
    all_docs = []
    for t in TICKERS:
        r = build_record(t, YEAR)
        all_docs.extend(record_to_docs(r))
    with open("data/financials.jsonl", "w", encoding="utf-8") as f:
        for d in all_docs:
            f.write(json.dumps(d, ensure_ascii=False) + "\n")
    print(f"Đã ghi {len(all_docs)} doc.")

if __name__ == "__main__":
    main()