import numpy as np
import os
mazeX = 6
mazeY = 5
mazeBx = 4
mazeBy = 4
maxState = mazeX*mazeY*mazeX*mazeY+2
numA = 5
verbose = False
import argparse
parser = argparse.ArgumentParser(
      formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument(
      "--T", type=int, default=15,
      help="Time-horizon.")
args = parser.parse_args()
T = args.T
data_dir = 'dataForT'+str(T)
if not os.path.isdir(data_dir):
    os.makedirs(data_dir)
def randargmax(b):
    """ a random tie-breaking argmax for axis=0"""
    res =np.zeros(shape=(b.shape[1],),dtype=int)
    b_Tanspose = np.array(list(zip(*b)))
    for i in range(b_Tanspose.shape[0]):
        imax = np.argwhere(list(b_Tanspose[i]) == np.amax(list(b_Tanspose[i])))
        imax = imax.reshape((-1,))
        res[i] = np.random.choice(imax)
    return res

rewardMatList = [None, None]
rewardMatList[0] = np.loadtxt('RewardMat' + str(0) + '.out', delimiter=',')
rewardMatList[1] = np.loadtxt('RewardMat' + str(1) + '.out', delimiter=',')
transProbMatList = [None] * numA
for a in range(numA):
    transProbMatList[a] = np.loadtxt('TransProbMat'+str(a)+'.out', delimiter=',')


uList = [None]*T
aList = [None]*T
uList[T-1] = rewardMatList[1]
aList[T-1]=np.zeros(shape=(maxState,),dtype=int)
for t in range(T-1,0,-1): # t 14:-1:1
    z = np.empty(shape=(numA, maxState))
    for a in range(numA):
        x = np.sum(transProbMatList[a]*uList[t], axis=1)
        z[a] = x + rewardMatList[0][a]
    uList[t-1] = np.max(z, axis=0)
    aList[t - 1] = randargmax(z)
    # aList[t - 1] = np.argmax(z,axis=0)

if os.path.exists(data_dir+'/'+'aListArray'+str(T)+'.npy'):
  os.remove(data_dir+'/'+'aListArray'+str(T)+'.npy')
np.array(aList).dump(open(data_dir+'/'+'aListArray'+str(T)+'.npy', 'wb'))
if os.path.exists(data_dir+'/'+'uListArray'+str(T)+'.npy'):
  os.remove(data_dir+'/'+'uListArray'+str(T)+'.npy')
np.array(uList).dump(open(data_dir+'/'+'uListArray'+str(T)+'.npy', 'wb'))
# os.rename('aListArray'+str(T)+'.npy', data_dir+'/'+'aListArray'+str(T)+'.npy')
# print('Storing action list is done')


