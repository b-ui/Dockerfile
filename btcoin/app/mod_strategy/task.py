# coding: utf-8
from flask_apscheduler import APScheduler

from app.mod_strategy.bi_duan import bi_duan_buy, bi_duan_sell
from app.mod_strategy.bi_duan_zk import bi_duan_zk_buy, bi_duan_zk_sell
from app.mod_strategy.bi_duan_1_1 import bi_duan_buy_1_1, bi_duan_sell_1_1

scheduler = APScheduler()

# scheduler.add_job('bi_duan_buy', bi_duan_buy, trigger='interval', seconds=5)
# scheduler.add_job('bi_duan_sell', bi_duan_sell, trigger='interval', seconds=5)
#
# scheduler.add_job('bi_duan_zk_buy', bi_duan_zk_buy, trigger='interval', seconds=5)
# scheduler.add_job('bi_duan_zk_sell', bi_duan_zk_sell, trigger='interval', seconds=5)

scheduler.add_job('bi_duan_zd_1.1', bi_duan_buy_1_1, trigger='interval', seconds=5, name=u'笔段做多')
scheduler.add_job('bi_duan_zk_1.1', bi_duan_sell_1_1, trigger='interval', seconds=5, name=u'笔段做空')