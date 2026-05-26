queries_maria = {
    "no_index": {
        "query_1": """
            ANALYZE SELECT name, title
            FROM Auth IGNORE INDEX (idx_auth_pubid), Publ IGNORE INDEX(idx_publ_pubid)
            WHERE Auth.pubID = Publ.pubID;
        """,
        "query_2": """
            ANALYZE SELECT title
            FROM Auth IGNORE INDEX (idx_auth_pubid), Publ IGNORE INDEX(idx_publ_pubid)
            WHERE Auth.pubID = Publ.pubID AND Auth.name = 'Divesh Srivastava';
        """,
    },
    "with_index": {
        "query_1": """
            ANALYZE SELECT name, title
            FROM Auth, Publ
            WHERE Auth.pubID = Publ.pubID;
        """,
        "query_2": """
            ANALYZE SELECT title
            FROM Auth, Publ
            WHERE Auth.pubID = Publ.pubID AND Auth.name = 'Divesh Srivastava';
        """,
    },
}

queries_postgres = {
    "no_index": {
        "query_1": """
            EXPLAIN ANALYZE SELECT name, title
            FROM Auth, Publ
            WHERE Auth.pubID = Publ.pubID;
        """,
        "query_2": """
            EXPLAIN ANALYZE SELECT title
            FROM Auth, Publ
            WHERE Auth.pubID = Publ.pubID AND Auth.name = 'Divesh Srivastava';
        """,
    },
    "with_index": {
        "query_1": """
            EXPLAIN ANALYZE SELECT name, title
            FROM Auth, Publ
            WHERE Auth.pubID = Publ.pubID;
        """,
        "query_2": """
            EXPLAIN ANALYZE SELECT title
            FROM Auth, Publ
            WHERE Auth.pubID = Publ.pubID AND Auth.name = 'Divesh Srivastava';
        """,
    },
}