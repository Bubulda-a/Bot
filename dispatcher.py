from aiogram import Dispatcher

import routers as r


def get_dispatcher():
    routers = [
        r.router_common,
        r.router_profile,
    ]

    dp = Dispatcher()
    for module in routers:
        dp.include_router(module.router)
    return dp
