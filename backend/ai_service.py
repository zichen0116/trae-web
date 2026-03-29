import json
import re
from openai import OpenAI
from prompts import build_system_prompt, build_user_message

API_KEY = "sk-be0e3af7df284df5abe735dce5ca6953"
BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
VISION_MODEL = "qwen-vl-max"
TEXT_MODEL = "qwen3.5-flash"

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)


def analyze(product_name: str, reason: str, price: float, persona: str, image_base64: str) -> dict:
    system_prompt = build_system_prompt(persona)
    user_text = build_user_message(product_name, reason, price)

    if image_base64:
        model = VISION_MODEL
        content = [
            {"type": "image_url", "image_url": {"url": image_base64}},
            {"type": "text", "text": user_text},
        ]
    else:
        model = TEXT_MODEL
        content = user_text

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": content},
        ],
    )

    raw = response.choices[0].message.content.strip()
    match = re.search(r'\{[\s\S]*\}', raw)
    if not match:
        raise ValueError(f"AI未返回有效JSON: {raw}")
    return json.loads(match.group())
