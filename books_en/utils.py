import os
import openai
import pydantic
import tiktoken

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
default_model_name = "gpt-4o"
default_encoding_name = "o200k_base"
default_context_window = 128000
default_max_completion_tokens = 16384

def query_gpt(prompt: str, schema: type[pydantic.BaseModel], model_name: str = default_model_name,retries: int = 3) -> type[pydantic.BaseModel]:
    # Use JSON schema
    print(f"输入 token 数：{num_tokens(prompt)} (最多 {default_context_window} )")
    result = None
    for retry in range(retries):
        completion = client.beta.chat.completions.parse(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            response_format=schema,
            max_completion_tokens=min(default_max_completion_tokens, default_context_window - int(num_tokens(prompt) * 1.02)),
            temperature=0.1,
        )
        message = completion.choices[0].message
        if message.parsed:
            result = message.parsed
            with open("log/gpt_output.txt", "w") as f:
                f.write(message.content)
            print(f"输出 token 数：{num_tokens(message.content)}")
            break
        else:
            print(f"失败，重试第 {retry + 1} 次")
    
    assert result is not None
    return result

def num_tokens(string: str, encoding_name: str = default_encoding_name) -> int:
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens