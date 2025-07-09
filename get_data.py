import matplotlib.pyplot as plt
import serial
import threading
from datetime import datetime
import csv

event = threading.Event()

def main():
    try:
        ser = serial.Serial('COM3', 9600, timeout=3) # COM3ポートを9600bpsで開く
    except Exception as e:
        print(f"[ERROR] シリアル通信失敗: \n{e}")
        return
    input_buf = ""
    x, y = [], []
    header_x, header_y = "timestamp", "voltage"
    all_data = []

    plt.ion() # インタラクティブモードに設定
    while not event.is_set():
        try:
            input_buf += ser.read(50).decode(errors="ignore") # 50バイト読み込み
        except Exception as e:
            print(f"[WARNING] データ読み込み失敗: \n{e}")
            continue
        
        if "\n" in input_buf:
            lines = input_buf.split('\n')
            for line in lines[:-1]: # 最後の\nを除く
                print(line) # 文字列を出力

                try:
                    parts = line.strip().split(',')

                    if len(parts) != 2:
                        raise ValueError("Invalid format")

                    voltage = int(parts[0])
                    timestamp = int(parts[1])

                    x.append(timestamp)
                    y.append(voltage)

                    all_data.append((timestamp, voltage))

                    if len(x) > 3000:
                        x.pop(0)
                        y.pop(0)

                except Exception as e:
                    print(f"[Warning] スキップされた行: '{line}' → {e}")
                    continue

            input_buf = lines[-1] # 最後の\n以降をinputに戻す
            

            plt.clf() # グラフをクリア
            plt.xlabel(header_x)
            plt.ylabel(header_y)
            plt.plot(x, y) # グラフを描画
            plt.pause(0.1)
    
    plt.ioff()
    plt.xlabel(header_x)
    plt.ylabel(header_y)
    plt.plot(x, y)
    plt.show(block=False)
    
    input("Click [Enter] to quit.\n")
    
    # ファイル名を年月日時分秒で作成
    filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".csv"
    try:
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([header_x, header_y])
            writer.writerows(all_data)
        print(f"[INFO] 測定データを {filename} に保存しました。\n")
    except Exception as e:
        print(f"[ERROR] ファイル保存失敗: \n{e}\n")    

def stopper():
    input("Click [Enter] to stop running.\n")
    event.set()

if __name__ == "__main__":
    main_thread = threading.Thread(target=stopper, daemon=True)
    main_thread.start()

    main()