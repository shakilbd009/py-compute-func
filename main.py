import base64,json,os,compute
import googleapiclient.discovery as gcp 



def compute_deployment(data:dict):
    engine  = gcp.build(serviceName='compute',version='v1',cache_discovery=False)
    vm      = compute.Compute_engine(compute=engine,project=data['project'],zone=data['zone'],name=data['name'],svc_account=os.getenv("SVC_ACCOUNT"),machine_type=data['machine_type'])
    try:
        ops = vm.create_compute_engine()
    except:
        raise
    try:
        vm.wait_for_operation(operation=ops['name'])
    except:
        raise
     


def hello_pubsub(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    data           = json.loads(pubsub_message)
    compute_deployment(data)

















import compute,os,json
import googleapiclient.discovery as gcp 


def run(project:str,zone:str,name:str):
    engine      = gcp.build(serviceName='compute',version='v1')
    svc_account = os.getenv("SVC_ACCOUNT") 
    return compute.create_compute_engine(engine,project,zone,name,svc_account)


