from app.extractor import extract_from_text
from app.tools.vnstock_tool import build_record

# Bộ test: văn bản + mã/kỳ (để lấy đáp án từ vnstock)
def make_text(r):
    """Sinh câu tin từ số thật, format dấu chấm kiểu Việt để test bẫy đơn vị."""
    rev = f"{int(round(r.revenue_bn)):,}".replace(",", ".")   # cố ý sai gấp đôi
    profit = f"{int(round(r.net_profit_bn)):,}".replace(",", ".")
    return (f"Năm {r.period}, {r.ticker} đạt doanh thu thuần {rev} tỷ đồng "
            f"và lợi nhuận sau thuế {profit} tỷ đồng.")

TICKERS = ["FPT", "HPG", "VNM", "MWG"]   # bỏ VCB: ngân hàng, revenue_bn = None
YEAR = "2024"

GOLD = []
for t in TICKERS:
    r = build_record(t, YEAR)
    GOLD.append({"ticker": t, "year": YEAR, "text": make_text(r)})

FIELDS = ["revenue_bn", "net_profit_bn"]   # tạm chấm 2 trường này

def values_match(pred, true, rel_tol=0.02):
    if pred is None and true is None:
        return True
    if pred is None or true is None:
        return False
    return abs(pred - true) <= rel_tol * abs(true)  

def main():
    correct = {f: 0 for f in FIELDS}
    total = {f: 0 for f in FIELDS}
    for ex in GOLD:
        truth = build_record(ex["ticker"], ex["year"])
        pred = extract_from_text(ex["text"])
        for f in FIELDS:
            total[f] += 1
            true_v = getattr(truth, f)
            pred_v = getattr(pred, f) if pred is not None else None
            ok = values_match(pred_v, true_v)
            if ok:
                correct[f] += 1
            print(f"{ex['ticker']} {f}: pred={pred_v}  true={true_v}  {'✓' if ok else '✗'}")
    # vòng này CHỈ in tổng kết, không chấm lại
    for f in FIELDS:
        print(f"{f}: {correct[f]}/{total[f]} = {correct[f] / total[f]:.0%}")

        
if __name__ == "__main__":
    main()