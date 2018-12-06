import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

x = np.arange(0,29)
# y = np.array([0,0,0,0,0,0,0,0,0,0,0,
#               0.617,0.759,0.798,0.832,0.855,0.894,0.918,0.931,0.938,0.952,0.962,0.977,0.972,0.98,0.982,0.992,0.993,0.993])

y = np.array([0,0,0,0,0,0,0,0,0,0,0,
              0.122,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1])


df = pd.DataFrame(y)
plt.scatter(x, y)
plt.xlabel('T')
plt.ylabel('Maximal Probability of Wining')
plt.grid()
plt.savefig('P1b_nostill.png')
# plt.savefig('P1b_still.png')
plt.show()