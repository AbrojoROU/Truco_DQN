# OPTIMISTIC INITIAL VALUES

import numpy as np
import inspect
import random
from enum import Enum
import pickle
import itertools
import json
import matplotlib.pyplot as plt
# %matplotlib inline

import time

# FUNCIONES A NIVEL MODULO
global start_timer
start_timer = time.time()

def printDebug(debugMsg):
    print("   #debug@ " + str(debugMsg) + "   ## " + str(inspect.stack()[1][3]) + "() " + "  ## T=" + str(time.time() - start_timer)[0:7] + "s" )
    return

# Inicializa el mazo en Reglas
def GenerarMazo():
    # Formato Cartas ID, Nombre, ValorTruco
    # Solucion final sera con 9 cartas (reduce statespace y permite codificar en base 10) tomadas al azar de las 40
    Carta.ResetContCarta()
    MAZO = []
    MAZO.append(Carta("carta nula", 0))  # ID: 0
    MAZO.append(Carta("4-Copa", 10))  # ID: 1
    MAZO.append(Carta("6-Copa", 20))  # ID: 2
    MAZO.append(Carta("6-Basto", 20))  # ID: 3
    MAZO.append(Carta("11-Copa", 30))  # ID: 4
    MAZO.append(Carta("11-Basto", 30))  # ID: 5
    MAZO.append(Carta("2-Basto", 40))  # ID: 6
    MAZO.append(Carta("2-Copa", 40))  # ID: 7
    MAZO.append(Carta("1-Basto", 80))  # ID: 8
    MAZO.append(Carta("1-Espada", 100))  # ID: 9
    return MAZO


class Carta:
    cont_interno = 0

    def __init__(self, nombre, valor_truco):
        self.ID = Carta.cont_interno
        self.Nombre = nombre
        self.ValorTruco = valor_truco
        Carta.cont_interno += 1

    def __repr__(self):
        # override print() oupput a consola
        return "ID:" + str(self.ID) + ", " + self.Nombre + ", vt:" + str(self.ValorTruco)

    def __str__(self):  # python
        # override del str()
        return "ID:" + str(self.ID) + ", " + self.Nombre + ", vt:" + str(self.ValorTruco)

    def __eq__(self, other):
        return self.ID == other.ID

    @staticmethod
    def ResetContCarta():
        Carta.cont_interno = 0

class Reglas:
    # Variables de Clase
    MAZO = GenerarMazo()
    Reparto_fijo = []
    JUGADOR1 = 1
    JUGADOR2 = 2


    class Accion(Enum):
        FOLD = 0  # FOLD (irme / rechazar apuesta)
        JUGAR_C1 = 1  # Jugar Carta mas alta
        JUGAR_C2 = 2  # Jugar 2da Carta mas alta
        JUGAR_C3 = 3  # Jugar 3ra Carta mas alta
        QUIERO_GRITO = 4  # Acetpar Grito/apuesta Truco
        GRITAR_TRUCO = 5
        GRITAR_RETRUCO = 6
        GRITAR_VALE4 = 7

    class EstadoTruco(Enum):
        NADA_DICHO = 0
        TRUCO_DICHO = 1
        TRUCO_ACEPTADO = 2
        RETRUCO_DICHO = 3
        RETRUCO_ACEPTADO = 4
        VALE4_DICHO = 5
        VALE4_ACEPTADO = 6
        FOLD = 7

    @staticmethod
    def RepartirCartas():
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

class Agente:
    def __init__(self, jugador):

        self.cartas_totales = []
        self.cartas_restantes = []
        self.state_history = []

        if jugador == Reglas.JUGADOR1:
            self.jugador = Reglas.JUGADOR1
        elif jugador == Reglas.JUGADOR2:
            self.jugador = Reglas.JUGADOR2
        elif jugador != self.jugador:
            self.jugador = None
            assert self.jugador is not None

    def TomarCartas(self, listaCartas, debug=False):
        self.cartas_totales = []
        self.cartas_restantes = []

        # Aqui asignamos las cartas al jugador en orden que coincide con el diseño de acciones
        listaCartas.sort(key=lambda x: x.ValorTruco, reverse=True)
        for i in listaCartas:
            self.cartas_restantes.append(i)
            self.cartas_totales.append(i)
        if debug: printDebug(str(self.cartas_restantes))

    def get_acciones_posibles(self,s):
        # Este metodo construye y retorna el vector de acciones posibles (tomados del enum Reglas.Acciones) con base en el estado actual s
        result = []
        result.append(Reglas.Accion.FOLD)

        if s.QuienJugariaCarta() == self.jugador: # me toca
            # Opciones de Truco : si me gritaron, agregar las acciones de aceptar (call) y subir apuesta (raise)
            if s.truco is Reglas.EstadoTruco.TRUCO_ACEPTADO :
                for j, a in s.acciones_hechas:
                    if (a is Reglas.Accion.GRITAR_TRUCO) and (j is not self.jugador): result.append(Reglas.Accion.GRITAR_RETRUCO)

            elif s.truco is Reglas.EstadoTruco.RETRUCO_ACEPTADO :
                for j, a in s.acciones_hechas:
                    if (a is Reglas.Accion.GRITAR_RETRUCO) and (j is not self.jugador): result.append(Reglas.Accion.GRITAR_VALE4)

            elif s.truco == Reglas.EstadoTruco.NADA_DICHO: result.append(Reglas.Accion.GRITAR_TRUCO)

            else:
                assert False  # WARNING: Si me toca, el estado del truco deberia estar en alguno case de los elif

            # solo resta agregar las acciones de jugar cartas aun en mano
            for c in self.cartas_restantes:
                result.append(Reglas.Accion(self.cartas_totales.index(c) + 1))

        else:
            # No me toca jugar carta, seguramente me gritaron
            if s.truco is Reglas.EstadoTruco.TRUCO_DICHO:
                result.append(Reglas.Accion.QUIERO_GRITO)
                result.append(Reglas.Accion.GRITAR_RETRUCO)
            elif s.truco is Reglas.EstadoTruco.RETRUCO_DICHO :
                result.append(Reglas.Accion.QUIERO_GRITO)
                result.append(Reglas.Accion.GRITAR_VALE4)
            elif s.truco == Reglas.EstadoTruco.VALE4_DICHO:
                result.append(Reglas.Accion.QUIERO_GRITO)


        return result

    def Elegir_Accion_Random(self, s, debug=False):
        a_posibles = self.get_acciones_posibles(s)

        # choose a random action
        if debug: printDebug("  Taking a random action")
        idx = np.random.choice(len(a_posibles))
        a = a_posibles[idx]

        return a

    # Ejecuta la accion que le llega, actualizando el estado y el agente de forma acorde
    def EjecutarAccion(self, s, a):

        if a is Reglas.Accion.FOLD: s.truco = Reglas.EstadoTruco.FOLD

        if a is Reglas.Accion.GRITAR_TRUCO: s.truco = Reglas.EstadoTruco.TRUCO_DICHO
        if a is Reglas.Accion.GRITAR_RETRUCO: s.truco = Reglas.EstadoTruco.RETRUCO_DICHO
        if a is Reglas.Accion.GRITAR_VALE4: s.truco = Reglas.EstadoTruco.VALE4_DICHO

        if a is Reglas.Accion.QUIERO_GRITO:
            if s.truco is Reglas.EstadoTruco.TRUCO_DICHO: s.truco = Reglas.EstadoTruco.TRUCO_ACEPTADO
            elif s.truco is Reglas.EstadoTruco.RETRUCO_DICHO: s.truco = Reglas.EstadoTruco.RETRUCO_ACEPTADO
            elif s.truco is Reglas.EstadoTruco.VALE4_DICHO: s.truco = Reglas.EstadoTruco.VALE4_DICHO
            else: assert False # No es posible pasar por aca, si quiso un grito es porque habia un truco, retruco o vale4 dicho

        if a is Reglas.Accion.JUGAR_C1:
            c = self.cartas_totales[0]
            assert c in self.cartas_restantes # valido que la carta a jugar aun esta en mi mano
            s.cartas_jugadas.append(c)  # actualizo el estado
            self.cartas_restantes.remove(c)  # la quito de las cartas restantes

        if a is Reglas.Accion.JUGAR_C2:
            c = self.cartas_totales[1]
            assert c in self.cartas_restantes # valido que la carta a jugar aun esta en mi mano
            s.cartas_jugadas.append(c)  # actualizo el estado
            self.cartas_restantes.remove(c)  # la quito de las cartas restantes

        if a is Reglas.Accion.JUGAR_C3:
            c = self.cartas_totales[2]
            assert c in self.cartas_restantes # valido que la carta a jugar aun esta en mi mano
            s.cartas_jugadas.append(c)  # actualizo el estado
            self.cartas_restantes.remove(c)  # la quito de las cartas restantes

        # finalmente agrego la accion al log de acciones hechas por el estado
        s.acciones_hechas.append((self.jugador, a))


class Estado:
    def __init__(self):
        self.cartas_jugadas = []
        self.truco = Reglas.EstadoTruco.NADA_DICHO
        self.acciones_hechas = []

    def reset(self):
        self.cartas_jugadas = []
        self.truco = Reglas.EstadoTruco.NADA_DICHO

    def QuienActua(self):

        if self.truco is Reglas.EstadoTruco.FOLD: return None

        if (self.truco is Reglas.EstadoTruco.NADA_DICHO) or (self.truco is Reglas.EstadoTruco.TRUCO_ACEPTADO) or \
                (self.truco is Reglas.EstadoTruco.RETRUCO_ACEPTADO) or (self.truco is Reglas.EstadoTruco.VALE4_ACEPTADO) :
            # si no hay pendiente de grito (nada gritado o se aceptó_todo), retornar quien jugaria carta
            return self.QuienJugariaCarta()
        else:
            # Si el estado es que hay algo gritado, devolver el opuesto del juegador que lo grito
            j, a = self.acciones_hechas[-1]  # j es el jugador, a es la acion,  -1 toma la ultima accion hecha
            assert ((a is Reglas.Accion.GRITAR_TRUCO) or (a is Reglas.Accion.GRITAR_RETRUCO) or (a is Reglas.Accion.GRITAR_VALE4)) # efectivamente la ultima accion fue un grito
            if j is Reglas.JUGADOR1 : return Reglas.JUGADOR2
            if j is Reglas.JUGADOR2 : return Reglas.JUGADOR1


    def QuienJugariaCarta(self):
        cartas_jugadas = self.cartas_jugadas

        # Estamos en primera Mano
        if len(cartas_jugadas) == 0:
            return Reglas.JUGADOR1
        if len(cartas_jugadas) == 1:
            return Reglas.JUGADOR2

        # En 2da mano
        if len(cartas_jugadas) == 2:
            if cartas_jugadas[0].ValorTruco >= cartas_jugadas[1].ValorTruco:
                return Reglas.JUGADOR1
            if cartas_jugadas[0].ValorTruco < cartas_jugadas[1].ValorTruco:
                return Reglas.JUGADOR2
        if len(cartas_jugadas) == 3:
            if cartas_jugadas[0].ValorTruco >= cartas_jugadas[1].ValorTruco:
                return Reglas.JUGADOR2
            if cartas_jugadas[0].ValorTruco < cartas_jugadas[1].ValorTruco:
                return Reglas.JUGADOR1

        # En 3ra mano
        if len(cartas_jugadas) == 4 or len(cartas_jugadas) == 5:
            # primero calculo resultados primeras dos manos y los guardo
            j1_gano_1raMano = cartas_jugadas[0].ValorTruco >= cartas_jugadas[1].ValorTruco
            if j1_gano_1raMano:
                # si j1 gano la 1ra mano, con empatar ya "gana" la 2da mano tambien (en el sentido de que mantiene el "saque")
                j1_gano_2daMano = cartas_jugadas[2].ValorTruco >= cartas_jugadas[3].ValorTruco
            else:
                # si j1 perdio la primer mano, entonces j1 esta obligado a ganar para para recuperar el "saque"
                j1_gano_2daMano = cartas_jugadas[2].ValorTruco < cartas_jugadas[3].ValorTruco

            # ahora aplico reglas
            if len(cartas_jugadas) == 4:
                if j1_gano_2daMano:
                    return Reglas.JUGADOR1
                else:
                    return Reglas.JUGADOR2
            if len(cartas_jugadas) == 5:
                if j1_gano_2daMano:
                    return Reglas.JUGADOR2
                else:
                    return Reglas.JUGADOR1

        return None

    def QuienGanoEpisodio(self):
        # Primero veo si alguien hizo Fold
        for j, a in self.acciones_hechas:
            if a is Reglas.Accion.FOLD:
                if j is Reglas.JUGADOR1: return Reglas.JUGADOR2
                if j is Reglas.JUGADOR2: return Reglas.JUGADOR1

        # Si no hay Fold, quizas se jugaron todas las manos (este ya devuelve None si no se jugaron 6 cartas aun)
        return self.QuienGanoManos()


    def QuienGanoManos(self):
        # Calcula quien gano las manos, puede retornar:
        # Reglas.JUGADOR1 or JUGADOR2
        # "None" si no se jugaron todas las manos aun (en esta nueva version esto rara vez se deberia usar, es parte de estado S)
        # 0 si es un triple empate en las 3 manos

        puntos_j1 = 0
        puntos_j2 = 0
        cartas_jugadas = self.cartas_jugadas

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

            # MANO 3
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
        else:  # igualados en puntos con 6 cartas jugadas
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

        assert False # no deberia llegar aqui


class Motor:

    @staticmethod
    def Construir_Lista_Cartas(lista_id_cartas):
        result = []

        for i in lista_id_cartas:
            result.append(Reglas.MAZO[int(i)])

        return result

    @staticmethod
    def Play_random_games(p1, p2, N, DEBUG):
        # SEEDING
        from numpy.random import seed
        seed(1)

        # Declaro variables de monitoreo
        cont_win_p1 = 0
        cont_win_p2 = 0
        cont_empate = 0

        s = Estado()

        for i in range(N):
            if DEBUG: printDebug("EPISODIO #" + str(i + 1) + "   ")

            # SETUP INICIAL repartir cartas
            cartas_p1, cartas_p2 = Reglas.RepartirCartas()
            p1.TomarCartas(cartas_p1)
            p2.TomarCartas(cartas_p2)
            s.reset()

            if DEBUG: printDebug("  Cartas Jugador 1: " + str(p1.cartas_totales))
            if DEBUG: printDebug("  Cartas Jugador 2: " + str(p2.cartas_totales))

            # Accion inicial
            current_player = p1
            a = p1.Elegir_Accion_Random(s, DEBUG)

            # loops until the game is over
            while (s.QuienGanoManos() is None) and (s.truco is not Reglas.EstadoTruco.FOLD) :

                sp, r = current_player.EjecutarAccion(s, a)
                if DEBUG: printDebug("      Nuevo estado: " + sp + ", con recompensa: " + str(r))

                # Tomo otro jugador
                if sp.QuienJugariaCarta() == Reglas.JUGADOR1:
                    next_player = p1
                else:
                    next_player = p2

                # Ahora calculo Q_Next, 4 opciones:  Terminal Gane, Terminal empate, Terminal Perdi o No terminal y propago
                if len(sp) == 6:
                    quien_gano = sp.QuienGanoManos()
                    assert (quien_gano is not None)  # imposible resultado None, debe ser 1, 2 o 0
                    if DEBUG: printDebug("- Partida terminada nro:" + str(i) + " s:" + sp)
                    if quien_gano == Reglas.JUGADOR1:
                        # Caso 1: terminal gané
                        if DEBUG: printDebug(" GANE! (jugador 1, s:" + sp)
                        cont_win_p1 = cont_win_p1 + 1
                    elif quien_gano == 0:
                        # Caso 2: terminal empate
                        if DEBUG: printDebug(" EMPATE!  s:" + sp)
                        cont_empate = cont_empate + 1
                    elif quien_gano == Reglas.JUGADOR2:
                        # Caso 3: terminal perdí
                        if DEBUG: printDebug(" GANE! (jugador 2, s:" + sp)
                        cont_win_p2 = cont_win_p2 + 1
                else:
                    # Caso no terminal, propago Q
                    ap = next_player.Elegir_Accion(sp, DEBUG)
                    #Q_Next = ...

                # Finalmente alterno jugador
                if sp.QuienJugariaCarta() == Reglas.JUGADOR1:
                    if DEBUG and type(current_player) is Agente: printDebug("JUGADOR:" + str(current_player.jugador) + " hace UPDATE de Q[" + str(current_player.s_cartas+s) + "][" + str(a) + "] = " + str(current_player.Q[int(current_player.s_cartas +s)][a])+ " y r:" + str(r))
                    current_player = p1
                else:
                    current_player = p2
                s = sp
                a = ap
            # Terminó el while gameover
        # Terminó el for N

        # Despliego resultados de la corrida
        winratio = cont_win_p1*100/(cont_win_p1+cont_win_p2+cont_empate)
        print("## RESULTADO ##  N= " + str(N) + " - j1: " + str(cont_win_p1) + ", j2: " + str(cont_win_p2) + ", Empates: " + str(cont_empate) + ", WINRATIO:"+ str(winratio)[0:5]+", S final: " + str(s))
        if DEBUG:
            if type(p1) is Agente : print("j1 - Q[0]: " + str(p1.Q[0]))
            for i in p1.cartas_totales:
                if type(p2) is Agente : print("j2 - Q[" + str(i.ID) + "]: " + str(p2.Q[i.ID]))

        return winratio

