import cv2
from PIL import Image
import os
from pdf2image import convert_from_path

def preprocess_image(image_path):
    ext = os.path.splitext(image_path)[-1].lower()

    if ext == ".pdf":
        try:
            images = convert_from_path(image_path, dpi=300)
            if not images:
                raise RuntimeError("PDFから画像が抽出できませんでした。")
            pil_image = images[0]
            image_path = "converted_from_pdf.png"
            pil_image.save(image_path)
        except Exception as e:
            raise RuntimeError(f"PDFの変換に失敗しました: {e}")

    unsupported_exts = ['.gif', '.heic', '.webp', '.svg']
    if ext in unsupported_exts or cv2.imread(image_path) is None:
        try:
            with Image.open(image_path) as im:
                image_path = "converted_for_cv2.png"
                im = im.convert("RGB")
                im.save(image_path)
        except Exception as e:
            raise RuntimeError(f"Pillowによる画像変換に失敗しました: {e}")

    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("画像が読み込めません。対応形式か確認してください。")

    height, width = img.shape[:2]
    scale_factor = 200 / 96
    new_height = int(height * scale_factor)
    new_width = int(width * scale_factor)

    resized_image = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_CUBIC)

    gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

    blurred = cv2.GaussianBlur(gray_image, (9, 9), 0)
    unsharp_image = cv2.addWeighted(gray_image, 1.5, blurred, -0.6, 0)

    denoised_image = cv2.bilateralFilter(unsharp_image, 9, 75, 75)

    _, binary_image = cv2.threshold(denoised_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return Image.fromarray(binary_image)