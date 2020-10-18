from google.cloud import bigquery
from datetime import datetime
import os

def Update_deployment(data):
    bq = bigquery.Client()
    table      = os.getenv('bigquery_table')
    dataset    = os.getenv('bigquery_dataset')
    date       = datetime.today().strftime("%Y-%m-%d")
    update = (
        f"UPDATE {data['project']}.{dataset}.{table} "
        f"SET cpu_type = '{data['machine_type']}',deployment_status = '{data['deployment_status']}'"
        f",job_status = '{data['job_status']}', instance_ip = '{data['instance_ip']}', deployed_on = '{data['deployed_on']}' "
        f"WHERE instance_name = '{data['instance_name']}' AND _PARTITIONTIME = '{date}' "
    )
    result =  bq.query(update)
    result.result()
    return {'status': "bigquery update successfull"}

if __name__ == "__main__":
    project = os.getenv('PROJECT_ID')
    instance = os.getenv('instance_name')
    print(Update_deployment({'instance_name': instance,'machine_type':'f4-micro','instance_ip': '123','project': project,'deployment_status': 'completed','job_status': 'running','deployed_on': '123','zone': 'us-east1-b'}))