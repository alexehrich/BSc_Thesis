int sensorPin = 34;

void setup() {
  Serial.begin(115200);
}

void loop(){
  float sensorValue = analogRead(sensorPin);
  delay(50);
  float voltage = ((((sensorValue/4095)-0.5)*3.3)/1009)*1000;
  Serial.println(voltage);
  }



  
