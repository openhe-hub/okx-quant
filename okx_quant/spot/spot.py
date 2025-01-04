from typing import Dict, Union

from okx_quant.utils.request_utils import AccountStatus, RequestMethod, RequestUtils
from okx_quant.utils.config_utils import ConfigUtils, APIConfig
from okx_quant.future.future import OrderType, TradeSide, MarginType

class Spot:
    def __init__(self, api_config: APIConfig, config: dict):
        self.config: dict = config
        self.api_config: APIConfig = api_config
        self.request_utils: RequestUtils = RequestUtils(api_config, config)
        self.account_status: AccountStatus = AccountStatus.Demo if config[
            'mode']['demo'] else AccountStatus.Trade

    def trade(self, spot_id: str, side: TradeSide, order_vol: float,
                      order_type: OrderType = OrderType.MARKET,
                      order_price: float = 0.0,
                      order_id: str = "") -> Union[Dict, None]:
        params = {
            "instId": spot_id,
            "tdMode": 'cash',
            "side": side.value,
            "ordType": order_type.value,
            "sz": f"{order_vol:.10f}"
        }

        if order_id != "":
            params["clOrdId"] = order_id

        if order_type != OrderType.MARKET:
            params["px"] = f"{order_price:.10f}"

        resp = self.request_utils.request(RequestMethod.POST,
                                          "/api/v5/trade/order", body=params, auth=True,
                                          account_status=self.account_status)
        return resp




