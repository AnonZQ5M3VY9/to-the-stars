import os
import openai
import pydantic

# Schema

class Paragraph(pydantic.BaseModel):
    language: str
    content: str

class AlignmentResult(pydantic.BaseModel):
    merged_paragraphs: list[Paragraph]

class TranslationImprovementResult(pydantic.BaseModel):
    paragraphs: list[Paragraph]

# LLM API

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def query_gpt(prompt: str, schema: type[pydantic.BaseModel], retries: int = 3) -> type[pydantic.BaseModel]:
    # Use JSON schema
    result = None
    for retry in range(retries):
        completion = client.beta.chat.completions.parse(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format=schema,
        )
        message = completion.choices[0].message
        if message.parsed:
            result = message.parsed
            break
        else:
            print(f"失败，重试第 {retry + 1} 次")
    
    assert result is not None
    return result