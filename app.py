import json
import csv
import boto3
import urllib.parse

def lambda_handler(event, context):
    # TODO implement
    file_name = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    fileName= file_name.replace('.json','')
    s3 = boto3.client('s3')
    s3.download_file('demo-mrc-bucket', file_name, '/tmp/'+file_name)
    with open('/tmp/'+file_name) as json_file:
        ##s3.download_fileobj('a205123-api-bucket', file_name, json_file)
        
        jsondata = json.load(json_file)
     
        data_file = open('/tmp/'+fileName+'.csv', 'w+', newline='')
        csv_writer = csv.writer(data_file)
     
        count = 0
        for data in jsondata:
            if count == 0:
                print(data)
                header = data.keys()
                csv_writer.writerow(header)
                count += 1
            csv_writer.writerow(data.values())
         
        data_file.close()
        s3.upload_file('/tmp/'+fileName+'.csv', 'demo-mrc-bucket', fileName+'.csv')
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
