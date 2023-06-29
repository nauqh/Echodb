"""
Load data to Postgresql 
"""
import time, hydra, psycopg2, logging
import pandas as pd
from omegaconf import DictConfig
from psycopg2.extras import RealDictCursor
from .log import get_log

logging.basicConfig(filename='data/logs.log',
                        # format="%(asctime)s | %(name)s | %(levelname)s | %(message)s (%(filename)s:%(lineno)d)"
                        format=":orange[[%(asctime)s]] %(levelname)s %(message)s",
                        datefmt='%H:%M:%S')
log = get_log(__name__)

@hydra.main(version_base=None, config_path="../config", config_name="main")
def get_db(cfg: DictConfig):
    while True:
        try:
            conn = psycopg2.connect(host=cfg['db']['host'],
                                database=cfg['db']['database'], 
                                user=cfg['db']['user'], 
                                password=cfg['db']['pwd'],
                                cursor_factory=RealDictCursor)
            curr = conn.cursor()
            print(f"🏬 Connected to database")
            break
        except Exception as e:
            print("Connection failed. Try reconnecting..")
            print(e)
            time.sleep(2)
    return conn, curr

class Database():
    __slots__ = ("conn", "curr")

    def __init__(self) -> None:
        self.conn, self.curr = get_db()
    
    def commit(self):
        self.conn.commit()
    
    def record(self):
        return self.curr.fetchone()

    def records(self):
        return self.curr.fetchall()
    
    # NOTE: LOAD DATA
    def add_playlist(self, playlist: dict):
        id = playlist['id']
        name = playlist['name']
        owner = playlist['owner']['display_name']
        description = playlist['description']
        followers = playlist['followers']['total']
        image = playlist['image']
        url = playlist['url']

        self.curr.execute("""SELECT * FROM playlist WHERE playlist_id = %s """, (str(id), ))
        
        query = self.record()
        if not query:
            self.curr.execute("INSERT INTO playlist VALUES (%s, %s, %s, %s, %s, %s, %s) returning * ",
                              (id, name, owner, description, followers, image, url))
            log.info(f"Added {name} playlist")
        else:
            log.warning(f"Playlist already exists")
        self.commit()

    def add_tracks(self, df: pd.DataFrame):
        df = df.sort_values('name').reset_index(drop=True)
        count = len(df)
        for i in range(len(df)):
            id = df.loc[i, 'track_id']
            name = df.loc[i, 'name']
            added_date = df.loc[i, 'added_date']
            release_date = df.loc[i, 'release_date']
            popularity = df.loc[i, 'track_pop']
            image = df.loc[i, 'image']
            url = df.loc[i, 'url']
            artist_id = df.loc[i, 'artist_id']

            self.curr.execute(
                """SELECT * FROM track WHERE track_id = (%s) """, (id, ))
            
            query = self.record()
            if not query:
                self.curr.execute("INSERT INTO track VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                                  (id, name, added_date, release_date, str(popularity), image, url, artist_id))
            else:
                count -= 1

        # log.info(f"Added {count} tracks")
        self.commit()

    def add_artists(self, df: pd.DataFrame):
        df = df.sort_values('name').reset_index(drop=True)
        count = len(df)
        for i in range(len(df)):
            id = df.loc[i, "artist_id"]
            name = df.loc[i, "name"]
            followers = df.loc[i, "followers"]
            genres = df.loc[i, "genres"]
            popularity = df.loc[i, "popularity"]
            image = df.loc[i, "image"]
            url = df.loc[i, "url"]

            self.curr.execute("SELECT * FROM artist WHERE id = (%s) ", (id, ))
            
            query = self.record()
            if not query:
                self.curr.execute("INSERT INTO artist VALUES (%s, %s, %s, %s, %s, %s, %s)",
                            (id, name, str(followers), genres, str(popularity), image, url))
            else:
                count -= 1

        # log.info(f"Added {count} artists")
        self.commit()
    
    # NOTE: RETRIEVE DATA
    def view(self, table: str):
        self.curr.execute(f"SELECT * FROM {table}")
        recs = self.records()
        if table == "playlist":
            return recs
        return pd.DataFrame([i.copy() for i in recs])