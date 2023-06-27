#include <MeMCore.h>
#include <Arduino.h>
#include <Wire.h>
#include <SoftwareSerial.h>

void setup() {
  Serial.begin(9600);
}

MeDCMotor motor_9(9);
MeDCMotor motor_10(10);

void move(int direction, int speed) {
  int leftSpeed = 0;
  int rightSpeed = 0;
  if(direction == 1) { // go forward
    leftSpeed = speed;
    rightSpeed = speed;
  } else if(direction == 2) { // go left
    leftSpeed = -speed;
    rightSpeed = -speed;
  } else if(direction == 3) { // turn right
    leftSpeed = -speed;
    rightSpeed = speed;
  } else if(direction == 4) { // turn left
    leftSpeed = speed;
    rightSpeed = -speed;
  }
  motor_9.run((9) == M1 ? -(leftSpeed) : (leftSpeed));
  motor_10.run((10) == M1 ? -(rightSpeed) : (rightSpeed));
}

void _delay(float seconds) { // freezes the program
  long endTime = millis() + seconds * 1000;
  while(millis() < endTime) _loop();
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readString();
    data.trim();
    if(data == "move"){
      move(1, 25 / 100.0 * 255);
      _delay(1);
      motor_9.run(0);
      motor_10.run(0);
    }
    else if(data == "left"){
      motor_10.run(35/100.0*255);
      motor_9.run(50/100.0*255);
      _delay(1);
      motor_9.run(0);
      motor_10.run(0);
    }
    else if(data == "right"){
      motor_9.run(35/100.0*255);
      motor_10.run(50/100.0*255);
      _delay(1);
      motor_9.run(0);
      motor_10.run(0);
    }
    else{
      Serial.println("N");
      return;
    }
    Serial.println("O");
  }
}

void _loop() {
}