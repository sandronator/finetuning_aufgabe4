from manager import Manager
from baseStrategy import BaseStrategy
from nestedInnerLoopStrategy import NestedInnerLoopStrategy
from sortMergeStrategy import SortMergeStrategy
from hashJoinStrategy import HashJoinStrategy
from setup import get_connection
from repositories.all_queries import queries_postgres
if __name__ == '__main__':
    join_manager: Manager | None = None

    
    db_post, conn_postsql = get_connection(maria=False)
    queries_explict_no_index_postgresql = queries_postgres["no_index"]
    
    
    #Test on Postgresql
    #Aufgabe 1
    join_manager = Manager(BaseStrategy(conn_postsql, db_post, queries_postgres["with_index"]))
    #join_manager.setup_db("no-index")
    #join_manager.setQueries(queries_ignore_index) 3 Billionen Einträge durch kreuzprodukt > 10min
    #join_manager.execute()
    join_manager.setup_db("unique-publ")
    join_manager.execute()
    join_manager.setup_db("cl-both")
    join_manager.execute()
    #Aufgabe 2
    join_manager.setStrategy(NestedInnerLoopStrategy(conn_postsql, db_post, queries_postgres["with_index"]))
    join_manager.setup_db("nc-publ")
    join_manager.execute()
    join_manager.setup_db("nc-auth")
    join_manager.execute()
    join_manager.setup_db("nc-both")
    join_manager.execute()
    #Aufgabe 3
    join_manager.setStrategy(SortMergeStrategy(conn_postsql, db_post, queries_postgres["no_index"]))
    join_manager.setup_db("no-index")
    join_manager.execute()
    join_manager.setQueries(queries_postgres["with_index"])
    join_manager.setup_db("nc-both")
    join_manager.execute()
    join_manager.setup_db("cl-both")
    #Aufgabe 4
    join_manager.setStrategy(HashJoinStrategy(conn_postsql, db_post, queries_postgres["no_index"]))
    join_manager.setup_db("no-index")
    join_manager.execute()

    
    
    