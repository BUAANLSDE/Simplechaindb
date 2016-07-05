__author__ = 'PC-LiNing'

from jsonschema import validate

payload_schema={
    "type":"object",
    "properties":{
        "msg":{"type":"string"},
        "issue":{"type":"string"},
        "category":{"type":"string"},
        "divided":{"type":"boolean"},
        "amount":{"type":"number"},
    }
}

def  validate_payload_format(payload):
    try:
        validate(payload,payload_schema)
        return True
    except Exception as e:
        return False


payload={"msg" : "Eggs","issue" : "buket","category" : "money","divided" :True, "amount" : 50.5}
print(validate_payload_format(payload))