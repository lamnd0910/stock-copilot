from app.schema import FinancialRecord

def test_record_valid():
    r = FinancialRecord(ticker="FPT", period="2024", revenue_bn=62848.79)
    assert r.ticker == "FPT"
    assert r.revenue_bn == 62848.79

def test_ticker_normalized():
    r = FinancialRecord(ticker="  fpt  ", period="2024")
    assert r.ticker == "FPT"      # validator viết hoa + cắt khoảng trắng