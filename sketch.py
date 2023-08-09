def Next(self, index):
    index = index + 1
    print(f"-------------\n{index}\n-------------")
    self.l, self.keys = dictExtract()
    self.vars, self.momo = strVarSet(self.l, self.keys)
    self.count = 0  # key for dict
    self.descs = {}  # dict
    for f in vars[index]:  # for values in DictList[index]
        self.count = self.count + 1  # key for dict
        self.descs[self.count] = f  # Extracting descriptions for Labels
        print("ff\n\n", f)
    return index


def Previous(self, index):
    index = index - 1
    self.l, self.keys = dictExtract()
    self.vars, self.momo = strVarSet(self.l, self.keys)
    self.count = 0
    self.descs = {}
    for f in vars[self.index]:
        self.count = self.count + 1
        self.descs[self.count] = f
        print(f)


def strVarSet(keys, values):
    y = 0
    vars = {}
    l = []
    for item in values:
        x = eval(item)
        for xtem in x:
            y = y + 1
            vars[y] = x[xtem]
    print("\nstrVarSet()\nReturning\n", vars, "\n\n", keys)
    return vars, keys