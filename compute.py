import time

class Compute_engine:
    def __init__(self,compute,project,zone,name,svc_account,machine_type):
        self.project        = project
        self.zone           = zone
        self.name           = name
        self.svc_acc        = svc_account
        self.compute        = compute
        self.machine_type   = machine_type

    def create_compute_engine(self):
        image_response    = self.compute.images().getFromFamily(
        project='debian-cloud', family='debian-9').execute()
        source_disk_image = image_response['selfLink']

    # Configure the machine
        machine_type = f"zones/{self.zone}/machineTypes/{self.machine_type}"
        config = {
               'name': self.name,
               'machineType': machine_type,
               'cpuPlatform': "automatic",

        # Specify the boot disk and the image to use as a source.
               'disks': [
            {
                'boot': True,
                'autoDelete': True,
                'initializeParams': {
                    'sourceImage': source_disk_image,
                }
            }
               ],

        # Specify a network interface with NAT to access the public
        # internet.
               'networkInterfaces': [{
                    'subnetwork': 'projects/%s/regions/us-east1/subnetworks/my-p-sub-east-app-001' % self.project,
               }],

        # Allow the instance to access cloud storage and logging.
               'serviceAccounts': [{
                    'email': self.svc_acc,
                    'scopes': [
                "https://www.googleapis.com/auth/devstorage.read_only",
                "https://www.googleapis.com/auth/logging.write",
                "https://www.googleapis.com/auth/monitoring.write",
                "https://www.googleapis.com/auth/servicecontrol",
                "https://www.googleapis.com/auth/service.management.readonly",
                "https://www.googleapis.com/auth/trace.append"
               ]
               }]
          }
        return self.compute.instances().insert(project=self.project,zone=self.zone,body=config).execute()

     # [START wait_for_operation]
    def wait_for_operation(self,operation):
        print('Waiting for operation to finish...')
        while True:
            result = self.compute.zoneOperations().get(
            project=self.project,
            zone=self.zone,
            operation=operation).execute()
            if result['status'] == 'DONE':
                print("deployment completed.")
                if 'error' in result:
                    raise Exception(result['error'])
                return result
        time.sleep(1)

    def list_instances(self):
        result = self.compute.instances().list(project=self.project, zone=self.zone).execute()
        return result['items'] if 'items' in result else None

    def get_details(self,data:dict):
        result =self.compute.instances().get(project=self.project,
        zone=self.zone,
        instance=self.name).execute()
        if "networkInterfaces" in result:
            data['instance_ip']       = result['networkInterfaces'][0]["networkIP"]
            data['job_status']        = 'completed'
            data['deployment_status'] = result['status']
            data['deployed_on']       = result["creationTimestamp"]
        return data
        
        

        
