#define BUZZER 11
#define TONE A0
#define DELAY A3

int sensorPotVal = 0;
int outPotVal = 0;

int sensorDelayVal = 0;
int outDelayVal = 0;

void setup() {
  // put your setup code here, to run once:
  pinMode(BUZZER, OUTPUT);
  pinMode(TONE, INPUT);
  pinMode(DELAY, INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  
  sensorPotVal = analogRead(TONE);
  outPotVal = map(sensorPotVal, 0, 1023, 1, 1023);

  sensorDelayVal = analogRead(DELAY);
  outDelayVal = map(sensorDelayVal, 0, 1023, 0, 255);  

  //analogWrite(BUZZER, sensorDelayVal);

  //tone(BUZZER, outPotVal-0.5f);
  //delay(outDelayVal);

  //analogWrite(BUZZER, outPotVal);
  tone(BUZZER, outPotVal);
  //delay(outDelayVal);
  
  //tone(BUZZER, outPotVal+0.5f);
  //delay(outDelayVal);
  //analogWrite(BUZZER, outVal);
}
