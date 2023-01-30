#!/usr/bin/env python3

from dns_client import DNSClient
from synchronizers import DnsASynchronizer
from certbot import dns_challenge, dns_cleanup
from config import EnvStore, StoreManager
from enum import Enum

import argparse

def init_config():
    config = StoreManager()
    config.add_store(EnvStore())
    return config

class Commands(Enum):
    SYNC = "sync"
    CERTBOT  = "certbot"

    def __str__(self):
        return self.value

class CertbotActions(Enum):
    CHALLENGE = "challenge"
    CLEANUP  = "cleanup"

    def __str__(self):
        return self.value


def build_parser():
    parser = argparse.ArgumentParser(prog='swissdns')
    sub_parsers = parser.add_subparsers(dest="command", required=True, help='sub-command help')
    sync = sub_parsers.add_parser(Commands.SYNC.value, help='make one or more dns record(s) point to your public ip')

    certbot = sub_parsers.add_parser(Commands.CERTBOT.value, help='handle certbot dns challenge')
    certbot.add_argument("mode", type=CertbotActions, choices=list(CertbotActions))

    return parser.parse_args()

config = init_config()

username = config.get("DNS_REGISTRAR_USERNAME")
token = config.get("DNS_REGISTRAR_TOKEN")
domain = config.get("DNS_DOMAIN")
provider = config.get("DNS_PROVIDER")
hosts = config.get("DNS_HOST_TO_REFRESH").split(" ")

args = build_parser()
dns_client = DNSClient(provider, username, token)

if args.command == Commands.SYNC.value:
    syncher = DnsASynchronizer(dns_client, domain, hosts)
    syncher.sync()
elif args.command == Commands.CERTBOT.value:
    if args.mode == CertbotActions.CHALLENGE:
        dns_challenge(dns_client, config)
    elif args.mode == CertbotActions.CLEANUP:
        dns_cleanup(dns_client)

