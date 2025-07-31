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

# ADE20Kにおける "sky" クラスのID
sky_class_id = 2
tile_size = 512

# 空透過処理
def process_tile(tile_img):
    inputs = feature_extractor(images=tile_img, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        pred = logits.argmax(dim=1)[0].cpu().numpy()
    mask = Image.fromarray(pred.astype(np.uint8)).resize(tile_img.size, resample=Image.NEAREST)
    mask = np.array(mask)
    alpha = np.where(mask == sky_class_id, 0, 255).astype(np.uint8)
    tile_rgba = tile_img.convert("RGBA")
    tile_np = np.array(tile_rgba)
    tile_np[..., 3] = alpha
    return Image.fromarray(tile_np)

# 画像を処理
for filename in os.listdir(input_path):
    if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        continue

    img_path = os.path.join(input_path, filename)
    image = Image.open(img_path).convert("RGB")
    width, height = image.size

    # 出力用の空画像（RGBA）を作成
    result_img = Image.new("RGBA", (width, height))

    # タイルごとに処理
    for top in range(0, height, tile_size):
        for left in range(0, width, tile_size):
            right = min(left + tile_size, width)
            bottom = min(top + tile_size, height)
            tile = image.crop((left, top, right, bottom))
            processed_tile = process_tile(tile)
            result_img.paste(processed_tile, (left, top))

    # 保存
    output_file = os.path.splitext(filename)[0] + ".png"
    output_img_path = os.path.join(output_path, output_file)
    result_img.save(output_img_path)
    print(f"保存しました: {output_img_path}")
