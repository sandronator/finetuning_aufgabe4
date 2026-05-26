from setup import get_connection
import time
import psycopg2
import mariadb

        

class BaseStrategy:
    
    def __init__(self, conn: psycopg2.extensions.connection | mariadb.Connection, db_name, queries: dict[str, str]):
        self.connection = conn
        self.cursor = conn.cursor()
        self.db_name = db_name
        self.queries = queries
        self.index_config = None  # vom Manager via setup_db gesetzt

    def set_queries(self, queries):
        self.queries = queries

    def run(self, aufgabe: str | None = None):
        strategy_name = self.__class__.__name__
        prefix_parts = []
        if aufgabe:
            prefix_parts.append(aufgabe)
        prefix_parts.append(strategy_name)
        if self.index_config:
            prefix_parts.append(f"idx={self.index_config}")
        prefix = " | ".join(prefix_parts)

        for query_name, query in self.queries.items():
            print(f"Running: [{prefix}] / {query_name}\n")
            start = time.time()
            self.cursor.execute(query)
            end = time.time()
            self._print_result(strategy, end, start)
        self.connection.commit()
            
        
    def _print_result(self, strategy, end, start):
        duration = end - start
        minutes = int(duration // 60)
        seconds = duration % 60

        print(f"---- RESULTS FROM {self.db_name} | {prefix} | Query: {query_name} ----\n")
        print(f"duration: {minutes}m {seconds:.2f}s")
        _print_cursor(self.cursor)

def _print_cursor(cursor):
    for row in cursor.fetchall():
        print(f"{row} '\n'")

