# Recovered module: src.py.com.yun.mao.auto.GlobalWorkingLock
# Source rebuilt from the module init constants and the qword slot mapping.
#
# The status constants are consumed as UI state values:
#   SCHEDULER_STATUS == STATUES_RUNNING -> normal icon
#   SCHEDULER_STATUS == STATUES_TIMING  -> timed-task icon
#   otherwise                           -> disabled/AIDL icon
# The names and module shape are confirmed; the concrete integer values are
# inferred from the init stores, because they are materialised from runtime
# PyLong objects instead of inline integers.
from __future__ import annotations

import threading


lock = threading.Lock()
work_doing = False

STATUES_RUNNING = 1
STATUES_TIMING = 2
STATUES_AIDL = 3

# Inferred initial state: no scheduler/task is active.
SCHEDULER_STATUS = STATUES_AIDL
