#  Application d’Analyse Multi-Datasets

##  Objectif du projet

Cette application développée avec **Streamlit** permet d’analyser dynamiquement deux jeux de données :

-  Ventes Walmart
-  Véhicules Électriques

L’objectif est de proposer une analyse interactive combinant :

- KPI calculés en SQL via DuckDB
- Visualisations interactives
- Corrélations statistiques
- Filtres dynamiques
- Analyse décisionnelle

---

##  Architecture du projet

EV-STREAMLIT-DUCKDB/
│
├── app.py # Point d'entrée principal
├── requirements.txt # Dépendances du projet
├── README.md # Documentation
│
├── analytics/ # Logique métier des dashboards
│ ├── walmart_dashboard.py
│ ├── ev_dashboard.py
│ └── kpi_queries.py
│
├── database/ # Gestion DuckDB
│ └── duckdb_manager.py
│
├── utils/ # Fonctions utilitaires
│ └── helpers.py
│
├── visualizations/ # Graphiques Plotly
│ └── charts.py
│
└── data/ # Datasets (non versionnés)


---

##  Description des modules

###  app.py
Point d’entrée principal de l’application.  
Gère la navigation entre les datasets et la configuration globale.

###  analytics/
Contient la logique métier des dashboards :
- Calcul des KPI
- Application des filtres
- Requêtes SQL via DuckDB
- Génération des graphiques

###  database/
Gestion de la connexion et des interactions avec DuckDB.

###  utils/
Fonctions utilitaires réutilisables (formatage, nettoyage, etc.).

###  visualizations/
Centralisation des graphiques Plotly.

---

##  Technologies utilisées

- Python
- Streamlit
- DuckDB
- Pandas
- Plotly

---

##  Fonctionnalités principales

###  Module Walmart

- Upload dynamique du CSV
- Filtres : magasin, période, semaines spéciales
- KPI calculés en SQL (DuckDB)
- Évolution temporelle des ventes
- Analyse par magasin
- Heatmap de corrélation
- Conclusion analytique automatique
- Affichage des données filtrées

---

### Module Véhicules Électriques

- Upload dynamique du CSV
- Filtres : marque, segment, autonomie
- KPI techniques calculés en SQL
- Top marques par autonomie moyenne
- Corrélation batterie / autonomie
- Heatmap technique
- Analyse statistique
- Données filtrées consultables

---

##  Approche analytique

Les indicateurs sont calculés via des requêtes SQL exécutées en mémoire grâce à DuckDB.

Cela permet :

- Une séparation claire entre données et visualisation
- Une approche proche des environnements professionnels
- Une meilleure structuration des calculs analytiques

Les matrices de corrélation permettent d’identifier :

- L’impact des facteurs économiques sur les ventes Walmart
- La relation entre capacité batterie et autonomie des véhicules

---

##  Installation et exécution locale

### Cloner le repository

```bash
git clone https://github.com/tacos91/ev-streamlit-duckdb.git

Installation des dépendances
pip install -r requirements.txt

Lancer l'application 
streamlit run app.py ou python -m streamlit run app.py

 Données

Les datasets sont importés dynamiquement via l’interface.
Ils ne sont pas stockés dans le repository.
