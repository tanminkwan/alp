from flask_restful import reqparse
from flask_api import status
from miniagent import api
from miniagent.executer import ExecuterCaller
from miniagent.event_receiver import Resource

class TesterBot(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('event_id', type=str)
    parser.add_argument('parallelism', type=int)
    parser.add_argument('exe_number', type=int)
    parser.add_argument('sleep_secs', type=int)

    def post(self):

        args = TesterBot.parser.parse_args()

        data = dict(
            initial_param = dict(
                env_params = dict(
                    event_id = args['event_id'],
                    exe_number = args['exe_number'],
                    sleep_secs = args['sleep_secs'],
                ),
                parallelism = args['parallelism'],
            ),
            executer = 'alp.executer.control_tower.TesterBot',
        )

        rtn, rtn_message = ExecuterCaller.instance().execute_command(data)

        if rtn > 0:
            status_code = status.HTTP_200_OK
        elif rtn == 0:
            return rtn_message, status.HTTP_204_NO_CONTENT
        else:
            status_code = status.HTTP_400_BAD_REQUEST

        return rtn_message, status_code

    def delete(self):

        data = dict(
            initial_param = dict(),
            executer = 'alp.executer.control_tower.TesterBot',
        )

        rtn, rtn_message = ExecuterCaller.instance().execute_command(data)

        if rtn > 0:
            status_code = status.HTTP_200_OK
        elif rtn == 0:
            return rtn_message, status.HTTP_204_NO_CONTENT
        else:
            status_code = status.HTTP_400_BAD_REQUEST

        return rtn_message, status_code

    post.permitted_roles = ["control_tower"]
    delete.permitted_roles = ["control_tower"]

class Scale(Resource):

    def put(self, deployment, replicas):

        data = dict(
            initial_param = dict(
                deployment = deployment,
                replicas = replicas
            ),
            executer = 'alp.executer.control_tower.ScaleInOut',
        )

        rtn, rtn_message = ExecuterCaller.instance().execute_command(data)

        if rtn > 0:
            status_code = status.HTTP_200_OK
        elif rtn == 0:
            return rtn_message, status.HTTP_204_NO_CONTENT
        else:
            status_code = status.HTTP_400_BAD_REQUEST

        return rtn_message, status_code

    put.permitted_roles = ["control_tower"]

class Route(Resource):

    def put(self, command):

        if command=='open':
            executer = 'alp.executer.control_tower.OpenFront'
        elif command=='openv2':
            executer = 'alp.executer.control_tower.OpenV2Front'
        elif command=='close':
            executer = 'alp.executer.control_tower.CloseFront'
        else:
            return {"error":"Param is not valid."}, status.HTTP_400_BAD_REQUEST
        
        data = dict(
            initial_param = {},
            executer = executer,
        )

        rtn, rtn_message = ExecuterCaller.instance().execute_command(data)

        if rtn > 0:
            status_code = status.HTTP_200_OK
        elif rtn == 0:
            return rtn_message, status.HTTP_204_NO_CONTENT
        else:
            status_code = status.HTTP_400_BAD_REQUEST

        return rtn_message, status_code

    put.permitted_roles = ["control_tower"]


api.add_resource(TesterBot, '/testerbot', endpoint='testerbot')
api.add_resource(Route, '/route/<string:command>', endpoint='route')
api.add_resource(Scale, '/scale/<string:deployment>/<int:replicas>', endpoint='scale')
