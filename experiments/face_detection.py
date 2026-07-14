import sys
import time
from pathlib import Path

import cv2
import numpy as np

# Make the shared config importable regardless of the current working directory
sys.path.append(str(Path(__file__).resolve().parent))
import config

pengklasifikasiWajah  = cv2.CascadeClassifier(config.HAAR_CASCADE)

videoCam = cv2.VideoCapture(config.CAMERA_INDEX)

if not videoCam.isOpened():
    print("Kamera tidak dapat diakses")
    exit()

tombolQditekan = False
while (tombolQditekan == False):
    ret, kerangka = videoCam.read()

    if ret == True:
        abuAbu = cv2.cvtColor(kerangka, cv2.COLOR_BGR2GRAY)
        dafWajah = pengklasifikasiWajah.detectMultiScale(abuAbu, scaleFactor = 1.3, minNeighbors = 2)

        for (x, y, w, h) in dafWajah:
            cv2.rectangle(kerangka, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        #print("Jumlah Wajah terdeksi: ", len(dafWajah))
        teks = "Jumlah Wajah Terdeteksi = " + str(len(dafWajah))

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(kerangka, teks, (0, 30), font, 1, (255, 0, 0), 1)

        cv2.imshow("Hasil", kerangka)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            tombolQditekan = True
            break


videoCam.release()
cv2.destroyAllWindows()