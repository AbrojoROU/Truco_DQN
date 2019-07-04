import multiprocessing as mp
import os
import sys
from Truco_Value_Network_v2_r2 import *
from Truco_Core_v2_r2 import *


def worker1():
    import logging
    logging.getLogger('tensorflow').disabled = True
    # printing process id
    p1 = AgenteRandom(Reglas.JUGADOR1)
    p2 = AgenteRandom(Reglas.JUGADOR2)
    episodios = Motor.Play_random_games(p1, p2, 10000, False)

    sys.stdout.flush()


def worker2():
    import logging
    logging.getLogger('tensorflow').disabled = True
    # printing process id
    p1 = AgenteRandom(Reglas.JUGADOR1)
    p2 = AgenteRandom(Reglas.JUGADOR2)
    episodios = Motor.Play_random_games(p1, p2, 10000, False)
    sys.stdout.flush()

def worker3(p1,p2, N, queue):
    print("")
    import logging
    logging.getLogger('tensorflow').disabled = True
    # printing process id
    episodios = Motor.Play_random_games(p1, p2, N, False)

    queue.put(episodios)

    sys.stdout.flush()



def MultiP_v1():
    printDebug("COMIENZO Multi-Threading")
    import logging
    logging.getLogger('tensorflow').disabled = True

    # printing main program process id
    print("ID of main process: {}".format(os.getpid()))

    # creating processes
    p1 = mp.Process(target=worker1)
    p2 = mp.Process(target=worker2)

    # starting processes
    p1.start()
    p2.start()

    # process IDs
    print("ID of process p1: {}".format(p1.pid))
    print("ID of process p2: {}".format(p2.pid))

    # wait until processes are finished
    p1.join()
    p2.join()

    # both processes finished
    print("Both processes finished execution!")

    # check if processes are alive
    print("Process p1 is alive: {}".format(p1.is_alive()))
    print("Process p2 is alive: {}".format(p2.is_alive()))
    printDebug("TERMINO Multi-Threading")

    print("")

    printDebug("COMIENZO single-Threading")
    worker1()
    worker2()
    printDebug("TERMINO single-Threading")

def MultiP_v2():
    printDebug("COMIENZO Multi-Threading")
    import logging
    logging.getLogger('tensorflow').disabled = True
    p1 = AgenteRandom(Reglas.JUGADOR1)
    p2 = AgenteRandom(Reglas.JUGADOR2)
    N = 1000

    queue1 = mp.Queue()
    queue2 = mp.Queue()

    process1 = mp.Process(target=worker3, args=(p1, p2, N, queue1))
    process2 = mp.Process(target=worker3, args=(p1, p2, N, queue2))

    process1.start()
    process2.start()

    episodios1 = queue1.get()
    episodios2 = queue2.get()  # Prints {"foo": True}

    process1.join()
    process2.join()
    eps = episodios1+episodios2
    print("largo:" + str(len(eps)))




    printDebug("TERMINO Multi-Threading")
    print("")
    printDebug("COMIENZO single-Threading")

    Motor.Play_random_games(p1, p2, 10000, False)
    Motor.Play_random_games(p1, p2, 10000, False)

    printDebug("TERMINO single-Threading")



#######################################################
###                    MAIN                         ###
#######################################################
if __name__ == '__main__':
    #MultiP_v1()
    print(str(mp.cpu_count()))
    MultiP_v2()