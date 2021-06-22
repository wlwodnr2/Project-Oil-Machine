#include <Adafruit_PWMServoDriver.h>
#include <Adafruit_INA219.h>
#define ndel 200
#define Servo_freq 50  //서보모터 주파수, 기본 50Hz

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0X43);
Adafruit_INA219 current(0x40);

void movearm(int arm_bf[], int arm_af[], int del, int sw) {
  int arm_diff[4];
  arm_diff[0] = (arm_af[0] - arm_bf[0]) / 10; //0번 축 차이
  arm_diff[1] = (arm_af[1] - arm_bf[1]) / 10; //5번 축 차이
  arm_diff[2] = (arm_af[2] - arm_bf[2]) / 10; //7번 축 차이
  switch (sw) {
    case 1:
      arm_diff[3] = 16;
      break;
    case 0:
      arm_diff[3] = 0;
      break;
    case -1:
      arm_diff[3] = -16;
      break;
  }
  //  arm_diff[3] = (arm_af[4] -/ arm_bf[4]) / 10; //11번 축 차이

  if (del >= 0 ) { //delay가 50 초과일 경우 빠르게 증가
    for (int i = 0; i < 10; i++) {
      arm_bf[0] += arm_diff[0];
      arm_bf[1] += arm_diff[1];
      arm_bf[2] += arm_diff[2];
      //      arm_bf[4] += arm_diff[3];
      arm_bf[4] = constrain(arm_bf[4] + arm_diff[3], 100, 280);

      pwm.setPWM(11, 0, arm_bf[4]);
      pwm.setPWM(0, 0, arm_bf[0]);
      pwm.setPWM(5, 0, arm_bf[1]);
      pwm.setPWM(7, 0, arm_bf[2]);

      Serial.print(arm_bf[0]);
      Serial.print(arm_bf[1]);
      Serial.print(arm_bf[2]);
      Serial.println(arm_bf[4]);
      delay(del);
    }
  }
  //  else { //delay 작으면 천천히 스무스하게 증가
  //    for (int i = arm_bf[1]; i < arm_af[1]; i++) {
  //      arm_bf[0] += arm_diff[0];
  //      arm_bf[1] += 1;
  //      arm_bf[2] += arm_diff[2];
  //      arm_bf[3] += arm_diff[3];
  //
  //      pwm.setPWM(11, 0, arm_bf[3]);
  //      pwm.setPWM(0, 0, arm_bf[0]);
  //      pwm.setPWM(5, 0, i);
  //      pwm.setPWM(7, 0, arm_bf[2]);
  //      delay(del);
  //    }
  //  }
  //  Serial.print(arm_bf[0]); Serial.print(" "); Serial.print(arm_bf[1]); Serial.print(" ");
  //  Serial.print(arm_bf[2]); Serial.print(" "); Serial.print(arm_bf[3]); Serial.print(" "); Serial.println(arm_bf[4]);
}
class ServoMotor {
    const int init[5] = {110, 410, 400, 0, 280}; //0번 PIN0, 1번 PIN5, 2번 PIN7, 3번 PIN9, 4번 PIN11, 초기값 FIX
    //110 400 350
    int arm_bf[5] = {init[0], init[1], init[2], init[3], init[4]};
    int arm_af[20][3] = {
      {110, 250, 200}, //주유커버 바로 앞 대기 전 동작
      {180, 250, 160}, //주유 커버 오픈 고정
      {130, 250, 170}, //주유 커버 오픈 고정 170 250 160
      {170, 410, 430}, //주유캡 앞으로 위치 (구멍 전 대기)
      {190, 360, 410}, // 주유캡 바로 앞 대기(열 때)210.340.390
      {230, 250, 350}, //주유 캡 앞으로 위치 (구멍 들어감)230 260 370
      {170, 410, 500}, // 주유동작 1
      {300, 110, 500}, // 주유동작 2
      {220, 260, 350},//주유 캡 꽂기 (닫을 때)
      {200, 320, 390}, // 주유캡 바로 앞 대기 (닫을 때)220 300 380210, 320,380  380
      {170, 410, 510},// 주유커버 닫는 동작 1-1 뒤로빼기 170 410 510
      {500, 90, 510}, //주유커버 닫는 동작 1-2 반대편으로 이동 500 90 510
      {500, 90, 470}, //주유커버 닫는 동작 1-3 차에 가깝게  500 90 440
      {420, 110, 470},//주유커버 닫기 중간단계    400 90 430 닫기단계
      {380, 110, 440}, //주유커버 닫기 단계  400 110 500
      {380, 110, 500},// 주유커버 닫기  400 300 500
      {120, 300, 500},//주유커버 밀어서 넣기
    };
    unsigned long time_bf = 0;
    bool start = true;
    float j = 0;
  public:

    void set() {
      pwm.begin();
      pwm.setOscillatorFrequency(27000000);
      pwm.setPWMFreq(Servo_freq);
      current.setCalibration_32V_1A();
      current.begin();

      pwm.setPWM(0, 0, arm_bf[0]); //초기값 동작
      pwm.setPWM(5, 0, arm_bf[1]);
      pwm.setPWM(7, 0, arm_bf[2]);
      pwm.setPWM(8, 0, arm_bf[3]);
      pwm.setPWM(11, 0, arm_bf[4]);
    }

    void operate(int mode) {
      switch (mode) {
        case 1:// 커버열고 구멍 앞 대기
          movearm(arm_bf, arm_af[0] , 70, 0);
          movearm(arm_bf, arm_af[1] , 100, 0);
          delay(1500);
          movearm(arm_bf, arm_af[2] , 50, 0);
          movearm(arm_bf, arm_af[3] , 70, 0);
          break;

        case 2:// 뚜껑 따고 구멍 앞 대기
          pwm.setPWM(11, 0, 255);
          arm_bf[4] = 255;
          movearm(arm_bf, arm_af[4] , 70, 0);
          delay(500);
          movearm(arm_bf, arm_af[5] , 70, -1);
          delay(2000);
          pwm.setPWM(11, 0, 280);
          arm_bf[4] = 280;
          delay(1000);//잡기

          pwm.setPWM(8, 0, 100);
          time_bf = millis();
          delay(2200);
          movearm(arm_bf, arm_af[3] , 70, 0);
          time_bf = millis() - time_bf;
          pwm.setPWM(8, 0, 0);
          Serial.println(time_bf);

          pwm.setPWM(8, 0, 500);
          delay(2755);//2875
          pwm.setPWM(8, 0, 0);
          break;

        case 3: //주유동작
          movearm(arm_bf, arm_af[6], 100, 0);
          movearm(arm_bf, arm_af[7], 100, 0);
          break;

        case 4:// 뚜껑 닫고 구멍 앞 대기
          movearm(arm_bf, arm_af[6], 100, 0);
          movearm(arm_bf, arm_af[3], 100, 0);
          movearm(arm_bf, arm_af[9] , 0, 0); //주유캡 바로 앞 대기2
          delay(2000);
          movearm(arm_bf, arm_af[8], 70, 0);
          delay(2000);
          time_bf = millis();
          pwm.setPWM(8, 0, 500);
          unsigned long error_det;
          while (1) {
            error_det = millis() - time_bf;
            if (error_det > 600) {
              j = fabs(current.getCurrent_mA());
              Serial.println(j);
              if (j > 400) {
                if (error_det < 1000) continue;
                else break;
              }
            }
          }
          time_bf = millis() - time_bf;
          pwm.setPWM(8, 0, 0);
          pwm.setPWM(11, 0, 100);
          arm_bf[4] = 100;
          delay(1000);
          movearm(arm_bf, arm_af[3] , 70, 0);
          pwm.setPWM(8, 0, 100);
          delay(time_bf);
          pwm.setPWM(8, 0, 0);
          pwm.setPWM(11, 0, 280);
          arm_bf[4] = 280;
          break;

        case 5: //주유커버 닫기
          movearm(arm_bf, arm_af[10] , 120, 0);
          movearm(arm_bf, arm_af[11] , 120, 0);
          movearm(arm_bf, arm_af[12] , 120, 0);
          movearm(arm_bf, arm_af[13] , 200, 0);
          movearm(arm_bf, arm_af[14] , 120, 0);
          delay(1000);
          movearm(arm_bf, arm_af[15] , 120, 0);
          movearm(arm_bf, arm_af[16] , 120, 0);
          movearm(arm_bf, init, 70, 0);
          break;
      }
    }
};