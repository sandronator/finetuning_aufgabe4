from manager import Manager
from baseStrategy import BaseStrategy
from nestedInnerLoopStrategy import NestedInnerLoopStrategy
from sortMergeStrategy import SortMergeStrategy
from hashJoinStrategy import HashJoinStrategy
from setup import get_connection, load_data_postgres
from repositories.all_queries import queries_postgres

if __name__ == '__main__':
    db_post, conn_postsql = get_connection(maria=False)
    # Autocommit verhindert, dass EXPLAIN ANALYZE Locks (AccessShareLock auf publ/auth)
    # bis zum naechsten Commit haelt -- sonst blockiert das spaeter DROP INDEX/CLUSTER.
    conn_postsql.autocommit = True

    # Daten einmalig laden; danach werden zwischen den Tests nur die Indexe getauscht.
    load_data_postgres()

    # Aufgabe 1
    join_manager = Manager(BaseStrategy(conn_postsql, db_post, queries_postgres["with_index"]))
    # join_manager.setup_db("no-index")
    # join_manager.execute(aufgabe="Aufgabe 1a")  # 3 Mrd. Tupel via Kreuzprodukt -> > 10 min
    join_manager.setup_db("unique-publ")
    join_manager.execute(aufgabe="Aufgabe 1b")
    join_manager.setup_db("cl-both")
    join_manager.execute(aufgabe="Aufgabe 1c")

    # Aufgabe 2
    # reload_data=True stellt die ursprüngliche Ladereihenfolge wieder her.
    join_manager.setStrategy(NestedInnerLoopStrategy(conn_postsql, db_post, queries_postgres["with_index"]))
    join_manager.setup_db("nc-publ", reload_data=True)
    join_manager.execute(aufgabe="Aufgabe 2a")
    join_manager.setup_db("nc-auth")
    join_manager.execute(aufgabe="Aufgabe 2b")
    join_manager.setup_db("nc-both")
    join_manager.execute(aufgabe="Aufgabe 2c")

    # Aufgabe 3 
    join_manager.setStrategy(SortMergeStrategy(conn_postsql, db_post, queries_postgres["no_index"]))
    join_manager.setup_db("no-index")
    join_manager.execute(aufgabe="Aufgabe 3a")
    join_manager.setQueries(queries_postgres["with_index"])
    join_manager.setup_db("nc-both")
    join_manager.execute(aufgabe="Aufgabe 3b")
    join_manager.setup_db("cl-both")
    join_manager.execute(aufgabe="Aufgabe 3c")

    # Aufgabe 4 — wieder vom CLUSTER-Zustand wegkommen.
    join_manager.setStrategy(HashJoinStrategy(conn_postsql, db_post, queries_postgres["no_index"]))
    join_manager.setup_db("no-index", reload_data=True)
    join_manager.execute(aufgabe="Aufgabe 4")
