#define throttle_pin 8

void setup() {
  // put your setup code here, to run once:
  pinMode(throttle_pin, OUTPUT);
  Serial.begin(115200);

  while(!Serial){
    delay(100);
    }
  Serial.print("Hello!\n");
  analogWrite(throttle_pin, 250);
  Serial.print("Wrote to pin\n");
}

void loop() {
  // put your main code here, to run repeatedly:

}
