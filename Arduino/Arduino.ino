#include <MeMCore.h>
#include <Arduino.h>
#include <Wire.h>
#include <SoftwareSerial.h>

void setup() {
  Serial.begin(9600);
}

MeLineFollower linefollower_2(2); // the line follower sensor is port 2
MeDCMotor motor_9(9);
MeDCMotor motor_10(10);

void align() { // get both captors on the white line
  while (linefollower_2.readSensors()!=3){
    if(linefollower_2.readSensors()==2){ // left captor out of the white line
     move(3, 30 / 100.0 * 255); // turn right
     _delay(0.125); // turn during 0.1s
     move(3, 0); // stop turning right
    }
    else if(linefollower_2.readSensors()==1){ //right captor out of the white line
     move(4, 30 / 100.0 * 255); // turn left
      _delay(0.125); // turn during 0.1s
     move(4, 0); // stop turning left
    }
  }
}

void move(int direction, int speed) { // used for going forward and neutral steering
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

void _delay(float seconds) { // acts like a timer: the program continues what it's doing for the duration of "seconds". Great for forcing the robot to keep doing a specific action during a certain time
  long endTime = millis() + seconds * 1000;
  while(millis() < endTime) _loop();
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readString();
    data.trim();
    if(data == "move"){
      move(1, 35/100.0 * 255);
      _delay(0.5);
      while(linefollower_2.readSensors()!=0){ //while not both line follower captors are outside of the white line
        align();
        move(1, 45/100.0 * 255);
        _delay(0.1);
      }
      motor_9.run(0);
      motor_10.run(0);
    
    }
    else if(data == "left"){
      move(1, 45/100.0 * 255);
      _delay(0.25);
      while(linefollower_2.readSensors()!=0){
        align();
        motor_9.run(  -1* 22/100.0*255);
        motor_10.run(46/100.0*255);
        _delay(0.1);
      }
      motor_9.run(0);
      motor_10.run(0);
    }
    else if(data == "right"){
      move(1, 45/100.0 * 255);
      _delay(0.25);
      while(linefollower_2.readSensors()!=0){
        align();
        motor_9.run(-1*46/100.0*255);
        motor_10.run(22/100.0*255);
        _delay(0.1);
      }
      motor_9.run(0);
      motor_10.run(0);
    }
    else{
      Serial.println("N"); //in case the command input doesn't exist
      return;
    }
    Serial.println("O"); //ACK
  }
}

void _loop() {
}