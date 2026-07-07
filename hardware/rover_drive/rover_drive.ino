/*
 * rover_drive.ino
 * -------------------------------------------------------------------------
 * Locomotion firmware for the rocker-bogie rover chassis.
 *
 * The six drive wheels are ganged into two banks (left / right) and driven
 * differentially through a dual H-bridge (L298N). Each L298N channel drives
 * one bank; wire the three motors of a bank in parallel to that channel
 * (or use one L298N per bank and mirror the pin pairs).
 *
 * Serial protocol (one command per line, terminated by '\n'):
 *     F   forward          B   backward
 *     L   pivot left       R   pivot right
 *     S   stop
 *     V<0-255>   set drive speed, e.g. "V180"
 *
 * Wiring (L298N):
 *   ENA -> D5  (PWM, left bank speed)     IN1 -> D7   IN2 -> D8   (left dir)
 *   ENB -> D6  (PWM, right bank speed)    IN3 -> D9   IN4 -> D10  (right dir)
 *   12V -> battery +   GND -> common ground (battery + Arduino)
 * -------------------------------------------------------------------------
 */

// Left bank
const uint8_t ENA = 5;   // PWM
const uint8_t IN1 = 7;
const uint8_t IN2 = 8;

// Right bank
const uint8_t ENB = 6;   // PWM
const uint8_t IN3 = 9;
const uint8_t IN4 = 10;

const long BAUD_RATE = 9600;

uint8_t driveSpeed = 200;   // 0-255
String  rxBuffer   = "";

void setLeft(int dir) {    // dir: +1 fwd, -1 rev, 0 stop
  digitalWrite(IN1, dir > 0);
  digitalWrite(IN2, dir < 0);
  analogWrite(ENA, dir == 0 ? 0 : driveSpeed);
}

void setRight(int dir) {
  digitalWrite(IN3, dir > 0);
  digitalWrite(IN4, dir < 0);
  analogWrite(ENB, dir == 0 ? 0 : driveSpeed);
}

void forward()  { setLeft(+1); setRight(+1); }
void backward() { setLeft(-1); setRight(-1); }
void pivotLeft(){ setLeft(-1); setRight(+1); }
void pivotRight(){ setLeft(+1); setRight(-1); }
void stopAll()  { setLeft(0);  setRight(0);  }

void applyCommand(const String &line) {
  if (line.length() == 0) return;
  char cmd = line.charAt(0);
  switch (cmd) {
    case 'F': forward();    break;
    case 'B': backward();   break;
    case 'L': pivotLeft();  break;
    case 'R': pivotRight(); break;
    case 'S': stopAll();    break;
    case 'V': {
      int v = line.substring(1).toInt();
      driveSpeed = (uint8_t)constrain(v, 0, 255);
      break;
    }
    default: break;   // unknown command, ignore
  }
}

void setup() {
  Serial.begin(BAUD_RATE);
  pinMode(ENA, OUTPUT); pinMode(IN1, OUTPUT); pinMode(IN2, OUTPUT);
  pinMode(ENB, OUTPUT); pinMode(IN3, OUTPUT); pinMode(IN4, OUTPUT);
  stopAll();
  rxBuffer.reserve(8);
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
