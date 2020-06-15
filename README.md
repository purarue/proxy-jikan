# proxy-jikan

spooky self-signed token-authenticated proxy for [Jikan](https://github.com/jikan-me/jikan-rest/)

### Setup

On a VPS/VM somewhere to use as a proxy:

Install: `python`, `pipenv`, `npm`, `openssl`

Set this up, use `forever` to daemonize processes.

```
git clone https://gitlab.com/seanbreckenridge/docker-jikan ../docker-jikan  # and set that up
sudo npm install -g forever
./setup
export PROXY_PORT=8001
export PROXY_TOKEN=hello
pipenv install
./restart
```

Once the servers are running, I copy the cert.pem down to my machine, put it in the same folder as `example.py`, and test it with:

```
PROXY_IP=41.193.... PROXY_PORT=8001 PROXY_TOKEN=hello python3 example.py
```
