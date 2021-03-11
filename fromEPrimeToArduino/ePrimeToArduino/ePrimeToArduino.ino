//const int analogInput = 0;
const int outputPINBNC = 13;
const int outputPINLPT1 = 8;
const int timeToDelay = 6; //to correspond to e-prime code
//int valueRead = 0;
//unsigned long timeArduino;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200); //to match e-prime
  pinMode(LED_BUILTIN, OUTPUT); // initialize digital pin LED_BUILTIN as an output.
  pinMode(outputPINBNC, OUTPUT);
  pinMode(outputPINLPT1, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  char receiving;
  if(Serial.available() > 0) {
    // Read from E-prime
    receiving = Serial.read();
//    timeArduino = micros();
    if (receiving == '1'){
      digitalWrite(LED_BUILTIN, HIGH); // turn the LED on (HIGH is the voltage level)
      digitalWrite(outputPINBNC, HIGH); // send to PIN 13 which is connected to Phantom camera
      digitalWrite(outputPINLPT1, HIGH); // send to PIN 8 which is connected to Neuroscan
      delayMicroseconds((timeToDelay*1000)/2); // half of the time we want to send HIGH and the other half send LOW
//      Serial.write(timeArduino);
    } else {
      digitalWrite(LED_BUILTIN, LOW); // turn the LED off by making the voltage LOW
      digitalWrite(outputPINBNC, LOW); // send to PIN 13 which is connected to Phantom camera
      digitalWrite(outputPINLPT1, LOW); // send to PIN 8 which is connected to Neuroscan
//      Serial.write(timeArduino);
    }
  }
} 
