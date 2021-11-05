from Module.SENTIO import SENTIO
from Module.Enumeration import *
import os.path
import time

def main():
    # Prepare communication
    __SENTIO = SENTIO.create_SENTIO()

    #1. Load subsite table

    subsiteListEastX = {
        1: 0,
        2: 50,
        3: 100,}
    subsiteListEastY = {
        1: 0,
        2: 50,
        3: 100,}

    subsiteListWestX = {
        1: 0,
        2: -50,
        3: -100,}
    subsiteListWestY = {
        1: 0,
        2: 50,
        3: 100,}

    for i in range(1, len(subsiteListEastX)+1):
        __SENTIO.move_probe_xy('east', 'Home', subsiteListEastX[i],  subsiteListEastY[i])

    ##for i in range(1, len(subsiteListWestX)+1):
        __SENTIO.move_probe_xy('west', 'Home', subsiteListWestX[i],  subsiteListWestY[i])

    __SENTIO.close_SENTIO()
    ##__CTP10.close_CTP10()
    print('>>Finish.')

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(str(e))
