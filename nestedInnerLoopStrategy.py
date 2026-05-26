from repositories.nested_loop_resolver import resolve
from baseStrategy import BaseStrategy

class NestedInnerLoopStrategy(BaseStrategy):
    def __init__(self, conn, db_name, all_queries):
        self.BASENAME = "Nested Inner Loop "
        super().__init__(conn, db_name, all_queries)

    def run(self, aufgabe: str | None = None):
        if self.db_name not in resolve:
            raise Exception("No Inner Loop Resolver Found")

        for disable in resolve[self.db_name]["disable"]:
            self.cursor.execute(disable)

        super().run(aufgabe=aufgabe)

        for reset in resolve[self.db_name]["reset"]:
            self.cursor.execute(reset)