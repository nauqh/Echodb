# Echodb - A tiny elt system

![Python](https://img.shields.io/badge/Made%20With-Python%203.8-blue.svg?style=for-the-badge&logo=Python&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Prefect](https://img.shields.io/badge/Prefect-%23ffffff.svg?style=for-the-badge&logo=prefect&logoColor=white)


**Update** (15 December 2022): View the web application here at [Resonance](https://resonance.streamlit.app/)

## About the project

Echodb is a tiny system for collecting and scheduling music data pipeline from [Spotify](https://engineering.atspotify.com/). In short, it allows you:

* Collect playlist such as `Discovery Weekly`, `Release Radar` (or even custom events of your choosing).
* Store the data in a scalable data warehouse you control ([Postgresql](https://www.postgresql.org/))
* Leverage a wide range of tools to model and analyze the behavioral data.

---

## Echodb datastack 101

![Pipeline](data/stack.png)



