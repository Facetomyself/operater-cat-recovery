# Recovered module: src.py.com.yun.mao.util.need.ShotUtils
# Behaviour-level reconstruction from Nuitka constants and Hex-Rays.
from __future__ import annotations

from functools import partial

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget


def disable_widget(widget) -> None:
    if widget is None:
        return
    widget.setEnabled(False)
    for child in widget.findChildren(QWidget):
        try:
            child.setEnabled(False)
        except Exception as e:
            _ = e
            continue


def enable_widget(widget) -> None:
    if widget is None:
        return
    widget.setEnabled(True)
    for child in widget.findChildren(QWidget):
        try:
            child.setEnabled(True)
        except Exception as e:
            _ = e
            continue


def handleTimeout(view) -> None:
    enable_widget(view)


def shot(view=None, millisecond: int = 1500):
    if view is None:
        return None
    disable_widget(view)
    QTimer.singleShot(
        int(millisecond),
        partial(handleTimeout, view),
    )
    return view


def changed_widget(widget, enable: bool = True) -> None:
    if widget is None:
        return
    widget.setEnabled(bool(enable))
