import base64,json,os,compute,bigquery,firestore,time
import googleapiclient.discovery as gcp 



def compute_deployment(data:dict):
    engine  = gcp.build(serviceName='compute',version='v1',cache_discovery=False)
    vm      = compute.Compute_engine(compute=engine,
    project = data['project'],
    zone    = data['zone'],
    name    = data['instance_name'],
    svc_account=os.getenv("SVC_ACCOUNT"),
    machine_type=data['machine_type'])
    try:
        ops = vm.create_compute_engine()
    except:
        raise
    try:
        vm.wait_for_operation(operation=ops['name'])
    except:
        raise
    return vm
    
     

# def my_pubsub_compute_func(event):
def my_pubsub_compute_func(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    data           = json.loads(pubsub_message)
    # data           = event.get_json(force=True)
    vm             = compute_deployment(data)
    print('vm deployed')
    # time.sleep(5)
    try:
        data       = vm.get_details(data)
        print(firestore.Firestore(data).update_deployment())
        print(bigquery.Update_deployment(data))
    except:
        raise
    else:
        print({'status': "function executed successfully"})
        return {'status': "function executed successfully"}





