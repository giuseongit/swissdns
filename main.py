#!/usr/bin/env python3

from dns_client import DNSClient
from synchronizers import DnsASynchronizer

username = os.environ["DNS_REGISTRAR_USERNAME"]
token = os.environ["DNS_REGISTRAR_TOKEN"]
domain = os.environ["DNS_DOMAIN"]
provider = os.environ["DNS_PROVIDER"]
hosts = os.environ["DNS_HOST_TO_REFRESH"].split(" ")


dns_client = DNSClient(provider, username, token)
syncher = DnsASynchronizer(dns_client, domain, hosts)

syncher.sync()
