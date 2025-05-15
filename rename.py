import os
import pandas as pd
from pathlib import Path
from datetime import datetime
import logging

def setup_logging(log_file="rename_log.txt"):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")

    # File-Handler
    file_handler = logging.FileHandler(log_file, mode='a')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Stream-Handler (für Konsole)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    logging.info("🟢 Logging gestartet (Datei + Konsole).")

def load_renaming_map(csv_path: str) -> dict:
    if csv_path.endswith(".csv"):
        df = pd.read_csv(csv_path)
    else:
        df = pd.read_excel(csv_path)

    if df.shape[1] < 2:
        raise ValueError("Die Datei muss mindestens zwei Spalten enthalten (alt, neu).")

    return dict(zip(df.iloc[:, 0], df.iloc[:, 1]))

def rename_files(base_dir: str, renaming_map: dict, dry_run: bool = False):
    renamed_count = 0
    not_found = []

    logging.info("🔍 Starte Durchlauf durch: %s", base_dir)

    for root, _, files in os.walk(base_dir):
        for filename in files:
            if filename in renaming_map:
                old_path = Path(root) / filename
                new_filename = renaming_map[filename]
                new_path = Path(root) / new_filename

                if dry_run:
                    logging.info("[DRY RUN] Datei gefunden: %s → Umbenennen zu: %s", old_path, new_path)
                else:
                    try:
                        os.rename(old_path, new_path)
                        logging.info("✔️ Umbenannt: %s → %s", old_path, new_path)
                        renamed_count += 1
                    except Exception as e:
                        logging.error("❌ Fehler bei Umbenennung %s: %s", old_path, str(e))
            else:
                not_found.append(filename)
                logging.warning("⚠️ Nicht in Mapping gefunden: %s", filename)

    logging.info("✅ Vorgang abgeschlossen. %d Datei(en) erfolgreich umbenannt.", renamed_count)
    if not_found:
        logging.info("%d Datei(en) nicht umbenannt, da nicht in Mapping enthalten.", len(not_found))

def main():
    # Konfiguration
    csv_path = "rename.csv"
    base_directory = "/home/marvin/dev/rename/test_dokumente"
    dry_run = False

    setup_logging()

    try:
        renaming_map = load_renaming_map(csv_path)
        rename_files(base_directory, renaming_map, dry_run=dry_run)
    except Exception as e:
        logging.critical("❗ Kritischer Fehler: %s", str(e))
        print(f"Fehler: {e}")

if __name__ == "__main__":
    main()
