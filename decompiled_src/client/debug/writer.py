#Embedded file name: I:/bag/tmp/tw2/res/entities\client\debug/writer.o
import csv
OUTPUT_FILE_NAME = 'npcId_seeker.csv'

def write2File(datas):
    writer = csv.writer(file(OUTPUT_FILE_NAME, 'w'))
    try:
        writer.writerow(['Ѱ·id', 'npcId', 'who'])
        for item in datas:
            writer.writerow([item['id'], item['npcId'], item['eWho']])

        return True
    except IOError:
        print 'дcsv�ļ����� %s', OUTPUT_FILE_NAME
        return False
