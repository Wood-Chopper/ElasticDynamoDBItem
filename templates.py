import datetime
from botocore.exceptions import ClientError

def chatMessages(Dynamo=None, Family=None, Part=0, Msg=None):
    msg_fill = Msg
    if msg_fill == None:
        msg_fill = {
            "M": {
                "author": {
                    "S": "0000"
                },
                "name": {
                    "S": "System"
                },
                "text": {
                    "S": "Welcome to the family !"
                },
                "time": {
                    "S": "_"
                }
            }
        }
    
    Dynamo.put_item(
        TableName='ChatMessages',
        Item={
            'family': {
                'S': Family
            },
            'part': {
                'N': str(Part)
            },
            'next': {
                'BOOL': False
            },
            'messages': {
                'L': [msg_fill]
            },
        },
        ConditionExpression='attribute_not_exists(#family) AND attribute_not_exists(#part)',
        ExpressionAttributeNames={'#family':'family', '#part':'part'}
    )