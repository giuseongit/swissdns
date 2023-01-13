from enum import Enum

from lexicon.client import Client
from lexicon.config import ConfigResolver

class RecordType(Enum):
    A    = "A"
    AAAA = "AAAA"
    TXT  = "TXT"

class ActionType(Enum):
    CREATE = "create"
    LIST   = "list"
    UPDATE = "update"
    DELETE = "delete"

class DNSClient(object):
    def __init__(self, provider: str, username: str, token: str):
        self.provider = provider
        self.username = username
        self.token = token

    def _prepare_action(self, action_type: ActionType, dtype: RecordType, domain: str, name: str=None, content: str=None):
        action = {
            self.provider: {
                "auth_username": self.username,
                "auth_token"   : self.token,
            },
            "provider_name" :  self.provider,
            "action":          action_type.value,
            "domain":          domain,
            "type":            dtype.value,
        }
        if action_type in (ActionType.CREATE, ActionType.UPDATE, ActionType.DELETE) and name is not None:
            action["name"] = name
        if action_type in (ActionType.CREATE, ActionType.UPDATE) and content is not None:
            action["content"] = content
            action["ttl"] = 300
        return action

    def _execute_dns_api_call(self, action):
        config = ConfigResolver().with_env().with_dict(action)
        return Client(config).execute()

    # "A" records
    def list_a_records(self, domain: str):
        action = self._prepare_action(ActionType.LIST, RecordType.A, domain)
        return self._execute_dns_api_call(action)

    def create_a_record(self, domain: str, name: str, content: str):
        action = self._prepare_action(ActionType.CREATE, RecordType.A, domain, name=name, content=content)
        return self._execute_dns_api_call(action)

    def update_a_record(self, domain: str, name: str, content: str):
        action = self._prepare_action(ActionType.UPDATE, RecordType.A, domain, name=name, content=content)
        return self._execute_dns_api_call(action)

    def delete_a_record(self, domain: str, name: str):
        action = self._prepare_action(ActionType.DELETE, RecordType.A, domain, name=name)
        return self._execute_dns_api_call(action)

    # "AAAA" records
    def list_aaaa_records(self, domain: str):
        action = self._prepare_action(ActionType.LIST, RecordType.AAAA, domain)
        return self._execute_dns_api_call(action)

    def create_aaaa_record(self, domain: str, name: str, content: str):
        action = self._prepare_action(ActionType.CREATE, RecordType.AAAA, domain, name=name, content=content)
        return self._execute_dns_api_call(action)

    def update_aaaa_record(self, domain: str, name: str, content: str):
        action = self._prepare_action(ActionType.UPDATE, RecordType.AAAA, domain, name=name, content=content)
        return self._execute_dns_api_call(action)

    def delete_aaaa_record(self, domain: str, name: str):
        action = self._prepare_action(ActionType.DELETE, RecordType.AAAA, domain, name=name)
        return self._execute_dns_api_call(action)

    # "TXT" records
    def list_txt_records(self, domain: str):
        action = self._prepare_action(ActionType.LIST, RecordType.TXT, domain)
        return self._execute_dns_api_call(action)

    def create_txt_record(self, domain: str, name: str, content: str):
        action = self._prepare_action(ActionType.CREATE, RecordType.TXT, domain, name=name, content=content)
        return self._execute_dns_api_call(action)

    def update_txt_record(self, domain: str, name: str, content: str):
        action = self._prepare_action(ActionType.UPDATE, RecordType.TXT, domain, name=name, content=content)
        return self._execute_dns_api_call(action)

    def delete_txt_record(self, domain: str, name: str):
        action = self._prepare_action(ActionType.DELETE, RecordType.TXT, domain, name=name)
        return self._execute_dns_api_call(action)
