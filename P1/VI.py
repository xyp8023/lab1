import numpy as np
import os
mazeX = 6
mazeY = 5
mazeBx = 4
mazeBy = 4
maxState = mazeX*mazeY*mazeX*mazeY+2
numA = 5
verbose = False

data_dir = 'dataForVI'
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


# aList = [None]

sigma = 100
epsilon = 0.01
Lambda = 1-1/30
Vn_star=np.zeros(shape=(maxState,1))
t=0
thres = epsilon*(1-Lambda)/Lambda
while sigma>thres:
    t+=1
    Vn = Vn_star
    z = np.empty(shape=(numA, maxState))
    for a in range(numA):
        what = np.sum(transProbMatList[a] * Vn, axis=1)
        z[a] =rewardMatList[0][a]+ Lambda*np.sum(transProbMatList[a]*Vn, axis=1)

    Vn_star = np.max(z,axis=0)
    aList= randargmax(z)
    sigma = np.linalg.norm( Vn_star-Vn)

# for t in range(T-1,0,-1): # t 14:-1:1
#     z = np.empty(shape=(numA, maxState))
#     for a in range(numA):
#         x = np.sum(transProbMatList[a]*uList[t], axis=1)
#         z[a] = x + rewardMatList[0][a]
#     uList[t-1] = np.max(z, axis=0)
#     aList[t - 1] = randargmax(z)
#     # aList[t - 1] = np.argmax(z,axis=0)

if os.path.exists(data_dir+'/'+'aListArray'+str(t)+'.npy'):
  os.remove(data_dir+'/'+'aListArray'+str(t)+'.npy')
np.array(aList).dump(open(data_dir+'/'+'aListArray'+str(t)+'.npy', 'wb'))
if os.path.exists(data_dir+'/'+'Vn'+str(t)+'.npy'):
  os.remove(data_dir+'/'+'Vn'+str(t)+'.npy')
np.array(Vn).dump(open(data_dir+'/'+'Vn'+str(t)+'.npy', 'wb'))
# os.rename('aListArray'+str(T)+'.npy', data_dir+'/'+'aListArray'+str(T)+'.npy')
# print('Storing action list is done')

os.system('python plot_VI.py'+' --T '+str(t))
