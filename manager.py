from baseStrategy import BaseStrategy
import setup

class Manager:
    def __init__(self, strategy: BaseStrategy, ):
        self.strategy = strategy
        self.current_index_config = None

    def setStrategy(self, strategy: BaseStrategy):
        self.strategy = strategy
        # Aktuellen Index-Config an die neue Strategy weiterreichen
        self.strategy.index_config = self.current_index_config

    def setQueries(self, queries: dict[str, str]):
        self.strategy.set_queries(queries)

    # Only Postgresql and MariaDb available at the moment
    def setup_db(self, index_config, reload_data=False):
        self.current_index_config = index_config
        self.strategy.index_config = index_config
        setup.reset_postgres(index_config, reload_data=reload_data)

    def execute(self, aufgabe: str | None = None):
        self.strategy.run(aufgabe=aufgabe)
        