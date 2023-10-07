from flask_restful import reqparse
from flask_api import status
from miniagent import api
from miniagent.executer import ExecuterCaller
from miniagent.event_receiver import Resource

class Front(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('event_id', type=str)

    def post(self):

        args = Front.parser.parse_args()
        data = dict(
            command = 'create',
            deployment = 'front_desk',
            event_id = args['event_id'],
            executer = 'alp.executer.control_tower.Deployment',
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
            command = 'delete',
            deployment = 'front_desk',
            executer = 'alp.executer.control_tower.Deployment',
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

api.add_resource(Route, '/route/<string:command>', endpoint='route')
api.add_resource(Scale, '/scale/<string:deployment>/<int:replicas>', endpoint='scale')
