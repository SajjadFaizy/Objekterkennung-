import xml.etree.ElementTree as ET
import os
import glob

def combine_annotation_xml_files(input_folder, output_file):
    """
    Kombiniert alle XML-Annotationsdateien zu einer großen Datei
    """
    # Alle XML-Dateien finden
    xml_files = glob.glob(os.path.join(input_folder, "*.xml"))
    
    if not xml_files:
        print(" Keine XML-Dateien gefunden!")
        return
    
    print(f" Gefunden: {len(xml_files)} XML-Dateien")
    
    # Neues Root-Element für kombinierte Daten
    combined_root = ET.Element("annotations")
    
    # Metadaten hinzufügen
    metadata = ET.SubElement(combined_root, "metadata")
    ET.SubElement(metadata, "total_files").text = str(len(xml_files))
    ET.SubElement(metadata, "combined_date").text = "2025-01-23"
    
    # Jede XML-Datei verarbeiten
    for i, xml_file in enumerate(xml_files, 1):
        try:
            filename = os.path.basename(xml_file)
            print(f" Verarbeite ({i}/{len(xml_files)}): {filename}")
            
            # XML parsen
            tree = ET.parse(xml_file)
            original_root = tree.getroot()
            
            # Container für diese Annotation erstellen
            annotation_elem = ET.SubElement(combined_root, "annotation_entry")
            annotation_elem.set("source_file", filename)
            annotation_elem.set("entry_id", str(i))
            
            # Wichtige Daten aus der Original-XML kopieren
            # filename und path anpassen, da sie sich auf einzelne Dateien beziehen
            for child in original_root:
                if child.tag not in ['filename', 'path']:
                    # Element tief kopieren
                    annotation_elem.append(deep_copy_element(child))
                else:
                    # filename und path anpassen mit Quelle-Hinweis
                    adjusted_elem = ET.SubElement(annotation_elem, child.tag)
                    adjusted_elem.text = f"{child.text} [from: {filename}]"
            
            print(f"    Enthält: {len(original_root.findall('object'))} Objekte")
            
        except Exception as e:
            print(f" Fehler bei {filename}: {e}")
    
    # Kombinierte Datei speichern
    tree = ET.ElementTree(combined_root)
    tree.write(output_file, encoding='utf-8', xml_declaration=True)
    
    print("\n" + "="*50)
    print(f" ERFOLG! {len(xml_files)} Dateien kombiniert")
    print(f" Ausgabedatei: {output_file}")
    print(f" Gesamt-Objekte: {len(combined_root.findall('.//object'))}")

def deep_copy_element(element):
    """Erstellt eine tiefe Kopie eines XML-Elements"""
    new_element = ET.Element(element.tag)
    new_element.text = element.text
    new_element.tail = element.tail
    new_element.attrib = element.attrib.copy()
    
    for child in element:
        new_element.append(deep_copy_element(child))
    
    return new_element

# Hauptprogramm
if __name__ == "__main__":
    # PFAD ANPASSEN: Hier den Ordner mit deinen XML-Dateien eingeben
    input_folder = r"C:\uni\python\1"  # Ordner wo deine XMLs liegen
    output_file = "combined_annotations.xml"
    
    combine_annotation_xml_files(input_folder, output_file)