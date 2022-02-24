class IndexMinPQ:
    def __init__(self, maxN):
        assert maxN > 0
        self._pq = [-1] * (maxN+1)
        self._qp = [-1] * (maxN+1)
        #记录item对应的index
        self._keys = [None] * (maxN + 1)
        self._maxN = maxN
        self._N = 0

    def append(self, key: int, item):
        """
        key(int): the index of item
        item(any): the item to be stored
        """
        assert key not in self
        self._N += 1
        self._qp[key] = self._N
        self._pq[self._N] = key
        self._keys[key] = item
        self._shiftdown(self._N)

    def change(self, key: int, item):
        """
        将索引key指向的元素设为item
        """
        assert key in self
        oldItem = self._keys[key]
        self._keys[key] = item
        if item < oldItem:
            self._shiftdown(self._qp[key])
        else:
            self._shiftup(self._qp[key])

    def _less(self, i, j):
        return self._keys[self._pq[i]] < self._keys[self._pq[j]]

    def _shiftdown(self, pos: int):
        while pos > 1 and self._less(pos, pos//2):
            self._exch(pos//2, pos)
            pos //= 2

    def _shiftup(self, pos):
        while 2*pos <= self._N:
            j = 2*pos
            if j < self._N and self._less(j+1, j):
                j += 1
            if not self._less(j, pos):
                break
            self._exch(pos, j)
            pos = j

    def __contains__(self, key: int):
        return self._qp[key] != -1

    def min(self):
        if self._keys:
            return self._keys[self._pq[1]]

    def minIndex(self):
        if self._keys:
            return self._pq[1]

    def _exch(self, i, j):
        self._pq[i], self._pq[j] = self._pq[j], self._pq[i]
        self._qp[self._pq[i]] = i
        self._qp[self._pq[j]] = j

    def delMin(self) -> int:
        assert self._N > 0
        indexOfmin = self._pq[1]
        self._exch(1, self._N)
        self._N -= 1
        self._shiftup(1)
        self._keys[self._pq[self._N+1]] = None
        self._qp[self._pq[self._N+1]] = -1
        return indexOfmin
    
    def pop(self) -> tuple:
        assert self._N > 0
        mini = self.min()
        indexOfmin = self.delMin()
        return indexOfmin, mini
    
    def delete(self, key:int):
        assert key in self
        index = self._qp[key]
        self._exch(index, self._N)
        self._pq[self._N] = -1
        self._N -= 1
        self._shiftdown(index)
        self._shiftup(index)
        self._keys[key] = None
        self._qp[key] = -1

    def isEmpty(self) -> bool: 
        return len(self) == 0

    def __len__(self):
        return self._N

    def __getitem__(self, key):
        assert key in self
        return self._keys[key]
    
    def __repr__(self):
        return str([(k,v) for k,v in enumerate(self._keys) if v is not None])
