#include <Servo.h>
#include <Wire.h>
#include <Adafruit_SSD1306.h> // Used for OLED Display

// OLED Display Variables
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1

Servo myServo;
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

bool objectDetected = false;
unsigned long lastDetection = 0;

// Set up both servo and Display
void setup() {
  Serial.begin(9600);
  myServo.attach(9);

  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  display.clearDisplay();
  display.setTextColor(WHITE);
  display.setTextSize(1);
}

void loop() {
  if (Serial.available()) {
    String data = Serial.readStringUntil('\n');

    // Date being received by Arduino
    if (data.startsWith("X")) {
      int angle = data.substring(1).toInt();
      angle = constrain(angle, 0, 180);
      myServo.write(angle);
      objectDetected = true;
      lastDetection = millis();

      // Update OLED
      display.clearDisplay();
      display.setCursor(0, 0);
      display.print("Red Object Tracked");
      display.setCursor(0, 20);
      display.print("Servo Angle: ");
      display.print(angle);
      display.display();
    }
  }

  // Clear display after no detection for 2s
  if (objectDetected && (millis() - lastDetection > 2000)) {
    objectDetected = false;
    display.clearDisplay();
    display.setCursor(0, 0);
    display.print("No object found");     // Display no object detected
    display.display();
  }
}