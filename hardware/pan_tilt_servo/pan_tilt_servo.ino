/*
 * pan_tilt_servo.ino
 * -------------------------------------------------------------------------
 * Native serial sketch for the CV-on-Rover face-tracking pan/tilt turret.
 *
 * This is an ALTERNATIVE to the pyfirmata path used by vision/facetracking.py.
 * Use this sketch if you prefer to drive the servos with a small custom
 * firmware instead of uploading StandardFirmata.
 *
 * Protocol (one command per line, terminated by '\n'):
 *     "<x>,<y>\n"     e.g.  "112,98\n"
 *   where <x> and <y> are integer servo angles in the range [0, 180].
 *
 * Wiring:
 *   Servo X (pan)  signal -> D9
 *   Servo Y (tilt) signal -> D10
 *   Servos VCC -> external 5V (NOT the Arduino 5V pin for two servos)
 *   Common GND between Arduino, servo supply and servos.
 * -------------------------------------------------------------------------
 */

#include <Servo.h>

const uint8_t SERVO_X_PIN = 9;
const uint8_t SERVO_Y_PIN = 10;
const long    BAUD_RATE   = 9600;

Servo servoX;
Servo servoY;

String rxBuffer = "";

int clampAngle(int a) {
  if (a < 0)   return 0;
  if (a > 180) return 180;
  return a;
}

void applyCommand(const String &line) {
  int comma = line.indexOf(',');
  if (comma < 0) return;                       // malformed, ignore

  int x = clampAngle(line.substring(0, comma).toInt());
  int y = clampAngle(line.substring(comma + 1).toInt());

  servoX.write(x);
  servoY.write(y);
}

void setup() {
  Serial.begin(BAUD_RATE);
  servoX.attach(SERVO_X_PIN);
  servoY.attach(SERVO_Y_PIN);

  // Center the turret on boot.
  servoX.write(90);
  servoY.write(90);
  rxBuffer.reserve(16);
}

void loop() {
  while (Serial.available() > 0) {
    char c = (char)Serial.read();
    if (c == '\n') {
      applyCommand(rxBuffer);
      rxBuffer = "";
    } else if (c != '\r') {
      rxBuffer += c;
    }
  }
}
