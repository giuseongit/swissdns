from dns_client import DNSClient
from config import StoreManager
import time
import re

challenge_hostname = "_acme-challenge"

def is_domain_or_subdomain(sld: str, to_test: str):
    domain = sld.replace(".", "\.")
    regexp = "([\d\w]\.)*{}$".format(domain)
    if re.search(regexp, to_test) is not None:
        to_test = to_test.replace(sld, "")
        if to_test == "":
            return True
        return to_test[-1] == "."
    return False

def dns_challenge(client: DNSClient, conf: StoreManager):
    certbot_domain = conf.get("CERTBOT_DOMAIN")
    personal_domain = conf.get("DNS_DOMAIN")
    # personal_domain is a sld while certbot_domain can be a subdomain
    if is_domain_or_subdomain(personal_domain, certbot_domain):
        print("uknown requested domain")
        exit(-1)
    challenge_response = conf.get("CERTBOT_VALIDATION")

    client.create_txt_record(challenge_hostname, challenge_response)
    time.sleep(1)


def dns_cleanup(client: DNSClient):
    client.delete_txt_record(challenge_hostname)