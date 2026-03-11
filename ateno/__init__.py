from .client import AtenoClient
from .rooms import RoomsService

class Ateno:
    def __init__(self, api_key=None, secret_key=None, base_url=None):
        config = {}
        if api_key: 
            config['api_key'] = api_key
        if secret_key: 
            config['secret_key'] = secret_key
        if base_url: 
            config['base_url'] = base_url
            
        self._client = AtenoClient(**config)
        self.rooms = RoomsService(self._client)

    @property
    def usage_count(self):
        return self._client.get_total_requests()