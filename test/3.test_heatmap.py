# 単純にmatplotlibに後からimshowを追加できるかテストする

import matplotlib.pyplot as plt
import numpy as np

data1 = np.random.rand(1, 10)
data2 = np.random.rand(1, 10)

fig, ax = plt.subplots()

# data1 を y=0 の位置に表示
ax.imshow(data1, aspect='auto', cmap='viridis', extent=[0, 10, 0-0.5, 0+0.5])

# data2 を y=1 の位置に表示
ax.imshow(data2, aspect='auto', cmap='plasma', extent=[0, 10, 1-0.5, 1+0.5])

# y軸の範囲を調整
ax.set_ylim(-0.5, 1.5)

# カラーバーを追加（最初の imshow に基づく）
plt.colorbar(ax.images[0], ax=ax, orientation='vertical', label='Data1')

plt.show()