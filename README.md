# World of Tanks BI Analysis

This projects automatize data scraping and exploitation from [tomato.gg](https://tomato.gg/tank-stats) via Selenium

---

## ✅ Requirements

- [Python 3.9+](https://www.python.org/downloads/)
- [Firefox](https://www.mozilla.org/fr/firefox/new/)
- [Geckodriver](https://github.com/mozilla/geckodriver/releases) 
- `git` 

---

## 📦 Installation

Run the installation.bat

## 🚀 Script execution

```bash
python main.py
```

Le script :
- opens Firefox Selenium
- scraps the site
- resilients to popups (cookies, ads)
- exports results to `results/wot_tank_stats_clean.csv`

---

## 📁 Project structure
```
pythonProject/
├── .venv/                    
├── main.py                  
├── geckodriver.exe            
├── requirements.txt          
```
