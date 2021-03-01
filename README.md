# ReadCsvFromS3AndLoadToDabase


# Create databse in RDS:(pass databasename,password, Public Access as yes, Select recent database version)

![image](https://user-images.githubusercontent.com/54719289/109562248-2671a600-7b04-11eb-9738-492fb81a25cf.png)
![image](https://user-images.githubusercontent.com/54719289/109562485-751f4000-7b04-11eb-94e0-423141f63ba2.png)


# Open dbeaver and give Endpoint as Host:

    Note: If there is any time out issue, check the secuirty group and include port 3306
    
![image](https://user-images.githubusercontent.com/54719289/109564351-f24bb480-7b06-11eb-9294-4ab0699ce257.png)


![image](https://user-images.githubusercontent.com/54719289/109564281-da743080-7b06-11eb-8b64-3ef97a0ce189.png)

![image](https://user-images.githubusercontent.com/54719289/109564437-14453700-7b07-11eb-8184-72399a8e4b71.png)


# If u face mysql-access denied issue,create new database and create table:

![image](https://user-images.githubusercontent.com/54719289/109565413-6fc3f480-7b08-11eb-8c7d-72882ef8f16a.png)

![image](https://user-images.githubusercontent.com/54719289/109566671-34c2c080-7b0a-11eb-9cea-8b30671dcc06.png)



# Refer Lambda layer and ConnecttoDatabase git hub

  import json
  import mysql.connector
  #from mysql.connector import Error
  #from mysql.connector import errorcode

  def lambda_handler(event, context):
     # TODO implement
    connection = mysql.connector.connect(host='mysql-database.ckfn3yov2iqa.eu-west-2.rds.amazonaws.com',
                                        database='empdb',
                                        user='admin',
                                        password='a****123')
    mysql_insert_query = "insert into employee_tbl (empid, empname, location,salary) values(%s, %s, %s,%s)"
    
    rows=[['101','Ganesh','India','1000'],['102','Archu','UK','2000']]
    cursor = connection.cursor()
    cursor.executemany(mysql_insert_query,rows)
    connection.commit()

    print(cursor.rowcount, " rows inserted successfully")
   
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }        


  
![image](https://user-images.githubusercontent.com/54719289/109573204-94be6480-7b14-11eb-83f2-3a599cd9c35b.png)


  import json
  import boto3
  import csv
  import mysql.connector
  #from mysql.connector import Error
  #from mysql.connector import errorcode

  s3client=boto3.client('s3')


  def lambda_handler(event, context):
     # TODO implement
     
    bucket = event['Records'][0]['s3']['bucket']['name']
    csv_file = event['Records'][0]['s3']['object']['key']
    response = s3client.get_object(Bucket=bucket, Key=csv_file)
    lines = response['Body'].read().decode('utf-8').split()
    results = []
    for row in csv.DictReader(lines):
        results.append(row.values())
    print(results)
    
    connection = mysql.connector.connect(host='mysql-database.ckfn3yov2iqa.eu-west-2.rds.amazonaws.com',
                                        database='empdb',
                                        user='admin',
                                        password='archu123')
    #mysql_insert_query = "insert into employee_tbl (empid, empname, location,salary) values(%s, %s, %s,%s)"
    
    #rows=[['101','Ganesh','India','1000'],['102','Archu','UK','2000']]
    #cursor = connection.cursor()
    #cursor.executemany(mysql_insert_query,rows)
    #connection.commit()

    #print(cursor.rowcount, " rows inserted successfully")
   
   
    mysql_insert = "insert into employee_tbl(empid,epname,location,salary) values(%s,%s,%s,%s)"
    
    cursor = connection.cursor()
    cursor.executemany(mysql_insert, results)
    connection.commit()
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }        
