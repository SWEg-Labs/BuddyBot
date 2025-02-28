class DbSaveOperationResponse:
    def __init__(self, success: bool, message: str):
        self.success = success
        self.message = message
