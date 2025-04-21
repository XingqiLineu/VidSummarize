import pandas as pd
import matplotlib.pyplot as plt

# 读取CSV文件
df = pd.read_csv("fine_tuning_metrics2.csv")

# 设置图表风格
plt.style.use('dark_background')

# 创建2x2子图布局
fig, axs = plt.subplots(2, 2, figsize=(12, 10))

# 绘制验证损失图
axs[0, 0].plot(df['step'], df['valid_loss'], color='#36a2eb')
axs[0, 0].set_title('valid_loss')
axs[0, 0].set_xlabel('Step')
axs[0, 0].grid(alpha=0.3)

# 绘制训练损失图
axs[0, 1].plot(df['step'], df['train_loss'], color='#36a2eb')
axs[0, 1].set_title('train_loss')
axs[0, 1].set_xlabel('Step')
axs[0, 1].grid(alpha=0.3)

# 绘制验证令牌准确率图
axs[1, 0].plot(df['step'], df['valid_mean_token_accuracy'], color='#36a2eb')
axs[1, 0].set_title('valid_mean_token_accuracy')
axs[1, 0].set_xlabel('Step')
axs[1, 0].grid(alpha=0.3)

# 绘制训练令牌准确率图
axs[1, 1].plot(df['step'], df['train_mean_token_accuracy'], color='#36a2eb')
axs[1, 1].set_title('train_mean_token_accuracy')
axs[1, 1].set_xlabel('Step')
axs[1, 1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig('fine_tuning_metrics_visualization2.png', dpi=300)
plt.show()
