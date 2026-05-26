from manager import Manager
from baseStrategy import BaseStrategy
from nestedInnerLoopStrategy import NestedInnerLoopStrategy
from sortMergeStrategy import SortMergeStrategy
from hashJoinStrategy import HashJoinStrategy
from setup import get_connection, load_data_postgres
from repositories.all_queries import queries_postgres

if __name__ == '__main__':
    db_post, conn_postsql = get_connection(maria=False)

    # Daten einmalig laden; danach werden zwischen den Tests nur die Indexe getauscht.
    load_data_postgres()

    # Aufgabe 1
    join_manager = Manager(BaseStrategy(conn_postsql, db_post, queries_postgres["with_index"]))
    # join_manager.setup_db("no-index")
    # join_manager.execute()  # 3 Mrd. Tupel via Kreuzprodukt -> > 10 min
    join_manager.setup_db("unique-publ")
    join_manager.execute()
    join_manager.setup_db("cl-both")
    join_manager.execute()

    # Aufgabe 2 — vorheriger Lauf war 'cl-both' (CLUSTER hat Tabelle physisch sortiert);
    # reload_data=True stellt die ursprüngliche Ladereihenfolge wieder her.
    join_manager.setStrategy(NestedInnerLoopStrategy(conn_postsql, db_post, queries_postgres["with_index"]))
    join_manager.setup_db("nc-publ", reload_data=True)
    join_manager.execute()
    join_manager.setup_db("nc-auth")
    join_manager.execute()
    join_manager.setup_db("nc-both")
    join_manager.execute()

    # Aufgabe 3 — Tabelle ist noch im Original-Layout, kein Reload nötig.
    join_manager.setStrategy(SortMergeStrategy(conn_postsql, db_post, queries_postgres["no_index"]))
    join_manager.setup_db("no-index")
    join_manager.execute()
    join_manager.setQueries(queries_postgres["with_index"])
    join_manager.setup_db("nc-both")
    join_manager.execute()
    join_manager.setup_db("cl-both")
    join_manager.execute()

    # Aufgabe 4 — wieder vom CLUSTER-Zustand wegkommen.
    join_manager.setStrategy(HashJoinStrategy(conn_postsql, db_post, queries_postgres["no_index"]))
    join_manager.setup_db("no-index", reload_data=True)
    join_manager.execute()
