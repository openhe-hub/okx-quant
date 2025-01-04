from typing import Union, Dict
from enum import Enum

from okx_quant.utils.config_utils import APIConfig, ConfigUtils
from okx_quant.utils.request_utils import RequestUtils, RequestMethod, AccountStatus

class TransferType(Enum):
    NORMAL = "0"
    MAIN_TO_SUB = "1"
    SUB_TO_MAIN = "2"     # for main api
    SUB_TO_MAIN_2 = "3"   # for sub api
    SUB_TO_SUB = "4"      # for sub api

class AccountType(Enum):
    FUNDING_ACC = "6"
    TRADING_ACC = "18"


class Account:
    def __init__(self, api_config: APIConfig, config: dict):
        self.api_config: APIConfig = api_config
        self.config: dict = config
        self.request_utils: RequestUtils = RequestUtils(api_config, config)
        self.account_status: AccountStatus = AccountStatus.Demo if config[
            'mode']['demo'] else AccountStatus.Trade

    def get_balance(self, currency: str) -> Union[Dict, None]:
        params = {"ccy": currency}
        uri = "/api/v5/account/balance"
        result = self.request_utils.request(
            RequestMethod.GET, uri=uri, params=params, auth=True,
            account_status=self.account_status
        )
        return result
    
    def get_assets(self, currency: str) -> Union[Dict, None]:
        params = {
            "ccy": currency,
        }
        uri = "/api/v5/asset/asset-valuation"
        result = self.request_utils.request(
            RequestMethod.GET, uri=uri, params=params, auth=True,
            account_status=self.account_status
        )
        return result
    
    def transfer(self, amount: float,
                from_account: AccountType, to_account: AccountType, 
                currency: str = 'USDT',
                transfer_type: TransferType = TransferType.NORMAL, 
                sub_account: str = '') -> Union[Dict, None]:
        params = {
            "type": transfer_type.value,
            "ccy": currency,
            "amt": f"{amount:.10f}",
            "from": from_account.value,
            "to": to_account.value,
        }

        if type in [TransferType.MAIN_TO_SUB, TransferType.SUB_TO_MAIN, TransferType.SUB_TO_SUB]:
            params["subAcct"] = sub_account
        
        uri = "/api/v5/asset/transfer"
        result = self.request_utils.request(
            RequestMethod.POST, uri=uri, body=params, auth=True,
            account_status=self.account_status
        )
        return result
