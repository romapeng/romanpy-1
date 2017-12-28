
from abupy import env
from abupy import abu


# 本地数据更新
# 用百度数据源，A股全市场更新
env.g_market_source = env.EMarketSourceType.E_MARKET_SOURCE_bd
env.g_data_cache_type = env.EDataCacheType.E_DATA_CACHE_CSV
# abu.run_kl_update(n_folds=1, market=env.EMarketTargetType.E_MARKET_TARGET_CN, n_jobs=10)
abu.run_kl_update(start='2016-08-08', end='2016-12-08', market=env.EMarketTargetType.E_MARKET_TARGET_CN)



