from prompt_templates import (
    alignment_prompt,
    translation_improvement_prompt,
    glossary,
)

from utils import (
    query_gpt,
    AlignmentResult,
    TranslationImprovementResult,
)

import os
import json
import hashlib

en_chapter_dir = "./"
zh_chapter_dir = "../books/"

exemplar_chapter_nums = [
    (2, 24)
]

os.makedirs("log", exist_ok=True)

def find_file(dir: str, filename_prefix: str):
    for file in os.listdir(dir):
        if file.startswith(filename_prefix):
            return os.path.join(dir, file)
    return None
                
def align_paragraphs(en_text: str, zh_text: str) -> list[dict[str, str]]:
    en_paragraphs = en_text.split("\n\n")
    en_paragraphs = [p.strip() for p in en_paragraphs if p.strip()]
    
    zh_paragraphs = zh_text.split("\n\n")
    zh_paragraphs = [p.strip() for p in zh_paragraphs if p.strip()]
    
    input_paragraphs = {
        "english_paragraphs": [{"language": "en", "content": en_paragraph} for en_paragraph in en_paragraphs],
        "chinese_paragraphs": [{"language": "zh", "content": zh_paragraph} for zh_paragraph in zh_paragraphs]
    }
    
    prompt = alignment_prompt.format(input_paragraphs=input_paragraphs)
    prompt_hash = hashlib.sha256(prompt.encode("utf-8")).hexdigest()
    with open(f"log/alignment_prompt_{prompt_hash}.md", "w", encoding="utf-8") as f:
        f.write(prompt)
    
    results: AlignmentResult = query_gpt(prompt, AlignmentResult)
    
    all_paragraphs = "\n\n".join([p.content for p in results.merged_paragraphs])
    all_paragraphs_hash = hashlib.sha256(all_paragraphs.encode("utf-8")).hexdigest()
    with open(f"log/alignment_results_{all_paragraphs_hash}.md", "w", encoding="utf-8") as f:
        f.write(all_paragraphs)
    
    print(f"翻译前的中英对照结果已保存至：log/alignment_results_{all_paragraphs_hash}.md")
    return results.merged_paragraphs

def polish_translation(en_text: str, zh_text: str) -> str:
    ref_texts = {}
    for id, (volume_num, chapter_num) in enumerate(exemplar_chapter_nums):
        en_path, zh_path = find_en_zh_paths(volume_num, chapter_num)
        if en_path is None or zh_path is None:
            print(f"未找到章节{volume_num}卷{chapter_num}章的英文章节或中文章节，跳过此参考")
            continue
        
        with open(en_path, "r", encoding="utf-8") as f:
            en_text = f.read()
        
        with open(zh_path, "r", encoding="utf-8") as f:
            zh_text = f.read()
        
        ref_texts[f"snippet_{id+1}"] = {
            "paragraphs": align_paragraphs(en_text, zh_text),
        }
    
    paragraphs = align_paragraphs(en_text, zh_text)
    prompt = translation_improvement_prompt.format(
        input_paragraphs=json.dumps(paragraphs, ensure_ascii=False),
        glossary=json.dumps(glossary, ensure_ascii=False),
        ref_texts=json.dumps(ref_texts, ensure_ascii=False),
    )
    
    prompt_hash = hashlib.sha256(prompt.encode("utf-8")).hexdigest()
    with open(f"log/translation_improvement_prompt_{prompt_hash}.md", "w", encoding="utf-8") as f:
        f.write(prompt)
        
    results: TranslationImprovementResult = query_gpt(prompt, TranslationImprovementResult)
    zh_paragraphs = "\n\n".join([p.content for p in results.paragraphs if p.language == "zh"])
    all_paragraphs = "\n\n".join([p.content for p in results.paragraphs])
    
    all_paragraphs_hash = hashlib.sha256(all_paragraphs.encode("utf-8")).hexdigest()
    with open(f"log/translation_improvement_results_{all_paragraphs_hash}.md", "w", encoding="utf-8") as f:
        f.write(all_paragraphs)
    
    print(f"翻译后的中英对照结果已保存至：log/translation_improvement_results_{all_paragraphs_hash}.md")
    return zh_paragraphs

def new_translation(en_text: str) -> str:
    raise NotImplementedError("从零翻译尚未实现")

def find_en_zh_paths(volume_num: int, chapter_num: int) -> tuple[str, str]:
    en_path = find_file(os.path.join(en_chapter_dir, str(volume_num).zfill(2)), str(chapter_num).zfill(3))
    zh_path = find_file(os.path.join(zh_chapter_dir, str(volume_num).zfill(2)), str(chapter_num).zfill(3))
    return en_path, zh_path

def translate_chapter(volume_num: int, chapter_num: int, inplace: bool = False):
    en_path, zh_path = find_en_zh_paths(volume_num, chapter_num)

    if en_path is None:
        raise FileNotFoundError(f"未找到英文章节：{volume_num}卷{chapter_num}章")
    print(f"找到英文章节：{en_path}")
    
    if zh_path is None:
        print(f"未找到已有中文章节：{volume_num}卷{chapter_num}章，将从零开始翻译")
    else:
        print(f"找到已有中文章节：{zh_path}，是否在此基础上进行润色(y)，还是从头开始翻译(n)？（y/n）")
        answer = input().lower().strip()
        assert answer in ["y", "n"]
        
        if answer == "n":
            zh_path = None
    
    with open(en_path, "r", encoding="utf-8") as f:
        en_text = f.read()
    
    if zh_path is None:
        zh_text = new_translation(en_text)
    else:
        with open(zh_path, "r", encoding="utf-8") as f:
            zh_text = f.read()
        zh_text = polish_translation(en_text, zh_text)
    
    save_path = zh_path if inplace else zh_path.replace(".md", "_new.md")
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(zh_text)
    
    print(f"翻译结果已保存至：{save_path}")
    
if __name__ == "__main__":
    volume_num = int(input("请输入翻译卷号（例：《小玛德莱娜》对应02）："))
    chapter_num = int(input("请输入翻译章节号（例：《小玛德莱娜》对应033）："))
    inplace = (input("翻译结果是否直接覆盖原文（y/n）：").lower().strip() == "y")
    if chapter_num in exemplar_chapter_nums and find_en_zh_paths(volume_num, chapter_num - 1)[1] is not None:
        use_prev_chapter = (input("是否使用上一章节的已有译文作为上下文参考？这取决于你认为上一章节的译文是否高质量（y/n）：").lower().strip() == "y")
        if use_prev_chapter:
            exemplar_chapter_nums.append((volume_num, chapter_num - 1))
    
    print(f"使用以下章节的已有译文作为上下文参考：")
    for volume_num, chapter_num in exemplar_chapter_nums:
        print(f"{volume_num}卷{chapter_num}章")
    
    translate_chapter(volume_num, chapter_num, inplace)