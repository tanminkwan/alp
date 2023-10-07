from miniagent import configure
from miniagent.executer import ExecuterInterface
from miniagent.adapters.kafka_producer import KafkaProducerAdapter
from miniagent.adapters.rest_caller import RESTCaller
from miniagent.common import now, ExitType
import logging
import random
from time import sleep

from . import _get_url

class Prework(ExecuterInterface):
    
    def execute_command(self, 
                            initial_param: dict,
                            rest_caller: RESTCaller,
                        ) -> tuple[int, dict]:

        sleep_secs = configure['C_SLEEP_SECS']
        exe_number = configure['C_EXE_NUMBER']
        event_id = configure['C_EVENT_ID']
                
        url = "http://"+_get_url('transfer')\
                 +"/transfers/" + event_id

        for i in range(exe_number):

            #user_name : tester_bot_00 ~ 99
            #account_id : a00000000000 ~ 99
            ints = random.sample(range(99),2)

            data_dict = dict(
                withdraw_account_id = 'a000000000{num:02d}'.format(num=ints[0]),
                withdraw_user_name = 'tester_bot_{num:02d}'.format(num=ints[0]),
                deposit_account_id = 'a000000000{num:02d}'.format(num=ints[1]),
                deposit_user_name = 'tester_bot_{num:02d}'.format(num=ints[1]),
                transfer_amount = ints[0]*100 + ints[1],
            )

            rtn, result = rest_caller.call_post(url=url, json=data_dict)

            if rtn != 200:
                message = "Tester bot error."
                logging.error(message)
                logging.error(str(rtn)+":"+str(result))
                return ExitType.ABNORMAL_EXIT.value, {'message':message}

            sleep(sleep_secs)

        return ExitType.STAY_RUNNING.value, result #job will be completed by itself