from datetime import datetime

from app.infrastructure.chan_query import ChanQuery
from app.infrastructure.model.chan import Fractal
from database import client

btc_query = ChanQuery(client, 'btc_chan', 'OKCOIN.SH')


def get_fractals(ktype, fractal_flag):
    condition = {'windCode': 'OKCOIN.SH', 'ktype': ktype, 'fractal_flag': fractal_flag}
    cur = client.btc_chan.fractal.find(condition).limit(10000)
    return [Fractal(e) for e in cur]


bi_top_fracs = get_fractals('1_1', 2)
bi_bottom_fracs = get_fractals('1_1', -2)

print(len(bi_top_fracs), len(bi_bottom_fracs))

all_bis = btc_query.bi_from('1_1', datetime.strptime('2017-01-01', '%Y-%m-%d'))
if all_bis:
    for e in all_bis:
        middle = e.chan_k_index[0] + int(len(e.chan_k_index) / 2)
