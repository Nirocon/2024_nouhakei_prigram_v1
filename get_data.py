import matplotlib.pyplot as plt
import serial
import threading
from datetime import datetime
import csv

event = threading.Event()

def main():
    # ファイル名を年月日時分秒で作成
    filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".csv"
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["time", "voltage"])  # ヘッダー

        ser = serial.Serial('COM3', 9600, timeout=3) # COM3ポートを9600bpsで開く
        input = ""
        x, y = [], []

        while not event.is_set():
            input += ser.read(10).decode(errors="ignore") # 10バイト読み込み

            if "\n" in input:
                lines = input.split('\n')
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

                        if len(x) > 300:
                            removed_x = x.pop(0)
                            removed_y = y.pop(0)
                            writer.writerow([removed_y, removed_x]) # 電圧, 時間で保存

                    except Exception as e:
                        print(f"[Warning] スキップされた行: '{line}' → {e}")
                        continue

                input = lines[-1] # 最後の\n以降をinputに戻す
                
                plt.clf()
                plt.plot(x, y) # グラフを描画
                plt.pause(0.1)
        
        plt.plot(x, y)
        plt.show()

if __name__ == "__main__":
    main_thread = threading.Thread(target=main, daemon=True)
    main_thread.start()

    input("Click [Enter] to stop running.")
    event.set()
    
    input("Click [Enter] to quit.")
