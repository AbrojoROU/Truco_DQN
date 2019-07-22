# OPTIMISTIC INITIAL VALUES

import numpy as np
import inspect
import random
import pickle
import itertools
import json
import matplotlib.pyplot as plt
# %matplotlib inline

import time


# FUNCIONES A NIVEL MODULO
global start_timer
start_timer = time.time()


def GenerarMazo():
    # Formato Cartas ID, Nombre, ValorTruco
    # Solucion final sera con 9 cartas (reduce statespace y permite codificar en base 10) tomadas al azar de las 40
    Carta.ResetContCarta()
    MAZO = []
    MAZO.append(Carta("4-Copa", 10)) # ID: 1
    MAZO.append(Carta("6-Copa", 20)) # ID: 2
    MAZO.append(Carta("6-Basto", 20)) # ID: 3
    MAZO.append(Carta("11-Copa", 30)) # ID: 4
    MAZO.append(Carta("11-Basto", 30)) # ID: 5
    MAZO.append(Carta("2-Basto", 40)) # ID: 6
    MAZO.append(Carta("2-Copa", 40)) # ID: 7
    MAZO.append(Carta("1-Basto", 80)) # ID: 8
    MAZO.append(Carta("1-Espada", 100)) # ID: 9


    return MAZO

def GenerarAcciones():
    # podrian ser "carta mas alta, media y baja en puntaje?", pero y si son todas absolutamente altas?
    # codificar la carta a jugar (accion) con base en un feature (puntaje relativo) parece suboptimo
    # usar puntaje absoluto implicaria demasiadas acciones posibles quedandome un SxA ya demasiado alto
    # Pareceria que cada accion/carta necesitaria un feature set mas amplio y una "activacion" no lineal
    ACCIONES = {}
    ACCIONES[1] = '1'  # Jugar Carta mas alta
    ACCIONES[2] = '2'  # Jugar 2da Carta mas alta
    ACCIONES[3] = '3'  # Jugar 3ra Carta mas alta
    return ACCIONES


def LoadEstado_FromHash(codigoHash, debug=False):
    # El 0 devuelve vacio
    cartas_jugadas = []
    for c in str(codigoHash):
        if debug: printDebug("caracter: " + c)
        if (int(c) > 0):
            cartas_jugadas.append(Reglas.MAZO[int(c) - 1])
    return cartas_jugadas

def GetAllStates(debug=False):
    # devuelve todos los estados posibles hasta 6 jugadas, incluyendo los acumulados
    results = []

    # Las 6 cartas de jugadas
    for i in range(6+3):  # son 6 jugadas, 3 por jugador
        for j in GetAllStatesCodes(Reglas.MAZO[:], i+1):
            if debug: printDebug("state code: " + j)
            unE = LoadEstado_FromHash(j)
            if debug: printDebug("estado: " + str(unE))
            results.append(unE)

    return results

def GetAllStatesCodes(mazoRestante, jugadasRestantes, debug=False):
    # TODO Optimizar que use listas de ints en lugar de cartas
    # metodo recursivo, invocado inicialmente desde GetAllStates() con 6 jugadas a calcular
    # esta variante "old" admite el 0
    results = []
    # Caso Base: retorno los digitiso del 1 al 9 (no se usan 0s)
    if jugadasRestantes == 1:
        for ultima_carta in mazoRestante:
            if debug: printDebug("caso terminal: " + str(ultima_carta.ID))
            results.append(ultima_carta.ID)
    else:
        # Caso Recursivo, 2 o mas digitos que debo devolver
        for j in mazoRestante[:]:  # Para cada carta en el mazo, va de 1 a N
            if debug: printDebug("Comienzo con carta:" + str(j.ID) + " de:" + str(len(mazoRestante)))
            mazoRestante.remove(j)  # Quito la carta del mazo antes de llamado recursivo
            for k in GetAllStatesCodes(mazoRestante[:], jugadasRestantes - 1):
                if debug: printDebug("pase por aca 3, k=" + str(k) + " mazorestante:" + str(len(mazoRestante)))
                unCode = str(j.ID) + str(k)
                if debug: printDebug("Agrego a mi retorno: " + unCode)
                results.append(unCode)

            mazoRestante.append(j)  # Retorno la carta j que habia quitado al mazo

    return results

def QuienGano(estadoTexto):
    puntos_j1 = 0
    puntos_j2 = 0
    cartas_jugadas = []

    #construyo lista de cartas asi tengo sus valoresTruco
    for c in str(estadoTexto):
        if (int(c) > 0):
            cartas_jugadas.append(Reglas.MAZO[int(c) - 1])

    # Si no llego a 6 cartas jugadas entonces no terminamos aun
    if len(cartas_jugadas) < 6:
        return None

    # PUNTOS MANO 1
    if cartas_jugadas[0].ValorTruco > cartas_jugadas[1].ValorTruco:
        puntos_j1 += 1
    elif cartas_jugadas[0].ValorTruco < cartas_jugadas[1].ValorTruco:
        puntos_j2 += 1

    # PUNTOS MANO 2
    if puntos_j2 == 1:
        # j2 gano la primer mano
        # j2 comienza la Mano 2, o sea, cartas[2] es de j2)
        if cartas_jugadas[2].ValorTruco > cartas_jugadas[3].ValorTruco:
            puntos_j2 += 1
        elif cartas_jugadas[2].ValorTruco < cartas_jugadas[3].ValorTruco:
            puntos_j1 += 1

        #MANO 3
        if puntos_j1 == 1:
            # j1 gano la 2da (y j2 la 1ra)
            # La quinta carta (cartas[4]) es de j1
            if cartas_jugadas[4].ValorTruco > cartas_jugadas[5].ValorTruco:
                puntos_j1 += 1
            elif cartas_jugadas[4].ValorTruco < cartas_jugadas[5].ValorTruco:
                puntos_j2 += 1
        else:
            # j1 no gano la 2da (j2 la 1ra)
            # La quinta carta (cartas[4]) es de j2 aunque hayan empatado
            if cartas_jugadas[4].ValorTruco > cartas_jugadas[5].ValorTruco:
                puntos_j2 += 1
            elif cartas_jugadas[4].ValorTruco < cartas_jugadas[5].ValorTruco:
                puntos_j1 += 1

    else:
        # j2 no gano la primer mano, el saque lo tiene j1 (aunque hayan empatado)
        # j1 comienza la Mano 2, o sea, cartas[2] es de j1)
        if cartas_jugadas[2].ValorTruco > cartas_jugadas[3].ValorTruco:
            puntos_j1 += 1
        elif cartas_jugadas[2].ValorTruco < cartas_jugadas[3].ValorTruco:
            puntos_j2 += 1

        # MANO 3
        if puntos_j2 == 1:
            # j2 gano la 2da (La primera fue empate o gano j1)
            # La quinta carta (cartas[4]) es de j2
            if cartas_jugadas[4].ValorTruco > cartas_jugadas[5].ValorTruco:
                puntos_j2 += 1
            elif cartas_jugadas[4].ValorTruco < cartas_jugadas[5].ValorTruco:
                puntos_j1 += 1
        else:
            # j2 no gano la 2da (y gano j1 o empataron)
            # La quinta carta (cartas[4]) es de j1
            if cartas_jugadas[4].ValorTruco > cartas_jugadas[5].ValorTruco:
                puntos_j1 += 1
            elif cartas_jugadas[4].ValorTruco < cartas_jugadas[5].ValorTruco:
                puntos_j2 += 1


    if puntos_j1 > puntos_j2:
        return Reglas.JUGADOR1
    elif puntos_j1 < puntos_j2:
        return Reglas.JUGADOR2
    else: #igualados en puntos con 6 cartas jugadas
        # Desempata la 1er mano?
        if cartas_jugadas[0].ValorTruco > cartas_jugadas[1].ValorTruco:
            return Reglas.JUGADOR1
        elif cartas_jugadas[0].ValorTruco < cartas_jugadas[1].ValorTruco:
            return Reglas.JUGADOR2
        else:
            # Si 1er mano fue empate, desempata la 2da mano
            # j1 comienza la Mano 2, o sea, cartas[2] es de j1)
            if cartas_jugadas[2].ValorTruco > cartas_jugadas[3].ValorTruco:
                return Reglas.JUGADOR1
            elif cartas_jugadas[2].ValorTruco < cartas_jugadas[3].ValorTruco:
                return Reglas.JUGADOR2
            else:
                # empataron las 3 manos
                return 0

def QuienLeToca(s):
    cartas_jugadas = LoadEstado_FromHash(s)

    # Estamos en primera Mano
    if len(s) == 0 or str(s)=="" or str(s)=="0":
        return Reglas.JUGADOR1
    if len(s) == 1:
        return Reglas.JUGADOR2

    # En 2da mano
    if len(s) == 2:
        if cartas_jugadas[0].ValorTruco >= cartas_jugadas[1].ValorTruco:
            return Reglas.JUGADOR1
        if cartas_jugadas[0].ValorTruco < cartas_jugadas[1].ValorTruco:
            return Reglas.JUGADOR2
    if len(s) == 3:
        if cartas_jugadas[0].ValorTruco >= cartas_jugadas[1].ValorTruco:
            return Reglas.JUGADOR2
        if cartas_jugadas[0].ValorTruco < cartas_jugadas[1].ValorTruco:
            return Reglas.JUGADOR1

    # En 3ra mano
    if len(s) == 4 or len(s) == 5:
        # primero calculo resultados primeras dos manos y los guardo
        j1_gano_1raMano = cartas_jugadas[0].ValorTruco >= cartas_jugadas[1].ValorTruco
        if j1_gano_1raMano:
            # si j1 gano la 1ra mano, con empatar ya "gana" la 2da mano tambien (en el sentido de que mantiene el "saque")
            j1_gano_2daMano = cartas_jugadas[2].ValorTruco >= cartas_jugadas[3].ValorTruco
        else:
            # si j1 perdio la primer mano, entonces j1 esta obligado a ganar para para recuperar el "saque"
            j1_gano_2daMano = cartas_jugadas[2].ValorTruco < cartas_jugadas[3].ValorTruco

        # ahora aplico reglas
        if len(s) == 4:
            if j1_gano_2daMano:
                return Reglas.JUGADOR1
            else:
                return Reglas.JUGADOR2
        if len(s) == 5:
            if j1_gano_2daMano:
                return Reglas.JUGADOR2
            else:
                return Reglas.JUGADOR1

    return None

def printDebug(debugMsg):
    print("   #debug@ " + str(debugMsg) + "   ## " + str(inspect.stack()[1][3]) + "() " + "  ## T=" + str(time.time() - start_timer)[0:7] + "s" )
    return

def train_agents(unN, DEBUG, p1=None, p2=None):
    # SEEDING
    # from numpy.random import seed
    # seed(1)

    if DEBUG: print("## TRAINING! ##            EPSILON = 0 !!")
    # Hiper Parametros
    N = unN
    GAMMA = 0.9
    ALPHA = 0.5
    if DEBUG :
        EPSILON = 0
    else:
        EPSILON = 0.20

    # Creamos e inicializamos los Agentes
    if p1 is None:
        p1 = Agente(Reglas.JUGADOR1, EPSILON, ALPHA, GAMMA)
        p1.InicializarQ()
    if p2 is None:
        p2 = Agente(Reglas.JUGADOR2, EPSILON, ALPHA, GAMMA)
        p2.InicializarQ()


    # Declaro variables de monitoreo
    cont_win_j1 = 0
    cont_win_j2 = 0
    cont_empate = 0

    for i in range(N):
        if DEBUG: printDebug("EPISODIO #" + str(i + 1) +"   ")
        print("\r" + str(((i+1)/N)*100)[0:5] + " % Training completado ", end="")
        #SETUP INICIAL repartir cartas
        cartas_p1, cartas_p2 = Reglas.RepartirCartas()
        p1.TomarCartas(cartas_p1)
        p2.TomarCartas(cartas_p2)
        s = "0"

        if DEBUG: printDebug("  Cartas Jugador 1: " + str(p1.cartas_totales))
        if DEBUG: printDebug("  Cartas Jugador 2: " + str(p2.cartas_totales))

        # Accion inicial
        current_player = p1
        a = p1.Elegir_Accion(s, DEBUG)

        # loops until the game is over
        while QuienGano(s) is None:

            sp, r = current_player.EjecutarAccion(s, a)
            if DEBUG: printDebug("      Nuevo estado: " + sp + ", con recompensa: " + str(r))

            # Tomo otro jugador
            if QuienLeToca(sp) == Reglas.JUGADOR1:
                next_player = p1
            else:
                next_player = p2

            # Ahora calculo Q_Next, 4 opciones:  Terminal Gane, Terminal empate, Terminal Perdi o No terminal y propago
            if len(sp) == 6:
                Q_Next = 0  # Estado terminal siempre es cero, la reward refleja la ganancia o perdida
                assert(QuienGano(sp) is not None) # imposible resultado None, debe ser 1, 2 o 0
                if QuienGano(sp) == Reglas.JUGADOR1:
                    # Caso 1: terminal gané
                    if DEBUG: printDebug(" GANE! (jugador 1, s:" + sp)
                    cont_win_j1 = cont_win_j1 +1
                elif QuienGano(sp) == 0:
                    # Caso 2: terminal empate
                    if DEBUG: printDebug(" EMPATE!  s:" + sp)
                    cont_empate = cont_empate + 1
                elif QuienGano(sp) == Reglas.JUGADOR2:
                    # Caso 3: terminal perdí
                    if DEBUG: printDebug(" GANE! (jugador 2, s:" + sp)
                    cont_win_j2 = cont_win_j2 + 1
            else:
                # Caso no terminal, propago Q
                ap = next_player.Elegir_Accion(sp,DEBUG)

                # cambia el signo de Q_Next si el jugador es distinto
                if next_player != current_player:
                    Q_Next = -next_player.Q[int(next_player.s_cartas + sp)][ap]
                else:
                    Q_Next = next_player.Q[int(next_player.s_cartas + sp)][ap]

            # Actualizo Q(s,a) dado que ya tengo sp y ap
            current_player.Q[int(current_player.s_cartas +s)][a] = current_player.Q[int(current_player.s_cartas +s)][a] + ALPHA*(r + GAMMA*Q_Next - current_player.Q[int(current_player.s_cartas +s)][a])

            if DEBUG: printDebug(
                "       JUGADOR:" + str(current_player.jugador) + " hace UPDATE de Q[" + str(current_player.s_cartas + s) + "][" + str(a) + "] = " + str(current_player.Q[int(current_player.s_cartas +s)][a]) + " y r:" + str(r))

            # Finalmente alterno jugador
            if QuienLeToca(str(sp)) == Reglas.JUGADOR1:
                current_player = p1
            else:
                current_player = p2
            s = sp
            a = ap

        #Terminó el while gameover
    #Terminó el for N

    # Despliego resultados de la corrida
    if DEBUG: print("## TRAINING TERMINADO ##  N= "+ str(N)+" - j1: "+ str(cont_win_j1)+", j2: "+ str(cont_win_j2)+", Empates: " + str(cont_empate))

    return p1,p2

def sequential_Train_and_Save(epochs, batch_size, DEBUG, p1=None,p2=None):
    #igual que train and save pero lo hace en etapas y guarda y retorna los ratios en zero
    results = []
    if p1 is None or p2 is None:
        p1, p2 = train_agents(0, False,p1,p2)

    print("Entrenando Agentes.. ( epochs=" + str(epochs) + ",   batch_size=" +str(batch_size) + " )" )
    # inicial
    partial_ratio = p2.ZeroRatio_en_Q()
    print("")
    if DEBUG: print("Ratio inicial: " + str(partial_ratio)[0:11])
    print("")
    results.append(partial_ratio)

    # Corros los epochs
    for i in range(epochs):
        if DEBUG: print("Epoch: " + str(i + 1))
        p1, p2 = train_agents(batch_size, False, p1,p2)
        partial_ratio = p2.ZeroRatio_en_Q()
        if DEBUG: printDebug("   Ratio: "+  str(partial_ratio)[0:11])
        results.append(partial_ratio)
        print("")

    # Finalmente guardando Q
    if DEBUG: print("2) Guardando Pickles..")
    p1.Save_Q_to_Disk("p1.pickle")
    p2.Save_Q_to_Disk("p2.pickle")
    if DEBUG: print("  Guardado en pickle Terminado !")

    return results


def play_game(p1, p2, N, DEBUG):
    # SEEDING
    from numpy.random import seed
    seed(1)

    # Declaro variables de monitoreo
    cont_win_j1 = 0
    cont_win_j2 = 0
    cont_empate = 0

    #Fuerzo a los jugadores a jugar full greedy
    p1.eps = 0
    p2.eps = 0

    for i in range(N):
        if DEBUG: printDebug("EPISODIO #" + str(i + 1) + "   ")

        # SETUP INICIAL repartir cartas
        cartas_p1, cartas_p2 = Reglas.RepartirCartas()
        p1.TomarCartas(cartas_p1)
        p2.TomarCartas(cartas_p2)
        s = "0"

        if DEBUG: printDebug("  Cartas Jugador 1: " + str(p1.cartas_totales))
        if DEBUG: printDebug("  Cartas Jugador 2: " + str(p2.cartas_totales))

        # Accion inicial
        current_player = p1
        a = p1.Elegir_Accion(s, DEBUG)

        # loops until the game is over
        while QuienGano(s) is None:

            sp, r = current_player.EjecutarAccion(s, a)
            if DEBUG: printDebug("      Nuevo estado: " + sp + ", con recompensa: " + str(r))

            # Tomo otro jugador
            if QuienLeToca(sp) == Reglas.JUGADOR1:
                next_player = p1
            else:
                next_player = p2

            # Ahora calculo Q_Next, 4 opciones:  Terminal Gane, Terminal empate, Terminal Perdi o No terminal y propago
            if len(sp) == 6:
                assert (QuienGano(sp) is not None)  # imposible resultado None, debe ser 1, 2 o 0
                if DEBUG: printDebug("- Partida terminada nro:" + str(i) + " s:" + sp)
                if QuienGano(sp) == Reglas.JUGADOR1:
                    # Caso 1: terminal gané
                    if DEBUG: printDebug(" GANE! (jugador 1, s:" + sp)
                    cont_win_j1 = cont_win_j1 + 1
                elif QuienGano(sp) == 0:
                    # Caso 2: terminal empate
                    if DEBUG: printDebug(" EMPATE!  s:" + sp)
                    cont_empate = cont_empate + 1
                elif QuienGano(sp) == Reglas.JUGADOR2:
                    # Caso 3: terminal perdí
                    if DEBUG: printDebug(" GANE! (jugador 2, s:" + sp)
                    cont_win_j2 = cont_win_j2 + 1
            else:
                # Caso no terminal, propago Q
                ap = next_player.Elegir_Accion(sp, DEBUG)
                #Q_Next = ...

            # Finalmente alterno jugador
            if QuienLeToca(str(sp)) == Reglas.JUGADOR1:
                if DEBUG and type(current_player) is Agente: printDebug("JUGADOR:" + str(current_player.jugador) + " hace UPDATE de Q[" + str(current_player.s_cartas+s) + "][" + str(a) + "] = " + str(current_player.Q[int(current_player.s_cartas +s)][a])+ " y r:" + str(r))
                current_player = p1
            else:
                current_player = p2
            s = sp
            a = ap
        # Terminó el while gameover
    # Terminó el for N

    # Despliego resultados de la corrida
    winratio = cont_win_j1*100/(cont_win_j1+cont_win_j2+cont_empate)
    print("## RESULTADO ##  N= " + str(N) + " - j1: " + str(cont_win_j1) + ", j2: " + str(cont_win_j2) + ", Empates: " + str(cont_empate) + ", WINRATIO:"+ str(winratio)[0:5]+", S final: " + str(s))
    if DEBUG:
        if type(p1) is Agente : print("j1 - Q[0]: " + str(p1.Q[0]))
        for i in p1.cartas_totales:
            if type(p2) is Agente : print("j2 - Q[" + str(i.ID) + "]: " + str(p2.Q[i.ID]))

    return winratio

def max_dict(d):
    # returns the argmax (key) and max (value) from a dictionary
    # put this into a function since we are using it so often
    max_key = None
    max_val = float('-inf')
    for k, v in d.items():
        if v > max_val:
            max_val = v
            max_key = k
    return max_key, max_val

# helper method para obtener input limpio
def get_non_negative_int(prompt, min, max):
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print(">> Perdón, no entendi el input")
            continue

        if value < min or value > max:
            print(">> Perdón, numero no esta dentro del rango permitido")
            continue
        else:
            break
    return value


class Carta:
    cont_interno = 0

    def __init__(self, nombre, valor_truco):
        Carta.cont_interno += 1
        self.ID = Carta.cont_interno
        self.Nombre = nombre
        self.ValorTruco = valor_truco

    def __repr__(self):
        # override print() oupput a consola
        return ("ID:" + str(self.ID) + ", " + self.Nombre + ", vt:" + str(self.ValorTruco))

    def __str__(self):  # python
        # override del str()
        return ("ID:" + str(self.ID) + ", " + self.Nombre + ", vt:" + str(self.ValorTruco))

    def __eq__(self, other):
        return self.ID == other.ID

    @staticmethod
    def ResetContCarta():
        Carta.cont_interno = 0

class Reglas:
    MAZO = GenerarMazo()
    ACCIONES = GenerarAcciones()
    Reparto_fijo = []
    JUGADOR1 = 1
    JUGADOR2 = 2


    @staticmethod
    def RepartirCartas():
        # SEEDING
        # from numpy.random import seed
        # seed(1)

        mazo = Reglas.MAZO[:]
        cartas_j1 = []
        cartas_j2 = []
        while len(cartas_j1) < 3:
            unaC = random.choice(mazo)
            cartas_j1.append(unaC)
            mazo.remove(unaC)
        while len(cartas_j2) < 3:
            unaC = random.choice(mazo)
            cartas_j2.append(unaC)
            mazo.remove(unaC)
        return cartas_j1, cartas_j2




    @staticmethod
    def RepartirCartasDEBUG(): # Reparte siempre la misma mano para hacer debugging
        mazo = Reglas.MAZO[:]
        cartas_j1 = []
        cartas_j2 = []
        cartas_j1.append(mazo[8])
        cartas_j1.append(mazo[4])
        cartas_j1.append(mazo[2])
        cartas_j2.append(mazo[7])
        cartas_j2.append(mazo[5])
        cartas_j2.append(mazo[0])

        return cartas_j1, cartas_j2

class Agente:
    def __init__(self, jugador, eps=0.2, alpha=0.5, gamma=0.9):
        self.cartas_totales = []
        self.cartas_restantes = []
        self.eps = eps  # probability of choosing random action instead of greedy
        self.alpha = alpha  # learning rate
        self.gamma = gamma  # discount factor
        self.state_history = []
        self.Q = {}
        self.s_cartas = "000"
        if jugador == Reglas.JUGADOR1:
            self.jugador = Reglas.JUGADOR1
        elif jugador == Reglas.JUGADOR2:
            self.jugador = Reglas.JUGADOR2
        elif jugador != self.jugador:
            self.jugador = None
            assert self.jugador is not None

    def Save_Q_to_Disk(self, filename):
        # Store data (serialize)
        with open(filename, 'wb') as handle:
            pickle.dump(self.Q, handle)

    def Load_Q_From_Disk(self, filename):
        # Load data (deserialize)
        with open(filename, 'rb') as handle:
            self.Q = pickle.load(handle)

    def ZeroRatio_en_Q(self, DEBUG=False):
        cont_ceros = 0
        cont_non_cero = 0

        for i in self.Q.values():
            for j in i:
                # print("output.  i:" + str(j) + "    j: " +str(i[j]))
                if i[j] == 0:
                    cont_ceros = cont_ceros + 1
                else:
                    cont_non_cero = cont_non_cero + 1

        if DEBUG: print("Elementos totales contados = " + str(cont_ceros + cont_non_cero) + " , subtotal NO en cero = " + str(cont_non_cero))
        #if DEBUG: print("De ellos, cantidad en cero = " + str(cont_ceros))
        if DEBUG: print("Ratio en cero: " + str(cont_ceros/ (cont_ceros + cont_non_cero)))

        return cont_ceros*100 / (cont_ceros + cont_non_cero)

    def EjecutarAccion(self, s, a):
        r = -1 #  Todo lo que no sea ganar lleva reward negativo (para evitar que empate le de igual)

        carta_propuesta = self.cartas_totales[int(a)-1]
        if s == "0":
            sp = str(carta_propuesta.ID)
        else:
            sp = s + str(carta_propuesta.ID)

        # Seteo reward segun estado resultante sp
        ganador = QuienGano(sp)
        if ganador == self.jugador:
            r = 1
        elif str(ganador) == "0":
            r = 0
        elif ganador is None:
            r = 0

        return sp, r

    def Elegir_Accion(self, s, debug=False):
        # choose an action based on epsilon-greedy strategy
        r = np.random.rand()

        s_total = self.s_cartas + s

        if r < self.eps:
            # take a random action
            if debug: printDebug("  Taking a random action")
            idx = np.random.choice(len(self.cartas_restantes))  # random 0,1 y 2
            carta_resultado = self.cartas_restantes[idx]
            id_carta_resultado = carta_resultado.ID
            a = self.cartas_totales.index(carta_resultado) +1
        else:
            #Falta agregar que sea una accion de las cartas restantes
            maxQvalue = -100000
            for i in self.cartas_restantes:
                accion_propuesta = self.cartas_totales.index(i) + 1  # a = la posicion de la carta en la mano
                if self.Q[int(s_total)][accion_propuesta] > maxQvalue:  # Greedy, siempre toma la mas alta (determinista fuera de training)
                    a = accion_propuesta
                    id_carta_resultado = i.ID
                    maxQvalue = self.Q[int(s_total)][accion_propuesta]

        #quitamos la carta
        self.cartas_restantes.remove(self.cartas_totales[a - 1])
        if debug: printDebug("      ## Jugador " + str(self.jugador) + " evaluando Carta con ID:" + str(id_carta_resultado))
        return a


    def TomarCartas(self, listaCartas, debug=False):
        self.cartas_totales = []
        self.cartas_restantes = []
        self.s_cartas = ""

        # Aqui asignamos las cartas al jugador en orden que coincide con el diseño de acciones
        listaCartas.sort(key=lambda x: x.ValorTruco, reverse=True)
        for i in listaCartas:
            self.s_cartas = self.s_cartas + str(i.ID)
            self.cartas_restantes.append(i)
            self.cartas_totales.append(i)
        if debug: printDebug(str(self.cartas_restantes))


    def InicializarQ(self):
        # initialize Q(s,a)
        self.Q = {}
        # Primero agrego el estado vacio
        self.Q[0] = {}
        for a in GenerarAcciones():
            self.Q[0][int(a)] = 0

        total = len(GetAllStatesCodes(Reglas.MAZO[:], 3))
        cont = 0
        # Primero genero las manos posibles con 3 cartas
        for m in GetAllStatesCodes(Reglas.MAZO[:], 3):
            cont = cont+1
            print("\r" + str((cont / total) * 100)[0:5] + " % inicializando Q de p" + str(self.jugador), end="")

            #primero agrego los subvacios
            self.Q[int(str(m) + "0")] = {}
            for a in GenerarAcciones():
                self.Q[int(str(m)+"0")][int(a)] = 0

            # Luego agrego todos los otros estados
            for i in range(5):  # son 6 jugadas, 3 por jugador pero solo agrego estados no terminales
                for s in GetAllStatesCodes(Reglas.MAZO[:], i + 1):
                    self.Q[int(str(m)+str(s))] = {}
                    for a in GenerarAcciones():
                        self.Q[int(str(m)+str(s))][int(a)] = 0 # deberia iniciar en cero pero pruebo con 1 para optimistic initial values
        print("")

class Humano:
    def __init__(self, jugador):
        self.cartas_totales = []
        self.cartas_restantes = []
        self.s_cartas = ""
        self.eps = 0
        if jugador == Reglas.JUGADOR1:
            self.jugador = Reglas.JUGADOR1
        elif jugador == Reglas.JUGADOR2:
            self.jugador = Reglas.JUGADOR2
        elif jugador != self.jugador:
            self.jugador = None
            assert self.jugador is not None

    def EjecutarAccion(self, s, a):
        r = -1

        carta_propuesta = self.cartas_totales[int(a) - 1]
        if s == "0":
            sp = str(carta_propuesta.ID)
        else:
            sp = s + str(carta_propuesta.ID)

        # Seteo reward segun estado resultante sp
        ganador = QuienGano(sp)
        if ganador == self.jugador:
            r = 1
        elif str(ganador) == "0":
            r = 0
        elif ganador is None:
            r = 0

        return sp, r

    def Elegir_Accion(self, unS, debug=False):
        # choose an action based on epsilon-greedy strategy

        print("")
        print("###  HUMANO, p" + str(self.jugador)+ "  ###")
        if unS == "0":
            print("   Debes elegir accion! el estado actual es: 0 (no se ha jugado ninguna carta aun)" )
        else:
            print("   Debes elegir accion! el estado actual es: " + unS + "  (ultima carta jugada: " + str(LoadEstado_FromHash(unS)[-1])+" )")
        print("   Te quedan las sigueintes cartas: " + str(self.cartas_restantes))
        print("")
        move = int(get_non_negative_int("   Ingrese accion (posicion array 0,1,2): ",0,len(self.cartas_restantes)-1))
        carta = self.cartas_restantes[move]
        print("   Jugando carta: " + str(carta))
        a = self.cartas_totales.index(carta) + 1  # a = la posicion de la carta en la mano

        # quitamos la carta
        self.cartas_restantes.remove(self.cartas_totales[a - 1])

        return a

    def TomarCartas(self, listaCartas, debug=False):
        self.cartas_totales = []
        self.cartas_restantes = []
        # Aqui asignamos las cartas al jugador en orden que coincide con el diseño de acciones
        listaCartas.sort(key=lambda x: x.ValorTruco, reverse=True)
        for i in listaCartas:
            self.cartas_restantes.append(i)
            self.cartas_totales.append(i)
        if debug: printDebug(str(self.cartas_restantes))

class AgenteRandom:
    def __init__(self, jugador):
        self.cartas_totales = []
        self.cartas_restantes = []
        self.eps = 1  # probability of choosing random action instead of greedy
        self.alpha = 0.5  # learning rate
        self.gamma = 0.9 # discount factor
        self.s_cartas = "000"
        self.state_history = []
        self.Q = {}
        if jugador == Reglas.JUGADOR1:
            self.jugador = Reglas.JUGADOR1
        elif jugador == Reglas.JUGADOR2:
            self.jugador = Reglas.JUGADOR2
        elif jugador != self.jugador:
            self.jugador = None
            assert self.jugador is not None


    def EjecutarAccion(self, s, a):
        r = -1 #  Todo lo que no sea ganar lleva reward negativo (para evitar que empate le de igual)

        carta_propuesta = self.cartas_totales[int(a)-1]
        if s == "0":
            sp = str(carta_propuesta.ID)
        else:
            sp = s + str(carta_propuesta.ID)

        # Seteo reward segun estado resultante sp
        ganador = QuienGano(sp)
        if ganador == self.jugador:
            r = 1
        elif str(ganador) == "0":
            r = 0
        elif ganador is None:
            r = 0

        return sp, r

    def Elegir_Accion(self, unS, debug=False):

        # take a random action
        idx = np.random.choice(len(self.cartas_restantes))  # random 0,1 y 2
        carta_resultado = self.cartas_restantes[idx]
        id_carta_resultado = carta_resultado.ID
        a = self.cartas_totales.index(carta_resultado) +1

        #quitamos la carta de la mano
        self.cartas_restantes.remove(self.cartas_totales[a - 1])

        if debug: printDebug("      ## Jugador " + str(self.jugador) + " (Taking a random action) evaluando Carta con ID:" + str(id_carta_resultado))
        return a


    def TomarCartas(self, listaCartas, debug=False):
        self.cartas_totales = []
        self.cartas_restantes = []
        self.s_cartas = ""
        # Aqui asignamos las cartas al jugador en orden que coincide con el diseño de acciones
        listaCartas.sort(key=lambda x: x.ValorTruco, reverse=True)
        for i in listaCartas:
            self.s_cartas = self.s_cartas + str(i.ID)
            self.cartas_restantes.append(i)
            self.cartas_totales.append(i)
        if debug: printDebug(str(self.cartas_restantes))

    def InicializarQ(self):
        # initialize Q(s,a)
        self.Q = {}
        # Primero agrego el estado vacio
        self.Q[0] = {}
        for a in GenerarAcciones():
            self.Q[0][int(a)] = 0

        total = len(GetAllStatesCodes(Reglas.MAZO[:], 3))
        cont = 0
        # Primero genero las manos posibles con 3 cartas
        for m in GetAllStatesCodes(Reglas.MAZO[:], 3):
            cont = cont + 1
            print("\r" + str((cont / total) * 100)[0:5] + " % inicializando Q de p" + str(self.jugador), end="")

            # primero agrego los subvacios
            self.Q[int(str(m) + "0")] = {}
            for a in GenerarAcciones():
                self.Q[int(str(m) + "0")][int(a)] = 0

            # Luego agrego todos los otros estados
            for i in range(5):  # son 6 jugadas, 3 por jugador pero solo agrego estados no terminales
                for s in GetAllStatesCodes(Reglas.MAZO[:], i + 1):
                    self.Q[int(str(m) + str(s))] = {}
                    for a in GenerarAcciones():
                        self.Q[int(str(m) + str(s))][int(a)] = 0  # deberia iniciar en cero pero pruebo con 1 para optimistic initial values
        print("")