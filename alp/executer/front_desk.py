from miniagent import configure
from miniagent.executer import ExecuterInterface
from miniagent.adapters.rest_caller import RESTCaller
import logging

from . import _get_url

class Stat(ExecuterInterface):

    def _unscramble_result(self, result):
        new_list = []
        for row in result:
            print('row:', row)
            new_row = dict(
                user_name = row['key'],
                count = row['doc_count'],
                deposit_amount = row['deposit_amount']['value'],
                withdraw_amount = row['withdraw_amount']['value'],
                balance = row['deposit_amount']['value'] - row['withdraw_amount']['value'],
                tot_tran_amount = row['deposit_amount']['value'] + row['withdraw_amount']['value'],
            )
            new_list.append(new_row)

        return new_list

    def execute_command(self, 
                            initial_param: dict,
                            rest_caller: RESTCaller,
                        ) -> tuple[int, dict]:
        
        url = "http://"+_get_url('opensearch_agent')+"/opensearch/ranks/"+initial_param['event_id']
        
        rtn, result = rest_caller.call_get(url=url)

        if rtn!=200:
            return 0, {}
        
        return rtn, {"results":self._unscramble_result(result)}
        
