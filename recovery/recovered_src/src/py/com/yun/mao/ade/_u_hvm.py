# Recovered module: src.py.com.yun.mao.ade._u_hvm
from __future__ import annotations

from ._u_common import encrypt_log


def iv_sk(result_list, header):
    return encrypt_log(result_list, header)
