import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import csv
import time
import shutil

GECKO_PATH= "geckodriver.exe"
FIREFOX_BINARY = "Mozilla Firefox\\firefox.exe"
options = Options()
options.binary_location = FIREFOX_BINARY
options.headless = True
service = Service(GECKO_PATH)
driver = webdriver.Firefox(service=service, options=options)

url = "https://tomato.gg/tank-stats"
driver.get(url)
try:
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody tr"))
    )
except Exception as e:
    print("Erreur de chargement :", e)
    driver.quit()
    exit()

time.sleep(1)

#data acquisition
# 1. Cliquer sur "Show 50"
dropdown = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Show 50')]"))
)
dropdown.click()
time.sleep(5)

# 2. Fermer la pub si elle existe
try:
    popup_buttons = driver.find_elements(By.TAG_NAME, "button")
    for btn in popup_buttons:
        html = btn.get_attribute("innerHTML")
        if "svg" in html or "path" in html:
            location = btn.location
            size = btn.size
            x, y = location['x'], location['y']
            w, h = size['width'], size['height']

            # Ajusté pour détecter celui en bas à droite
            if x > 1000 and y > 1500 and w < 100 and h <= 100:
                try:
                    driver.execute_script("arguments[0].click();", btn)
                    print("✅ Popup détectée et fermée")
                    time.sleep(1)
                    break
                except Exception as e:
                    print(f"❌ Erreur au clic sur popup : {e}")
                    continue
    else:
        print("❕ Aucun bouton de fermeture détecté")
except Exception as e:
    print("❌ Exception inattendue durant la détection de popup :", e)


# 2. Simuler navigation clavier : descendre dans la liste jusqu'à "Show 500"
# En général : 3 flèches ↓ (Show 100 → Show 250 → Show 500)
actions = ActionChains(driver)
actions.send_keys(Keys.ARROW_DOWN).pause(0.3)
actions.send_keys(Keys.ARROW_DOWN).pause(0.3)
actions.send_keys(Keys.ARROW_DOWN).pause(0.3)
actions.send_keys(Keys.ENTER).perform()

print("✅ 'Show 500' sélectionné via clavier")
time.sleep(2)

# 4. Scraper les 2 pages
parsed_data = []

for page_num in range(1, 3):
    print(f"📄 Scraping page {page_num}")
    time.sleep(2)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    rows = soup.select("table tbody tr")

    for row in rows:
        cols = [td for td in row.find_all('td') if not td.has_attr('colspan')]
        try:
            nation = cols[0].find('img')['alt'] if cols[0].find('img') else cols[0].text.strip()
            tank_type = cols[1].find('img')['alt'] if cols[1].find('img') else cols[1].text.strip()
            tier = cols[2].text.strip()
            name = cols[3].text.strip()
            dpm = cols[5].text.strip()
            dmg = cols[6].text.strip()
            reload_time = cols[7].text.strip()
            pen = cols[8].text.strip()
            velo = cols[9].text.strip()
            acc = cols[10].text.strip()
            aim = cols[11].text.strip()
            dispersion = cols[12].text.strip()
            dep_elev = cols[13].text.strip()
            speed = cols[14].text.strip()
            traverse = cols[15].text.strip()
            power = cols[16].text.strip()
            pw = cols[17].text.strip()
            weight = cols[18].text.strip()
            health = cols[19].text.strip()
            vr = cols[20].text.strip()
        except Exception as e:
            print("⚠️ Ligne ignorée :", e)
            continue

        parsed_data.append([nation, tank_type, tier, name,
            dpm, dmg, reload_time, pen,
            velo, acc, aim, dispersion,
            dep_elev, speed, traverse,
            power, pw, weight, health, vr])

    try:
        next_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "(//button[contains(@class, 'rt-reset rt-BaseButton rt-r-size-2 rt-variant-ghost rt-IconButton')])[3]")))
        # Attendre que le contenu change après le clic
        try:
            first_tank_before = soup.select_one("table tbody tr td:nth-of-type(4)").text.strip()
        except:
            first_tank_before = None
        driver.execute_script("arguments[0].click();", next_button)
        print("➡️ Clic sur page suivante")
        WebDriverWait(driver, 10).until(
            lambda d: d.find_element(By.CSS_SELECTOR, "table tbody tr td:nth-of-type(4)").text.strip() != first_tank_before
        )
        print("✅ Contenu de page mis à jour")
        driver.execute_script("arguments[0].click();", next_button)
        print("➡️ Passage à la page suivante")
    except:
        print("⚠️ Aucun bouton 'page suivante' cliquable — probablement fin de pagination.")

# Écrire dans un fichier CSV
os.makedirs("results/raw", exist_ok=True)
os.makedirs("results/clean", exist_ok=True)
with open("results/raw/wot_tank_stats.csv", "w", newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["Nation", "Type", "Tier", "Name",
    "DPM", "Dmg", "Reload", "Pen",
    "Velo", "Acc", "Aim", "Dispersion",
    "Dep/Elev", "Speed", "Traverse",
    "Power", "P/W", "Weight", "Health", "VR"])
    writer.writerows(parsed_data)

print(f"{len(parsed_data)} first parse saved into wot_tank_stats.csv ✅")

#data cleaning
df = pd.read_csv("results\\raw\\wot_tank_stats.csv")
df["Reload"] = df["Reload"].str.replace("s", "", regex=False).astype(float)
df["Aim"] = df["Aim"].str.replace("s", "", regex=False).astype(float)
df[["DispStatic", "DispMove", "DispTankTurn"]] = df["Dispersion"].str.extract(r"([\d.]+)\s*/\s*([\d.]+)\s*/\s*([\d.]+)").astype(float)
df[["Dep", "Elev"]] = df["Dep/Elev"].str.extract(r"(-?\d+)°\s*/\s*\+?(\d+)°").astype(float)
df[["SpeedFwd", "SpeedBack"]] = df["Speed"].str.extract(r"(\d+)\s*/\s*(\d+)").astype(float)
df["Traverse"] = df["Traverse"].str.replace("°/s", "", regex=False).astype(float)
df["Weight"] = df["Weight"].str.replace("t", "", regex=False).astype(float)
df.drop(columns=["Dispersion", "Dep/Elev", "Speed"], inplace=True)

df.to_csv("results\\clean\\wot_tank_stats_clean.csv", index=False)
print(f"{len(df)} data cleaned as wot_tank_stats_clean.csv ✅")

source_file = "results/clean/wot_tank_stats_clean.csv"
final_file = "results/wot_stats.csv"

try:
    shutil.move(source_file, final_file)
    print("✅ Fichier déplacé vers :", final_file)
except Exception as e:
    print("❌ Échec du déplacement du fichier :", e)

# Supprimer les sous-dossiers raw/ et clean/
for subdir in ["results/raw", "results/clean"]:
    if os.path.exists(subdir):
        try:
            shutil.rmtree(subdir)
            print(f"🗑️ Dossier supprimé : {subdir}")
        except Exception as e:
            print(f"⚠️ Erreur lors de la suppression de {subdir} :", e)
driver.quit()