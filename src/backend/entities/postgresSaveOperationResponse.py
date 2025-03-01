class PostgresSaveOperationResponse:
    def __init__(self, success: bool, message: str):
        self.success = success
        self.message = message

    def __eq__(self, other):
        if not isinstance(other, PostgresSaveOperationResponse):
            return False
        return self.success == other.success and self.message == other.message