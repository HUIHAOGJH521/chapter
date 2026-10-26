import time

import numpy as np
dt=np.dtype(np.int32)
print(dt)
a=np.array([[1,2,3],[4,5,6],[7,8,9]])
print(a)
arr=np.empty([4,2],dtype=int)
print(arr)
arr=np.zeros([4,2],dtype=int)
print(arr)
arr=np.arange(4,dtype=np.int32)
print(arr)
t1 =time.time()

t2 =time.time()
print(t2-t1)






