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

  Firebase.getInt(firebaseData,"/EMGdata/Measure_patients");
  int patients = firebaseData.intData();
  patients++;
  Firebase.setInt(firebaseData,"/EMGdata/Measure_patients",patients);

  int j=1;
  int i=0;
  while (j<6){
    if (j==1){
      Serial.println("Hello! We are starting the test soon.");
      delay(2000);
      Serial.println("Prepare the first gesture, please.");
      delay(2000);
      Serial.println("We are starting...");
      delay(2000);
    }
    else{
      Serial.println("Measuring time is over.");
      delay(2000);
      Serial.println("Prepare the following gesture, please.");
      delay(2000);
      Serial.println("It's staring...");
      delay(2000); 
    }
      while (i<100){
        float sensorValue = analogRead(sensorPin);
        delay(30);
        float voltage = ((((sensorValue/4095)-0.5)*3.3)/1009)*1000;
        Serial.println(voltage);
    
        if (Firebase.pushFloat(firebaseData, "/EMGdata/Gesture"+String(j), voltage)){
        }
        else{
          Serial.println("Failed");
          Serial.println("REASON: " + firebaseData.errorReason());
        }      
        i++;
      } 
   i=0;
   j++;
   }

   Serial.println("Thank you very much for your help!");
   delay(2000);
   Serial.println("Bye-Bye!");
   delay(2000);
 }

 
void loop(){}
