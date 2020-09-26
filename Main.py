from UtilAgentPac.UtilAgent import UtilAgent
from CybosAgentPac.CybosAgent import CybosAgent
from DbAgentPac.DbAgent import DbAgent
from UtilAgentPac.UtilPac import TimerUtil as Tu

# wake agent up
util_agent = UtilAgent()
cybos_agent = CybosAgent()
db_agent = DbAgent()

# do job
start_time = Tu.stamp_start_time()

db_agent.update_db_w_all_id_wo_date()
db_agent.update_db()

print(Tu.get_elapsed_time(start_time))
print("Done")

# # sample
"""
import pandas as pd
a = {'A': [1, 2, 3], 'B': ['a', 'b', 'c'], 'C': [7, 8, 9]}
df_a = pd.DataFrame(a)
b = {'A': [1, 2, 4], 'B': ['a', 'b', 'c'], 'C': [7, 8, 9]}
df_b = pd.DataFrame(b)
"""
