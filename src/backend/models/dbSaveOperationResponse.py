class DbSaveOperationResponse:
    def __init__(self, success: bool, message: str):
        self.__success = success
        self.__message = message

    def get_success(self):
        return self.__success

    def get_message(self):
        return self.__message

    def __eq__(self, other):
        if not isinstance(other, DbSaveOperationResponse):
            return False
        return self.get_success() == other.get_success() and self.get_message() == other.get_message()
