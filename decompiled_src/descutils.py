#Embedded file name: /WORKSPACE/data/entities/common/descutils.o
from data import fame_data as FMD

def getFameName(fameId):
    return FMD.data.get(fameId, {}).get('name', '')
