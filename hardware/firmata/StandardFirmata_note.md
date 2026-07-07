# Firmata firmware for `vision/facetracking.py`

`vision/facetracking.py` talks to the Arduino through **pyfirmata**, which
requires the **StandardFirmata** firmware to be running on the board. There is
no custom sketch to write for this path — you upload the stock Firmata sketch
that ships with the Arduino IDE.

## Upload steps

1. Open the **Arduino IDE**.
2. Go to **File → Examples → Firmata → StandardFirmata**.
3. Select your board (**Tools → Board → Arduino Uno**) and the correct serial
   port (**Tools → Port**).
4. Click **Upload**.

## Then run the tracker

Set the matching port in [`vision/config.py`](../../vision/config.py):

```python
ARDUINO_PORT = "COM7"     # Windows, or "/dev/ttyUSB0" on Linux/Mac
SERVO_PIN_X  = 9
SERVO_PIN_Y  = 10
```

and run:

```bash
python vision/facetracking.py
```

## Prefer a custom sketch instead?

If you would rather not use Firmata, upload
[`../pan_tilt_servo/pan_tilt_servo.ino`](../pan_tilt_servo/pan_tilt_servo.ino)
and drive it with plain `"<x>,<y>\n"` serial commands. Note that
`facetracking.py` as written uses pyfirmata, so you would swap its board setup
for a `pyserial` connection in that case.
