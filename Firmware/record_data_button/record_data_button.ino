#include <WiFi.h>
#include <FirebaseESP32.h>
#include "Secret_keys.h"

int sensorPin = 34;
int cont = 1;
int interruption = 0;
int GPIOPin = 26;
unsigned long Time = millis();

const char* ssid = WIFI_SSID;
const char* password = WIFI_PASSWORD;
const char* host = FIREBASE_HOST;
const char* auth = FIREBASE_AUTH;

//Firebase Data Object
FirebaseData firebaseData;

void IRAM_ATTR isr() {
    interruption=1;
    detachInterrupt(GPIOPin);
}

void setup() {
  Serial.begin(115200);
  Serial.println();

  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED){
    Serial.print(".");
    delay(300);
  }
  
  Serial.println("WiFi succesfully connected!");
  
  Firebase.begin(host, auth);
  Firebase.reconnectWiFi(true);

  attachInterrupt(digitalPinToInterrupt(GPIOPin), isr, RISING);
}

void send_data(int cont){
  int i = 0;
  int users = 0;
  while (i<100){
    float sensorValue = analogRead(sensorPin);
    delay(100);
    float voltage = ((((sensorValue/4095)-0.5)*3.3)/1009)*1000;
    Serial.println(voltage);
    Firebase.setInt(firebaseData, "/EMGdata/Gesture" + String(cont) + "/init_val",0);
    Firebase.pushInt(firebaseData, "/EMGdata/Gesture" + String(cont), voltage);
    Firebase.pushInt(firebaseData, "/EMGdata/Gesture" + String(cont), Time);    //Prints time
    i += 1;
    }
  users = Firebase.get(firebaseData, "/EMGdata/MeasuredUsers");
  users += 1;
  Firebase.set(firebaseData, "EMGdata/MeasuredUsers", users);
  interruption = 0;
  }
  
void loop(){
  if (cont == 7){
    cont = 1;
    }
  if (interruption == 1) {
    send_data(cont);
    cont++;
    }
    }
