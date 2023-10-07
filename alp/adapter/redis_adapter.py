from miniagent.adapter import Adapter
from miniagent import configure
import redis_lock

class RedisCaller(Adapter):

    def update_balance(self, redis_conn, key:str, add:int) -> int:
        
        new_balance = 0

        if not add:
            add = 0

        with redis_lock.Lock(redis_conn, "tiffanie"):
            p = redis_conn.get(key)

            if p:
                new_balance = int(p) + add
            else:
                new_balance = add
            redis_conn.set(key, new_balance)

        return new_balance
    
    def get_status(self) -> int:
        return 1