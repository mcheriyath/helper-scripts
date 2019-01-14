import os
import boto3
import psycopg2
import sys
import logging
import traceback
import psycopg2.extras

logger=logging.getLogger()
logger.setLevel(logging.INFO)


def log_err(errmsg):
    logger.error(errmsg)
    return {"body": errmsg , "headers": {}, "statusCode": 400,
        "isBase64Encoded":"false"}

def lambda_handler(event, context):
  REDSHIFT_DATABASE = os.environ['REDSHIFT_DATABASE']
  REDSHIFT_USER = os.environ['REDSHIFT_USER']
  REDSHIFT_PASSWD = os.environ['REDSHIFT_PASSWD']
  REDSHIFT_PORT = os.environ['REDSHIFT_PORT']
  REDSHIFT_ENDPOINT = os.environ['REDSHIFT_ENDPOINT']
  REDSHIFT_CLUSTER = os.environ['REDSHIFT_CLUSTER']
  REDSHIFT_QUERY = "SELECT * FROM pg_table_def WHERE tablename = 'sales'"

  try:
    client = boto3.client('redshift')
    creds = client.get_cluster_credentials(
      DbUser=REDSHIFT_USER,
      DbName=REDSHIFT_DATABASE,
      ClusterIdentifier=REDSHIFT_CLUSTER,
      DurationSeconds=3600)
    logger.info("Get Cluster credentials: SUCCESS.")
  except:
    return log_err ("ERROR: Cannot get credentials.\n{}".format(
    	traceback.format_exc()) )
    sys.exit(1)

  try:
    conn = psycopg2.connect(
      dbname=REDSHIFT_DATABASE,
      user=creds['DbUser'],
      password=creds['DbPassword'],
      port=REDSHIFT_PORT,
      host=REDSHIFT_ENDPOINT)
    logger.info("Connecting to Redshift with temp credentials: SUCCESS.")
  except:
    return log_err ("ERROR: Cannot connect.\n{}".format(
    	traceback.format_exc()) )
    sys.exit(1)

  try:
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(REDSHIFT_QUERY)
    results_list=[]
    for result in cursor: results_list.append(result)
    #print(results_list)
    cursor.close()
    conn.commit()
    conn.close()
    logger.info("Query Run: SUCCESS.")
  except:
    return log_err ("ERROR: Cannot execute.\n{}".format(
    	traceback.format_exc()) )
    sys.exit(1)

  return {"body": str(results_list), "headers": {}, "statusCode": 200,
        "isBase64Encoded":"false"}

if __name__== "__main__":
    lambda_handler(None,None)
