import templates
from botocore.exceptions import ClientError

def get(dynamo, query):
    currentpart = 0
    query['Key']['part'] = {'N' : str(currentpart)}
    elastic_attributes = query['ElasticAttributes']
    query.pop('ElasticAttributes', None)
    base = dynamo.get_item(**query)
    item = base['Item']
    print(str(item['part']['N']))
    while item['next']['BOOL']:
        currentpart+=1
        query['Key']['part'] = {'N' : str(currentpart)}
        item2 = dynamo.get_item(**query)['Item']
        print(str(item2['part']['N']))
        item['next'] = item2['next']
        print('a')
        for attribute in elastic_attributes:
            item[attribute]['L'].extend(item2[attribute]['L'])
        print('b')
    base['Item'] = item
    return base

def put(dynamo, query):
    currentpart = 0
    query['Key']['part'] = {'N' : str(currentpart)}
    item = dynamo.get_item(TableName=query['TableName'], Key=query['Key'], AttributesToGet=['next'])['Item']
    while item['next']['BOOL']:
        currentpart+=1
        query['Key']['part'] = {'N' : str(currentpart)}
        item2 = dynamo.get_item(TableName=query['TableName'], Key=query['Key'])['Item']
        item['next'] = item2['next']
    query['ConditionExpression'] = '#next = :false'
    if 'ExpressionAttributeNames' not in query:
        query['ExpressionAttributeNames'] = {}
    query['ExpressionAttributeNames']['#next'] = 'next'
    if 'ExpressionAttributeValues' not in query:
        query['ExpressionAttributeValues'] = {}
    query['ExpressionAttributeValues'][':false'] = {
        'BOOL' : False
    }

    try:
        result = dynamo.update_item(**query)
    except Exception as e:
        if "Item size to update has exceeded the maximum allowed size" in str(e):
            try:
                currentpart+=1
                result = templates.chatMessages(Dynamo=dynamo, Family=query['Key']['family']['S'], Part=currentpart, Msg=query['ExpressionAttributeValues'][':val']['L'][0])
                oldpart = currentpart - 1
                old_item_query = {
                    'TableName' : query['TableName'],
                    'Key' : query['Key'],
                    'UpdateExpression' : "SET #next = :next",
                    'ExpressionAttributeNames' : {
                        '#next' : "next"
                    },
                    'ExpressionAttributeValues' : {
                        ':next' : {
                            'BOOL' : True
                        }
                    }
                }
                old_item_query['Key']['part']['N'] = str(oldpart)

                dynamo.update_item(**old_item_query)
            except ClientError as e:
                query['Key']['part'] = {'N' : str(currentpart)}
                result = dynamo.update_item(**query)
    return result





