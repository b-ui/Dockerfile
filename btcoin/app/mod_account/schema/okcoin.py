from app.common import ContainerTag, VField

user_info_rsp_field = {
    'info': ContainerTag('info', skip=True, content={
        'funds': ContainerTag('funds', skip=True, content={
            'asset': ContainerTag('asset', skip=True, content={
                'net': VField('net_asset', required=True),
                'total': VField('total_asset', required=True)
            }),
            'free': ContainerTag('free', skip=True, content={
                'btc': VField('free_btc', required=True),
                'usd': VField('free_usd'),
                'cny': VField('free_cny', required=True),
                'ltc': VField('free_ltc', required=True)
            }),
            'freezed': ContainerTag('freezed', skip=True, content={
                'btc': VField('freezed_btc', required=True),
                'usd': VField('freezed_usd'),
                'ltc': VField('freezed_ltc', required=True)
            })
        })
    }),
    'result': VField('result', required=True)
}
