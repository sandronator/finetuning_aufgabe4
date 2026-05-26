# nestedLoopResolver.py
resolve = {
    "postgresql": {
        "disable": ["SET enable_hashjoin = off", "SET enable_mergejoin = off"],
        "reset": ["RESET enable_hashjoin", "RESET enable_mergejoin"],
    },
    "mariadb": {
        "disable": ["SET optimizer_switch='block_nested_loop=off'"],
        "reset": ["SET optimizer_switch=DEFAULT"],
    },
}