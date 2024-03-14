import enum
from typing import Dict, List, Union
from dataclasses import dataclass

from loguru import logger

from okx_quant.utils.config_utils import APIConfig
from okx_quant.utils.request_utils import RequestUtils, RequestMethod


class GridType(enum.Enum):
    SPOT = 'grid'
    FUTURE = 'contract_grid'


class OrderStatus(enum.Enum):
    LIVE = 'live'
    FILLED = 'filled'


@dataclass
class GridBotData:
    instance_name: str
    grid_type: GridType
    investment: float
    grid_num: int
    arbitrage_num: int
    grid_profit: float
    float_profit: float
    max_price: float
    min_price: float
    total_pnl: float
    # for future grid bots
    lever: int
    liq_price: float
    # order lists
    buy_lists: List[float]
    sell_lists: List[float]


class GridBot:
    def __init__(self, api_config: APIConfig, config: dict):
        self.api_config: APIConfig = api_config
        self.config: dict = config
        self.request_utils: RequestUtils = RequestUtils(api_config, config)
        self.grid_bots: Dict[str, GridBotData] = {}
        self.sync_once()

    def get_grid_order_list(self, grid_type: GridType) -> dict:
        params = {
            'algoOrdType': grid_type.value,
        }
        uri = "/api/v5/tradingBot/grid/orders-algo-pending"
        result = self.request_utils.request(
            RequestMethod.GET, uri, params=params, auth=True
        )
        return result

    def get_grid_order_details(self, grid_type: GridType, algo_id: Union[str, int]) -> dict:
        params = {
            'algoOrdType': grid_type.value,
            'algoId': algo_id,
        }
        uri = "/api/v5/tradingBot/grid/orders-algo-details"
        result = self.request_utils.request(
            RequestMethod.GET, uri, params=params, auth=True
        )
        return result

    def get_grid_sub_orders(self, grid_type: GridType, algo_id: Union[str, int],
                            order_status: OrderStatus) -> dict:
        params = {
            'algoOrdType': grid_type.value,
            'algoId': algo_id,
            'type': order_status.value,
        }
        uri = "/api/v5/tradingBot/grid/sub-orders"
        result = self.request_utils.request(
            RequestMethod.GET, uri, params=params, auth=True
        )
        return result

    def get_grid_positions(self, grid_type: GridType, algo_id: Union[str, int]) -> dict:
        params = {
            'algoOrdType': grid_type.value,
            'algoId': algo_id,
        }
        uri = "/api/v5/tradingBot/grid/positions"
        result = self.request_utils.request(
            RequestMethod.GET, uri, params=params, auth=True
        )
        return result

    def sync_once(self):
        grid_types = [GridType.SPOT, GridType.FUTURE]
        for grid_type in grid_types:
            # get order details
            grid_order_list = self.get_grid_order_list(grid_type)
            grid_order_list = grid_order_list['data']
            for grid_order in grid_order_list:
                bot_id = grid_order['algoId']
                self.grid_bots[bot_id] = GridBotData(
                    grid_order['instId'],
                    grid_type,
                    grid_order['investment'],
                    grid_order['gridNum'],
                    grid_order['arbitrageNum'],
                    grid_order['gridProfit'],
                    grid_order['floatProfit'],
                    grid_order['maxPx'],
                    grid_order['minPx'],
                    grid_order['totalPnl'],
                    grid_order['lever'],
                    grid_order['liqPx'],
                    [], []
                )

            # get order sub orders
            for bot_id in self.grid_bots.keys():
                sub_orders = self.get_grid_sub_orders(self.grid_bots[bot_id].grid_type, bot_id, OrderStatus.LIVE)
                sub_orders = sub_orders['data']
                for sub_order in sub_orders:
                    if sub_order['side'] == 'buy':
                        self.grid_bots[bot_id].buy_lists.append(sub_order['px'])
                    elif sub_order['side'] == 'sell':
                        self.grid_bots[bot_id].sell_lists.append(sub_order['px'])
