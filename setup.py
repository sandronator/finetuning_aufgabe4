import mariadb
import psycopg2
import time
import os
import argparse
from dotenv import load_dotenv

load_dotenv()

COUNT_AUTH_ENTRIES_QUERY = "SELECT COUNT(*) FROM auth"
COUNT_PUBL_ENTRIES_QUERY = "SELECT COUNT(*) FROM publ"

INDEX_CONFIGS = {
    "no-index": [],
    "unique-publ": [
        "CREATE UNIQUE INDEX publ_pubid_idx ON publ(pubid);",
    ],
    "nc-publ": [
        "CREATE INDEX publ_pubid_idx ON publ(pubid);",
    ],
    "nc-auth": [
        "CREATE INDEX auth_pubid_idx ON auth(pubid);",
    ],
    "nc-both": [
        "CREATE INDEX publ_pubid_idx ON publ(pubid);",
        "CREATE INDEX auth_pubid_idx ON auth(pubid);",
    ],
    "cl-both": [
        "CREATE INDEX publ_pubid_idx ON publ(pubid);",
        "CLUSTER publ USING publ_pubid_idx;",
        "CREATE INDEX auth_pubid_idx ON auth(pubid);",
        "CLUSTER auth USING auth_pubid_idx;",
    ],
}


def create_distribute_postgres(index_config):
    _, connection = get_connection(maria=False)
    cursor = connection.cursor()

    _create_tables_force(cursor)

    start = time.time()

    file_auth = open(f"{os.getenv("PATH_AUTH")}", "r", encoding="utf-8")
    file_publ = open(f"{os.getenv("PATH_PUBL")}", "r", encoding="utf-8")

    cursor.copy_from(file_auth, "auth", sep="\t", columns=("name", "pubid"))
    cursor.copy_from(
        file_publ,
        "publ",
        sep="\t",
        columns=("pubid", "type", "title", "booktitle", "year", "publisher"),
    )

    connection.commit()
    end = time.time()
    entries = 0
    cursor.execute(COUNT_AUTH_ENTRIES_QUERY)
    entries += cursor.fetchall()[0][0]
    print("Entries Auth: " + str(entries))
    cursor.execute(COUNT_PUBL_ENTRIES_QUERY)
    publ_entries = cursor.fetchall()[0][0]
    print("Entries Publ: " + str(publ_entries))
    entries += publ_entries

    print("Total Entries (Auth, Publ): " + str(entries))

    print("PostgreSQL Runtime:", end - start, "seconds")

    for command in INDEX_CONFIGS[index_config]:
        print("Applying:", command)
        cursor.execute(command)
    connection.commit()

    cursor.close()
    connection.close()


def create_distribute_maria(index_config):
    _ ,connection = get_connection(maria=True)
    cursor = connection.cursor()
    _create_tables_force(cursor)

    start = time.time()

    cursor.execute(f"""
    LOAD DATA LOCAL INFILE '{os.getenv("PATH_AUTH")}'
    INTO TABLE auth
    FIELDS TERMINATED BY '\\t'
    LINES TERMINATED BY '\\n'
    (name, pubid)
    """)

    cursor.execute(f"""
    LOAD DATA LOCAL INFILE '{os.getenv("PATH_PUBL")}'
    INTO TABLE publ
    FIELDS TERMINATED BY '\\t'
    LINES TERMINATED BY '\\n'
    (pubid, type, title, booktitle, year, publisher)
    """)

    connection.commit()
    end = time.time()

    print("MariaDB Runtime:", end - start, "seconds")

    for command in INDEX_CONFIGS[index_config]:
        if command.startswith("CLUSTER"):
            print("Skipping (not supported in MariaDB):", command)
            continue
        print("Applying:", command)
        cursor.execute(command)
    connection.commit()

    cursor.execute(COUNT_AUTH_ENTRIES_QUERY)
    entries = cursor.fetchall()[0][0]
    print("Entries Auth: " + str(entries))
    cursor.execute(COUNT_PUBL_ENTRIES_QUERY)
    publ_entries = cursor.fetchall()[0][0]
    print("Entries Publ: " + str(publ_entries))
    entries += publ_entries

    print("Total Entries (Auth, Publ): " + str(entries))

    cursor.close()
    connection.close()


def get_connection(maria: bool) -> tuple[str, mariadb.Connection | psycopg2.extensions.connection]:
    connection = None
    db_name = "None"
    if not maria:
        connection = psycopg2.connect(
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASS"),
            host="localhost",
            port="5432",
        )
        db_name = "postgresql"

    else:
        connection = mariadb.connect(
            user=os.getenv("MARIA_USER"),
            password=os.getenv("MARIA_PASS"),
            host="localhost",
            port=3306,
            database=os.getenv("MARIA_DB"),
            local_infile=True,
        )
        db_name = "mariadb"

    return (db_name, connection)


def _create_tables_force(cursor):  # type: ignore

    cursor.execute("DROP TABLE IF EXISTS auth")
    cursor.execute("DROP TABLE IF EXISTS publ")

    cursor.execute("""CREATE TABLE auth (
        name VARCHAR(49),
        pubid VARCHAR(129)
        
    )""")

    cursor.execute("""
                CREATE TABLE publ (
                pubid VARCHAR(129),
                type VARCHAR(13),
                title VARCHAR(700),
                booktitle VARCHAR(132),
                year VARCHAR(4),
                publisher VARCHAR(196)
                )
            """)


def setupBoth(index_config):
    create_distribute_postgres(index_config)
    create_distribute_maria(index_config)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "index", choices=INDEX_CONFIGS.keys(), help="Index configuration to apply"
    )
    args = parser.parse_args()

    print(f"Index: {args.index}")
    setupBoth(args.index)
