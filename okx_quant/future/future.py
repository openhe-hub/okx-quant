import enum
from typing import Dict, Union

from okx_quant.utils.request_utils import AccountStatus, RequestMethod, RequestUtils
from okx_quant.utils.config_utils import ConfigUtils, APIConfig


class MarginType(enum.Enum):
    CROSS = "cross"
    ISOLATED = "isolated"


class OrderType(enum.Enum):
    LIMIT = "limit"
    MARKET = "market"
    POST_ONLY = "post_only"  # only for maker order
    # advanced type, see official doc
    FOK = "fok"
    IOC = "ioc"
    OPTIMAL_LIMIT_IOC = "optimal_limit_ioc"
    MMP = "mmp"
    MMP_AND_POST_ONLY = "mmp_and_post_only"


class TradeSide(enum.Enum):
    # buy & sell in long_short_mode
    BUY = "buy"
    SELL = "sell"
    # long & short in net_mode
    LONG = "long"
    SHORT = "short"


class MarginAdjustType(enum.Enum):
    ADD = "add"
    REDUCE = "reduce"


class Future:
    def __init__(self, api_config: APIConfig, config: dict):
        self.config: dict = config
        self.api_config: APIConfig = api_config
        self.request_utils: RequestUtils = RequestUtils(api_config, config)
        self.account_status: AccountStatus = AccountStatus.Demo if config[
            'mode']['demo'] else AccountStatus.Trade

    def open_position(self, future_id: str, side: TradeSide, order_vol: float,
                      order_type: OrderType = OrderType.MARKET,
                      margin_type: MarginType = MarginType.ISOLATED,
                      order_price: float = 0.0,
                      order_id: str = "", lever: float = -1) -> Union[Dict, None]:
        params = {
            "instId": future_id,
            "tdMode": margin_type.value,
            "side": side.value,
            "ordType": order_type.value,
            "sz": f"{order_vol:.10f}"
        }

        if order_id != "":
            params["clOrdId"] = order_id

        if order_type != OrderType.MARKET:
            params["px"] = f"{order_price:.10f}"

        if lever != -1 and lever >= 0:
            self.set_future_lever(future_id, lever, margin_type)

        resp = self.request_utils.request(RequestMethod.POST,
                                          "/api/v5/trade/order", body=params, auth=True,
                                          account_status=self.account_status)
        return resp

    def query_position(self, future_id: str) -> Union[Dict, None]:
        params = {
            "instId": future_id
        }

        resp = self.request_utils.request(
            RequestMethod.GET, "/api/v5/account/positions", params=params, auth=True, account_status=self.account_status)
        return resp

    def has_position(self, future_id: str) -> bool:
        resp = self.query_position(future_id)
        px_str = resp['data'][0]['avgPx']
        px = float(px_str) if px_str != "" else 0.0
        return px > 0.0

    def close_position(self, future_id: str,
                       margin_type: MarginType = MarginType.ISOLATED,
                       order_id: str = "") -> Union[Dict, None]:
        params = {
            "instId": future_id,
            "mgnMode": margin_type.value,
        }

        if order_id != "":
            params["clOrdId"] = order_id

        resp = self.request_utils.request(RequestMethod.POST, "/api/v5/trade/close-position",
                                          body=params, auth=True, account_status=self.account_status)
        return resp

    def set_future_lever(self, future_id: str, lever: float,
                         margin_type: MarginType = MarginType.ISOLATED) -> Union[Dict, None]:
        params = {
            "instId": future_id,
            "lever": f"{lever:.2f}",
            "mgnMode": margin_type.value,
        }

        resp = self.request_utils.request(
            RequestMethod.POST, "/api/v5/account/set-leverage", body=params, auth=True, account_status=self.account_status)
        return resp

    def adjust_margin(self, future_id: str, adjust_type: MarginAdjustType,
                      amount: float, ccy: str = 'USDT') -> Union[Dict, None]:
        params = {
            "instId": future_id,
            "posSide": "net",  # pos side should always be net under default mode
            "type": adjust_type.value,
            "amt": f"{amount:.10f}",
        }

        if ccy != 'USDT':
            params['ccy'] = ccy

        resp = self.request_utils.request(
            RequestMethod.POST, "/api/v5/account/position/margin-balance", body=params, auth=True, account_status=self.account_status)
        return resp

    def get_max_trade_size(self, future_id: str, lever: float = -1, order_price: float = -1,
                        margin_type: MarginType = MarginType.ISOLATED) -> Union[Dict, None]:
        params = {
            "instId": future_id,
            "tdMode": margin_type.value,
        }

        if order_price != -1:
            params["px"] = f"{order_price: 10f}"

        if lever != -1:
            self.set_future_lever(future_id, lever)

        resp = self.request_utils.request(
            RequestMethod.GET, "/api/v5/account/max-size",
            params=params,
            auth=True,
            account_status=self.account_status
        )
        return resp

    def get_max_margin(self, future_id: str,
                order_price: float = -1,
                margin_type: MarginType = MarginType.ISOLATED) -> Union[Dict, None]:
        params = {
            "instId": future_id,
            "tdMode": margin_type.value,
        }

        if order_price != -1:
            params["px"] = f"{order_price: 10f}"
        
        resp = self.request_utils.request(
            RequestMethod.GET, "/api/v5/account/max-avail-size",
            params=params,
            auth=True,
            account_status=self.account_status
        )
        return resp