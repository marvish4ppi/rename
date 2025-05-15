import os
import random
from pathlib import Path

def generate_test_files(output_dir: str, total_files: int = 300):
    os.makedirs(output_dir, exist_ok=True)

    # Mögliche Dateiendungen für den Test
    extensions = [".pdf", ".xlsx", ".jpg", ".docx"]
    
    for _ in range(total_files):
        rand_number = random.randint(100000, 999999)
        extension = random.choice(extensions)
        filename = f"{rand_number}{extension}"
        file_path = Path(output_dir) / filename

        # Dummy-Datei mit etwas Inhalt anlegen
        with open(file_path, "w") as f:
            f.write("Dies ist eine Dummy-Datei für Testzwecke.\n")

    print(f"{total_files} Testdateien wurden erstellt in: {output_dir}")

if __name__ == "__main__":
    generate_test_files("test_dokumente")