from db import get_connection

with get_connection() as conn, conn.cursor() as cur:
    cur.execute("""
            CREATE TABLE IF NOT EXISTS mentionData (
                ID serial PRIMARY KEY ,
                UniqueID text NOT NULL UNIQUE,
                Title varchar(255) NOT NULL,
                Source text NOT NULL,
                SourceType varchar(32) NOT NULL,
                Topic varchar(64) NOT NULL,
                Content text,
                publishDate TIMESTAMPTZ NOT NULL,
                fetched TIMESTAMPTZ NOT NULL  
            );
    """)
    print("Table Created")
    conn.commit()
