from google.cloud import firestore
import os

class Firestore:
    def __init__(self,data:dict):
        self.instance_name     = data['instance_name']
        self.project           = data['project']
        self.machine_type      = data['machine_type']
        self.deployment_status = data['deployment_status']
        self.job_status        = data['job_status']
        self.instance_ip       = data['instance_ip']
        self.deployed_on       = data['deployed_on']
        self.environment       = data['environment']

    def update_deployment(self):
        db          = firestore.Client(self.project)
        update_data = {
            'deployment_status': self.deployment_status,
            'job_status': self.job_status,
            'instance_ip': self.instance_ip,
            'machine_type': self.machine_type,
            'deployed_on': self.deployed_on
        }
        fb         = db.collection("my-compute-firestore-table").document(self.environment).collection("compute_engine").document(self.instance_name)
        result     = fb.update(update_data)
        print(result)
        return {'status': "firestore update successfull"}

if __name__ == "__main__":
    project = os.getenv('PROJECT_ID')
    instance = os.getenv('instance_name')
    f = Firestore({'instance_name': instance,'machine_type':'f4-micro','instance_ip': '123','project': project,'deployment_status': 'completed','job_status': 'running','deployed_on': '123','environment': 'prod'})
    print(f.update_deployment())