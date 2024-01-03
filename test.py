from config import *
import jwt
import hashlib
import os
import requests
import uuid
from urllib.parse import urlencode, unquote
from pprint import pprint

access_key = ACCESS_KEY
secret_key = SECRET_KEY
server_url = 'https://api.upbit.com/v1/deposit'

params = {
  'uuid': '689321e7-5de1-4099-b1b5-33ac9527fb64'
}
query_string = unquote(urlencode(params, doseq=True)).encode("utf-8")

m = hashlib.sha512()
m.update(query_string)
query_hash = m.hexdigest()

payload = {
    'access_key': access_key,
    'nonce': str(uuid.uuid4()),
    'query_hash': query_hash,
    'query_hash_alg': 'SHA512',
}

jwt_token = jwt.encode(payload, secret_key)
authorization = 'Bearer {}'.format(jwt_token)
headers = {
  'Authorization': authorization,
}

res = requests.get(server_url, params=params, headers=headers)
pprint(res.json())