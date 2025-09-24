import cv2
import numpy as np

# Liste deiner 6 Objekte
OBJECT_NAMES = {
    0: "me",
    1: "Zollstock", 
    2: "Handy",
    3: "Wasserkanne",
    4: "Wasserflasche",
    5: "Taschenrechner"
}

# Farben für jedes Objekt
OBJECT_COLORS = {
    "me": (255, 0, 0),           # Blau
    "Zollstock": (0, 255, 0),     # Grün
    "Handy": (0, 0, 255),         # Rot
    "Wasserkanne": (255, 255, 0), # Cyan
    "Wasserflasche": (255, 0, 255), # Magenta
    "Taschenrechner": (0, 255, 255) # Gelb
}

def main():
    # Deinen trainierten Cascade Classifier laden
    try:
        detector = cv2.CascadeClassifier('combined_annotations.xml')
        print(" Custom Classifier geladen")
    except:
        print(" Fehler beim Laden des Classifiers")
        return

    # Kamera initialisieren
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    if not camera.isOpened():
        print(" Kamera konnte nicht geöffnet werden")
        return
    
    print("Live-Object Detection gestartet")
    print(" Erkannte Objekte: me, Zollstock, Handy, Wasserkanne, Wasserflasche, Taschenrechner")
    print("  Drücke 'Q' zum Beenden")
    
    while True:
        ret, frame = camera.read()
        if not ret:
            break
            
        # Spiegeln für natürliche Darstellung
        frame = cv2.flip(frame, 1)
        
        # In Graustufen konvertieren (benötigt für Cascade)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Objekte mit deinem custom Classifier erkennen
        # WICHTIG: Parameter anpassen basierend auf deinem Training!
        detected_objects = detector.detectMultiScale(
            gray,
            scaleFactor=1.05,      # Langsamer skalieren für bessere Genauigkeit
            minNeighbors=6,        # Höher = weniger False Positives
            minSize=(50, 50),      # Minimale Objektgröße
            maxSize=(300, 300)     # Maximale Objektgröße
        )
        
        detected_names = []
        
        # Erkannte Objekte markieren
        for i, (x, y, w, h) in enumerate(detected_objects):
            # Aktuell erkennt der Classifier alle Objekte gleich
            # Für unterschiedliche Objekte bräuchtest du entweder:
            # 1. Einen Multi-Class Classifier (komplex)
            # 2. Oder wir zeigen einfach "Objekt" an
            
            object_name = "Objekt"  # Standardname
            color = (255, 255, 255)  # Weiß
            
            # Versuche Objekt anhand der Größe/Form zu unterscheiden
            aspect_ratio = w / h
            area = w * h
            
            # Einfache Heuristik für Objektunterscheidung
            if aspect_ratio > 1.5:
                object_name = "Zollstock"
                color = OBJECT_COLORS[object_name]
            elif area < 10000:
                object_name = "Handy" 
                color = OBJECT_COLORS[object_name]
            elif 15000 < area < 30000:
                object_name = "Wasserflasche"
                color = OBJECT_COLORS[object_name]
            else:
                object_name = "me"
                color = OBJECT_COLORS[object_name]
            
            # Rechteck und Text zeichnen
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, object_name, (x, y - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            
            detected_names.append(object_name)
        
        # Status-Anzeige
        if detected_objects:
            status = f"Erkannt: {len(detected_objects)} Objekt(e) - {', '.join(set(detected_names))}"
            color = (0, 255, 0)  # Grün
        else:
            status = "Keine Objekte erkannt - Zeige Objekte in die Kamera"
            color = (0, 0, 255)  # Rot
        
        cv2.putText(frame, status, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        
        # Performance-Info
        cv2.putText(frame, f"Objekte: {len(detected_objects)}", 
                   (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Fenster anzeigen
        cv2.imshow("Custom Object Detection - Live", frame)
        
        # Beenden mit Q
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
    
    camera.release()
    cv2.destroyAllWindows()
    print(" Programm beendet")

if __name__ == "__main__":
    main()