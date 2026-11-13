# Recovered module: src.py.com.yun.mao.fea._sq_jqm
# Behavioural reconstruction from runtime metadata and Hex-Rays output.
from __future__ import annotations

import json
import time
from pathlib import Path


YOU_KE = 0
HUI_YUAN = 1
FREEZE = 2
CARD_GEEK = 2
EXP_EIGHT = 3
HAS_NO_EXP = 0
HAS_EXP = 1
NOT_EXIT = -1
ABILITY_DISABLE = 0
ABILITY_ENABLE = 1
AI_EMPLOYEE_API_KEY = "new_ai_employee_api_key"
AI_EMPLOYEE_GROUP = "ai_employee_group"
CODE_FILE_NAME = ".code"
LEGACY_BEAN_NAME = "uni_code_yun_yin_mao_bean"
LEGACY_ACCOUNT_INFO_KEY = b"Ek1Y4ElRdHuP8npyojkmJETrBkCj6Y44AnEWDQLNcTk="


class SqJqm:
    """Account/licence state returned by the remote report endpoint."""

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

    def open_premium(self) -> bool:
        return bool(self.openPremium)

    def get_price_config(self) -> dict:
        try:
            return json.loads(self.priceConfig or "{}")
        except (TypeError, ValueError):
            return {}

    def geneDisplay(self) -> str:
        if self.grade == HUI_YUAN:
            return f"机器码：{self.ucode}，你是会员身份。"
        if self.grade == EXP_EIGHT:
            return f"机器码：{self.ucode}，你是体验会员身份。"
        return f"机器码：{self.ucode}，你是游客身份，功能不可用！"

    def is_exp_eight(self) -> bool:
        return self.grade == EXP_EIGHT

    def has_exp_permission(self) -> bool:
        return bool(self.hasExperi) or self.grade in (HUI_YUAN, EXP_EIGHT)

    def genHuiyuanGrade(self) -> str:
        return {
            HUI_YUAN: "你好初级卡会员",
            EXP_EIGHT: "体验会员",
            FREEZE: "会员已冻结",
        }.get(self.grade, "游客")

    def gen_grade_card_str(self) -> str:
        return {
            YOU_KE: "游客",
            HUI_YUAN: "会员",
            FREEZE: "冻结",
            EXP_EIGHT: "体验会员",
        }.get(self.grade, "游客")

    def is_multi_permission(self) -> bool:
        return bool(self.mul)

    def get_cloud_bot(self) -> str:
        return self.cloudBot

    def get_experi_duration_hours(self) -> int:
        return self.experiDuration

    def has_ai_ability(self) -> bool:
        return self.aiAbility == ABILITY_ENABLE

    def has_bot_ability(self) -> bool:
        return self.botAbility == ABILITY_ENABLE

    def has_ai_ability_but_no_key(self) -> bool:
        return self.has_ai_ability() and not bool(self.apiKey)

    def gen_ka_info(self) -> str:
        return "企业版" if self.is_multi_permission() else "个人版"

    def zh_ye_xx(self) -> dict:
        return dict(self.__dict__)


class SqJqmEnc:
    @classmethod
    def default(cls, obj: object) -> object:
        if hasattr(obj, "__dict__"):
            return dict(obj.__dict__)
        return obj


current_account_info = SqJqm()


def has_ai_ability_but_no_key() -> bool:
    return current_account_info.has_ai_ability_but_no_key()
current_account_time = time.time()


def zh_bc_xs(value: object) -> str:
    return "" if value is None else str(value)


def zh_code_pth() -> Path:
    return (
        Path.home()
        / "AppData"
        / "Roaming"
        / "Microsofteis"
        / "lang"
        / "union_code_release"
        / "union_code"
        / CODE_FILE_NAME
    )


def zh_info_pth() -> Path:
    return zh_code_pth().with_suffix(".info")


def zh_old_pth() -> Path:
    return zh_code_pth().with_name(CODE_FILE_NAME + ".old")


def _union_code_dir() -> Path:
    return zh_code_pth().parent


def _sec(name: str) -> str:
    try:
        from ..link._fds_jm import sec

        return sec(name)
    except Exception:
        return name


def _static_cipher():
    """Return the TwCtx Fernet instance used for the union-code file."""
    from ..link._tw_ctx import TwCtx

    if not TwCtx.tw_jm_ok():
        raise RuntimeError(_sec("jqm_pz_no_ready_16"))
    return TwCtx._static_cipher_instance()


def _zh_rd_code(path: Path | None = None):
    """Read and decrypt the union-code payload.

    The returned tuple is ``(ucode, mul)``.  The decoded JSON carries only
    ``ucode`` and optional ``muli``; the caller updates
    ``current_account_info``.
    """
    code_path = Path(path) if path is not None else zh_code_pth()
    if not code_path.exists():
        return "", False
    try:
        raw = code_path.read_bytes()
        dic = json.loads(_static_cipher().decrypt(raw).decode("utf-8"))
        ucode = str(dic.get("ucode", "") or "")
        mul = bool(dic.get("muli", False)) if "muli" in dic else False
        return ucode, mul
    except Exception as exc:
        print(_sec("jqm_sh_01"), exc)
        return "", False


def _zh_bc_uc(ucode: str, mul: bool = False) -> None:
    """Encrypt and write the union-code payload."""
    try:
        muli = CARD_GEEK if mul else 0
        payload = json.dumps(
            {"ucode": str(ucode or ""), "muli": muli},
            ensure_ascii=False,
        ).encode("utf-8")
        encrypted = _static_cipher().encrypt(payload)
        code_path = zh_code_pth()
        code_path.parent.mkdir(parents=True, exist_ok=True)
        code_path.write_bytes(encrypted)
    except Exception as exc:
        print(_sec("jqm_sh_01"), exc)


def _read_ucode_from_legacy_bean() -> str:
    """Read the legacy ``.code.old`` payload and return its ucode."""
    path = zh_old_pth()
    if not path.exists():
        return ""
    try:
        raw = path.read_bytes()
        plain = _static_cipher().decrypt(raw).decode("utf-8")
        obj = json.loads(plain)
        ucode = str(obj.get("ucode", "") or "")
        mul = bool(obj.get("muli", False))
        current_account_info.ucode = ucode
        current_account_info.mul = mul
        return ucode
    except Exception as exc:
        print(_sec("jqm_sh_02"), exc)
        return ""


def _migrate_legacy_bean_if_needed() -> None:
    """Migrate the legacy ``.code.old`` file to the current ``.code`` file."""
    try:
        ucode = _read_ucode_from_legacy_bean()
        code_exists = zh_code_pth().exists()
        legacy_exists = zh_old_pth().exists()
        if ucode and not code_exists and legacy_exists:
            _zh_bc_uc(ucode, current_account_info.mul)
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(_sec("jqm_load_tpl_15").format(now=now))
    except Exception as exc:
        try:
            from ..util import TracePrinterHelper

            TracePrinterHelper.print_trace(_sec("jqm_sh_03"), exc)
        except Exception:
            print(_sec("jqm_sh_03"), exc)


def zh_rd_code() -> str:
    return _zh_rd_code()[0]


def zh_zw_uc(value: str) -> str:
    return value


def zh_jz_xx() -> None:
    _migrate_legacy_bean_if_needed()
    ucode, mul = _zh_rd_code()
    if ucode:
        current_account_info.ucode = ucode
        current_account_info.mul = mul
    return None


def zh_sc_wj() -> None:
    _zh_bc_uc(current_account_info.ucode, current_account_info.mul)


def dic_to_AiModelObj(value: dict) -> dict:
    return value


def get_ai_default_api_key() -> str:
    return current_account_info.apiKey


def get_ai_model_list() -> list:
    try:
        return json.loads(current_account_info.modelList or "[]")
    except (TypeError, ValueError):
        return []


def get_ai_model_obj_list() -> list:
    return [dic_to_AiModelObj(item) for item in get_ai_model_list()]


def get_default_ai_model() -> dict | None:
    models = get_ai_model_list()
    return models[0] if models else None
