import json
from pydantic import ValidationError
from groq import Groq
from app.config import settings
from app.schema import FinancialRecord

client = Groq(api_key=settings.groq_api_key)

SYSTEM = (
    "Bạn trích xuất số liệu tài chính từ văn bản và CHỈ trả về JSON. "
    "Các khóa: ticker, period, revenue_bn, net_profit_bn, total_assets_bn, "
    "equity_bn, total_liabilities_bn, eps. Khóa nào không có dữ liệu thì để null."
)

def _call_llm(user_content: str) -> dict:
    """Gọi Groq 1 lần, trả về dict (chưa validate)."""
    resp = client.chat.completions.create(
        model="qwen/qwen3.6-27b",
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": user_content},
        ],
        response_format={"type": "json_object"},
        temperature=0,
        max_tokens=1024,   # đủ rộng để JSON hoàn chỉnh không bị cụt
    )
    return json.loads(resp.choices[0].message.content)

def extract_from_text(text: str, max_retries: int = 2) -> FinancialRecord | None:
    user_content = text
    for attempt in range(max_retries + 1):     # +1 vì lần đầu cũng tính
        try:
            data = _call_llm(user_content)
            return FinancialRecord(**data)      # khớp schema -> trả luôn
        except ValidationError as e:
            print(f"[Lần {attempt + 1}] validate fail, đang thử lại...")
            user_content = (
                f"Văn bản: {text}\n\n"
                f"JSON bạn trả lần trước SAI schema, lỗi:\n{str(e)}\n\n"
                f"Hãy trả lại JSON đúng schema."
            )
        except Exception as e:                       # lỗi API / JSON hỏng / hết token
            print(f"[Lần {attempt}] lỗi gọi LLM: {e}")
            continue    
    return None