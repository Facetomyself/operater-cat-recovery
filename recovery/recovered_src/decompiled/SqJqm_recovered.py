"""Reconstructed SqJqm model.

Evidence:
- runtime module dictionary of src.py.com.yun.mao.fea._sq_jqm
- Hex-Rays pseudocode of has_ai_ability / has_bot_ability /
  is_multi_permission / gen_grade_card_str / gen_ka_info
- guest-state observations in the pre-shutdown runtime dump

The class body is a reconstruction, not original source.
"""

from __future__ import annotations

import json


YOU_KE = 0
HUI_YUAN = 1
FREEZE = 2
CARD_GEEK = 2
EXP_EIGHT = 3


class SqJqm:
    # exact: fields observed in current_account_info.__dict__
    def __init__(
        self,
        ucode: str = "",
        status: int = 0,
        grade: int = 0,
        limit: int = 0,
        descs: str = "",
        hours: int = 0,
        startTime: str = "",
        endTime: str = "",
        expire: bool = True,
        hasExperi: int = 0,
        sendAtName: str = "",
        keFu: str = "",
        cloudBot: str = "",
        botAbility: int = 0,
        aiAbility: int = 0,
        experiDuration: int = 1,
        openPremium: int = 1,
        priceConfig: str = "{}",
        maoContacts: str = "",
        remainingSec: int = 0,
        apiKey: str = "",
        modelList: str = "[]",
        mul: bool = False,
    ) -> None:
        self.ucode = ucode
        self.status = status
        self.grade = grade
        self.limit = limit
        self.descs = descs
        self.hours = hours
        self.startTime = startTime
        self.endTime = endTime
        self.expire = expire
        self.hasExperi = hasExperi
        self.sendAtName = sendAtName
        self.keFu = keFu
        self.cloudBot = cloudBot
        self.botAbility = botAbility
        self.aiAbility = aiAbility
        self.experiDuration = experiDuration
        self.openPremium = openPremium
        self.priceConfig = priceConfig
        self.maoContacts = maoContacts
        self.remainingSec = remainingSec
        self.apiKey = apiKey
        self.modelList = modelList
        self.mul = mul

    # high: guest observation -> True because openPremium=1
    def open_premium(self) -> bool:
        return bool(self.openPremium)

    # high: priceConfig is a JSON string in the captured guest state
    def get_price_config(self) -> dict:
        try:
            return json.loads(self.priceConfig or "{}")
        except (TypeError, ValueError):
            return {}

    # inferred: exact formatting is not recovered yet
    def geneDisplay(self) -> str:
        if self.grade == HUI_YUAN:
            return f"机器码：{self.ucode}，你是会员身份。"
        if self.grade == EXP_EIGHT:
            return f"机器码：{self.ucode}，你是体验会员身份。"
        return f"机器码：{self.ucode}，你是游客身份，功能不可用！"

    # high: guest grade=0 -> False; EXP_EIGHT=3 constant
    def is_exp_eight(self) -> bool:
        return self.grade == EXP_EIGHT

    # TODO: exact condition not recovered
    def has_exp_permission(self) -> bool:
        return bool(self.hasExperi) or self.grade in (HUI_YUAN, EXP_EIGHT)

    # inferred: grade -> display label
    def genHuiyuanGrade(self) -> str:
        if self.grade == HUI_YUAN:
            return "你好初级卡会员"
        if self.grade == EXP_EIGHT:
            return "体验会员"
        if self.grade == FREEZE:
            return "会员已冻结"
        return "游客"

    # high: guest grade=0 -> "游客"; member label inferred from constants
    def gen_grade_card_str(self) -> str:
        return {
            YOU_KE: "游客",
            HUI_YUAN: "会员",
            FREEZE: "冻结",
            EXP_EIGHT: "体验会员",
        }.get(self.grade, "游客")

    # high: guest mul=False; member multi flag comes from server field mul
    def is_multi_permission(self) -> bool:
        return bool(self.mul)

    # exact: field observed
    def get_cloud_bot(self) -> str:
        return self.cloudBot

    # exact: field observed
    def get_experi_duration_hours(self) -> int:
        return self.experiDuration

    # high: ABILITY_ENABLE=1 / ABILITY_DISABLE=0
    def has_ai_ability(self) -> bool:
        return self.aiAbility == 1

    # high: ABILITY_ENABLE=1 / ABILITY_DISABLE=0
    def has_bot_ability(self) -> bool:
        return self.botAbility == 1

    # high: guest output was "个人版"; multi permission switches to enterprise
    def gen_ka_info(self) -> str:
        return "企业版" if self.is_multi_permission() else "个人版"
