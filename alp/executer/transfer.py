from miniagent import configure
from miniagent.executer import ExecuterInterface
from miniagent.adapters.kafka_producer import KafkaProducerAdapter
from miniagent.common import now
import logging
import uuid

class Transfer(ExecuterInterface):

    def execute_command(self, 
                            initial_param: dict, 
                            producer: KafkaProducerAdapter,
                        ) -> tuple[int, dict]:
        
        topic = 'alp.transfer'
        
        message = initial_param.copy()
        message.update(dict(
            transfer_id=uuid.uuid4().hex[-12:],
            transfer_date=now().isoformat(),
            ))

        rtn, result = producer.produce_message(
                        topic= topic,
                        message= message
                    )
        return rtn, result