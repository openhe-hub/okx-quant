from datetime import datetime, timedelta
import time
import pandas as pd

from okx_quant.utils.time_utils import str_to_timestamp_ms, timestamp_ms_to_str
from okx_quant.utils.request_utils import RequestUtils, RequestMethod
from okx_quant.utils.config_utils import APIConfig



class Kline:
    def __init__(self, api_config: APIConfig, config: dict):
        self.config: dict = config
        self.api_config: APIConfig = api_config
        self.request_utils: RequestUtils = RequestUtils(api_config, config)

    def get_history_kline(self, symbol: str, begin: str, end: str, period: str='1D',
                        limit: int=100, time_seg: float = 0.1):
        all_klines = []
        begin_dt = datetime.strptime(begin, "%Y-%m-%d")
        end_dt = datetime.strptime(end, "%Y-%m-%d")
        
        while end_dt >= begin_dt:
            diff = abs((end_dt - begin_dt).days)
            params = {
                "instId": symbol,
                "before": str_to_timestamp_ms(begin_dt.strftime("%Y-%m-%d")),
                "after": str_to_timestamp_ms((begin_dt + timedelta(days=min(diff, limit))).strftime("%Y-%m-%d")),
                "bar": period,
                "limit": limit,
            }
            
            try:
                result = self.request_utils.request(RequestMethod.GET, "/api/v5/market/history-candles", params=params, auth=True)
                klines = result['data']
                all_klines.extend(klines)
                
                begin_dt += timedelta(days=limit-1)
                time.sleep(time_seg)
                
            except Exception as e:
                print(f"Error fetching data: {e}")
                break
        
        df = None
        try:
            if all_klines:
                cols = ['timestamp', 'open', 'high', 'low', 'close', 'vol', 'volCcy', 'volCcyQuote', 'confirm']
                kline_dict = {col: [] for col in cols}
                
                for kline in all_klines:
                    kline[0] = timestamp_ms_to_str(int(kline[0]))
                    for idx, col in enumerate(cols):
                        kline_dict[col].append(kline[idx] if col == 'timestamp' else float(kline[idx]))
                
                df = pd.DataFrame(kline_dict)
                df = df.sort_values('timestamp').drop_duplicates(subset=['timestamp']).reset_index(drop=True)
                
        except Exception as e:
            print(f"Error processing data: {e}")
        
        return df
