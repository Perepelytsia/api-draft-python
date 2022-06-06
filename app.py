from flask import Flask, request, json
import requests_cache
import pandas as pd
from multiprocessing import Pool
import constants as c

app = Flask(__name__)
# the request data is saved in a sqlite database for cache
cache_manager = None


@app.route('/api/ping', methods=['GET'])
def get_ping():
    return {c.KEY_API_SUCC: True}


@app.route('/api/profile', methods=['GET'])
def get_posts():
    users = request.args.get(c.KEY_API_USERS)

    if not users:
        response = c.ERR_MSG_USERS, c.STATUS_CODE_400
    else:
        try:
            # parallelize API requests
            pool = Pool(initializer=init_process, processes=len(users))
            data = pool.map(process_api, users.split(","))
            pool.close()
            pool.join()
            users = pd.DataFrame(data)
            # sort data
            users = users.sort_values(by=[c.KEY_API_ID])
            response = {c.KEY_API_USERS: users.to_dict('records')}
        except:
            return {}, c.STATUS_CODE_500

    return response


def init_process():
    global cache_manager
    cache_manager = requests_cache.CachedSession('api_cache')


def process_api(user):
    global cache_manager
    # get data from API
    api_response = cache_manager.get(c.API_GITHUB + "/" + c.KEY_API_USERS + "/" + user)
    if api_response.status_code == c.STATUS_CODE_200:
        return json.loads(api_response.text)
    else:
        return []


if __name__ == '__main__':
    app.run()
