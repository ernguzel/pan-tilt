#include <Servo.h>

Servo panServo;  // Yatay hareket için
Servo tiltServo; // Dikey hareket için

int panAngle = 90;  // Başlangıç açısı
int tiltAngle = 90; // Başlangıç açısı
int lastPanAngle = 90; // Son pan açısı
int lastTiltAngle = 90; // Son tilt açısı
int threshold = 1;  // Pan ve tilt hareketi için eşiği belirle

void setup() {
  panServo.attach(9);  // Pan servoyu pin 9'a bağla
  tiltServo.attach(10); // Tilt servoyu pin 10'a bağla
  panServo.write(panAngle);
  tiltServo.write(tiltAngle);

  Serial.begin(9600); // Seri haberleşme başlat
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n'); // Python'dan gelen veriyi al
    int delimiterIndex = data.indexOf(',');
    int dx = data.substring(0, delimiterIndex).toInt();
    int dy = data.substring(delimiterIndex + 1).toInt();

    // Pan ve tilt açılarındaki değişiklikleri hesapla
    int newPanAngle = constrain(panAngle + dx, 0, 180);
    int newTiltAngle = constrain(tiltAngle + dy, 0, 180);

    // Eşik değeri ile hareketi sınırla
    if (abs(newPanAngle - lastPanAngle) > threshold) {
      panAngle = newPanAngle;
      panServo.write(panAngle);
      lastPanAngle = panAngle;
    }

    if (abs(newTiltAngle - lastTiltAngle) > threshold) {
      tiltAngle = newTiltAngle;
      tiltServo.write(tiltAngle);
      lastTiltAngle = tiltAngle;
    }
  }
}
