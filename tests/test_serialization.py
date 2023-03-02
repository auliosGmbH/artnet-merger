from src.serialization import SerializeObj
import json

from src.settings import Settings, MergeSettings,MergeMethod,UniverseRange
import os

def test_settings():

    settings = Settings("169.254.216.70")

    settings.merge_settings.append(MergeSettings([0,1],1,MergeMethod.RANGE))
    settings.merge_settings[0].range = [UniverseRange(0,0,500),UniverseRange(1,0,512)]

    settings.merge_settings.append(MergeSettings([3,4],2,MergeMethod.PRIO))
    settings.merge_settings[1].prio = 3

    obj = SerializeObj()
    obj.obj_to_json(settings)
    obj.save_json(path="pytest.json")

    obj.load_json(path="pytest.json")

    settings2 = json.loads(obj.json,object_hook=Settings.from_json)

    assert settings2.reciver_ip == settings.reciver_ip
    assert settings2.merge_settings[0].prio == settings.merge_settings[0].prio


    os.remove("pytest.json") 






