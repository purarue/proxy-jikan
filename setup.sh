#!/bin/bash
# sets up the self signed cert

set -e
echo "use the following IP for FQDN:"
curl --silent ipinfo.io | sed -e "s/^[{}]//" -e "s/^\s*//" -e "s/,$//" -e "s/\"//g" -e "/^\s*$/d" | head -n 1
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
