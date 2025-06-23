import matplotlib.pyplot as plt
import serial
import threading
from datetime import datetime
import csv

event = threading.Event()

def main():
    ser = serial.Serial('/dev/cu.usbserial-0001', 9600, timeout=3) # COM3ポートを9600bpsで開く
    input_buf = ""
    x, y = [], []
    all_data = []

    while not event.is_set():
        input_buf += ser.read(10).decode(errors="ignore") # 10バイト読み込み

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

                    all_data.append((voltage, timestamp))

                    if len(x) > 300:
                        x.pop(0)
                        y.pop(0)

                except Exception as e:
                    print(f"[Warning] スキップされた行: '{line}' → {e}")
                    continue

            input_buf = lines[-1] # 最後の\n以降をinputに戻す
            
            plt.clf()
            plt.plot(x, y) # グラフを描画
            plt.pause(0.1)
    
    plt.plot(x, y)
    plt.show(block=False)
    
    input("Click [Enter] to quit.")
    
    # ファイル名を年月日時分秒で作成
    filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".csv"
    try:
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["voltage", "timestamp"])
            writer.writerows(all_data)
        print(f"[INFO] 測定データを {filename} に保存しました。")
    except Exception as e:
        print(f"[ERROR] ファイル保存失敗: {e}")    

def stopper():
    input("Click [Enter] to stop running.")
    event.set()

if __name__ == "__main__":
    main_thread = threading.Thread(target=stopper, daemon=True)
    main_thread.start()

    main()