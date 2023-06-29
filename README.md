# Echodb - A tiny elt system

![Python](https://img.shields.io/badge/Made%20With-Python%203.8-blue.svg?style=for-the-badge&logo=Python&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)


**Update** (15 December 2022): View the web application here at [Resonance](https://resonance.streamlit.app/)

## About the project

Echodb is a tiny system for collecting and scheduling music data pipeline from [Spotify](https://engineering.atspotify.com/). In short, it allows you to:

* Collect playlist such as `Discovery Weekly`, `Release Radar` (or even custom events of your choosing).
* Store the data in a scalable database w/ [Postgresql](https://www.postgresql.org/) and [SQLAlchemy](https://www.sqlalchemy.org/).
* Leverage a wide range of tools to model and analyze the behavioral data.
* Generate reports and deploy online dashboard for easy management.

---

## Echodb Datastack 101

![Pipeline](data/stack.png)

The repository structure follows the conceptual architecture of Echodb, which consists of six loosely-coupled sub-systems connected by five standardized data protocols/formats.

To briefly explain these six sub-systems:

* **[Extractor][extractor]** Utilizes `Prefect` as an orchestration scheduler and `Pydantic` for data validation, ensuring successful reception and processing of Spotify data from various trackers and storing them in different dataframes. Once validated, the data is then made available in-stream for real-time processing, and can also be loaded to blob storage and data warehouse for analysis.
* **[Storage][storage]** relies on `Postgresql` as the primary database for storing Spotify data, and leverages `SQLAlchemy` as the interface for efficient data modeling, retrieval, and manipulation.
* **[Analytics][analytics]** Employs Plotly for visualizing the Snowplow event data, Pandas for data transformation and preparation, and Streamlit for deploying interactive dashboards that enable exploration and sharing of insights derived from the analyzed data.

**For more information on the current Snowplow architecture, please see the [Technical architecture][architecture]**.

[extractor]: https://www.postgresql.org/
[storage]: https://www.postgresql.org/
[analytics]: https://www.postgresql.org/