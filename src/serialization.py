import json


class SerializeObj:
    def __init__(self):
        self.__json = None

    def obj_to_json(self,obj) -> dict:
        self.__json = json.dumps(obj, default=lambda o: o.to_json(), indent=2)
        return self.__json

    def save_json(self,path):
        with open(path, "w") as f:
            f.write(self.__json)

    def load_json(self,path) -> dict:
        with open(path, "r") as f:
            self.__json = json.dumps(json.load(f)) 
        return self.__json

    @property
    def json(self):
        return self.__json