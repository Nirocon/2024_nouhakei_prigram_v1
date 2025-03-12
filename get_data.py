import matplotlib.pyplot as plt
import serial
import threading

event = threading.Event()

def main():
    ser = serial.Serial('COM6', 9600, timeout=3) # COM3ポートを9600bpsで開く
    input = ""
    x, y = [], []

    while not event.is_set():
        input += ser.read(10).decode() # 10バイト読み込み

        if len(input.split('\n')) > 2:
            for i in input.split('\n')[:-1]: # 最後の\nを除く
                print(i) # 文字列を出力

                x.append(int(i.split(',')[1])) # x座標(時間)
                y.append(int(i.split(',')[0])) # y座標(電圧)

                if len(x) > 300: # 300個まで保存
                    x.pop(0)
                    y.pop(0)

            input = input.split('\n')[-1] # 最後の\n以降をinputに戻す
            
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
