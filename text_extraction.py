# text_extraction.py
import re
import pytesseract
from PIL import Image
from preprocess_img import preprocess_image

def extract_text(image_path):
    image = preprocess_image(image_path)
    config = '--oem 1 --psm 6'
    return pytesseract.image_to_string(image, lang='jpn+eng', config=config)

def auto_fix_text(text):
    non_empty_lines = [line.strip() for line in text if line.strip()]
    joined_sample = ''.join(non_empty_lines)
    is_japanese = re.search(r'[\u3040-\u30FF\u4E00-\u9FFF]', joined_sample)

    if is_japanese:
        fixed = re.sub(r'[\n\r\u3000 ]+', '', joined_sample)
    else:
        text = re.sub(r'[\n\r]+', ' ', text)
        fixed_lines = []
        for line in text.splitlines():
            if re.fullmatch(r'(\s?[A-Za-z])+\s*', line):
                fixed_lines.append(line.replace(" ", ""))
            else:
                fixed_lines.append(line)
        fixed = "\n".join(fixed_lines)

    return fixed

def split_into_sentences(text):
    pattern = re.compile(r'(.*?[。．.])', re.DOTALL)
    raw_sentences = pattern.findall(text)
    return [s.strip() for s in raw_sentences if len(s.strip()) > 2]

def contains_japanese(text):
    return re.search(r'[\u3040-\u30FF\u4E00-\u9FFF]', text) is not None