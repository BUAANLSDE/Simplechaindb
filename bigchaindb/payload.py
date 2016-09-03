__author__ = 'PC-LiNing buaa'

from jsonschema import validate

payload_schema={
    "type":"object",
    "properties":{
        # additional description
        "msg":{"type":"string"},
        # item
        # currency : cost/earn/charge
        # asset :   create/transfer/destroy
        "issue":{"type":"string"},
        # on behalf of the transaction type.such as the  currency transaction or the goods assets transaction or
        # the system generate transaction .
        # 'currency','asset','system'
        "category":{"enum":["currency","asset","system"]},
        # amount of virtual currency
        "amount":{"type":"number"},
        # hash of goods
        "asset":{"type":"string"},
        # total asset of the transaction owner,before this transaction.
        "account":{"type":"number"},
        # previous account transaction id,if it is the first one, value should be 'genesis'.
        "previous":{"type":"string"},
        # trader,if issue is charge, trader is the node or null value .
        "trader":{"type":"string"}
    },
    "required":["issue","category","asset","previous"]
}

def validate_payload_format(payload):
    try:
        validate(payload,payload_schema)
        return True
    except Exception as e:
        #return False
        print(e)

payload = {
            "msg": "charge",
            "issue": "charge",
            "category": "currency",
            "amount": 300,
            "asset": "",
            "previous": ""
          }
print(validate_payload_format(payload))
