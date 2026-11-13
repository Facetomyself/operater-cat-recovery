# Recovered module: src.py.com.yun.mao.dclass.LoadEmployeeClass
from __future__ import annotations

import json
from pathlib import Path

from ..util.need.AllBeanDef import AiEmployeeBean, AiEmployeeListWrapper


try:
    from ..config import YunYinMaoConfig

    _base = Path(YunYinMaoConfig.abs_cache_dir)
except Exception:
    _base = Path.home() / "YunYinData"

EmployeeFile = _base / "ai_employee_data" / "employee.json"
aiEmployeeListWrapper = AiEmployeeListWrapper()


def init_default_sexy_employee() -> None:
    uid = 1
    if str(uid) not in aiEmployeeListWrapper.employeeMap:
        aiEmployeeListWrapper.employeeMap[str(uid)] = AiEmployeeBean(
            uid=uid,
            name="官方色情大师",
            role="role",
            pre_text="",
            sensitive="",
            word_min=20,
            word_max=100,
        )


def init_default_news_employee() -> None:
    uid = 2
    if str(uid) not in aiEmployeeListWrapper.employeeMap:
        aiEmployeeListWrapper.employeeMap[str(uid)] = AiEmployeeBean(
            uid=uid,
            name="官方中文记者",
            role="role",
            pre_text="",
            sensitive="",
            word_min=20,
            word_max=100,
        )


def loadEmployee() -> None:
    try:
        if EmployeeFile.exists():
            data = json.loads(EmployeeFile.read_text(encoding="utf-8"))
            for uid, value in (data.get("employeeMap") or {}).items():
                aiEmployeeListWrapper.employeeMap[str(uid)] = AiEmployeeBean(**value)
    except Exception:
        pass
    init_default_sexy_employee()
    init_default_news_employee()


def addOrUpdate(bean) -> None:
    aiEmployeeListWrapper.employeeMap[str(bean.uid)] = bean
    writeToDist()


def deleteAiEmployeeBean(uid) -> None:
    aiEmployeeListWrapper.employeeMap.pop(str(uid), None)
    writeToDist()


def getEmployeeMap() -> dict:
    return aiEmployeeListWrapper.employeeMap


def getAiEmployee(uid):
    return aiEmployeeListWrapper.employeeMap.get(str(uid))


def getAiEmployeeName(uid) -> str:
    bean = getAiEmployee(uid)
    return bean.name if bean is not None else "AI员工不存在"


def writeToDist() -> None:
    try:
        EmployeeFile.parent.mkdir(parents=True, exist_ok=True)
        EmployeeFile.write_text(
            json.dumps(
                {
                    "employeeMap": {
                        key: dict(value.__dict__)
                        for key, value in aiEmployeeListWrapper.employeeMap.items()
                    }
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
    except Exception:
        pass
