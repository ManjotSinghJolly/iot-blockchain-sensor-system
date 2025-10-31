#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>

/****************************************************
  IoT + Blockchain Sensor Client
  Hardware: ESP32 + DHT22
  Purpose: Send temperature & humidity to Flask backend

  NOTE:
  Replace WiFi SSID, Password, and server URL 
  before flashing to ESP32.
****************************************************/

// Wi-Fi credentials
const char* ssid = "YOUR_WIFI_SSID"
const char* password = "YOUR_WIFI_PASSWORD"

// DHT sensor setup
DHT dht(26, DHT22);

// HTTP Endpoint
const char* serverURL = "http://YOUR_SERVER_IP:5000/api/sensor";
// Example: "http://192.168.1.53:5000/api/sensor"

void setup() {
  Serial.begin(115200);
  delay(1000);

  // Initializing the DHT sensor
  dht.begin();
  Serial.println("DHT22 sensor initialized...");

  // Connect to Wi-Fi
  Serial.print("Connecting to WiFi...");
  WiFi.begin(ssid, password);

  int retryCount = 0;
  while(WiFi.status() != WL_CONNECTED && retryCount < 30) {
    delay(500);
    Serial.print(".");
    retryCount++;
  }

  if(WiFi.status() == WL_CONNECTED) {
    Serial.println("\n WiFi connected!");
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\n WiFi connection failed!");
  }
  delay(2000);

}

void loop() {
  float temp = dht.readTemperature();
  float humidity = dht.readHumidity();

  if (isnan(temp) || isnan(humidity)) {
    Serial.println("Failed to read from DHT22 sensor!");
    delay(2000);
    return;
  }

  // Printing readings to the Serial Monitor
  Serial.print("Temp: ");
  Serial.print(temp);
  Serial.print(" °C | Humidity: ");
  Serial.print(humidity);
  Serial.println(" %");

  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverURL);
    http.addHeader("Content-Type", "application/json");

    String payload = "{\"temperature\": " + String(temp, 2) + 
                    ", \"humidity\": " + String(humidity, 2) + "}";

    Serial.println("Sending payload: " + payload);
    int httpResponseCode = http.POST(payload);

    Serial.print("Server Response: ");
    Serial.println(httpResponseCode);
    http.end();
  } else {
    Serial.println("WiFi not connected!");
  }


  delay(5000);


}
