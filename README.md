# ElasticDynamoDBItem

Library used to extend the DynamoDB items size limit is AWS.

The principle of *ElasticDynamoDBItem* is simple:
 - step 0: The initial structure of an item.
 - step 1: When inserting an entry in a list, if an exception is thrown because the item exceeds the size limit.
 - step 2: A second item is created just like the first with a messages attributes that contains the new message.
 - step 3: The next attribute of the first part is then set to TRUE since there is a new part.
 
The process is repeated each time the list of messages in the last part is full. These new parts extending the first one are numbered to keep the order of the lists. To get an item with the whole list, *ElasticDynamoDBItem* takes each part and merges each part of the lists. It is possible that these operations works in parallel execution. So, if two instances of the Lambda try to create a new part, one of them will only add the new entry in the new part.

![alt tag](/image/steps.png?raw=true "Steps")
