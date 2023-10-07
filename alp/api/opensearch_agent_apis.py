from flask_api import status
from flask_restful import reqparse
from miniagent import api
from miniagent.executer import ExecuterCaller
from miniagent.event_receiver import Resource

class TransferDeposit(Resource):

    def get(self, event_id, transfer_id):

        data = dict(
            initial_param = dict(
                index = 'alp.balance',
                bool = [
                    {"event_id":event_id},
                    {"transfer_id": transfer_id},
                    {"transaction_type": "deposit"},
                ],
            ),
            executer = 'alp.executer.opensearch_agent.Query',
        )

        rtn, rtn_message = ExecuterCaller.instance().execute_command(data)

        if rtn < 0:
            return rtn_message, status.HTTP_500_INTERNAL_SERVER_ERROR
        elif rtn == 0 or not rtn_message['results']:
            return rtn_message, status.HTTP_204_NO_CONTENT

        return rtn_message['results'][0], status.HTTP_200_OK

    get.permitted_roles = ["opensearch_agent"]

class LatestBalance(Resource):

    def get(self, event_id, account_id):

        data = dict(
            initial_param = dict(
                index = 'alp.balance',
                bool = [
                    {"event_id":event_id},
                    {"account_id":account_id},
                ],
                sort = { "create_date": "desc"},
                size = 1,
            ),
            executer = 'alp.executer.opensearch_agent.Query',
        )

        rtn, rtn_message = ExecuterCaller.instance().execute_command(data)
        
        if rtn < 0:
            return rtn_message, status.HTTP_500_INTERNAL_SERVER_ERROR
        elif rtn == 0 or not rtn_message['results']:
            return rtn_message, status.HTTP_204_NO_CONTENT
        
        return rtn_message['results'][0], status.HTTP_200_OK

    get.permitted_roles = ["opensearch_agent"]

class BalanceRanks(Resource):

    def get(self, event_id):

        aggs = \
        {
            "withdraw_amount": {
                "sum": {
                    "field": "withdraw_amount"
                }
            },
            "deposit_amount": {
                "sum": {
                    "field": "deposit_amount"
                }
            }
        }

        data = dict(
            initial_param = dict(
                index = 'alp.balance',
                bool = [
                    {"event_id":event_id}
                ],
                groupby = "user_name",
                aggs = aggs,
            ),
            executer = 'alp.executer.opensearch_agent.Query',
        )

        rtn, rtn_message = ExecuterCaller.instance().execute_command(data)
        
        if rtn < 0:
            return rtn_message, status.HTTP_500_INTERNAL_SERVER_ERROR
        elif rtn == 0 or not rtn_message['results']:
            return rtn_message, status.HTTP_204_NO_CONTENT
        
        return rtn_message['results'], status.HTTP_200_OK

class Balances(Resource):

    def get(self, event_id, account_id):

        data = dict(
            initial_param = dict(
                index = 'alp.balance',
                bool = [
                    {"event_id":event_id},
                    {"account_id":account_id},
                ],
                sort = { "create_date": "desc"},
            ),
            executer = 'alp.executer.opensearch_agent.Query',
        )

        rtn, rtn_message = ExecuterCaller.instance().execute_command(data)
        
        if rtn < 0:
            return rtn_message, status.HTTP_500_INTERNAL_SERVER_ERROR
        elif rtn == 0 or not rtn_message['results']:
            return rtn_message, status.HTTP_204_NO_CONTENT
        
        return rtn_message['results'], status.HTTP_200_OK

    get.permitted_roles = ["opensearch_agent"]

class LastCount(Resource):

    def get(self, index, secs):

        aggs = \
        {
            "document_count": {
                "value_count": {
                    "field": "_id"
                }
            },
        }

        data = dict(
            initial_param = dict(
                index = index,
                range = {"transfer_date": {"gte": "now-"+secs+"s/s","lte": "now/s"}},
                aggs = aggs,
            ),
            executer = 'alp.executer.opensearch_agent.Query',
        )

        rtn, rtn_message = ExecuterCaller.instance().execute_command(data)

        if rtn < 0:
            return rtn_message, status.HTTP_500_INTERNAL_SERVER_ERROR
        elif rtn == 0 or not rtn_message['document_count']:
            return rtn_message, status.HTTP_204_NO_CONTENT
        
        return rtn_message['document_count'], status.HTTP_200_OK

    get.permitted_roles = ["opensearch_agent"]

api.add_resource(LastCount, '/opensearch/lastcount/<string:index>/<string:secs>',\
                  endpoint='LastCount')
api.add_resource(BalanceRanks, '/opensearch/ranks/<string:event_id>',\
                  endpoint='ranks')
api.add_resource(Balances, '/opensearch/balances/<string:event_id>/<string:account_id>',\
                  endpoint='balances')
api.add_resource(LatestBalance, '/opensearch/latest_balance/<string:event_id>/<string:account_id>',\
                  endpoint='latest_balance')
api.add_resource(TransferDeposit, '/opensearch/transfer_deposit/<string:event_id>/<string:transfer_id>',\
                  endpoint='transfer_deposit')