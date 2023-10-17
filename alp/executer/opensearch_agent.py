from miniagent import configure
from miniagent.executer import ExecuterInterface
from miniagent.adapters.opensearch_caller import OpensearchCaller
from datetime import datetime, timedelta
import logging
from pprint import pprint

url = "http://"+configure.get('ELASTIC_SEARCH_DOMAIN_NAME')\
            +":"+configure.get('ELASTIC_SEARCH_PORT')

class Query(ExecuterInterface):

    def _parcer4groupby(self, response):

        q = response.get('aggregations').get('groupby').get('buckets')
        
        return 1, {"results":q}

    def _parcer4paggs(self, response):

        q = response.get('aggregations').get('paggs').get('buckets')
        
        return 1, {"results":q}

    def _parcer4aggs(self, response):

        q = response.get('aggregations')
        
        return 1, q

    def _parcer(self, response):

        if not response['hits']['hits']:
            return 0, {"results":[]}

        results = []
        
        for q in response['hits']['hits']:
            results.append(q['_source'])

        return 1, {"results":results}

    def execute_command(self, 
                            initial_param: dict,
                            os_caller: OpensearchCaller,
                        ) -> tuple[int, dict]:
        
        index = initial_param['index']
        query =\
        {
            "query": {
                "bool": {
                    "must": []
                }
            }
        }
        parcer = self._parcer

        if initial_param.get('bool'):
                    
            for q in initial_param['bool']:

                query['query']['bool']['must'].append({"match": q})
        
        if initial_param.get('sort'):

            query.update(dict(
                sort = initial_param['sort'])
            )

        if initial_param.get('size')!=None:
            
            query.update(dict(
                size = initial_param['size'])
            )

        if initial_param.get('range'):

            query['query']['bool']['must'].append(dict(
                range = initial_param['range'])
            )

        if initial_param.get('groupby'):

            aggs =\
            {
                "aggs":{
                    "groupby":{
                        "terms":{
                            "field": initial_param['groupby']+".keyword",
                            "size": 1000
                        },
                        "aggs": initial_param['aggs']
                    }
                }
            }
            query.update(aggs)
            parcer = self._parcer4groupby

        elif initial_param.get('paggs'):

            aggs =\
            {
                "aggs":{
                    "paggs":initial_param['paggs']
                }
            }
            query.update(aggs)
            logging.error(str(query))
            parcer = self._parcer4paggs

        elif initial_param.get('aggs'):

            aggs =\
            {
                "aggs": initial_param['aggs']
            }
            query.update(aggs)
            parcer = self._parcer4aggs       

        return os_caller.call_get(url, index, query, parcer)