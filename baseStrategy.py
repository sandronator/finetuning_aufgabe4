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
    
    def set_queries(self, queries):
        self.queries = queries
        
    def run(self):
        for strategy, query in self.queries:
            print("Running: " + strategy + "\n")
            start = time.time()
            self.cursor.execute(query)
            end = time.time()
            self._print_result(strategy, end, start)
            
        
    def _print_result(self, strategy, end, start):
        duration = end - start
        minutes= int(duration // 60)
        seconds = duration % 60
        
        print(f"---- RESULTS FROM {self.db_name} Strategy: {strategy} ----\n")
        print(f"duration: {minutes}m {seconds:.2f}s")
        _print_cursor(self.cursor)

def _print_cursor(cursor):
    for row in cursor.fetchall():
        print(f"{row} '\n'")

