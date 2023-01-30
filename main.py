#!/usr/bin/env python3

from dns_client import DNSClient
from synchronizers import DnsASynchronizer
from config import EnvStore, StoreManager

config = StoreManager()
config.add_store(EnvStore())

username = config.get("DNS_REGISTRAR_USERNAME")
token = config.get("DNS_REGISTRAR_TOKEN")
domain = config.get("DNS_DOMAIN")
provider = config.get("DNS_PROVIDER")
hosts = config.get("DNS_HOST_TO_REFRESH").split(" ")

dns_client = DNSClient(provider, username, token)
syncher = DnsASynchronizer(dns_client, domain, hosts)

syncher.sync()
