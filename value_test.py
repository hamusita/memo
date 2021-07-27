import ctypes
import numpy as np
import multiprocessing as mp
import cv2
import pickle

def valueToNdarray(v):
    return np.ctypeslib.as_array(v.get_obj())  # Valueからndarrayに変換

def ndarrayToValue(n):
    n_h, n_w, n_ch = n.shape  # サイズ、チャンネル数を取得
    v = mp.Value(((ctypes.c_uint8 * n_ch) * n_w) * n_h)  # 同サイズ、同チャンネル数の共有メモリを生成
    valueToNdarray(v)[:] = n  # コピー
    return v

def filter(v):
    n = valueToNdarray(v)  # Valueからndarrayに変換
    n_h, n_w, n_ch = n.shape  # 画像サイズ、チャンネル数の取得
    M = cv2.getRotationMatrix2D((n_w / 2, n_h / 2), 45, 1)  # 画像の中心を軸に45度回転する行列を求める
    n[:] = cv2.warpAffine(n, M, (n_w, n_h))  # 生成した行列で画像を回転させる

if __name__ == '__main__':
    # 適当な画像からndarrayの生成
    input_img = cv2.imread(r"img_path")
    print(type(input_img))

    # Valueに変換
    v = ndarrayToValue(input_img)

    # 画像を45度回転するプロセスを生成
    p = mp.Process(target = filter, args = (v, ))
    p.start()  # プロセスの開始
    p.join()  # プロセスの終了待機

    # 処理結果をndarrayに変換
    output_img = valueToNdarray(v)

    # プレビュー
    cv2.imshow("input", input_img)
    cv2.imshow("output", output_img)
    cv2.waitKey(0)