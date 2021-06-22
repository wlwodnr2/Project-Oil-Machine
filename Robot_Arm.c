#include "ServoMotor.h"
#include "StepMotor.h"

ServoMotor servoM;
StepMotor stepM;

int mode = 0;
int sw;
void setup() {
  Serial.begin(9600);
  servoM.set();
  stepM.set();
}

void serialEvent() {
  mode = Serial.parseInt();
  Serial.println(mode);
  if (mode / 1000 == 0) {
    stepM.operate(mode % 1000);
    Serial.write("ok");
  }
  else {
    sw = mode / 1000;
    switch (sw) {
      case 1: // 커버열기  
        servoM.operate(1);
        Serial.write("ok");
        break;
      case 2: // 캡따기
        servoM.operate(2);
        Serial.write("ok");
        break;
      case 3: // 주유
        servoM.operate(3);
        Serial.write("ok");
        break;
      case 4: // 캡닫기
        servoM.operate(4);
        Serial.write("ok");
        break;
      case 5: // 커버닫기
        servoM.operate(5);
        Serial.write("ok");
        break;
      case 6: // 손중앙
        stepM.operatehandmid(mode % 1000);
        Serial.write("ok");
        break;
      case 7: // 종료
        stepM.backtozero();
        Serial.write("ok");
        break;
    }
  }
}

void loop() {

}