class PostgresSaveOperationResponse:
    def __init__(self, success: bool, message: str):
        self.__success = success
        self.__message = message

    def get_success(self):
        return self.__success
    
    def get_message(self):
        return self.__message

    def __eq__(self, other):
        if not isinstance(other, PostgresSaveOperationResponse):
            return False
        return self.__success == other.get_success() and self.__message == other.get_message()
