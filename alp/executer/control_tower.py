from miniagent import configure
from miniagent.executer import ExecuterInterface
from miniagent.adapters.rest_caller import RESTCaller
import logging
import yaml
from pathlib import Path
from . import _get_url

def _create_k8s_job(rest_caller, job_name, parallelism, env_params):

    url = "http://"+_get_url('k8s_agent')+"/k8s/jobs/alp"

    file_name = './k8s/'+job_name+'-job.yaml'

    yaml_dict = yaml.safe_load(Path(file_name).read_text())

    yaml_dict['metadata']['name'] = job_name
    yaml_dict['spec']['template']['metadata']['labels']['app'] = job_name
    yaml_dict['spec']['template']['spec']['containers'][0]['name'] = job_name
    yaml_dict['spec']['parallelism'] = parallelism
    envs = yaml_dict['spec']['template']['spec']['containers'][0]['env']

    if env_params:
        for item, value in env_params.items():
            envs.append(dict(
                name = item.upper(),
                value = str(value)
            ))

    job_dict = {"job":yaml_dict}

    try:
        rtn, result = rest_caller.call_post(
                            url=url, 
                            json=job_dict
                        )
    except Exception as e:
        message = "Exception : " + e.__str__()
        logging.error(message)
        return -1, {"error":message}
            
    if rtn == 200:
        return 1, result
    else:
        return -1, {"error":result}

def _create_k8s_deployment(rest_caller, service_name):

    url = "http://"+_get_url('k8s_agent')+"/k8s/deployments/alp"

    file_name = './k8s/'+service_name+'-deployment.yaml'

    yaml_dict = yaml.safe_load(Path(file_name).read_text())
    deployment_dict = {"deployment":yaml_dict}

    logging.warning("deployment : "+ file_name)
    logging.warning(str(deployment_dict))
    
    try:
        rtn, result = rest_caller.call_post(
                            url=url, 
                            json=deployment_dict
                        )
    except Exception as e:
        message = "Exception : " + e.__str__()
        logging.error(message)
        return -1, {"error":message}
            
    if rtn == 200:
        return 1, result
    else:
        return -1, {"error":result}

def _create_k8s_service(rest_caller, service_name):

    url = "http://"+_get_url('k8s_agent')+"/k8s/services/alp"

    file_name = './k8s/'+service_name+'-service.yaml'

    yaml_dict = yaml.safe_load(Path(file_name).read_text())
    service_dict = {"service":yaml_dict}

    try:
        rtn, result = rest_caller.call_post(
                            url=url, 
                            json=service_dict
                        )
    except Exception as e:
        message = "Exception : " + e.__str__()
        logging.error(message)
        return -1, {"error":message}
            
    if rtn == 200:
        return 1, result
    else:
        return -1, {"error":result}

def _kill_k8s_deployment(rest_caller, service_name):

    deployment_name = service_name.replace('_','-') + '-v1'
    url = "http://"+_get_url('k8s_agent')+"/k8s/deployment/alp/" + deployment_name

    try:
        rtn, result = rest_caller.call_delete(url=url)
    except Exception as e:
        message = "Exception : " + e.__str__()
        logging.error(message)
        return -1, {"error":message}
            
    if rtn == 200:
        return 1, result
    else:
        return -1, {"error":result}

def _kill_k8s_service(rest_caller, service_name):

    service_name = service_name.replace('_','-')
    url = "http://"+_get_url('k8s_agent')+"/k8s/service/alp/" + service_name

    try:
        rtn, result = rest_caller.call_delete(url=url)
    except Exception as e:
        message = "Exception : " + e.__str__()
        logging.error(message)
        return -1, {"error":message}
            
    if rtn == 200:
        return 1, result
    else:
        return -1, {"error":result}

def _patch_k8s_virtualservice(rest_caller, file_name):

    url = "http://"+_get_url('k8s_agent')+\
    "/k8s/customobject/alp/networking.istio.io/v1alpha3/virtualservices/alp-external"

    file_path = './k8s/'+file_name+'.yaml'

    yaml_dict = yaml.safe_load(Path(file_path).read_text())

    custom_object_dict = {"custom_object":yaml_dict}

    try:
        rtn, result = rest_caller.call_put(
                            url=url, 
                            json=custom_object_dict
                        )
    except Exception as e:
        message = "Exception : " + e.__str__()
        logging.error(message)
        return -1, {"error":message}

    if rtn == 200:
        return 1, result
    else:
        return -1, {"error":result}

def _change_k8s_deployment_replicas(rest_caller, service_name, count):

    deployment_name = service_name.replace('_','-') + '-v1'
    url = "http://"+_get_url('k8s_agent')+"/k8s/scale/alp/" + deployment_name + "/" + str(count)

    try:
        rtn, result = rest_caller.call_put(url=url, json={})
    except Exception as e:
        message = "Exception : " + e.__str__()
        logging.error(message)
        return -1, {"error":message}
            
    if rtn == 200:
        return 1, result
    else:
        return -1, {"error":result}

def _change_k8s_deployment_replicas_old(rest_caller, service_name, count):

    deployment_name = service_name.replace('_','-') + '-v1'
    url = "http://"+_get_url('k8s_agent')+"/k8s/deployments/alp/" + deployment_name

    file_name = './k8s/'+service_name+'-deployment.yaml'

    yaml_dict = yaml.safe_load(Path(file_name).read_text())
    deployment_dict = {"deployment_object":yaml_dict}

    deployment_dict['spec']['replicas'] = count

    logging.warning("deployment : "+ file_name)
    logging.warning(str(deployment_dict))
    
    try:
        rtn, result = rest_caller.call_put(
                            url=url, 
                            json=deployment_dict
                        )
    except Exception as e:
        message = "Exception : " + e.__str__()
        logging.error(message)
        return -1, {"error":message}
            
    if rtn == 200:
        return 1, result
    else:
        return -1, {"error":result}

class OpenFront(ExecuterInterface):

    def execute_command(self, 
                            initial_param: dict,
                            rest_caller: RESTCaller,
                        ) -> tuple[int, dict]:

        return _patch_k8s_virtualservice(rest_caller, 'alp-external-virtualservice-open')
    
class CloseFront(ExecuterInterface):

    def execute_command(self, 
                            initial_param: dict,
                            rest_caller: RESTCaller,
                        ) -> tuple[int, dict]:

        return _patch_k8s_virtualservice(rest_caller, 'alp-external-virtualservice-close')
    
class ScaleInOut(ExecuterInterface):

    def execute_command(self, 
                            initial_param: dict,
                            rest_caller: RESTCaller,
                        ) -> tuple[int, dict]:

        deployment = initial_param['deployment']
        replicas = initial_param['replicas']

        return _change_k8s_deployment_replicas(rest_caller, deployment, replicas)
    
class TransferInOut(ExecuterInterface):

    def execute_command(self, 
                            initial_param: dict,
                            rest_caller: RESTCaller,
                        ) -> tuple[int, dict]:

        url = "http://"+_get_url('opensearch_agent')+"/opensearch/lastcount/"\
            +"/alp.transfer/"+str(initial_param['secs'])
        
        rtn, result = rest_caller.call_get(url=url)

        if rtn!=200 or not result.get('value'):
            return 0, {}
        
        traffic = result['value']

        is_current_traffic_high = False
        replica = 1 # Scale in
        if initial_param['traffic_threshold'] < traffic:
            is_current_traffic_high = True
            replica = 3 # Scale out

        if configure['IS_CURRENT_TRAFFIC_HIGH'] == is_current_traffic_high:
            return 1, {}
        
        configure['IS_CURRENT_TRAFFIC_HIGH'] = is_current_traffic_high
                
        return _change_k8s_deployment_replicas(rest_caller, 'transfer', replica)

class TesterBot(ExecuterInterface):

    def _set_env_params(self, initial_param):

        env_params = initial_param.copy()

        return env_params

    def execute_command(self, 
                            initial_param: dict,
                            rest_caller: RESTCaller,
                        ) -> tuple[int, dict]:

        parallelism = initial_param['parallelism'],
        env_params = initial_param['env_params']

        return _create_k8s_job(rest_caller, 'tester-bot-', parallelism, env_params)