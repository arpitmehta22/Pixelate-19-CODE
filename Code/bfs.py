import numpy as np
import queue
import ajcacency_9 as ad

adjMat = ad.adj
vis = np.zeros(82)
parent = np.zeros(82,int)

n = int(9)


def bfs(node,shape,imgMat):
    dest=-1
    q = queue.Queue(82)
    vis[node] = 1
    q.put(node)
    while q.empty() == 0:
        front = q.get()

        r = int(front/n)
        c = int(front%n)
        c = c-1
        if c== -1:
            r = r-1
            c = n-1
        if(imgMat[r][c] == shape):
            dest = front
            break
        for i in range(1,82):
            if adjMat[front,i] == 1:
                if vis[i] == 0:
                    vis[i] = 1
                    q.put(i)
                    parent[i] = front
                    
    path=[]
    if dest != -1:
        while True:
            if dest==node:
                break
            path.append(dest)
            dest = parent[dest]
        path.reverse()
        return path
    
        
    
    
