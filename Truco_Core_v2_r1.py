# OPTIMISTIC INITIAL VALUES

import numpy as np
import inspect
import random
import copy
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
    MAZO.append(Carta("carta nula", 0))  # ID: 0 para que Carta.ID = Mazo[index]
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
        JUGAR_C1 = 1  # Jugar Carta mas alta
        JUGAR_C2 = 2  # Jugar 2da Carta mas alta
        JUGAR_C3 = 3  # Jugar 3ra Carta mas alta
        QUIERO_GRITO = 4  # Acetpar Grito/apuesta Truco
        GRITAR_TRUCO = 5
        GRITAR_RETRUCO = 6
        GRITAR_VALE4 = 7
        FOLD = 8  # FOLD (irme / rechazar apuesta)

    class EstadoTruco(Enum):
        NADA_DICHO = 1
        TRUCO_DICHO = 2
        TRUCO_ACEPTADO = 3
        RETRUCO_DICHO = 4
        RETRUCO_ACEPTADO = 5
        VALE4_DICHO = 6
        VALE4_ACEPTADO = 7
        FOLD = 8


    @staticmethod
    def RepartirCartas():
        mazo = Reglas.MAZO[:]
        cartas_j1 = []
        cartas_j2 = []
        while len(cartas_j1) < 3:
            unaC = random.choice(mazo)
            if not unaC.ID == 0: # que no sea la carta nula
                cartas_j1.append(unaC)
                mazo.remove(unaC)
        while len(cartas_j2) < 3:
            unaC = random.choice(mazo)
            if not unaC.ID == 0: # que no sea la carta nula
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

            elif s.truco == Reglas.EstadoTruco.VALE4_ACEPTADO : pass

            else:
                assert False  # WARNING: Si me toca, el estado del truco deberia estar en alguno case de los elif, a menos que permita Re-Raise

            # solo resta agregar las acciones de jugar cartas aun en mano
            for c in self.cartas_restantes:
                result.append(Reglas.Accion(self.cartas_totales.index(c) + 1))

        else:
            # No me toca jugar carta, seguramente me gritaron
            if s.truco is Reglas.EstadoTruco.TRUCO_DICHO:
                result.append(Reglas.Accion.QUIERO_GRITO)
                #result.append(Reglas.Accion.GRITAR_RETRUCO)  # Por ahora no permitimos Re-Raise
            elif s.truco is Reglas.EstadoTruco.RETRUCO_DICHO :
                result.append(Reglas.Accion.QUIERO_GRITO)
                #result.append(Reglas.Accion.GRITAR_VALE4)  # Por ahora no permitimos Re-Raise
            elif s.truco == Reglas.EstadoTruco.VALE4_DICHO:
                result.append(Reglas.Accion.QUIERO_GRITO)


        return result

    def Elegir_Accion_Random(self, s, debug=False):
        a_posibles = self.get_acciones_posibles(s)
        if debug: printDebug("  acciones posibles: " + str(a_posibles))
        # choose a random action
        idx = np.random.choice(len(a_posibles))
        a = a_posibles[idx]

        ## COMIENZA HACK para reducir probabilidad de Fold (quitar esta seccion si se quiere igual prob
        if a is Reglas.Accion.FOLD: # si salio Fold que trate de nuevo (si sale de vuelta, bueno que salga)
            # choose a random action
            idx = np.random.choice(len(a_posibles))
            a = a_posibles[idx]
        if a is Reglas.Accion.FOLD:  # si salio Fold que trate de nuevo (si sale de vuelta, bueno que salga)
            # choose a random action
            idx = np.random.choice(len(a_posibles))
            a = a_posibles[idx]
        ## TERMINA HACK para reducir probabilidad de Fold

        if debug: printDebug("  Taking a random action: " + str(a))

        return a

    # Ejecuta la accion que le llega, actualizando el estado y el agente de forma acorde
    def EjecutarAccion(self, s, a, DEBUG=False):

        if a is Reglas.Accion.FOLD: s.truco = Reglas.EstadoTruco.FOLD

        if a is Reglas.Accion.GRITAR_TRUCO: s.truco = Reglas.EstadoTruco.TRUCO_DICHO
        if a is Reglas.Accion.GRITAR_RETRUCO: s.truco = Reglas.EstadoTruco.RETRUCO_DICHO
        if a is Reglas.Accion.GRITAR_VALE4: s.truco = Reglas.EstadoTruco.VALE4_DICHO

        if a is Reglas.Accion.QUIERO_GRITO:
            if s.truco is Reglas.EstadoTruco.TRUCO_DICHO: s.truco = Reglas.EstadoTruco.TRUCO_ACEPTADO
            elif s.truco is Reglas.EstadoTruco.RETRUCO_DICHO: s.truco = Reglas.EstadoTruco.RETRUCO_ACEPTADO
            elif s.truco is Reglas.EstadoTruco.VALE4_DICHO: s.truco = Reglas.EstadoTruco.VALE4_ACEPTADO
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
        if DEBUG : printDebug("  p" + str(self.jugador) + " - ejecutando accion: " + str(a))
        s.acciones_hechas.append((self.jugador, a))

class Episodio:
    def __init__(self):
        self.estados = []
        self.ganador = None # 4 estados posibles. None si nadie, 0 si empate, p1  o p2
        self.p1 = None
        self.p2 = None

class Estado:
    def __init__(self):
        self.cartas_jugadas = []
        self.truco = Reglas.EstadoTruco.NADA_DICHO
        self.acciones_hechas = []

    def __repr__(self):
        # override print() oupput a consola
        return " ## cartas jugadas:" + str(self.cartas_jugadas) + ", estado:" + self.truco.name + ", acciones:" + str(self.acciones_hechas) + " ##"

    def __str__(self):  # python
        # override del str()
        return " Partida, cartas jugadas:" + str(self.cartas_jugadas) + ", estado:" + self.truco.name + ", acciones:" + str(self.acciones_hechas)

    def get_last_action_from_player(self, jugador):
        # Devuelve la ultima accion de un jugador
        for i in reversed(self.acciones_hechas):
            if i[0] == jugador:
                return i[1]


    def reset(self):
        self.cartas_jugadas = []
        self.truco = Reglas.EstadoTruco.NADA_DICHO
        self.ganador = None  # 4 estados posibles. None si nadie, 0 si empate, p1  o p2
        self.acciones_hechas = []

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
        # from numpy.random import seed
        # seed(1)

        lista_episodios = []

        # Declaro variables de monitoreo
        cont_win_p1 = 0
        cont_win_p2 = 0
        cont_empate = 0

        for i in range(N):
            if DEBUG: printDebug("EPISODIO #" + str(i + 1) + "   ")

            e = Episodio()
            s = Estado()

            # SETUP INICIAL repartir cartas
            cartas_p1, cartas_p2 = Reglas.RepartirCartas()
            p1.TomarCartas(cartas_p1)
            p2.TomarCartas(cartas_p2)
            e.p1 = p1
            e.p2 = p2

            if DEBUG: printDebug("  Cartas Jugador 1: " + str(p1.cartas_totales))
            if DEBUG: printDebug("  Cartas Jugador 2: " + str(p2.cartas_totales))

            # Accion inicial
            current_player = p1
            a = p1.Elegir_Accion_Random(s, False)

            # loops until the game is over
            while (s.QuienGanoManos() is None) and (s.truco is not Reglas.EstadoTruco.FOLD) :

                current_player.EjecutarAccion(s, a, DEBUG)
                if DEBUG: printDebug("      Nuevo estado: " + str(s.cartas_jugadas))

                # Tomo otro jugador
                if s.QuienActua() == Reglas.JUGADOR1:
                    next_player = p1
                else:
                    next_player = p2

                # Me fijo si termino, 4 opciones:  Terminal Gane, Terminal empate, Terminal Perdi o No terminal y propago
                if s.QuienGanoEpisodio() is not None:
                    quien_gano = s.QuienGanoEpisodio()

                    if DEBUG: printDebug("- Partida terminada nro:" + str(i+1) + " s:" + str(s.cartas_jugadas))
                    if quien_gano == Reglas.JUGADOR1:
                        # Caso 1: terminal gané
                        if DEBUG: printDebug(" GANE! (jugador 1)")
                        e.ganador = Reglas.JUGADOR1
                        cont_win_p1 = cont_win_p1 + 1
                    elif quien_gano == 0:
                        # Caso 2: terminal empate
                        if DEBUG: printDebug(" EMPATE! ")
                        cont_empate = cont_empate + 1
                        e.ganador = 0
                    elif quien_gano == Reglas.JUGADOR2:
                        # Caso 3: terminal perdí
                        if DEBUG: printDebug(" GANE! (jugador 2)")
                        e.ganador = Reglas.JUGADOR2
                        cont_win_p2 = cont_win_p2 + 1
                else:
                    # Caso no terminal
                    a = next_player.Elegir_Accion_Random(s, False)

                # Finalmente alterno jugador
                if s.QuienActua() == Reglas.JUGADOR1:
                    current_player = p1
                else:
                    current_player = p2
                #Termino la mano
                e.estados.append(copy.deepcopy(s))  # Agrego el estado intermedio al episodio

            # Terminó el while gameover
            lista_episodios.append(e)  # Agrego el episodio a la lista de episodios
            if DEBUG : print("")
        # Terminó el for N

        # Despliego resultados de la corrida
        winratio = cont_win_p1*100/(cont_win_p1+cont_win_p2+cont_empate)
        print("## RESULTADO ##  N= " + str(N) + " - j1: " + str(cont_win_p1) + ", j2: " + str(cont_win_p2) + ", Empates: " + str(cont_empate) + ", WINRATIO p1:"+ str(winratio)[0:5] + " ##")

        return lista_episodios

    @staticmethod
    def Save_Games_to_Disk(lista_episodios, filename):
        # Store data (serialize)
        with open(filename, 'wb') as handle:
            pickle.dump(lista_episodios, handle)

    @staticmethod
    def Load_Games_From_Disk(filename):
        # Load data (deserialize)
        with open(filename, 'rb') as handle:
            result = pickle.load(handle)
        return result

    @staticmethod
    def ConverToVector(jugador, estado, normalized=True): # Aca construimos el vector de largo fijo y normalizado para usar de input a la Red Neuronal
        result = []

        # 1ro ESTADO TRUCO (1 neurona)
        if normalized : result.append(estado.truco.value / len(Reglas.EstadoTruco))  # normalizo usando total de estados posibles de truco
        else: result.append(estado.truco.value)

        # 2do CARTAS DEL JUGADOR (3)
        for c in jugador.cartas_totales:
            if normalized : result.append(c.ValorTruco / 101)    # 100 es maximo valortruco de cualquier carta, uso 101 para normalizar
            else: result.append(c.ValorTruco)

        # 3ro CARTAS JUGADAS (6 neuronas, fijo), en su forma de valor truco. (esto reduce total de combinaciones, de 40 ID posibles a 14 valores truco posibles)
        for i in range(6):
            if len(estado.cartas_jugadas) > i:
                if normalized : result.append(estado.cartas_jugadas[i].ValorTruco/101)  # 100 es maximo valortruco de cualquier carta, uso 101 para normalizar
                else: result.append(estado.cartas_jugadas[i].ValorTruco)
            else:  # padding (largo fijo 6, el resto completo con 0's)
                result.append(0)

        # 4to ACCIONES (40 neuronas, fijo = 20 acciones x 2 (jugador + codigo accion) )
        for i in range(20):
            if len(estado.acciones_hechas) > i:
                result.append(estado.acciones_hechas[i][0])
                if normalized : result.append(estado.acciones_hechas[i][1].value/(len(Reglas.Accion)+1))
                else: result.append(estado.acciones_hechas[i][1].value)

            else: # padding (largo fijo 20, el resto completo con 0's)
                result.append(0)
                result.append(0)

        return result

    @staticmethod
    def Generate_Training_Games(batch_size, epochs, DEBUG):
        p1_data = []
        p1_labels= []
        p2_data = []
        p2_labels = []

        p1 = Agente(Reglas.JUGADOR1)
        p2 = Agente(Reglas.JUGADOR2)

        print("Generando Partidas.. ( epochs=" + str(epochs) + ",   batch_size=" + str(batch_size) + " )")
        print("")

        # Corremos los epochs
        for i in range(epochs):
            if DEBUG: print("Epoch: " + str(i + 1))
            episodios = Motor.Play_random_games(p1, p2, batch_size, False)
            for e in episodios:

                for s in e.estados:
                    if e.ganador is Reglas.JUGADOR1:
                        if s.acciones_hechas[-1][0] == Reglas.JUGADOR1:
                            p1_data.append(Motor.ConverToVector(e.p1,s, not DEBUG))
                            p1_labels.append(s.get_last_action_from_player(Reglas.JUGADOR1).value)
                    elif e.ganador is Reglas.JUGADOR2:
                        if s.acciones_hechas[-1][0] == Reglas.JUGADOR2:
                            p2_data.append(Motor.ConverToVector(e.p2,s, not DEBUG))
                            p2_labels.append(s.get_last_action_from_player(Reglas.JUGADOR2).value)

        return (p1_data, p1_labels), (p2_data, p2_labels)
