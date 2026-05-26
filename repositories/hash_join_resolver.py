resolve = {
    "postgresql": {
        "disable": ["SET enable_nestloop = off", "SET enable_mergejoin = off"],
        "reset": ["RESET enable_nestloop", "RESET enable_mergejoin"],
    },
    "mariadb": {
        "disable": ["SET optimizer_switch='join_cache_hashed=on'", "SET join_cache_level=8"],
        "reset": ["SET optimizer_switch=DEFAULT", "SET join_cache_level=DEFAULT"],
    },
}