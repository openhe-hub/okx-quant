from dataclasses import dataclass

import toml


@dataclass
class APIConfig:
    api_key: str
    secret_key: str
    passphrase: str
    base_url: str = 'https://www.dojqutmbiuuo.com'


class ConfigUtils:
    def __init__(self, config_path: str):
        self.config: dict = toml.load(config_path)
        self.api_config: APIConfig = self.read_config()

    def read_config(self) -> APIConfig:
        api_key: str = self.config['api']['api_key']
        secret_key: str = self.config['api']['secret_key']
        passphrase: str = self.config['api']['passphrase']
        base_url: str = 'https://www.dojqutmbiuuo.com'
        if 'base_url' in self.config:
            base_url = self.config['base_url']
        return APIConfig(api_key, secret_key, passphrase, base_url)
