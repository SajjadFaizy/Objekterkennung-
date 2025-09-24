import cv2
import os
import glob

def resize_to_32x32(input_path, output_folder):
    """
    Skaliert Bilder auf exakt 32x32 Pixel
    """
    # Unterstützte Dateiformate
    extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff']
    
    # Prüfen ob Eingabe ein Ordner oder Datei ist
    if os.path.isdir(input_path):
        image_files = []
        for ext in extensions:
            image_files.extend(glob.glob(os.path.join(input_path, ext)))
    else:
        image_files = [input_path]
    
    # Ausgabeordner erstellen
    os.makedirs(output_folder, exist_ok=True)
    
    for image_file in image_files:
        try:
            # Bild laden
            img = cv2.imread(image_file)
            if img is None:
                continue
            
            # Auf exakt 32x32 skalieren
            resized = cv2.resize(img, (32, 32), interpolation=cv2.INTER_AREA)
            
            # Dateinamen vorbereiten
            filename = os.path.basename(image_file)
            output_path = os.path.join(output_folder, filename)
            
            # Speichern
            cv2.imwrite(output_path, resized)
            print(f"Skaliert: {filename} -> 32x32")
            
        except Exception as e:
            print(f"Fehler bei {image_file}: {e}")

# HIER GEBEN SIE DIE PFADE EIN: ################################

# Beispiel 1: Wenn Ihre Bilder hier liegen:
# C:\universität\python\p
input_pfad = r"C:\universität\python\p"

# Beispiel 2: Oder wenn Sie einen anderen Ordner haben:
# input_pfad = r"C:\Users\IhrName\Bilder\waffen_bilder"

# WO DIE BILDER GESPEICHERT WERDEN SOLLEN:
output_pfad = r"C:\universität\python\n\resized_images"

# Funktion aufrufen
resize_to_32x32(input_pfad, output_pfad)

print("Fertig! Alle Bilder wurden skaliert.")