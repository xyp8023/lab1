import os
nums = 1000
os.system('python TransProbAndRewMat.py')
# T = 3
# os.system('python ActionMat.py --T '+str(T))
for T in range(1,30):
    # T+=3
    os.system('python ActionMat.py --T '+str(T))
    os.system('python RunMaze.py --T '+str(T)+' --nums '+str(nums) +' --verbose False')