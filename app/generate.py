import google.generativeai as genai
from app.config import settings

genai.configure(api_key=settings.gemini_api_key)
_model = genai.GenerativeModel("gemini-2.5-flash")

PROMPT = """Bạn là trợ lý phân tích cổ phiếu. CHỈ dùng thông tin trong NGỮ CẢNH.
Nếu không đủ dữ liệu, nói "Tôi không có đủ dữ liệu". Mọi ý phải trích nguồn [id].

NGỮ CẢNH:
{context}

CÂU HỎI: {question}
TRẢ LỜI:"""

def answer(question, hits):
    context = "\n".join(f"[{d['id']}] {d['text']}" for d, _ in hits)
    return _model.generate_content(
        PROMPT.format(context=context, question=question)
    ).text