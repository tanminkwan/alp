
from flask import request, make_response, render_template, redirect
from miniagent import api, app, configure
from flask_restful import reqparse
from flask_api import status
from miniagent.executer import ExecuterCaller
from miniagent.event_receiver import Resource

class Withdraws(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('withdraw_account_id', type=str)
    parser.add_argument('withdraw_amount', type=int)

    def post(self, event_id):

        args = Withdraws.parser.parse_args()

        initial_param = dict(
            withdraw_account_id = args['withdraw_account_id'],
            withdraw_amount = args['withdraw_amount'],
            event_id  = event_id
        )

        param = dict(
                initial_param = initial_param ,
                executer = 'alp.executer.withdraw.Withdraw',
            )

        rtn, rtn_message = ExecuterCaller.instance().execute_command(param)

        if rtn > 0:
            status_code = status.HTTP_200_OK
        elif rtn == 0:
            return rtn_message, status.HTTP_204_NO_CONTENT
        else:
            status_code = status.HTTP_400_BAD_REQUEST

        return rtn_message, status_code

    post.permitted_roles = ["withdraw"]

api.add_resource(Withdraws, '/withdraws/<string:event_id>', endpoint='withdraws')