import numpy as np
import os
import argparse
parser = argparse.ArgumentParser(
      formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument(
      "--T", type=int, default=15,
      help="Time-horizon.")
parser.add_argument(
      "--nums", type=int, default=1,
      help="Run Numbers.")
parser.add_argument(
      "--verbose", type=bool, default=False,
      help="Verbose.")
args = parser.parse_args()
T = args.T
RUN_NUMS = args.nums
def randargmax(b):
    """ a random tie-breaking argmax for shape=(N,)"""
    # res =np.zeros(shape=(b.shape[1],),dtype=int)
    # b_Tanspose = np.array(list(zip(*b)))
    # for i in range(b_Tanspose.shape[0]):
    #     imax = np.argwhere(list(b_Tanspose[i]) == np.amax(list(b_Tanspose[i])))
    #     imax = imax.reshape((-1,))
    #     res[i] = np.random.choice(imax)
    return np.random.choice(np.flatnonzero(b == b.max()))

def determineAction(S,a):
    Action = {0:'Up', 1:'Down', 2:'Left', 3:'Right', 4:'Stay'}
    if S==(0,1) or S==(1,0):
        return '-'
    else:
        return Action[a]

mazeX = 6
mazeY = 5
mazeBx = 4
mazeBy = 4
maxState = mazeX*mazeY*mazeX*mazeY+2
numA = 5
verbose = args.verbose
#T = 14
data_dir = 'dataForT'+str(T)
#RUN_NUMS = 100
EXIT_NUMS = 0
P = 0.0
Position = list(np.load(open('PositionArray'+'.npy', 'rb')))
rewardMatList = [None, None]
rewardMatList[0] = np.loadtxt('RewardMat' + str(0) + '.out', delimiter=',')
rewardMatList[1] = np.loadtxt('RewardMat' + str(1) + '.out', delimiter=',')
transProbMatList = [None]*numA
for a in range(numA):
    transProbMatList[a] = np.loadtxt('TransProbMat'+str(a)+'.out', delimiter=',')

initPosition = (0,0,4,4)
initIndex = Position.index(initPosition+(0,0))

# if verbose:
#     print('Check the sum of transition probobility of initial state is {}'.format(np.sum(transProbMatList[1][initIndex])))
#     print('Check the sum of transition probobility of initial state is {}'.format(np.sum(transProbMatList[3][initIndex])))
Px, Py, Mx, My = initPosition
initState = (Px, Py, Mx, My, 0, 0)

for num in range(RUN_NUMS):
    # os.system('python ActionMat.py --T '+str(T))
    aList = list(np.load(open(data_dir+'/'+'aListArray' + str(T) + '.npy', 'rb')))
    uList = list(np.load(open(data_dir + '/' + 'uListArray' + str(T) + '.npy', 'rb')))
    actionRecord = []
    sumReward = 0
    for t in range(T):
        if t==0:
            curState = initState
        curIndex = Position.index(curState)
        a = aList[t][curIndex]
        u = uList[t][curIndex]
        P+=u
        curAction = determineAction(curState, a)
        actionRecord.append(a)

        if t==T-1:
            # if verbose:
            #     print('for T = {t} current state is {curState}\n\t\t  current reward is {curReward}\n\t\t  current action is {curAction}'.format(t=t,
            #                                                                                                                                  curState=curState,
            #                                                                                                                                  curReward=rewardMatList[1][curIndex],
            #                                                                                                                                  curAction=curAction))
            sumReward+=rewardMatList[1][curIndex]
        else:
            # if verbose:
            #     print('for T = {t} current state is {curState}\n\t\t  current reward is {curReward}\n\t\t  current action is {curAction}'.format(t=t,
            #                                                                                                                            curState=curState,
            #                                                                                                                            curReward=rewardMatList[0][a][curIndex],
            #                                                                                                                            curAction=curAction))
            sumReward += rewardMatList[0][a][curIndex]

        # curIndex = np.argmax(transProbMatList[a][curIndex])
        curIndex = randargmax(transProbMatList[a][curIndex])
        curState = Position[curIndex]

        if curState==(1,0):
            curIndex = -2
        if curState==(0,1):
            curIndex=-1
    # if verbose:
    #     print('the action is {}'.format(actionRecord))
    #     print('the sum of reward collected is {}'.format(sumReward))
    #     print('done')
    if sumReward>=1:
        EXIT_NUMS+=1

print('The probability of exit for T={T} is {EXIT_PROB}'.format(T=T, EXIT_PROB=EXIT_NUMS/RUN_NUMS))
P/=(T*RUN_NUMS)
print('P is {}'.format(P))
