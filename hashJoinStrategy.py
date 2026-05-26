from repositories.hash_join_resolver import resolve
from baseStrategy import BaseStrategy

class HashJoinStrategy(BaseStrategy):
    def __init__(self, conn, db_name, all_queries):
        self.BASENAME = "Hash Join "

        super().__init__(conn, db_name, all_queries)

    def run(self):
        if self.db_name not in resolve:
            raise Exception("Hash Join not supported for " + self.db_name)

        for disable in resolve[self.db_name]["disable"]:
            self.cursor.execute(disable)

        super().run()

        for reset in resolve[self.db_name]["reset"]:
            self.cursor.execute(reset)