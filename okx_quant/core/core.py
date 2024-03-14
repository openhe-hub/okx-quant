from okx_quant.utils.config_utils import APIConfig, ConfigUtils
from okx_quant.utils.request_utils import RequestUtils, RequestMethod


class Core:
    def __init__(self, api_config: APIConfig, config: dict):
        self.api_config: APIConfig = api_config
        self.config: dict = config
        self.request_utils: RequestUtils = RequestUtils(api_config, config)

    def get_balance(self, currency: str):
        params = {"ccy": currency}
        uri = "/api/v5/account/balance"
        result = self.request_utils.request(
            RequestMethod.GET, uri=uri, params=params, auth=True
        )
        return result
