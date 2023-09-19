from miniagent import configure
import redis

def _get_url(agent_name:str):
    return configure.get('C_SERVICE_ENDPOINT').get(agent_name)

redis_conn = None
if 'balance' in configure['AGENT_ROLES']:

    redis_conn = redis.StrictRedis(host=configure['REDIS_DOMAIN_NAME'], 
                                   port=configure['REDIS_PORT'], 
                                   db=0, 
                                   decode_responses=True)
