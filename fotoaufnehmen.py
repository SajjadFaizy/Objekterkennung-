import cv2
import keyboard
import os
from datetime import datetime

# Ordner, in dem die Bilder gespeichert werden sollen
output_folder = r"C:\uni\python\Foto"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Webcam öffnen
cap = cv2.VideoCapture(0)

# Überprüfen, ob die Kamera geöffnet werden konnte
if not cap.isOpened():
    print("Fehler: Kamera konnte nicht geöffnet werden!")
    exit()

# Kameraeinstellungen (optional)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # Breite
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # Höhe
cap.set(cv2.CAP_PROP_FPS, 30)  # Bildrate

# Zähler für die Bildnummer
image_counter = 0

print("Webcam wird geöffnet...")
print("Drücke 'P', um ein Foto aufzunehmen.")
print("Drücke 'Q', um das Programm zu beenden.")

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Fehler: Frame konnte nicht gelesen werden!")
            break

        # Bild anzeigen
        cv2.imshow('Webcam - Drücke P für Foto, Q zum Beenden', frame)

        # Tastatureingaben überprüfen
        key = cv2.waitKey(1) & 0xFF
        
        # Wenn 'P' gedrückt wird, Foto aufnehmen
        if keyboard.is_pressed('p') or key == ord('p'):
            # Zeitstempel für eindeutigen Dateinamen
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            image_path = os.path.join(output_folder, f"foto_{timestamp}_{image_counter:04d}.jpg")
            
            # Bild speichern (JPEG mit hoher Qualität)
            cv2.imwrite(image_path, frame, [cv2.IMWRITE_JPEG_QUALITY, 95])
            print(f"✅ Bild gespeichert: {image_path}")
            image_counter += 1
            
            # Visuelles Feedback - Rahmen kurz grün anzeigen
            cv2.rectangle(frame, (10, 10), (frame.shape[1]-10, frame.shape[0]-10), (0, 255, 0), 3)
            cv2.imshow('Webcam - Drücke P für Foto, Q zum Beenden', frame)
            cv2.waitKey(300)  # Kurze Verzögerung für Feedback

        # Wenn 'Q' gedrückt wird, das Programm beenden
        if keyboard.is_pressed('q') or key == ord('q'):
            print("Programm wird beendet...")
            break

except KeyboardInterrupt:
    print("\nProgramm durch Benutzer beendet.")

finally:
    # Ressourcen freigeben
    cap.release()
    cv2.destroyAllWindows()
    print("Kamera freigegeben. Programm beendet.")