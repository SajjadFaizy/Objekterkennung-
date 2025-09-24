import numpy as np
import cv2
import imutils

# Klassifikator laden
gun_cascade = cv2.CascadeClassifier('combined_annotations.xml')
camera = cv2.VideoCapture(0)

while True:
    ret, frame = camera.read()
    if not ret:
        break
        
    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detektor mit optimierten Parametern
    gun = gun_cascade.detectMultiScale(
        gray, 
        scaleFactor=1.1,
        minNeighbors=10,
        minSize=(120, 120),
        maxSize=(400, 400)
    )
    
    gun_detected = False
    
    for (x, y, w, h) in gun:
        # Zusätzliche Filter zur Vermeidung von Falscherkennungen
        aspect_ratio = w / float(h)
        area = w * h
        
        # Nur Objekte mit waffenähnlichen Proportionen berücksichtigen
        if 0.8 < aspect_ratio < 2.2 and 5000 < area < 30000:
            frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.putText(frame, "Weapon", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            gun_detected = True
    
    # Statusanzeige
    status = "Weapon detected!" if gun_detected else "Monitoring..."
    cv2.putText(frame, status, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    
    cv2.imshow("Security Feed", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()