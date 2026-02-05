# 🚗 EV Streamlit DuckDB – Dashboard d’analyse des véhicules électriques

## 🎯 Objectif du projet
Ce projet consiste à développer une **application web interactive** avec **Streamlit**
permettant d’analyser un jeu de données sur les **véhicules électriques**.

L’application permet :
- de téléverser un fichier CSV,
- de stocker les données dans une base **DuckDB**,
- d’exécuter des **requêtes SQL** pour calculer des indicateurs clés,
- de visualiser dynamiquement les résultats à l’aide de graphiques interactifs,
- d’appliquer des **filtres dynamiques** pour affiner l’analyse.

Ce projet s’inscrit dans le cadre du module **DEVS OPS / Data Applications**.

---

## 🛠️ Technologies utilisées
- **Python 3**
- **Streamlit** – interface web interactive
- **DuckDB** – base de données analytique
- **Pandas** – manipulation des données
- **Plotly** – visualisations interactives
- **Git & GitHub** – collaboration et versioning

---

## 📂 Jeu de données
Dataset utilisé (Kaggle) :  
**Electric Vehicle Specifications Dataset 2025**

Les fichiers CSV ne sont pas versionnés dans le dépôt Git.  
Les données sont téléversées directement via l’interface Streamlit.

---

## 📊 Indicateurs clés de performance (KPI)

L’application affiche **4 KPI distincts**, calculés à l’aide de requêtes SQL DuckDB :

1. 🔋 **Capacité moyenne de batterie (kWh)**  
   Indicateur global de la capacité énergétique des véhicules électriques.

2. 🏭 **Top 10 des marques de véhicules électriques**  
   Classement des marques les plus représentées dans le dataset.

3. 🚘 **Autonomie moyenne par marque (km)**  
   Comparaison de l’autonomie moyenne des véhicules selon les marques.

4. ⚡ **Relation entre vitesse maximale et capacité batterie**  
   Analyse de la corrélation entre performance et capacité énergétique.

---

## 🎛️ Filtres dynamiques
L’utilisateur peut affiner l’analyse à l’aide de filtres interactifs :

- **Marque** (menu déroulant)
- **Autonomie (km)** via un slider (plage minimale et maximale)

Les filtres sont appliqués **directement dans les requêtes SQL DuckDB**, garantissant
des résultats cohérents et performants.

---

## 🖥️ Fonctionnalités principales
- Téléversement de fichiers CSV
- Stockage des données dans DuckDB
- Requêtes SQL dynamiques
- Visualisations interactives avec Plotly
- Interface intuitive avec Streamlit
- Workflow Git avec branches et Pull Requests

---

## ▶️ Lancer l’application

### 1️⃣ Installer les dépendances
```bash
pip install streamlit pandas duckdb plotly
