import json


class MessageModal:
    def __init__(self, code, message):
        self.code = code
        self.message = message

    @classmethod
    def from_json(cls, json_dict):
        json_string = json.dumps(json_dict)
        json_dict = json.loads(json_string)
        return cls(**json_dict)


class TokenViewModel:
    def __init__(self, token, expires, status, result):
        self.token = token
        self.expires = expires
        self.status = status
        self.result = result

    @classmethod
    def from_json(cls, json_dict):
        json_string = json.dumps(json_dict)
        json_dict = json.loads(json_string)
        return cls(**json_dict)
