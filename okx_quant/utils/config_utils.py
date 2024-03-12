import dataclasses

import toml


@dataclasses
class APIConfig:
    base_url: str = 'https://www.iihvvs.com'
    api_key: str
    secret_key: str
    passphrase: str


class ConfigUtils:
    def __init__(self, config_path: str):
        self.config: dict = toml.load(config_path)
        self.api_config = None
        self.read_config()

    def read_config(self):
        api_key: str = self.config['api_key']
        secret_key: str = self.config['secret_key']
        passphrase: str = self.config['passphrase']
        base_url: str = 'https://www.iihvvs.com'
        if 'base_url' in self.config:
            base_url = self.config['base_url']
        self.api_config = APIConfig(base_url, api_key, secret_key, passphrase)
