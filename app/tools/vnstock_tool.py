import pandas as pd
from vnstock.api.financial import Finance
from app.schema import FinancialRecord
def fetch_income_statement(ticker, source="VCI"):
    return Finance(symbol=ticker, source=source).income_statement(period="year")

def fetch_balance_sheet(ticker, source="VCI"):
    return Finance(symbol=ticker, source=source).balance_sheet(period="year")

def get_value(df, item_id, year):
    """Lấy giá trị thô của một chỉ tiêu (theo item_id) ở một năm. Trả float hoặc None."""
    row = df[df["item_id"] == item_id]
    if row.empty:
        return None
    value = row[year].values[0]
    if pd.isna(value):
        return None
    return value

def build_record(ticker, year):
    """Lấy báo cáo của 1 mã, rút các chỉ tiêu cần, trả về FinancialRecord."""
    df = fetch_income_statement(ticker)

    revenue = get_value(df, "net_sales", year)
    net_profit = get_value(df, "net_profit_loss_after_tax", year)
    eps = get_value(df, "eps_basic_vnd", year)

    return FinancialRecord(
        ticker=ticker,
        period=year,
        revenue_bn= revenue / 1e9 if revenue is not None else None,
        net_profit_bn= net_profit / 1e9 if net_profit is not None else None,
        eps= eps
    )

def build_record(ticker, year):
    df_is = fetch_income_statement(ticker)          # đổi tên cũ cho rõ: income statement
    df_bs = fetch_balance_sheet(ticker)         

    revenue = get_value(df_is, "net_sales", year)
    net_profit = get_value(df_is, "net_profit_loss_after_tax", year)
    eps = get_value(df_is, "eps_basic_vnd", year)

    total_assets = get_value(df_bs, "total_assets", year)        
    equity = get_value(df_bs, "owners_equity", year)             
    total_liabilities = get_value(df_bs, "liabilities", year)   

    return FinancialRecord(
        ticker=ticker,
        period=year,
        revenue_bn=revenue / 1e9 if revenue is not None else None,
        net_profit_bn=net_profit / 1e9 if net_profit is not None else None,
        total_assets_bn=total_assets / 1e9 if total_assets is not None else None,
        equity_bn=equity / 1e9 if equity is not None else None,
        total_liabilities_bn=total_liabilities / 1e9 if total_liabilities is not None else None,
        eps=eps,
    )