# Recovered module: src.py.com.yun.mao.util.need.CoolUtils
# Behaviour-level reconstruction from Nuitka constants and Hex-Rays.
from __future__ import annotations

from PyQt5.QtCore import QTimer


class ButtonCooldownManager:
    def __init__(self) -> None:
        self.cooldown_status: dict[str, bool] = {}

    def reset_cooldown(self, button_name: str) -> None:
        self.cooldown_status[button_name] = False

    def handle_click(
        self,
        button,
        cooldown_time: int,
        callback,
    ) -> None:
        if button is None:
            return
        button_name = button.objectName()
        if self.cooldown_status.get(button_name, False):
            return
        self.cooldown_status[button_name] = True
        QTimer.singleShot(
            int(cooldown_time),
            lambda: self.reset_cooldown(button_name),
        )
        if callable(callback):
            callback()
