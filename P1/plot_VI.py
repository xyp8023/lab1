import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import argparse
parser = argparse.ArgumentParser(
      formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument(
      "--T", type=int, default=46,
      help="Time-horizon.")
args = parser.parse_args()
T = args.T
data_dir = 'dataForVI'
file_path = data_dir+'/'+'Vn'+str(T)+'.npy'
v = np.load(file_path)
df = pd.DataFrame(v)
# df = pd.read_csv(file_path)
y = df.values
plt.plot(y)
plt.savefig('plot_value.png')
plt.show()
print('Done')