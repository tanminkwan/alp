from miniagent import db
from miniagent.executer import ExecuterInterface
from miniagent.common import now, local_dt_str

from ..dbquery.account_queries import select_accounts, insert_account

class AccountList(ExecuterInterface):

    def execute_command(self, 
                            initial_param: dict,
                        ) -> tuple[int, dict]:
        
        event_id = initial_param.get('event_id')
        reqs = select_accounts(event_id)

        results = []
        if reqs:

            for row in reqs:
            
                results.append(dict(
                    event_id     = row.event_id,
                    account_id   = row.account_id,
                    user_name    = row.user_name,
                    created_date = row.created_date.isoformat()
                ))

        return 1 if results else 0, dict(results=results)
    
class Account(ExecuterInterface):

    def execute_command(self, 
                            initial_param: dict,
                        ) -> tuple[int, dict]:
        
        now_t =  now()
        
        message = dict(
            event_id = initial_param.get('event_id'),
            account_id = initial_param.get('account_id'),
            user_name = initial_param.get('user_name'),
            created_date =now_t.isoformat(),
        )

        insert_account(message)

        db.session.commit()

        return 1, message