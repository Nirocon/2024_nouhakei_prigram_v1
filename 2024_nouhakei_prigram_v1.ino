#include <BTAddress.h>
#include <BTAdvertisedDevice.h>
#include <BTScan.h>
#include <BluetoothSerial.h>

BluetoothSerial SerialBT;

int i = 0;
unsigned long t = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin( 9600 );
  Serial.println("Serial has been connected.");

  SerialBT.begin("ESP32test");
}

void loop() {
  // put your main code here, to run repeatedly:
  i = analogRead(4); // pin26
  t = millis(); // 時間の取得

  Serial.printf("%d,%d\n", i, t); // 「(電位差),(時間ms)\n」で返す
  delay(100);
}
