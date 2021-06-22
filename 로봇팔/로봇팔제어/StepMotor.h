#include <Stepper.h>
#define stepsPerRevolution 360
#define setspeed 20
#define steps20_ratio_up 10/19
#define steps20_ratio_down 10/17
Stepper myStepper(stepsPerRevolution, 8, 9, 10, 11);

class StepMotor {
    int steps_bf = 0;
  public :
    void set() {
      myStepper.setSpeed(setspeed);
      myStepper.step(240);
      steps_bf = 240;
      Serial.write("ok");
      //      Serial.println(steps_bf);
    }
    void operate(int steps_af) {
      //      steps_af=steps_af*steps_ratio;
      //      if (steps_af > 0) steps_af = round(steps_af/10)*10;
      //      else steps_af = round(steps_af /10)*10;

      myStepper.step(steps_af);
      steps_bf += steps_af;
      //      Serial.println(steps_bf);
      delay(300);
//      Serial.write("ok");
    }
    void operatehandmid(int i) {
      (i > 0) ? myStepper.step(200) : myStepper.step(-200);
      delay(500);
    }
    void backtozero() {
      //      /Serial.print("steps"); Serial.print(" : "); Serial.println(steps_bf);
      myStepper.step(-steps_bf);
      steps_bf -= steps_bf;
    }
};
