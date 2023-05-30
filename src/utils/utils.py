import os
def mkdirIfNotExist(path):
    folder = os.path.exists(path)
    if folder: 
        return
    os.makedirs(path)  
    print('文件夹创建成功：', path)