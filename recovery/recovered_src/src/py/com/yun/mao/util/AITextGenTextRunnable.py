# Recovered module: src.py.com.yun.mao.util.AITextGenTextRunnable
from __future__ import annotations

try:
    from PyQt5.QtCore import QRunnable
except Exception:
    class QRunnable:
        pass

from src.py.com.yun.mao.ai.AiTextGenFlow import AiTextGenFlow
from src.py.com.yun.mao.ai.AiTextGenStatus import AiTextGenStatus
from src.py.com.yun.mao.util.need.AllBeanDef import AiEmployeeBean


class AITextGenTextRunnable(QRunnable):
    def __init__(
        self,
        api_key: str,
        source: str,
        employee: AiEmployeeBean | None = None,
        finish_call=None,
        result_print: bool = False,
    ):
        super().__init__()
        self.api_key = api_key
        self.source = source
        self.employee = employee
        self.finish_call = finish_call
        self.result_print = bool(result_print)

    def run(self) -> None:
        try:
            status, tart = AiTextGenFlow.generate_text(
                source=self.source,
                employee=self.employee,
                api_key=self.api_key,
                production=True,
                result_print=self.result_print,
            )
            if callable(self.finish_call):
                self.finish_call(status, tart)
            if status is AiTextGenStatus.FAILED:
                print("AI文案生成失败")
        except Exception as exc:
            print("发生异常:", exc)
            if callable(self.finish_call):
                self.finish_call(AiTextGenStatus.FAILED, self.source)
