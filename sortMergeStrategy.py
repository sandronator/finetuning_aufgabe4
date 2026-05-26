from repositories.sort_merge_resolver import resolve
from baseStrategy import BaseStrategy

class SortMergeStrategy(BaseStrategy):
    def __init__(self, conn, db_name, all_queries):
        self.BASENAME = "Sort Merge "
        super().__init__(conn, db_name, all_queries)

    def run(self):
        if self.db_name not in resolve:
            raise Exception("Sort-Merge Join not supported for " + self.db_name)

        for disable in resolve[self.db_name]["disable"]:
            self.cursor.execute(disable)

        super().run()

        for reset in resolve[self.db_name]["reset"]:
            self.cursor.execute(reset)