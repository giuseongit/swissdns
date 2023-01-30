from abc import abstractmethod
from typing import Optional, List
import json
import os

class AbstractStore(object):
    @abstractmethod
    def get(self, key: str) -> Optional[str]:
        pass

    @abstractmethod
    def set(self, key: str, value: str):
        pass

class FileStore(AbstractStore):
    def __init__(self, fpath: str):
        self.file_path = fpath

    def _use_file(self):
        f = open(self.file_path, 'r')
        data = json.load(f.read())
        f.close()
        yield data
        f = open(self.file_path, 'w')
        to_write = json.dump(data)
        f.write(to_write)
        f.close()

    def get(self, key: str) -> Optional[str]:
        with self._use_file() as data:
            return data.get(key)

    def set(self, key: str, value: str):
        with self._use_file() as data:
            data[key] = value

class EnvStore(AbstractStore):
    def get(self, key: str) -> Optional[str]:
        return os.environ.get(key)

    def set(self, key: str, value: str):
        os.environ[key] = value


class StoreManager(AbstractStore):
    def __init__(self):
        self.store: List[AbstractStore] = []

    def add_store(self, store: AbstractStore):
        self.store.append(store)

    def get(self, key: str) -> Optional[str]:
        for store in self.store:
            val = store.get(key)
            if val is not None:
                return val
        return None

    def set(self, key: str, value: str):
        for store in self.store:
            if isinstance(store, FileStore):
                store.set(key, value)
