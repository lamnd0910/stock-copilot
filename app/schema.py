from pydantic import BaseModel, field_validator

class FinancialRecord(BaseModel):
    """Một bản ghi tài chính của 1 mã trong 1 kỳ.
    ĐƠN VỊ: các trường _bn = tỷ đồng; eps = đồng/cổ phiếu.
    """
    # Định danh (bắt buộc)
    ticker: str
    period: str

    # Số liệu tiền tệ — tỷ đồng (cho phép trống)
    revenue_bn: float | None = None
    net_profit_bn: float | None = None
    total_assets_bn: float | None = None
    equity_bn: float | None = None
    total_liabilities_bn: float | None = None

    # Ngoại lệ đơn vị: đồng/cổ phiếu
    eps: float | None = None

    @field_validator("ticker")
    @classmethod
    def normalize_ticker(cls, v):
        return v.strip().upper()
    
    @field_validator("total_assets_bn")
    @classmethod
    def assets_not_negative(cls, v):
        # v có thể là None (trường cho phép trống) — phải xử lý trường hợp đó trước
        if v is not None and v < 0:
            raise ValueError("total_assets_bn không được âm")   # thông báo lỗi rõ nghĩa
        return v