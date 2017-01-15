from common.vdict_field_mapping import VDictSchema

from app.common.log_util import logger
from app.mod_account.schema.okcoin import user_info_rsp_field
from app.mod_btcoin import OKCoinSpot


class OKCoinAccount(object):
    OKCOIN_HOST = 'www.okcoin.cn'

    def __init__(self, api_key, secret_key):
        self.okcoin_spot = OKCoinSpot(self.OKCOIN_HOST, api_key, secret_key)
        self.free_btc = 0
        self.free_cny = 0

    def sync(self):
        account_info = self.okcoin_spot.userinfo()
        if account_info.get('result'):
            res, errs = VDictSchema(user_info_rsp_field).dict_mapping(account_info)
            logger.info(errs)
            self.free_btc = res['free_btc']
            self.free_cny = res['free_cny']

