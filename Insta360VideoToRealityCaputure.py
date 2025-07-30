import subprocess
import os

# 動画を保存しているフォルダ　作業フォルダ
path = r'C:\Users\2\Desktop\フォトグラメトリ\16 360Test' + '\\'
# ファイル名 (拡張子は含まず)
filiname ='VID_20250718_092343_00_003_Short'
# 拡張子名
extension ='mp4'

# 出力フォルダ (なければ作る)
output_path = fr'{path}Export' + '\\'
os.makedirs(output_path, exist_ok=True)

input_file_path = f'{path}{filiname}.{extension}'

# 視点リスト(yaw,pitch,roll)


''' 
# 8方向
transforms = (
 ( 0, 0,0),
 ( 45, 0,0),
 ( 90, 0,0),
 ( 135, 0,0),
 ( 180, 0,0),
 (-135, 0,0),
 ( -90, 0,0),
 ( -45, 0,0),
 )
'''

'''
# 8方向＋見上げ4方向
transforms = (
 ( 0, 0,0),
 ( 0, 20,0),
 ( 45, 0,0),
 ( 90, 0,0),
 ( 90, 20,0),
 ( 135, 0,0),
 ( 180, 0,0),
 ( 180, 20,0),
 (-135, 0,0),
 ( -90, 0,0),
 ( -90, 20,0),
 ( -45, 0,0),
 )
'''

#'''　
# 12方向
transforms = (
 ( 0, 0,0),
 ( 30, 0,0),
 ( 60, 0,0),
 ( 90, 0,0),
 ( 120, 0,0),
 ( 150, 0,0),
 ( 180, 0,0),
 (-150, 0,0),
 (-120, 0,0),
 ( -90, 0,0),
 ( -60, 0,0),
 ( -30, 0,0),
 )
#'''

# 画像切り出しのフレームレート 撮影時の移動スピードや対象物からの距離をみて調節
fps = 2

# 明るさ調整 (ただしコントラストが落ち階調も失われるので次のガンマ調整を使った方が良さそう)
brightness = 0

# ガンマ調整
gamma = 1.0


# 各視点で書き出す
for index, transform in enumerate(transforms):

    # 出力ファイル名をつくる
    # %04dで4桁連番
    #output_file_path=fr'{output_path}Output_{index}_%04d.jpg'
    output_file_path=fr'{output_path}{filiname}_%04d_{index}.jpg'

    # v360ライブラリのオプション (16:9にする時は 'h_fov=121.28', 'v_fov=90', 'w=2587', 'h=1455')
    v360_options = ':'.join([
    'input=e', # Equirectangular projection.
    'output=rectilinear', # Regular video.
    'h_fov=90',
    'v_fov=90',
    'w=1920',
    'h=1920',
    # 'interp=gauss',
    f'yaw={transform[0]}',
    f'pitch={transform[1]}',
    f'roll={transform[2]}'
    ])

    # コマンドをつくる
    
    # 順再生
    command = f'ffmpeg -i "{input_file_path}" -vf "v360={v360_options}, eq=gamma={gamma}" -qmin 1 -q 1 -r {fps} "{output_file_path}"'

    # 逆再生
    # command = f'ffmpeg -i "{input_file_path}" -vf "v360={v360_options}, eq=gamma={gamma}, reverse" -qmin 1 -q 1 -r {fps} "{output_file_path}"'

    # ffmpegを実行
    subprocess.call(command, shell=True)



