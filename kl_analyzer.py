from abupy import ABuSymbolPd
from abupy.CoreBu.ABuEnv import EMarketDataFetchMode
import seaborn as sn
import numpy as np
import matplotlib.pyplot as plt

#回测从本地池获得数据
g_data_fetch_mode = EMarketDataFetchMode.E_DATA_FETCH_FORCE_LOCAL

df = ABuSymbolPd.make_kl_df('sz000022', n_folds=1)
df.tail()

sn.regplot(x=np.arange(0, df.shape[0]), y=df.close.values)
plt.show()

# plt.plot(scw_df.close.index, scw_df.close.values, c='r')
plt.plot(df.close,c='g')
plt.show()


"""
sb.regplot(x=np.arange(0, scw_df.shape[0]),y=scw_df.close.values)
plt.show()

scw_part_df = scw_df[-30:]
import matplotlib.finance as mpf
fig, ax = plt.subplots(figsize=(14,7))
qutotes = []
for index, (d,o,c,h,l) in enumerate(
    zip(scw_part_df.index, scw_part_df.open, scw_part_df.close,scw_part_df.high,scw_part_df.low)):
    d = mpf.date2num(d)
    val = (d,o,c,h,l)
    qutotes.append(val)
mpf.candlestick_ochl(ax,qutotes,width=0.6,colorup="red",colordown="green")
ax.autoscale_view()
ax.xaxis_date()
"""