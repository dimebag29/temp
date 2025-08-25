import os
import numpy as np
from PIL import Image
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing
from tqdm import tqdm  # 進捗バー表示（pip install tqdm）

# 入力フォルダと出力フォルダ
input_folder = r""
output_folder = r""

# 塗りつぶす色 (R, G, B, A)
fill_color = np.array([67, 148, 240, 255], dtype=np.uint8)

# 塗りつぶす割合 (上からの高さの比率)
fill_ratio = 0.5

# 出力フォルダがなければ作成
os.makedirs(output_folder, exist_ok=True)


def process_file(filename):
    """1枚の画像を処理してJPEG保存する"""
    if not filename.lower().endswith(".png"):
        return None

    input_path = os.path.join(input_folder, filename)
    output_filename = os.path.splitext(filename)[0] + ".jpg"
    output_path = os.path.join(output_folder, output_filename)

    # RGBAで読み込み → NumPy配列に変換
    img = Image.open(input_path).convert("RGBA")
    arr = np.array(img, dtype=np.uint8)

    # 塗りつぶす高さ
    target_height = int(arr.shape[0] * fill_ratio)

    # 上部透過部分を一括置換
    mask = arr[:target_height, :, 3] == 0
    arr[:target_height][mask] = fill_color

    # RGBに変換してJPEG保存
    Image.fromarray(arr[..., :3]).save(output_path, "JPEG", quality=100)

    return filename


if __name__ == "__main__":
    files = [f for f in os.listdir(input_folder) if f.lower().endswith(".png")]

    # CPUコア数
    max_workers = multiprocessing.cpu_count()

    print(f"CPUコア数: {max_workers} で並列処理を実行します。")

    # 並列処理＋進捗バー
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_file, f) for f in files]
        for future in tqdm(as_completed(futures), total=len(futures), desc="処理中"):
            _ = future.result()

    print("すべての処理が完了しました。")
