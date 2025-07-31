import os
import torch
import numpy as np
from PIL import Image
from transformers import SegformerFeatureExtractor, SegformerForSemanticSegmentation

# 入出力フォルダ
input_path = r''
output_path = r''
os.makedirs(output_path, exist_ok=True)

# モデルと前処理の読み込み
feature_extractor = SegformerFeatureExtractor.from_pretrained("nvidia/segformer-b2-finetuned-ade-512-512")
model = SegformerForSemanticSegmentation.from_pretrained("nvidia/segformer-b2-finetuned-ade-512-512")
model.eval()

# ADE20Kでの sky クラスID
sky_class_id = 2

# 画像を処理
for filename in os.listdir(input_path):
    if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        continue

    # 画像読み込み
    img_path = os.path.join(input_path, filename)
    image = Image.open(img_path).convert("RGB")
    orig_size = image.size

    # 前処理
    inputs = feature_extractor(images=image, return_tensors="pt")

    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits  # shape = (1, 150, H, W)
        pred = logits.argmax(dim=1)[0].cpu().numpy()  # shape = (H, W)

    # 元画像サイズにリサイズ
    mask = Image.fromarray(pred.astype(np.uint8)).resize(orig_size, resample=Image.NEAREST)
    mask = np.array(mask)

    # skyクラスだけ透過 (alpha = 0)、他は不透明 (alpha = 255)
    alpha = np.where(mask == sky_class_id, 0, 255).astype(np.uint8)

    # RGBA合成
    image_rgba = image.convert("RGBA")
    image_np = np.array(image_rgba)
    image_np[..., 3] = alpha  # アルファチャネルを上書き

    # 保存
    output_file = os.path.splitext(filename)[0] + ".png"
    output_img_path = os.path.join(output_path, output_file)
    Image.fromarray(image_np).save(output_img_path)
    print(f"保存しました: {output_img_path}")
