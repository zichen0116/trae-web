from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ai_service import analyze

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    product_name: str
    reason: str
    price: float
    persona: str = "caishen"
    image_base64: str = ""


@app.post("/api/analyze")
def analyze_endpoint(req: AnalyzeRequest):
    try:
        result = analyze(
            product_name=req.product_name,
            reason=req.reason,
            price=req.price,
            persona=req.persona,
            image_base64=req.image_base64,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI解析失败，请重试: {str(e)}")


@app.get("/health")
def health():
    return {"status": "ok"}
