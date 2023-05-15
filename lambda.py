#Lets import boto3 module
import boto3
#We will invoke the client for S3 and resource for dynamodb
s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('dynamodb_pdt')  # DynamoDB table name
#First we will fetch bucket name from event json object
def lambda_handler(event, context):
    # TODO implement
bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
#Now we will fetch file name which is uploaded in s3 bucket from event json object
s3_file_name = event["Records"][0]["s3"]["object"]["key"]
#We will call now get_object() function to Retrieves objects from Amazon S3. To use GET , you must have READ access to the object. If you grant READ access to the anonymous user, you can return the object without using an authorization
resp = s3_client.get_object(Bucket=bucket_name, Key=s3_file_name)
#Lets decode the json object returned by function which will return string
 data = resp['Body'].read().decode('utf-8')
 print (data) # This print statement will be displayed on Lambda console as well as on CloudWatch. 
#Use Split() which will split a string into a list where each word is a list item
 productdetails = data.split("\n")
#Now we will traverse through the list pick elements one by one and push it to dynamodb table using table.put_item()
 for prdt in productdetails:
  prdt_data = prdt.split(",")
    
        table.put_item(Item = {
            "Variantid": prdt_data[0],
            "color": prdt_data[1],
            "size": prdt_data[2],
            "Fit": prdt_data[3],
            "Stock": prdt_data[4]
        })
    return 'success'
