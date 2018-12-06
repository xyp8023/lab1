# The Maze and the Random Minotaur
import numpy as np
import os
# import argparse
# parser = argparse.ArgumentParser(
#       formatter_class=argparse.ArgumentDefaultsHelpFormatter)
# parser.add_argument(
#       "--T", type=int, default=15,
#       help="Time-horizon.")
# args = parser.parse_args()
# T = args.T
mazeX = 6
mazeY = 5
mazeBx = 4
mazeBy = 4
maxState = mazeX*mazeY*mazeX*mazeY+2
numA = 5
verbose = False
T = 15
# data_dir = 'dataForT'+str(T)
# if not os.path.isdir(data_dir):
#     os.makedirs(data_dir)
# initialize the position matrix, transition probability matrix, reward matrix
Position = []
transProbMatList = [np.zeros(shape=(maxState,maxState)),np.zeros(shape=(maxState,maxState)),np.zeros(shape=(maxState,maxState)),np.zeros(shape=(maxState,maxState)),np.zeros(shape=(maxState,maxState))]
rewardMatList = [np.zeros(shape=(numA, maxState)), np.zeros(shape=(1, maxState))]
wallList =[(1,0,3), (1,1,3), (1,2,3), (2,0,2),(2,1,2),(2,2,2),(3,1,3),(3,2,3),(4,1,2),(4,1,1),(4,2,2),(4,2,0),(5,1,1),(5,2,0),(1,3,1),(2,3,1),(
    3,3,1),(4,3,1),(1,4,0),(2,4,0),(3,4,0),(3,4,3),(4,4,0),(4,4,2)]
edgeList = [(0,0,0), (0,0,2),(0,1,2),(0,2,2),(0,3,2),(0,4,2),(0,4,1),(1,4,1),(2,4,1),(3,4,1),(4,4,1),(5,4,1),(5,4,3),(5,3,3),(5,2,3),(5,1,3),(5,0,3),(5,0,0),(4,0,0),(3,0,0),(2,0,0),(1,0,0)]
def rewardFunc(S, a, t):
    Px, Py, Mx, My, Dead, Win = S
    curPosition = (Px, Py, Mx, My)
    # if t==T:
    #     if Dead==1:
    #         rewardMatList[1][0][-2] = -1
    #     elif Win==1:
    #         rewardMatList[1][0][-1]=1
    # else:
    wall =(Px,Py,a)

    # if Dead==1:
    #     rewardMatList[0][a][-2] = -1
    #     rewardMatList[0][a][-2] = 0
    # elif Win==1:
        # rewardMatList[0][a][-1]=1
        # rewardMatList[0][a][-1] = 0
    if Dead==0 and Win==0 and Px == mazeBx and Py==mazeBy:
        rewardMatList[0][a][Position.index(curPosition)]=1
    elif Dead==0 and Win==0 and Px == Mx and Py==My:
        rewardMatList[0][a][Position.index(curPosition)] = -1
    elif  wall in wallList or wall in edgeList: # wall
        rewardMatList[0][a][Position.index(curPosition)]=-100


def transitionProb(S_new, S, a):
    # return the P(S_new|S,a) and filled in the ProbMat
    Px, Py, Mx, My, Dead, Win = S
    Px_new, Py_new, Mx_new, My_new, Dead_new, Win_new = S_new
    if (Dead==1 and Win==1) or (Dead_new==1 and Win_new==1):
        raise NameError('Error! Dead cannot happen with Win together')
    elif (Dead==1 and Win==0) and (Dead_new==1 and Win_new==0):
        transProbMatList[a][-2][-2]=1

    elif (Dead==0 and Win==1) and (Dead_new==0 and Win_new==1):
        transProbMatList[a][-1][-1]=1

    elif (Dead==0 and Win==0):
        currPosition = (Px, Py, Mx, My)
        newPosition = (Px_new, Py_new, Mx_new, My_new)
        x = Position.index(currPosition)
        y = Position.index(newPosition)
        if (Mx==0 and My==0 ) or (Mx==mazeX-1 and My==0) or (Mx==0 and My==mazeY-1) or (Mx==mazeX-1 and My==mazeY-1) : # corner
            # Pr = 1/(numA-2)
            Pr = 1 / (numA - 3) # no stand still
        elif (Mx==0 and 0<My<mazeY-1) or (Mx==mazeX-1 and 0<My<mazeY-1) or (My==0 and 0<Mx<mazeX-1) or (My==mazeY-1 and 0<Mx<mazeX-1) : # egde but not corner
            # Pr = 1/(numA-1)
            Pr = 1 / (numA - 2)  # no stand still
        else:
            # Pr=1/numA
            Pr = 1 / (numA - 1)  # no stand still

        if (Px==Mx and Py==My):
            if (Dead_new==1 and Win_new==0):
                transProbMatList[a][x][-2]=1

        elif (Px==mazeBx and Py==mazeBy) :
            if (Dead_new==0 and Win_new==1):
                transProbMatList[a][x][-1]=1

        # elif (abs(My_new-My)<=1 and Mx_new==Mx) or (abs(Mx_new-Mx)<=1 and My_new==My):
        # if the minotaur is not allowed to stand still
        elif (abs(My_new - My) == 1 and Mx_new == Mx) or (abs(Mx_new - Mx) == 1 and My_new == My):
            if a==0: # Up
                if (Px==Px_new) and ((Py-Py_new)==1):
                    transProbMatList[a][x][y] = Pr

            # elif (a == 1) and (Px == Px_new) and ((Py - Py_new) == 1): # Down
            if a==1: # Down
                if (Px == Px_new) and ((Py_new - Py) == 1):
                    transProbMatList[a][x][y] = Pr

            if a==2:
                if ((Px-Px_new)==1) and (Py_new==Py): # Left
                    transProbMatList[a][x][y] = Pr

            if a==3:
                if ((Px_new-Px)==1) and (Py_new==Py): # Right
                    transProbMatList[a][x][y] = Pr

            if a==4 :
                if (Px==Px_new) and (Py_new==Py): # Stay
                    transProbMatList[a][x][y] = Pr

for Px in range(mazeX):
    for Py in range(mazeY):
        for Mx in range (mazeX):
            for My in range(mazeY):
                Position.append((Px, Py, Mx, My))
initPosition = (0,0,mazeBx,mazeBy)
initIndex = Position.index(initPosition)

print('Storing reward mat and transition prob mat is starting')
for Px in range(mazeX):
    for Py in range(mazeY):
        for Mx in range (mazeX):
            for My in range(mazeY):
                for Dead in range(2):
                    for Win in range(2):
                        for a in range(numA):
                            if (Dead == 1 and Win == 1):
                                break
                            S = (Px, Py, Mx, My, Dead, Win)
                            rewardFunc(S, a, 1)
                            rewardFunc(S,a,T)
                            for Px_new in range(mazeX):
                                for Py_new in range(mazeY):
                                    for Mx_new in range(mazeX):
                                        for My_new in range(mazeY):
                                            for Dead_new in range(2):
                                                for Win_new in range(2):
                                                    if  (Dead_new==1 and Win_new==1) :
                                                        break
                                                    S = (Px, Py, Mx, My, Dead, Win )
                                                    S_new =  (Px_new, Py_new, Mx_new, My_new, Dead_new, Win_new )
                                                    transitionProb(S_new, S, a)

# saving the transition probability matrix, the reward matrix
if os.path.exists('RewardMat' + str(0) + '.out'):
  os.remove('RewardMat' + str(0) + '.out')
np.savetxt('RewardMat' + str(0) + '.out', rewardMatList[0], delimiter=',', fmt='%-d')

if os.path.exists('RewardMat' + str(1) + '.out'):
  os.remove('RewardMat' + str(1) + '.out')
np.savetxt('RewardMat' + str(1) +'.out', rewardMatList[1], delimiter=',', fmt='%-d')
print('Saving Reward Matrix is Done')

for a in range(numA):
    if os.path.exists('TransProbMat'+str(a)+'.out'):
        os.remove('TransProbMat'+str(a)+'.out')
    np.savetxt('TransProbMat'+str(a)+'.out', transProbMatList[a], delimiter=',',fmt ='%-.2f')
    if verbose:
        print(np.sum(transProbMatList[a],axis=1))
        print('\n')
print('Saving Transition Prob Matrix is Done')


Position = []
for Px in range(mazeX):
    for Py in range(mazeY):
        for Mx in range (mazeX):
            for My in range(mazeY):
                Position.append((Px, Py, Mx, My,0,0))
Position.append((1,0))
Position.append((0,1))
if os.path.exists('PositionArray'+'.npy'):
  os.remove('PositionArray'+'.npy')
np.array(Position).dump(open('PositionArray'+'.npy', 'wb'))
print('Storing Position list is done')