# sortMergeResolver.py
resolve = {
    "postgresql": {
        "disable": ["SET enable_hashjoin = off", "SET enable_nestloop = off"],
        "reset": ["RESET enable_hashjoin", "RESET enable_nestloop"],
    },
}