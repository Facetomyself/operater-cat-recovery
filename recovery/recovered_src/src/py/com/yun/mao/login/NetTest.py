# Recovered module: src.py.com.yun.mao.login.NetTest
# Telegram connectivity test task reconstructed from the runtime constants.
from __future__ import annotations

import asyncio

from PyQt5.QtCore import QRunnable, QThreadPool
from telethon import TelegramClient

from ..config import InnerAppIdConfig, net_config
from ..util import DirManager
from ..util.need import CommonCode, utils


class FastTelegramTestTask(QRunnable):
    def __init__(self, test_session: str, finish_call=None):
        super().__init__()
        self.test_session = test_session
        self.finish_call = finish_call

    def run(self):
        try:
            fast_test(self.test_session, self.finish_call)
        except Exception as exc:
            print("发生异常:", exc)
            if self.finish_call:
                self.finish_call(False, str(exc))


def net_test_path() -> str:
    uni_session = utils.gen_unit_name_by_ns() + ".session"
    return DirManager.get_net_test_dir() + "\\" + uni_session


async def fast_test_inner(test_session: str, finish_call=None):
    print("开始测试连接电报服务器.....")
    soft_name = CommonCode.read_soft_name()
    proxy = net_config.get_proxy_config() if net_config.enable_proxy() else None
    client = TelegramClient(
        test_session,
        InnerAppIdConfig.get_api_id(),
        InnerAppIdConfig.get_api_hash(),
        proxy=proxy,
    )
    try:
        await client.connect()
        print("恭喜你，电报服务器连接成功，" + soft_name + "网络畅通！")
        if finish_call:
            finish_call(True, soft_name)
        return True, client
    except Exception as exc:
        print("网络连接失败，请根据以下建议检查！！！！")
        print(
            "1、如果是海外用户，不需要勾选【"
            + soft_name
            + "】右上角的【是否启用代理】！"
        )
        print(
            "2、如果使用了快连VPN，因为它是全局代理模式，不需要勾选"
            "右上角的【是否启用代理】！"
        )
        print(
            "3、如果是大陆用户，或者其他VPN，请检查代理端口是否配置正确！"
            "是否勾选了【"
            + soft_name
            + "】右上角的【是否启用代理】！"
        )
        print(
            "【注意：如果确认你配置都是正确的，可以进行多次连接测试，"
            "因为网络波动也可能会导致测试失败！】"
        )
        if finish_call:
            finish_call(False, str(exc))
        return False, exc
    finally:
        try:
            await CommonCode.safe_disconnect(client)
        except Exception:
            pass
        utils.safe_del_file(test_session)
        print("网络测试完成！")


def fast_test(test_session: str | None = None, finish_call=None):
    test_session = test_session or net_test_path()
    return asyncio.run(fast_test_inner(test_session, finish_call))


def FastNetTest(finish_call=None, test_session: str = ""):
    if callable(finish_call) and not test_session:
        finish_call, test_session = finish_call, ""
    elif callable(test_session) and finish_call is None:
        finish_call, test_session = test_session, ""
    task = FastTelegramTestTask(test_session or net_test_path(), finish_call)
    QThreadPool.globalInstance().start(task)
    return task
