from dns_client import DNSClient
from config import StoreManager
import time

challenge_hostname = "_acme-challenge"

def dns_challenge(client: DNSClient, conf: StoreManager):
    certbot_domain = conf.get("CERTBOT_DOMAIN")
    personal_domain = conf.get("DNS_DOMAIN")
    if certbot_domain != personal_domain:
        print("uknown requested domain")
        exit(-1)
    challenge_response = conf.get("CERTBOT_VALIDATION")

    client.create_txt_record(challenge_hostname, challenge_response)
    time.sleep(1)


def dns_cleanup(client: DNSClient):
    client.delete_txt_record(challenge_hostname)