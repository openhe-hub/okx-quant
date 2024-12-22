from typing import Union, Dict
from enum import Enum

from okx_quant.utils.request_utils import RequestMethod, RequestUtils
from okx_quant.utils.config_utils import APIConfig, ConfigUtils


class EarnOperateType(Enum):
    PURCHASE = "purchase"
    REDEMPT = "redempt"


class Earn():
    def __init__(self, api_config: APIConfig, config: dict):
        self.config: dict = config
        self.api_config: APIConfig = api_config
        self.request_utils: RequestUtils = RequestUtils(api_config, config)
    

    def get_balance(self, currency: str = 'USDT') -> Union[Dict, None]:
        params = {
            "ccy": currency,
        }

        uri = "/api/v5/finance/savings/balance"
        resp = self.request_utils.request(
            method=RequestMethod.GET,
            uri=uri, 
            params=params,
            auth=True
        )
        return resp

    def trade(self, amount: float, side: EarnOperateType,
            currency: str= 'USDT', rate: float = 0.01) -> Union[Dict, None]:
        params = {
            "ccy": currency,
            "amt": f"{amount:.10f}",
            "side": side.value,
            "rate": f"{rate:.10f}",
        }

        uri = "/api/v5/finance/savings/purchase-redempt"
        resp = self.request_utils.request(
            method=RequestMethod.POST,
            uri=uri, 
            body=params,
            auth=True
        )
        return resp
        