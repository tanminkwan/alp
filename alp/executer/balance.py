from miniagent import configure
from miniagent.common import ExitType
from miniagent.executer import ExecuterInterface
from miniagent.adapters.kafka_producer import KafkaProducerAdapter
from ..adapter.redis_adapter import RedisCaller
from miniagent.common import now
from datetime import datetime
import logging
import redis

from . import redis_conn

class Prework(ExecuterInterface):

    def execute_command(self, 
                            initial_param: dict,
                            redis_caller: RedisCaller,
                        ) -> tuple[int, dict]:
        
        try:

            redis.StrictRedis(host=configure['REDIS_DOMAIN_NAME'], 
                            port=configure['REDIS_PORT'], 
                            db=0, 
                            decode_responses=True)
            
        except redis.exceptions.ConnectionError as e:
            logging.error("Redis server connection error.")
            return ExitType.ABNORMAL_EXIT.value, {}
        except Exception as e:
            logging.error("Exception : " + e.__str__())
            return ExitType.ABNORMAL_EXIT.value, {}

        return 1, {"message":"OK"}
    
class IncreaseBalance(ExecuterInterface):

    def execute_command(self, 
                            initial_param: dict,
                            redis_caller: RedisCaller,
                            producer: KafkaProducerAdapter,
                        ) -> tuple[int, dict]:        

        topic = 'alp.balance'

        if not initial_param.get('deposit_account_id'):
            return -1, {"message":"deposit_account_id item not exists"}

        deposit_account_id = initial_param['deposit_account_id']
        deposit_amount = initial_param['deposit_amount']

        balance = redis_caller.update_balance(redis_conn, deposit_account_id,\
                                               deposit_amount)

        message = dict(
            account_id = deposit_account_id,
            user_name = initial_param['deposit_user_name'],
            balance = balance,
            transaction_type = 'deposit',
            event_id = initial_param['event_id'],
            deposit_id = initial_param['deposit_id'],
            deposit_date = initial_param['deposit_date'],
            deposit_amount = initial_param['deposit_amount'],
            create_date = now().isoformat()
        )

        if initial_param.get('transfer_id'):
            message.update(dict(
                transfer_id = initial_param['transfer_id'],
                withdraw_account_id = initial_param['withdraw_account_id'],
                withdraw_user_name = initial_param['withdraw_user_name'],
                ))

        return producer.produce_message(
            topic= topic,
            message= message
            )
    
class ReduceBalance(ExecuterInterface):

    def execute_command(self, 
                            initial_param: dict,
                            redis_caller: RedisCaller,
                            producer: KafkaProducerAdapter,
                        ) -> tuple[int, dict]:        

        topic = 'alp.balance'

        if not initial_param.get('withdraw_account_id'):
            return -1, {"message":"withdraw_account_id item not exists"}

        withdraw_account_id = initial_param['withdraw_account_id']
        withdraw_amount = initial_param['withdraw_amount']

        balance = redis_caller.update_balance(redis_conn, withdraw_account_id,\
                                               withdraw_amount*(-1))

        message = dict(
            account_id = withdraw_account_id,
            user_name = initial_param['withdraw_user_name'],
            balance = balance,
            transaction_type = 'withdraw',
            event_id = initial_param['event_id'],
            withdraw_id = initial_param['withdraw_id'],
            withdraw_date = initial_param['withdraw_date'],
            withdraw_amount = withdraw_amount,
            create_date = now().isoformat()
        )
        
        if initial_param.get('transfer_id'):
            message.update(dict(
                transfer_id = initial_param['transfer_id'],
                deposit_account_id = initial_param['deposit_account_id'],
                deposit_user_name = initial_param['deposit_user_name'],
                ))

        return producer.produce_message(
            topic= topic,
            message= message
            )