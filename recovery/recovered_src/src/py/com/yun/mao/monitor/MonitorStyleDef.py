# Recovered module: src.py.com.yun.mao.monitor.MonitorStyleDef
monitor_table_style_def = """
<style>
table { width: 100%; max-width: 100%; font-family: 'Segoe UI', Arial, sans-serif;
        border-collapse: separate; border-spacing: 4pt 2pt; color: #e0e0e0;
        table-layout: fixed; }
th, td { padding: 10pt 12pt; font-size: 10pt; border-bottom: 1px solid #5a5d60;
         text-align: left; min-width: 5%; overflow: hidden; text-overflow: ellipsis;
         box-sizing: border-box; word-wrap: break-word; }
th { background-color: #4a4d50; font-size: 12pt; font-weight: bold; white-space: nowrap;
     border-right: 10pt solid #5a5d60; }
th:last-child { border-right: none; }
tr:nth-child(even) { background-color: #44474a; }
tr:nth-child(odd) { background-color: #3c3f42; }
.item-name { color: #66b3ff; }
.total-sent { color: #33cc99; font-size: 12pt; font-weight: 600; }
</style>
<table>
<tr><th style='width:15%;'>刷新时间</th><th style='width:35%;'>条目</th>
<th style='width:12%;'>队列数量</th><th style='width:28%;'>已搬运/总数</th>
<th style='width:10%;'>合计搬运</th></tr>
"""
