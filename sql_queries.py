import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create = """
    CREATE TABLE IF NOT EXISTS staging_events (
        ste_artist varchar,
        ste_auth varchar,
        ste_fname varchar,
        ste_gender char,
        ste_itemsInSessions int,
        ste_lname varchar,
        ste_length numeric,
        ste_level varchar,
        ste_location varchar,
        ste_method varchar,
        ste_page varchar,
        ste_registration bigint,
        ste_session_id int,
        ste_song varchar,
        ste_status int,
        ste_ts bigint,
        ste_userAgent varchar,
        ste_user_id int
    );

"""

staging_songs_table_create = """
    CREATE TABLE IF NOT EXISTS staging_songs (
        num_songs int,
        artist_id varchar,
        artist_latitude numeric,
        artist_longitude numeric,
        artist_location varchar,
        artist_name varchar,
        song_id varchar,
        title varchar,
        duration numeric,
        year int                                        
    );
"""

songplay_table_create = """
    CREATE TABLE IF NOT EXISTS songplays (
        sp_songplays_id int IDENTITY(0, 1),
        sp_start_time timestamp NOT NULL distkey,
        sp_user_id int NOT NULL,
        sp_level varchar NOT NULL,
        sp_song_id varchar,
        sp_artist_id varchar,
        sp_session_id int,
        sp_location varchar,
        sp_useragent varchar
    );
 """

user_table_create = """
    CREATE TABLE IF NOT EXISTS users (
        u_user_id int distkey,
        u_first_name varchar,
        u_last_name varchar,
        u_gender char,
        u_level varchar NOT NULL       
    );
"""

song_table_create = """
    CREATE TABLE IF NOT EXISTS songs (
        s_song_id varchar NOT NULL distkey,
        s_title varchar NOT NULL,
        s_artist_id varchar NOT NULL ,
        s_year int,
        s_duration numeric
    ); 
"""

artist_table_create = """
    CREATE TABLE IF NOT EXISTS artists (
        a_artist_id varchar NOT NULL distkey,
        a_name varchar NOT NULL,
        a_location varchar,
        a_latitude numeric,
        a_longitude numeric
    );
"""

time_table_create = """
    CREATE TABLE IF NOT EXISTS time (
        start_time timestamp NOT NULL distkey, 
        hour int,
        day int,
        week int,
        month int,
        year int,
        weekday int
        
    );
"""

# STAGING TABLES

staging_events_copy = f"""
    COPY staging_events from {config.get("S3", "LOG_DATA")}
    iam_role {config.get("IAM_ROLE", "ARN")}
    format as json {config.get("S3", "LOG_JSONPATH")}
"""


staging_songs_copy = f"""
    COPY staging_songs from {config.get("S3", "SONG_DATA")}
    iam_role {config.get("IAM_ROLE", "ARN")}
    format as json 'auto';
"""

# FINAL TABLES

songplay_table_insert = ("""
    INSERT INTO songplays (
        sp_start_time, sp_user_id, sp_level, sp_song_id,
        sp_artist_id, sp_session_id, sp_location, sp_useragent
    ) SELECT 
        TIMESTAMP 'epoch' + ste.ste_ts/1000 * INTERVAL '1 Second' AS sp_start_time,
        ste.ste_user_id AS sp_user_id,
        ste.ste_level AS  sp_level,
        sts.song_id AS sp_song_id,
        sts.artist_id AS sp_artist_id,
        ste.ste_session_id AS sp_session_id,
        ste.ste_location AS sp_location,
        ste.ste_useragent AS sp_useragent
    
      FROM staging_songs sts 
      JOIN staging_events ste
      ON sts.title = ste.ste_song AND (sts.artist_name = ste.ste_artist)
      WHERE ste.ste_page = 'NextSong'    
""")

user_table_insert = ("""
    INSERT INTO users (
        u_user_id, u_first_name, u_last_name,
        u_gender, u_level
        
    ) SELECT 
        ste.ste_user_id AS u_user_id,
        ste.ste_fname AS u_first_name,
        ste.ste_lname AS u_last_name,
        ste.ste_gender AS u_gender,
        ste.ste_level AS u_level
        
     FROM staging_events ste
""")

song_table_insert = ("""
    INSERT INTO songs (
       s_song_id, s_title, s_artist_id,
        s_year, s_duration
    ) SELECT 
        sts.song_id AS s_song_id,
        sts.title AS s_title,
        sts.artist_id AS s_artist_id,
        sts.year AS s_year,
        sts.duration AS s_duration
        
     FROM staging_songs sts
""")

artist_table_insert = ("""
    INSERT INTO artists (
       a_artist_id, a_name, a_location,
       a_latitude, a_longitude
    ) SELECT 
        sts.artist_id AS a_artist_id,
        sts.artist_name AS a_name,
        sts.artist_location AS a_location,
        sts.artist_latitude AS a_latitude,
        sts.artist_longitude AS a_longitude
     FROM staging_songs sts
""")

time_table_insert = ("""
    INSERT INTO time (
        start_time, hour, day,
        week, month, year,
        weekday
    ) SELECT 
        TIMESTAMP 'epoch' + ste.ste_ts/1000 * INTERVAL '1 Second' AS start_time,
        DATE_PART(hour, start_time) AS hour,
        DATE_PART(day, start_time) AS day,
        DATE_PART(week, start_time) AS week,
        DATE_PART(month, start_time) AS month,
        DATE_PART(year, start_time) AS year,
        DATE_PART(weekday, start_time) AS weekday
     FROM staging_events ste
     WHERE ste.ste_page = 'NextSong'
""")

# QUERY LISTS

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]

