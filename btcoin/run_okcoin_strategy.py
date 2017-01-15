from apscheduler.schedulers.background import BlockingScheduler
from app.mod_strategy.bi_duan_zk import bi_duan_zk_buy, bi_duan_zk_sell
from pytz import utc

from app.mod_strategy.bi_duan import bi_duan_buy, bi_duan_sell

scheduler = BlockingScheduler()
scheduler.configure(timezone=utc)

scheduler.add_job(bi_duan_buy, trigger='interval', seconds=5)
scheduler.add_job(bi_duan_sell, trigger='interval', seconds=5)

scheduler.add_job(bi_duan_zk_buy, trigger='interval', seconds=5)
scheduler.add_job(bi_duan_zk_sell, trigger='interval', seconds=5)

scheduler.start()
