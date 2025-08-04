import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline
from app.prompts import build_prompt
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("screening-api")

app = FastAPI()

# Хелсчек
@app.get("/healthz")
def health():
    return {"status": "ok"}

# Загружаем модель
try:
    logger.info("Загрузка генеративной модели...")
    model_name = os.getenv("LLM_MODEL", "tiiuae/falcon-7b-instruct")  # можно заменить
    gen_pipeline = pipeline("text-generation", model=model_name, tokenizer=model_name, max_new_tokens=500)
    logger.info("Модель успешно загружена.")
except Exception as e:
    logger.exception("Ошибка загрузки модели:")
    raise RuntimeError("Не удалось загрузить модель")

class ScreeningRequest(BaseModel):
    text: str

@app.post("/screen/")
def screen_text(req: ScreeningRequest):
    text = req.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Текст пуст")

    try:
        prompt = build_prompt(text)
        result = gen_pipeline(prompt)[0]["generated_text"]
        return {
            "status": "ok",
            "summary": result.strip()
        }
    except Exception as e:
        logger.exception("Ошибка анализа текста:")
        raise HTTPException(status_code=500, detail="Ошибка анализа текста")
