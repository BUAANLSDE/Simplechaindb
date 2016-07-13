__author__ = 'PC-LiNing'

from jsonschema import validate

payload_schema={
    "type":"object",
    "properties":{
        # additional description
        "msg":{"type":"string"},
        # item,matter.such as 'reward','demand','recharge' and so on.
        "issue":{"type":"string"},
        # on behalf of the transaction type.such as the  currency transaction or the goods assets transaction.
        "category":{"type":"string"},
        # amount of virtual currency
        "amount":{"type":"number"},
        # hash of goods
        "asset":{"type":"string"},
        # total asset of the transaction owner
        "account":{"type":"number"}
    }
}

def  validate_payload_format(payload):
    try:
        validate(payload,payload_schema)
        return True
    except Exception as e:
        return False


payload={"msg" : "i like this video.","issue" : "reward","category" : "currency", "amount" : 50.5,"asset":"hash of this video","account":3000}
print(validate_payload_format(payload))