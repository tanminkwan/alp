import os
import logging
from datetime import datetime, timedelta
from pytz import timezone
from random import randrange

#DEBUG
DEBUG = os.getenv("DEBUG", 'True').lower() in ('true', '1', 't')

#
TIMEZONE = "Asia/Seoul"

#
COMMAND_RECEIVER_ENABLED = False
MESSAGE_RECEIVER_ENABLED = \
    os.environ.get('MESSAGE_RECEIVER_ENABLED', 'True').lower() in ('true', '1', 't')

RUN_TYPE = os.environ.get('RUN_TYPE') or 'service' #service, job, app
PLATFORM_TYPE = os.environ.get('PLATFORM_TYPE') or 'linux' #k8s, docker, linux

import __main__
AGENT_NAME = os.environ.get('AGENT_NAME') or \
    os.path.basename(__main__.__file__).rsplit('.',1)[0]

AGENT_ROLES = os.environ.get('AGENT_ROLES') or \
    (AGENT_NAME.split('.')[0] if AGENT_NAME not in ['linuxshell_agent','docker_agent'] else 'launcher')

#Infra hosts
ZIPKIN_DOMAIN_NAME = os.environ.get('ZIPKIN_DOMAIN_NAME') or 'localhost'
ZIPKIN_PORT =  os.environ.get('ZIPKIN_PORT') or '9411'
ZIPKIN_ADDRESS = (ZIPKIN_DOMAIN_NAME,int(ZIPKIN_PORT))
ZIPKIN_SAMPLE_RATE = int(os.environ.get('ZIPKIN_SAMPLE_RATE', '20'))

KAFKA_BOOTSTRAP_SERVERS = os.environ.get('KAFKA_BOOTSTRAP_SERVERS') or 'localhost:9092'
KAFKA_BOOTSTRAP_SERVERS = KAFKA_BOOTSTRAP_SERVERS.split(',')
ELASTIC_SEARCH_DOMAIN_NAME = os.environ.get('ELASTIC_SEARCH_DOMAIN_NAME') or 'localhost'
ELASTIC_SEARCH_PORT = os.environ.get('ELASTIC_SEARCH_PORT') or '9200'
REDIS_DOMAIN_NAME = os.environ.get('REDIS_DOMAIN_NAME') or 'localhost'
REDIS_PORT = os.environ.get('REDIS_PORT') or '6379'

logging.warning("RUN_TYPE : "+RUN_TYPE)
logging.warning("AGENT_NAME : "+AGENT_NAME)
logging.warning("AGENT_ROLES : "+AGENT_ROLES)

CUSTOM_APIS_PATH = "alp.api"

if 'account' in AGENT_ROLES:
    C_VALID_PERIOD = int(os.environ.get('VALID_PERIOD', '20'))
    base_dir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, AGENT_NAME+'.db')

    CUSTOM_MODELS_PATH = "alp.model"    

if 'tester_bot' in AGENT_ROLES:
    C_SLEEP_SECS = int(os.environ.get('SLEEP_SECS', '1'))
    C_EXE_NUMBER = int(os.environ.get('EXE_NUMBER', '10'))

if 'front_desk' in AGENT_ROLES:
    C_FRONT_VERSION = os.environ.get('FRONT_VERSION', 'v1')

#alp services
CONTROL_TOWER_SERVICE_ADDRESS     = \
    os.environ.get('CONTROL_TOWER_SERVICE_ADDRESS') or 'localhost:5010'
ACCOUNT_SERVICE_ADDRESS     = \
    os.environ.get('ACCOUNT_SERVICE_ADDRESS') or 'localhost:5011'
FRONT_DESK_SERVICE_ADDRESS     = \
    os.environ.get('FRONT_DESK_SERVICE_ADDRESS') or 'localhost:5012'
TRANSFER_SERVICE_ADDRESS     = \
    os.environ.get('TRANSFER_SERVICE_ADDRESS') or 'localhost:5013'
WITHDRAW_SERVICE_ADDRESS     = \
    os.environ.get('WITHDRAW_SERVICE_ADDRESS') or 'localhost:5014'
DEPOSIT_SERVICE_ADDRESS     = \
    os.environ.get('DEPOSIT_SERVICE_ADDRESS') or 'localhost:5015'
BALANCE_SERVICE_ADDRESS     = \
    os.environ.get('BALANCE_SERVICE_ADDRESS') or 'localhost:5016'
K8S_AGENT_SERVICE_ADDRESS     = \
    os.environ.get('K8S_AGENT_SERVICE_ADDRESS') or 'alp.leebalso.org'
ELASTICSEARCH_AGENT_SERVICE_ADDRESS = \
    os.environ.get('ELASTICSEARCH_AGENT_SERVICE_ADDRESS') or 'localhost:5022'

C_SERVICE_ENDPOINT =\
{
    "account":ACCOUNT_SERVICE_ADDRESS+"/api/v1",
    "transfer":TRANSFER_SERVICE_ADDRESS+"/api/v1",
    "withdraw":WITHDRAW_SERVICE_ADDRESS+"/api/v1",
    "deposit":DEPOSIT_SERVICE_ADDRESS+"/api/v1",
    "k8s_agent":K8S_AGENT_SERVICE_ADDRESS+"/api/v1",
    "opensearch_agent":ELASTICSEARCH_AGENT_SERVICE_ADDRESS+"/api/v1",
}

PREWORK =\
[
    {
        "executer":"alp.executer.balance.Prework",
        "agent_roles":["balance"],
    },
    {
        "executer":"alp.executer.tester_bot.Prework",
        "agent_roles":["tester_bot"],
    },
]

EXECUTERS_BY_TOPIC =\
[
    {"topic":"alp.transfer",
    "executer":"alp.executer.withdraw.Withdraw",
    "agent_roles":["withdraw"]},
    {"topic":"alp.transfer.withdrawn",
    "executer":"alp.executer.deposit.Deposit",
    "agent_roles":["deposit"]},
    {"topic":"alp.deposit",
    "executer":"alp.executer.balance.IncreaseBalance",
    "agent_roles":["balance"]},
    {"topic":"alp.withdraw",
    "executer":"alp.executer.balance.ReduceBalance",
    "agent_roles":["balance"]},
]

#Scheduler
SCHEDULER_API_ENABLED = True
EXIT_AFTER_JOBS = False

schedules = []

SCHEDULED_JOBS =os.environ.get('SCHEDULED_JOBS') or schedules

# job list : /scheduler/jobs

C_EVENT_ID = os.environ.get('EVENT_ID') or 'eve_alpha'

"""
if os.environ.get('GAME_START_DATE'):

    game_start_date = datetime.fromisoformat(os.environ.get('GAME_START_DATE'))
    #game_start_date = timezone('Asia/Seoul').localize(tmp)

    C_GAME_START_DATE = max(datetime.now(timezone(TIMEZONE)), game_start_date)
else:
    C_GAME_START_DATE = datetime.now(timezone(TIMEZONE)) + timedelta(seconds = 10)
"""
# Game Duration In Seconds
#C_GAME_DURATION = int(os.environ.get('GAME_DURATION', str(600)))
IS_CURRENT_TRAFFIC_HIGH = False

game_schedules = []
if 'control_tower' in AGENT_ROLES:

    """
    game_schedules.append(dict(
        executer="alp.executer.control_tower.StartGame",
        trigger="date",
        id="start_game",
        name="Start Game",
        run_date=C_GAME_START_DATE,
        agent_roles=["control_tower"],
    ))

    game_schedules.append(dict(
        executer="alp.executer.control_tower.EndGame",
        trigger="date",
        id="end_game",
        name="end Game",
        run_date=C_GAME_START_DATE + timedelta(seconds = C_GAME_DURATION),
        agent_roles=["control_tower"],
    ))
    """
    game_schedules.append(dict(
        executer="alp.executer.control_tower.TransferInOut",
        trigger="interval",
        id="check_scaling",
        name="Check_Scaling",
        params=dict(
            traffic_threshold=30,
            secs=30
        ),            
        seconds=30,
        start_date=datetime.now()+timedelta(minutes=1)
    ))

SCHEDULED_JOBS = os.environ.get('SCHEDULED_JOBS') or game_schedules