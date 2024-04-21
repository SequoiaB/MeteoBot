
def decode_entry_cycle(data, tempInfo):

    tempInfo = {'City': "?",
                'start': 0,
                'finish': 0,
                }
    
    if data == 0:
        tempInfo['start'] = 0
        return tempInfo
    
    if data == 1:
        tempInfo['start'] = 1
        return tempInfo
    
    if data == 2:
        tempInfo['start'] = 2
        return tempInfo
    
    if data == 3:
        tempInfo['start'] = 3
        return tempInfo
    
    if data == 4:
        tempInfo['start'] = 4
        return tempInfo

def decode_giorno_inizio(data, tempInfo):
    # bisogna restituire il numero 
    # di giorni da cui cominciare
    # 0 = oggi, 1 = domani ...
    tempInfo = {'City': "?",
                'start': 0,
                'finish': 0,
                }
    
    if data == 0:
        tempInfo['start'] = 0
        return tempInfo
    
    if data == 1:
        tempInfo['start'] = 1
        return tempInfo
    
    if data == 2:
        tempInfo['start'] = 2
        return tempInfo
    
    if data == 3:
        tempInfo['start'] = 3
        return tempInfo
    
    if data == 4:
        tempInfo['start'] = 4
        return tempInfo
    
def decode_giorno_fine(data, tempInfo):
    # bisogna restituire il numero 
    # di giorni da aspettare da tempInfo['start']
    
    if data == 0:
        tempInfo['finish'] = tempInfo['start'] + 1
        return tempInfo
    
    if data == 1:
        tempInfo['finish'] = tempInfo['start'] + 2
        return tempInfo
    
    if data == 2:
        tempInfo['finish'] = tempInfo['start'] + 3
        return tempInfo
    
    if data == 3:
        tempInfo['finish'] = tempInfo['start'] + 4
        return tempInfo
    
    if data == 4:
        tempInfo['finish'] = tempInfo['start'] + 5
        return tempInfo