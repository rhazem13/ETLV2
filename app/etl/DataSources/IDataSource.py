class IDataSource:
    def __init__(self, type) -> None:
        self.type = type
        
    def extract(self, path:str):
        """Extract function is not implemented yet"""
        pass

    def load(self, path:str):
        """Load function is not implemented yet"""
        pass