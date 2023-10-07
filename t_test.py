import requests
import uuid
import random
from time import sleep

r = requests.put('http://localhost:5017/api/v1/route/open')
#r = requests.put('http://localhost:5017/api/v1/scale/k8sh/1')

print(r.headers)
print(r.text)

"""

j_dict = dict(
    withdraw_account_id = 'aaaa',
    withdraw_user_name = 'kim',
    deposit_account_id = 'aaaa',
    deposit_user_name = 'kim',
    transfer_amount = 100
)

r = requests.post('http://www.leebalso.org/api/v1/transfers/eve_1111', json=j_dict)

print(r.headers)
print(r.text)


import redis
import redis_lock

#r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
r = None
def update_balance(key:str, add:int):
    new_balance = 0
    with redis_lock.Lock(r, "tiffanie"):
        p = r.get(key)
        if p:
            new_balance = int(p) + add
        else:
            new_balance = add
        r.set(key, new_balance)
    return new_balance

print(update_balance('test2', 500))
print(update_balance('test2', 1000))
print(update_balance('test2', 500))

import base64
from io import BytesIO

from flask import Flask

from matplotlib.figure import Figure

app = Flask(__name__)

@app.route("/")
def hello():
    # Generate the figure **without using pyplot**.
    fig = Figure()
    ax = fig.subplots()
    ax.plot([1, 2])
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"

if __name__ == '__main__': 
   app.run()
"""
