#include <Servo.h>

int LED = 13;
String data;



Servo myservo;  // create servo object to control a servo

void setup()
{
  myservo.attach(9);
  Serial.begin(921600);
  //pinMode(LED,OUTPUT);
  //digitalWrite(LED,LOW);
}

void loop()
{
  while(Serial.available())
  {
    data = Serial.readString();
    myservo.write(data.toInt());
  }
  

//  if(data == '1')
//  {
//    //digitalWrite(LED,HIGH);
//    myservo.write(50);          // tell servo to go to position in variable 'pos'
//    delay(15); 
//    Serial.println("LED turned on");
//  }
//
//  else if(data == '0')
//  {
//    myservo.write(100);          // tell servo to go to position in variable 'pos'
//    delay(15); 
//    Serial.println("LED turned off");
//  }
}

