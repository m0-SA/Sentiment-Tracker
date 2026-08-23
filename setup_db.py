from db import get_connection


def create_table():
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
                                    fetched TIMESTAMPTZ NOT NULL,  
                                    positive REAL,
                                    negative REAL,
                                    neutral REAL,
                                    compound REAL
                                );
                        """)
        print("Table Created")
        conn.commit()


def alter_table():
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute("""
                ALTER TABLE mentionData 
                ADD COLUMN IF NOT EXISTS positive REAL,
                ADD COLUMN IF NOT EXISTS negative REAL,
                ADD COLUMN IF NOT EXISTS neutral REAL,
                ADD COLUMN IF NOT EXISTS compound REAL
                """)
        print("Table Altered")
        conn.commit()
