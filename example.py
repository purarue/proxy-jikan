import os
import requests
import jikanpy
from functools import partial

import urllib3
urllib3.disable_warnings(urllib3.exceptions.SubjectAltNameWarning)

PROXY_IP = os.environ["PROXY_IP"]
PROXY_PORT = os.environ["PROXY_PORT"]
PROXY_TOKEN = os.environ["PROXY_TOKEN"]

PROXY_FULL = "https://{}:{}".format(PROXY_IP, PROXY_PORT)

print("Requesting to", PROXY_FULL)

session = requests.Session()
# re-assign session.get with partial that validates HTTPS
session.get = partial(session.get, verify='cert.pem')

# update default headers to include authentication
session.headers.update({"Proxy-Token": PROXY_TOKEN})

jikan_instance = jikanpy.Jikan(selected_base=PROXY_FULL, session=session)

resp = session.get(PROXY_FULL, headers={"Proxy-To": "https://httpbin.org"})
resp.raise_for_status()
print(resp)

print(jikan_instance.anime(1)["title"])

