# Recovered module: src.py.com.yun.mao.prices.CreateOrderResponseClass
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class Order:
    aiAbility: int = 0
    hours: int = 0
    amount: float = 0.0
    onumber: str = ""
    otype: str = ""
    odesc: str = ""
    address: str = ""
    createTime: str = ""
    hasRecharge: bool = False
    grade: int = 0
    id: int = 0
    ucode: str = ""
    hasPaid: bool = False
    botAbility: int = 0


@dataclass
class CreateOrderResponse:
    msg: str = ""
    code: Any = None
    isError: bool = False
    data: Any = None
    timestamp: Any = None
    isSuccess: bool = False
    path: str = ""
    extra: Any = None
