import requests
import os
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed


SRC_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(SRC_DIR, os.pardir))
HTML_DIR = os.path.join(PROJECT_ROOT, "data", "data_html")
os.makedirs(HTML_DIR, exist_ok=True)


def download_html(fiche_url, index):
    try:
        response = requests.get(fiche_url, timeout=10)
        if response.status_code == 200:
            filepath = os.path.join(HTML_DIR, f"{str(index)}.html")
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(response.text)
            print(f"[OK] {filepath}")
        else:
            print(f"[ERREUR] {index}: Status {response.status_code} -> {fiche_url}")
    except Exception as e:
        print(f"[EXCEPTION] {index}: {e}")


def main():
    chemin_json = os.path.join(PROJECT_ROOT,"data","fr-esr-cartographie_formations_parcoursup.json")
    df = pd.read_json(chemin_json)


    formations = [(idx, row) for idx, row in df.iterrows() if  20000< idx <= 21000 and isinstance(row.get("fiche"), str)]

    print(f"{len(formations)} fiches à traiter")

    with ThreadPoolExecutor(max_workers=7) as executor:
        futures = [ executor.submit(download_html, row["fiche"], idx) for idx, row in formations]

        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print("[ERREUR THREAD] :", e)




if __name__ == "__main__":
    main()
