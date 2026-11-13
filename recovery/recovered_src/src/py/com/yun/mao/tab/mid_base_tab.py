# Recovered module: src.py.com.yun.mao.tab.mid_base_tab
# The original module exposes exactly two instance methods.  It is a small
# controller mixin: concrete tabs own the generated ``ui`` object.
from __future__ import annotations


class MidBaseTab:
    def __init__(self) -> None:
        super().__init__()

    def on_tab_show(self) -> None:
        """Lifecycle hook intentionally kept side-effect free in the base."""
        return None


__all__ = ["MidBaseTab"]
