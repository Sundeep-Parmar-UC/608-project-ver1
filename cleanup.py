import shutil
import os

def Cleanup(EBSpath,fileName,uncompressedFilePath):
    os.remove(fileName)
    os.remove(uncompressedFilePath)
    usage = shutil.disk_usage(uncompressedFilePath[:6])
    free_bytes = usage.free
    free_gb = free_bytes / (1024 ** 2)
    return free_gb
