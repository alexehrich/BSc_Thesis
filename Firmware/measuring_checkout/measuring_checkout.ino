#include <WiFi.h>
#include <FirebaseESP32.h>
#include "Secret_keys.h"

int sensorPin = 34;
const char* ssid = WIFI_SSID;
const char* password = WIFI_PASSWORD;
const char* host = FIREBASE_HOST;
const char* auth = FIREBASE_AUTH;

FirebaseData firebaseData;

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
  Firebase.setInt(firebaseData,"/EMGdata/Checkout","Okey");

  int i=0;
  while (i<150){
    float sensorValue = analogRead(sensorPin);
    delay(30);
    float voltage = ((((sensorValue/4095)-0.5)*3.3)/1009)*1000;
    Serial.println(voltage);
    i++;
  }
}


void loop() {}
