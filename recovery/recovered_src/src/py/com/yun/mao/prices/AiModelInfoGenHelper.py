# Recovered module: src.py.com.yun.mao.prices.AiModelInfoGenHelper
from __future__ import annotations

import json


def create_model_price_table(model_list_str: str) -> str:
    try:
        models = json.loads(model_list_str or "[]")
    except Exception:
        models = []
    rows = []
    for model in models if isinstance(models, list) else []:
        if not isinstance(model, dict):
            continue
        rows.append(
            '<tr><td class="model-name">'
            + str(model.get("name", "未知模型"))
            + '</td><td class="price">'
            + str(model.get("price", "-"))
            + "</td></tr>"
        )
    return (
        '<div class="container"><div class="title">模型价格表</div>'
        "<table><thead><tr><th>模型名称</th>"
        '<th style="text-align:right;">价格（美元/百万token）</th>'
        "</tr></thead><tbody>"
        + "".join(rows)
        + '</tbody></table><div class="note">100万Token ≈ 60万～80万中文汉字</div></div>'
    )
