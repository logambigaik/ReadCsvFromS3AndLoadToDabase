import json
import csv
import boto3
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode

s3client=boto3.client('s3')
def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    csv_file = event['Records'][0]['s3']['object']['key']
    response = s3client.get_object(Bucket=bucket,Key=csv_file)
    lines = response['Body'].read().decode('utf-8').split()
    results = []
    for row in csv.DictReader(lines):
        results.append(row.values())
    # print(results)
    connection = mysql.connector.connect(host='mysqldb.c79sd2kyheg7.us-east-1.rds.amazonaws.com',database='employeedb',user='admin',password='Naresh#240')
    mysql_insert_query = "insert into employee (empid, ename, salary) values(%s, %s, %s)"
    # results=[['101','Naresh','1000'],['102','Suresh','2000']]
    cursor = connection.cursor()
    cursor.executemany(mysql_insert_query,results)
    connection.commit()
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
