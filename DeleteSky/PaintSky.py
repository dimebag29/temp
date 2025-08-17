import os
from PIL import Image

# 入力フォルダと出力フォルダを指定
input_folder = r""
output_folder = r""

# 塗りつぶす色 (R, G, B, A)
fill_color = ( 67, 148, 240, 255)

# 塗りつぶす割合 (上からの高さの比率)
fill_ratio = 0.5  # 上から50%を処理対象にする

# 出力フォルダがなければ作成
os.makedirs(output_folder, exist_ok=True)

# 入力フォルダ内のpngファイルを処理
for filename in os.listdir(input_folder):
    if filename.lower().endswith(".png"):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        # 画像をRGBAで読み込み
        img = Image.open(input_path).convert("RGBA")
        pixels = img.load()

        # 塗りつぶす高さを計算
        target_height = int(img.height * fill_ratio)

        # 上部 target_height の範囲だけ処理
        for y in range(target_height):
            for x in range(img.width):
                r, g, b, a = pixels[x, y]
                if a == 0:  # 完全に透明なら置き換え
                    pixels[x, y] = fill_color

        # 保存
        img.save(output_path, "PNG")

print("処理が完了しました。")
