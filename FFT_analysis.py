import csv
import matplotlib.pyplot as plt
import numpy as np

def main():
    x, y = [], []
    header_x, header_y = "", ""

    # csvファイルのパスを入力させる
    path = input("Enter the path of the csv file: ")
    if not path.endswith('.csv'):
        raise ValueError("Invalid file format")

    # csvファイルを読み込む
    try:
        with open(path, newline='') as f:
            # 最初の行はヘッダーとして保存する
            reader = csv.reader(f)
            header_x, header_y = next(reader)

            for row in reader:
                x.append(int(row[0]))
                y.append(int(row[1]))
    except Exception as e:
        print(f"[ERROR] Failed to read the csv file: \n{e}")
        return
    
    # サンプル数を計算する
    N = len(y)

    # フーリエ変換を行う
    fft_y = np.fft.fft(y)
    
    # 周波数軸を計算する
    freq = np.fft.fftfreq(N, d=0.001)

    # 振幅軸を計算する
    amp = np.abs(fft_y)

    # 縦軸のヘッダーを書き変える
    header_x = "Amplitude"
    
    # フーリエ変換後の信号をプロットする
    plt.plot(freq[1:int(N/2)], amp[1:int(N/2)]) # 0Hzとナイキスト周波数以降を除く
    plt.xlabel(header_x)
    plt.ylabel(header_y)
    plt.show()

if __name__ == "__main__":
    main()
