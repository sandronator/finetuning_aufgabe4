from baseStrategy import BaseStrategy
import setup

class Manager:
    def __init__(self, strategy: BaseStrategy, ):
        self.strategy = strategy
        
    def setStrategy(self, strategy: BaseStrategy):
        self.strategy = strategy
    
    def setQueries(self, queries: dict[str, str]):
        self.strategy.set_queries(queries)
        
    # Only Postgresql and MariaDb available at the moment
    def setup_db(self, index_config):
        setup.setupBoth(index_config)
        
    def execute(self):
        self.strategy.run()
        