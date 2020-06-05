import os

import requests
from flask import Flask, request, Response

app = Flask(__name__)

PROXY_TOKEN = os.environ["PROXY_TOKEN"]

excluded_req_headers = ["host", "proxy-to", "proxy-token"]
excluded_resp_headers = [
    "content-length",
    "content-type",
    "content-encoding",
    "transfer-encoding",
    "connection",
]

default_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0",
    "Upgrade-Insecure-Requests": "1",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "TE": "Trailers",
}


def clean_response(resp):
    cleaned_headers = {
        (k, v)
        for (k, v) in resp.raw.headers.items()
        if k.lower() not in excluded_resp_headers
    }
    return Response(resp.content, resp.status_code, cleaned_headers)


def generic_proxy_request(url, headers) -> Response:
    """
    proxies url and headers back to the requester
    """
    # remove proxy info
    passed_headers = {
        k: v for k, v in headers.items() if (k.lower() not in excluded_req_headers)
    }
    # add default headers
    for k, v in default_headers.items():
        passed_headers[k] = v
    # log request
    app.logger.info("proxying '{}' {}".format(url, passed_headers))
    # send proxy request
    resp = requests.request(
        method="GET", url=url, headers=passed_headers, allow_redirects=False
    )
    # remove request-specific headers
    return clean_response(resp)


def proxy_jikan_request(path):
    """
    proxies to the local jikan-rest server on port 8000
    """
    # e.g. proxies to localhost:8000/v3/anime/1 from IPADDR:PORT/anime/1
    resp = requests.get("http://localhost:8000/v3/{}".format(path))
    return clean_response(resp)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def proxy(path):
    auth = request.headers.get("Proxy-Token")
    if auth is None or auth != PROXY_TOKEN:
        return f"Proxy-Token is missing or doesnt match", 403
    if "Proxy-To" in request.headers:
        return generic_proxy_request(request.headers["Proxy-To"], request.headers)
    else:
        return proxy_jikan_request(path)


if __name__ == "__main__":
    app.run(
        ssl_context=("cert.pem", "key.pem"),
        port=int(os.environ["PROXY_PORT"]),
        host="0.0.0.0",
        debug=True,
    )
