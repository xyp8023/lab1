import numpy as np

def randargmax(b):
    """ a random tie-breaking argmax for shape=(N,)"""
    return np.random.choice(np.flatnonzero(b == b.max()))

def determineAction(S,a):
    Action = {0:'Up', 1:'Down', 2:'Left', 3:'Right', 4:'Stay'}
    if S==(0,1) or S==(1,0):
        return '-'
    else:
        return Action[a]

numA = 5
T = 46
initPosition = (0,0,4,4)
Position = list(np.load(open('PositionArray'+'.npy', 'rb')))
initIndex = Position.index(initPosition+(0,0))
Px, Py, Mx, My = initPosition
initState = (Px, Py, Mx, My, 0, 0)
data_dir = 'dataForVI'
aList = list(np.load(open(data_dir+'/'+'aListArray' + str(T) + '.npy', 'rb')))
file_path = data_dir+'/'+'Vn'+str(T)+'.npy'
V = np.load(file_path)
rewardMatList = [None, None]
rewardMatList[0] = np.loadtxt('RewardMat' + str(0) + '.out', delimiter=',')
rewardMatList[1] = np.loadtxt('RewardMat' + str(1) + '.out', delimiter=',')
transProbMatList = [None] * numA
for a in range(numA):
    transProbMatList[a] = np.loadtxt('TransProbMat'+str(a)+'.out', delimiter=',')
actionRecord = []
RUN_NUMS = 10000
EXIT_NUMS = 0
verbose = False
for run_time in range(RUN_NUMS):
    sumReward = 0
    t=0
    curReward = 0
    while curReward<1:
        if t == 0:
            curState = initState
        t+=1
        if verbose:
            print('current state is {}'.format(curState))
        curIndex = Position.index(curState)
        a = aList[curIndex]
        v = V[curIndex]
        curAction = determineAction(curState, a)
        if verbose:
            print('current action is {}'.format(curAction))
        actionRecord.append(a)
        curReward = rewardMatList[0][a][curIndex]
        if verbose:
            print('Current reward is {}'.format(curReward))
        sumReward += curReward
        curIndex = randargmax(transProbMatList[a][curIndex])
        curState = Position[curIndex]
        if curReward<0:
            break
    if sumReward>=1:
        EXIT_NUMS+=1
    if verbose:
        print('Sum reward is {}'.format(sumReward))
        print('T is {}'.format(t))
print('The Prob is {}.'.format(EXIT_NUMS/RUN_NUMS))