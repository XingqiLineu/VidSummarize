from openai import OpenAI
import os
import pandas as pd

# 设置API密钥
client = OpenAI(api_key="")

# 获取微调作业信息
job_id = ""
fine_tune_job = client.fine_tuning.jobs.retrieve(job_id)

# 获取事件数据
events = client.fine_tuning.jobs.list_events(fine_tuning_job_id=job_id, limit=100)

# 创建数据框
data = []
for event in events.data:
    if event.type == "metrics":
        data.append(event.data)

# 转换为pandas DataFrame并保存为CSV
if data:
    df = pd.DataFrame(data)
    df.to_csv("fine_tuning_metrics2.csv", index=False)
    print(f"数据已保存至 fine_tuning_metrics2.csv")
