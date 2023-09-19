from miniagent import configure
from miniagent.executer import ExecuterInterface
from miniagent.adapters.kafka_producer import KafkaProducerAdapter
from miniagent.common import now
from datetime import datetime
import logging
import uuid

class Withdraw(ExecuterInterface):

    def execute_command(self, 
                            initial_param: dict,
                            producer: KafkaProducerAdapter,
                        ) -> tuple[int, dict]:        

        self.initial_param = initial_param.copy()
        self.producer = producer

        topic = 'alp.withdraw'
        
        self.initial_param.update(dict(
            withdraw_id = uuid.uuid4().hex[-12:],
            withdraw_date = now().isoformat()
        ))
        
        if self.initial_param.get('transfer_id'):
            self.initial_param.update(dict(
                withdraw_account_id=self.initial_param['sender'],
                withdraw_amount=self.initial_param['transfer_amount'],
                ))
            self._send2deposit()
        
        return producer.produce_message(
            topic= topic,
            message= self.initial_param
            )
    
    def _send2deposit(self) -> dict:
        
        topic = 'alp.transfer.withdrawn'

        return self.producer.produce_message(
            topic= topic,
            message= self.initial_param
            )