# Recovered module: src.py.com.yun.mao.util.XAIKeyValidator
# QThread-backed xAI key smoke test.  Network work happens only in run().
from __future__ import annotations

import time

try:
    from PyQt5.QtCore import QThread, pyqtSignal
except Exception:
    class QThread:
        def __init__(self, *args, **kwargs):
            pass

        def start(self):
            self.run()

    def pyqtSignal(*args, **kwargs):
        class _Signal:
            def connect(self, *a, **kw):
                return None

            def emit(self, *a, **kw):
                return None

        return _Signal()


class XAIKeyValidator(QThread):
    finished = pyqtSignal(bool, str)

    def __init__(self, api_key: str, parent=None):
        super().__init__(parent)
        self.api_key = api_key.strip()

    def run(self) -> None:
        if not self.api_key.startswith("xai-"):
            self.finished.emit(
                False,
                "API Key 格式错误，必须以 'xai-' 开头",
            )
            return
        try:
            from openai import OpenAI, OpenAIError
        except Exception as exc:
            self.finished.emit(False, f"网络或未知错误：{exc}")
            return

        start_time = time.time()
        try:
            client = OpenAI(
                api_key=self.api_key,
                base_url="https://api.x.ai/v1",
                timeout=10.0,
            )
            client.chat.completions.create(
                model="grok-3",
                messages=[{"role": "user", "content": "ok"}],
                max_tokens=3,
                temperature=0.0,
            )
            elapsed = round(time.time() - start_time, 2)
            self.finished.emit(
                True,
                f"API Key 有效 ✓ （耗时 {elapsed} 秒，可正常生成文本）",
            )
        except OpenAIError as exc:
            error_str = str(exc).lower()
            if "401" in error_str or "invalid api key" in error_str or "unauthorized" in error_str:
                msg = "API Key 无效或已过期（401 Unauthorized）"
            elif "403" in error_str:
                msg = (
                    "API Key 没有访问权限（403 Forbidden）\n\n"
                    "可能原因：\n"
                    "1. 该 Key 未被授予对应模型权限\n"
                    "2. 账号 Credits / 免费额度已用完\n"
                    "3. Key 被禁用或团队权限受限\n\n"
                    "请前往 https://console.x.ai/ 重新创建一个新 API Key，\n"
                    "并确保勾选了你要使用的模型权限。"
                )
            elif "429" in error_str:
                msg = "请求太频繁（429 Rate Limit），请稍后重试"
            else:
                msg = f"校验失败：{str(exc)[:140]}"
            self.finished.emit(False, msg)
        except Exception as exc:
            self.finished.emit(
                False,
                f"网络或未知错误：{str(exc)[:120]}",
            )
