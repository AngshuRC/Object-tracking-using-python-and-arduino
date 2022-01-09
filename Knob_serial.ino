
#include <Servo.h>

Servo myservo;  // create servo object to control a servo


String val;    
int pos;
void setup() {
  myservo.attach(9); 
  Serial.begin(9600);
}

void loop() {
  if(Serial.available()){            
  val = Serial.readString();  // Read String from Serial    
  pos=val.toInt();           // Converting Serial to Integer
  pos=map(pos,0,500,180,0);  // maping value from 0 - 500 to 180 - 0
  myservo.write(pos);        // finally writing the pulse to the servo          
  }
}
