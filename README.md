# World of Tanks BI Analysis

Ce projet automatise le scraping de données de tanks depuis [tomato.gg](https://tomato.gg/tank-stats) via Selenium, et produit un fichier CSV nettoyé prêt pour l’analyse en Business Intelligence.

---

## ✅ Prérequis

- [Python 3.9+](https://www.python.org/downloads/)
- [Firefox](https://www.mozilla.org/fr/firefox/new/)
- [Geckodriver](https://github.com/mozilla/geckodriver/releases) (doit correspondre à ta version de Firefox)
- `git` (facultatif mais recommandé)

---

## 📦 Installation

### 1. Cloner le projet

```bash
git clone https://github.com/Subzero710/World-of-Tank-BI-analysis.git
cd World-of-Tank-BI-analysis/pythonProject
```

### 2. Créer et activer l’environnement virtuel

```bash
python -m venv .venv
.\.venv\Scripts activate  # Sous Windows
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

---

## 🚀 Exécution du script

```bash
python main.py
```

Le script :
- ouvre Firefox avec Selenium
- scrape les données de tanks (2 pages de 500 chars)
- ferme automatiquement les popups (cookies, pub)
- exporte le CSV propre dans `results/wot_tank_stats_clean.csv`

---

## 📁 Structure du projet

```
pythonProject/
├── .venv/                      # Environnement virtuel (non tracké)
├── main.py                    # Script principal
├── geckodriver.exe            # Driver Firefox local
├── requirements.txt           # Dépendances
```
