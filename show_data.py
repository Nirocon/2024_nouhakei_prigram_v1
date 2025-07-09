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
    
    # データをnumpy配列に変換してプロット
    x, y = np.array(x), np.array(y)
    plt.xlabel(header_x)
    plt.ylabel(header_y)
    plt.plot(x, y)
    plt.show()

if __name__ == "__main__":
    main()
