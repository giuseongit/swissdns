#!/usr/bin/env python3

import os
import time
from typing import List

import requests

from dns_client import DNSClient

username = os.environ["DNS_REGISTRAR_USERNAME"]
token = os.environ["DNS_REGISTRAR_TOKEN"]
domain = os.environ["DNS_DOMAIN"]
provider = os.environ["DNS_PROVIDER"]
hosts = os.environ["DNS_HOST_TO_REFRESH"].split(" ")

class DnsASynchronizer(object):
    def __init__(self, dns_client: DNSClient, domain: str, hosts_to_sync: List[str]):
        self.dns_client = dns_client
        self.domain = domain
        self.hosts_to_sync = hosts_to_sync

    def _my_ip(self):
        resp = requests.get("https://api.my-ip.io/ip")
        return resp.text if resp.status_code == 200 else None

    def sync(self):
        _records = self.dns_client.list_a_records(self.domain)
        records = { x["name"].split(".")[0]: x for x in _records }

        ip = self._my_ip()
        while not ip:
            time.sleep(0.2)
            ip = self._my_ip()

        for host in self.hosts_to_sync:
            record = records.get(host)
            if not record:
                continue # skip host that are not active on the registrar
            if record["content"] != ip:
                ok = self.dns_client.update_a_record(self.domain, host, ip)
                if not ok:
                    # TODO: better error handling
                    print("something went wrong for host {host}.{domain}".format(host=host, domain=domain))

dns_client = DNSClient(provider, username, token)
syncher = DnsASynchronizer(dns_client, domain, hosts)

syncher.sync()
