import os, sys, shutil

class DirInfo:
    def __init__(self, path, depth=0, fileCount=0):
        self.path = path
        self.depth = depth
        self.fileCount = fileCount

# Return dict<string, DirInfo>
def getDirDict(curPath, curName, depth=0):
    dirDict = dict() # dict<string, DirInfo>
    removeList = []

    curInfo = DirInfo(curPath, depth)
    for name in os.listdir(curPath):
        path = os.path.join(curPath, name)
        if os.path.isdir(path):
            (dic, lis) = getDirDict(path, name, depth + 1)
            removeList.extend(lis)
            for dirName, dirInfo in dic.items():
                if dirName in dirDict and dirDict[dirName].fileCount >= dirInfo.fileCount:
                    removeList.append(dirInfo.path)
                    continue
                dirDict[dirName] = dirInfo
        elif os.path.isfile(path):
            if not path.endswith(".zip"):
                curInfo.fileCount += 1
            else:
                os.remove(path)
    
    if curInfo.fileCount > 0 and (curName not in dirDict or dirDict[curName].fileCount < curInfo.fileCount):
        dirDict[curName] = curInfo
    elif depth > 0:
        removeList.append(curPath)

    return (dirDict, removeList)

def main():
    if len(sys.argv) <= 1:
        print("Usage: main.py <path>")
        return 
    
    rootDir = sys.argv[1]
    if not os.path.isdir(rootDir):
        print("Wrong path:", rootDir)
        return

    (dirDict, _) = getDirDict(rootDir, "")
    dirList = sorted(list(dirDict.items()), key=lambda x: x[1].depth, reverse=True)
    
    for (dirName, dirInfo) in dirList:
        os.rename(dirInfo.path, os.path.join(rootDir, dirName))

main()