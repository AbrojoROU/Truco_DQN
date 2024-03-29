# OPTIMISTIC INITIAL VALUES
import numpy as np
import inspect
import random
import copy
from enum import Enum
import pickle
import time
import itertools



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
    MAZO.append(Carta("carta nula", 0, 0, 0))  # ID: 0 para que Carta.ID = Mazo[index]
    MAZO.append(Carta("4-Copa", 7, Carta.Palo.COPA, 4))  # ID: 1
    MAZO.append(Carta("4-Oro", 7, Carta.Palo.ORO, 4))  # ID: 2
    MAZO.append(Carta("4-Basto", 7, Carta.Palo.BASTO, 4))  # ID: 3
    MAZO.append(Carta("4-Espada", 7, Carta.Palo.ESPADA, 4))  # ID: 4
    MAZO.append(Carta("5-Copa", 14, Carta.Palo.COPA, 5))  # ID: 5
    MAZO.append(Carta("5-Oro", 14, Carta.Palo.ORO, 5))  # ID: 6
    MAZO.append(Carta("5-Basto", 14, Carta.Palo.BASTO, 5))  # ID: 7
    MAZO.append(Carta("5-Espada", 14, Carta.Palo.ESPADA, 5))  # ID: 8
    MAZO.append(Carta("6-Copa", 21, Carta.Palo.COPA, 6))  # ID: 9
    MAZO.append(Carta("6-Oro", 21, Carta.Palo.ORO, 6))  # ID: 10
    MAZO.append(Carta("6-Basto", 21, Carta.Palo.BASTO, 6))  # ID: 11
    MAZO.append(Carta("6-Espada", 21, Carta.Palo.ESPADA, 6))  # ID: 12
    MAZO.append(Carta("7-Copa", 28, Carta.Palo.COPA, 7))  # ID: 13
    MAZO.append(Carta("7-Basto", 28, Carta.Palo.BASTO, 7))  # ID: 14
    MAZO.append(Carta("10-Copa", 35, Carta.Palo.COPA, 0))  # ID: 15
    MAZO.append(Carta("10-Oro", 35, Carta.Palo.ORO, 0))  # ID: 16
    MAZO.append(Carta("10-Basto", 35, Carta.Palo.BASTO, 0))  # ID: 17
    MAZO.append(Carta("10-Espada", 35, Carta.Palo.ESPADA, 0))  # ID: 18
    MAZO.append(Carta("11-Copa", 42, Carta.Palo.COPA, 0))  # ID: 19
    MAZO.append(Carta("11-Oro", 42, Carta.Palo.ORO, 0))  # ID: 20
    MAZO.append(Carta("11-Basto", 42, Carta.Palo.BASTO, 0))  # ID: 21
    MAZO.append(Carta("11-Espada", 42, Carta.Palo.ESPADA, 0))  # ID: 22
    MAZO.append(Carta("12-Copa", 49, Carta.Palo.COPA, 0))  # ID: 23
    MAZO.append(Carta("12-Oro", 49, Carta.Palo.ORO, 0))  # ID: 24
    MAZO.append(Carta("12-Basto", 49, Carta.Palo.BASTO, 0))  # ID: 25
    MAZO.append(Carta("12-Espada", 49, Carta.Palo.ESPADA, 0))  # ID: 26
    MAZO.append(Carta("1-Copa", 56, Carta.Palo.COPA, 1))  # ID: 27
    MAZO.append(Carta("1-Oro", 56, Carta.Palo.ORO, 1))  # ID: 28
    MAZO.append(Carta("2-Copa", 63, Carta.Palo.COPA, 2))  # ID: 29
    MAZO.append(Carta("2-Oro", 63, Carta.Palo.ORO, 2))  # ID: 30
    MAZO.append(Carta("2-Basto", 63, Carta.Palo.BASTO, 2))  # ID: 31
    MAZO.append(Carta("2-Espada", 63, Carta.Palo.ESPADA, 2))  # ID: 32
    MAZO.append(Carta("3-Copa", 70, Carta.Palo.COPA, 3))  # ID: 33
    MAZO.append(Carta("3-Oro", 70, Carta.Palo.ORO, 3))  # ID: 34
    MAZO.append(Carta("3-Basto", 70, Carta.Palo.BASTO, 3))  # ID: 35
    MAZO.append(Carta("3-Espada", 70, Carta.Palo.ESPADA, 3))  # ID: 36
    MAZO.append(Carta("7-Oro", 77, Carta.Palo.ORO, 7))  # ID: 37
    MAZO.append(Carta("7-Espada", 84, Carta.Palo.ESPADA, 7))  # ID: 38
    MAZO.append(Carta("1-Basto", 91, Carta.Palo.BASTO, 1))  # ID: 39
    MAZO.append(Carta("1-Espada", 98, Carta.Palo.ESPADA, 1))  # ID: 40
    return MAZO

def get_non_negative_int(prompt, list_valid_numbers):
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print(">> Perdón, no entendí el input. Ingresar un numero válido")
            continue

        if value not in list_valid_numbers:
            print(">> Perdón, ese número no es una opción válida")
            continue
        else:
            break
    return value

class Carta:
    cont_interno = 0

    class Palo(Enum):
        BASTO = 1
        COPA = 2
        ESPADA = 3
        ORO = 4

    def __init__(self, nombre, valor_truco, palo, valor_envido):
        self.ID = Carta.cont_interno
        self.Nombre = nombre
        self.ValorTruco = valor_truco
        self.Palo = palo
        self.ValorEnvido = valor_envido
        Carta.cont_interno += 1

    def __repr__(self):
        # override print() oupput a consola
        return self.Nombre  # output parcial para jugar
        # return "ID:" + str(self.ID) + ", " + self.Nombre + ", vt:" + str(self.ValorTruco) # output completo para debug

    def __str__(self):  # python
        # override del str()
        return self.Nombre  # output parcial para jugar
        # return "ID:" + str(self.ID) + ", " + self.Nombre + ", vt:" + str(self.ValorTruco) # output completo para debug

    def __eq__(self, other):
        return self.ID == other.ID

    def Palo_to_categorical_vector(self, normalized):
        result = []
        if normalized is True:
            if self.Palo is Carta.Palo.BASTO: result.append(0.5)
            else: result.append(-0.5)
            if self.Palo is Carta.Palo.COPA: result.append(0.5)
            else: result.append(-0.5)
            if self.Palo is Carta.Palo.ESPADA: result.append(0.5)
            else: result.append(-0.5)
            if self.Palo is Carta.Palo.ORO: result.append(0.5)
            else: result.append(-0.5)
        else:
            if self.Palo is Carta.Palo.BASTO: result.append(1)
            else: result.append(0)
            if self.Palo is Carta.Palo.COPA: result.append(1)
            else: result.append(0)
            if self.Palo is Carta.Palo.ESPADA: result.append(1)
            else: result.append(0)
            if self.Palo is Carta.Palo.ORO: result.append(1)
            else: result.append(0)
        return result

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
        GRITAR = 5
        FOLD = 6  # FOLD (irme / rechazar apuesta Truco)
        ENVIDO = 7
        REALENVIDO = 8
        FALTAENVIDO = 9
        RECHAZAR_TANTO = 10
        ACEPTAR_TANTO = 11

    class EstadoTruco(Enum):
        NADA_DICHO = 1
        TRUCO_DICHO = 2
        TRUCO_ACEPTADO = 3
        RETRUCO_DICHO = 4
        RETRUCO_ACEPTADO = 5
        VALE4_DICHO = 6
        VALE4_ACEPTADO = 7
        FOLD = 8

    class EstadoEnvido(Enum):
        # El detalle de estados debe existir para poder hacer control de flujo del envido en el motor
        # Luego simplificare a NODICHO, ACEPTADO, RECHAZADO  y PUNTOS cuando convierta en vector para la red

        NADA_DICHO = 1
        #RECHAZADO = 2
        # ENVIDO
        E_DICHO = 3
        E_ACEPTADO = 4
        E_RECHAZADO = 5
        # ENVIDO - FALTA ENVIDO
        EF_DICHO = 6
        EF_ACEPTADO = 7
        EF_RECHAZADO = 8
        # ENVIDO - ENVIDO
        EE_DICHO = 9
        EE_ACEPTADO = 10
        EE_RECHAZADO = 11
        # ENVIDO - ENVIDO - FALTA ENVIDO
        EEF_DICHO = 12
        EEF_ACEPTADO = 13
        EEF_RECHAZADO = 14
        # ENVIDO - REAL ENVIDO
        ER_DICHO = 15
        ER_ACEPTADO = 16
        ER_RECHAZADO = 17
        # ENVIDO - REAL ENVIDO - FALTA ENVIDO
        ERF_DICHO = 18
        ERF_ACEPTADO = 19
        ERF_RECHAZADO = 20
        # REAL ENVIDO
        R_DICHO = 21
        R_ACEPTADO = 22
        R_RECHAZADO = 23
        # REAL ENVIDO - FALTA ENVIDO
        RF_DICHO = 24
        RF_ACEPTADO = 25
        RF_RECHAZADO = 26
        # FALTA ENVIDO
        F_DICHO = 27
        F_ACEPTADO = 28
        F_RECHAZADO = 29


    @staticmethod
    def ContarEnvido(cartas):
        # llega lista con 3 cartas
        maxT = 0

        for x in itertools.combinations(cartas, 2):
            if x[0].Palo == x[1].Palo:
                t = 20 + x[0].ValorEnvido + x[1].ValorEnvido
            else:
                t = max(x[0].ValorEnvido, x[1].ValorEnvido)
            if t > maxT : maxT = t

        return maxT


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

# Este agente toma decisiones al azar
class AgenteRandom:
    def __init__(self, jugador):

        self.cartas_totales = []
        self.cartas_restantes = []
        self.eps = 0
        self.puntos_envido = 0

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

        self.puntos_envido = Reglas.ContarEnvido(self.cartas_totales)

    def get_acciones_posibles(self,s):
        # Este metodo construye y retorna el vector de acciones posibles (tomados del enum Reglas.Acciones) con base en el estado actual "s"
        result = []

        # ESTAMOS EN PLENO CICLO DE ENVIDO?  (prioritario, debe resolverse antes de hablar de otra cosa)
        if s.envido is Reglas.EstadoEnvido.E_DICHO:
            result.append(Reglas.Accion.ENVIDO)
            result.append(Reglas.Accion.REALENVIDO)
            result.append(Reglas.Accion.FALTAENVIDO)
            result.append(Reglas.Accion.ACEPTAR_TANTO)
            result.append(Reglas.Accion.RECHAZAR_TANTO)
        elif s.envido is Reglas.EstadoEnvido.EE_DICHO:
            result.append(Reglas.Accion.FALTAENVIDO)
            result.append(Reglas.Accion.ACEPTAR_TANTO)
            result.append(Reglas.Accion.RECHAZAR_TANTO)
        elif s.envido in [Reglas.EstadoEnvido.R_DICHO, Reglas.EstadoEnvido.ER_DICHO]:
            result.append(Reglas.Accion.FALTAENVIDO)
            result.append(Reglas.Accion.ACEPTAR_TANTO)
            result.append(Reglas.Accion.RECHAZAR_TANTO)
        elif s.envido in [Reglas.EstadoEnvido.EF_DICHO, Reglas.EstadoEnvido.EEF_DICHO ,
                          Reglas.EstadoEnvido.ERF_DICHO , Reglas.EstadoEnvido.RF_DICHO ,
                          Reglas.EstadoEnvido.F_DICHO]:
            result.append(Reglas.Accion.ACEPTAR_TANTO)
            result.append(Reglas.Accion.RECHAZAR_TANTO)

        else: # NO ESTAMOS EN MEDIO DE UN CICLO DE ENVIDO

            # ESTAMOS EN UN CICLO DE TRUCO?  (prioritario luego del envido)
            if s.truco is Reglas.EstadoTruco.TRUCO_DICHO:
                if (s.envido is Reglas.EstadoEnvido.NADA_DICHO) and (len(self.cartas_restantes) == 3):
                    result.append(Reglas.Accion.ENVIDO)
                    result.append(Reglas.Accion.REALENVIDO)
                    result.append(Reglas.Accion.FALTAENVIDO)
                result.append(Reglas.Accion.QUIERO_GRITO)
                result.append(Reglas.Accion.GRITAR)  # Permitimos Re-Raise (poco lógico, lo podriamos restringir a ultima mano bajo un if len(self.cartas_restantes) == 0)
                result.append(Reglas.Accion.FOLD)
            elif s.truco is Reglas.EstadoTruco.RETRUCO_DICHO:
                result.append(Reglas.Accion.QUIERO_GRITO)
                result.append(Reglas.Accion.GRITAR)  # Permitimos Re-Raise (poco lógico, lo podriamos restringir a ultima mano bajo un if len(self.cartas_restantes) == 0)
                result.append(Reglas.Accion.FOLD)
            elif s.truco == Reglas.EstadoTruco.VALE4_DICHO:
                result.append(Reglas.Accion.QUIERO_GRITO)
                result.append(Reglas.Accion.FOLD)

            # NO ESTAMOS EN MEDIO DE UN CICLO DE TRUCO
            else:
                # ES POSIBLE DECIR ENVIDO: todavia no pasamos por envido y tengo 3 cartas en la mano (si jugue algo ya fui)
                if (s.envido is Reglas.EstadoEnvido.NADA_DICHO) and (len(self.cartas_restantes) == 3):
                    # validar que el truco lo permite (todavia no se dijo el Truco)
                    if s.truco is Reglas.EstadoTruco.NADA_DICHO:
                        result.append(Reglas.Accion.ENVIDO)
                        result.append(Reglas.Accion.REALENVIDO)
                        result.append(Reglas.Accion.FALTAENVIDO)

                # ENVIDO YA GESTIONADO QUEDA TRUCO Y CARTAS
                if s.QuienJugariaCarta() == self.jugador: # me toca
                    # Opciones de Truco : si me gritaron, agregar las acciones de aceptar (call) y subir apuesta (raise)
                    if s.truco is Reglas.EstadoTruco.TRUCO_ACEPTADO :
                        for j, a in reversed(s.acciones_hechas):
                            if a is Reglas.Accion.GRITAR:
                                if j is not self.jugador:
                                    result.append(Reglas.Accion.GRITAR)
                                break  # hago break en el primer GRITAR que encuentre en reversa, si no fui yo agrego Gritar pero siempre break

                    elif s.truco is Reglas.EstadoTruco.RETRUCO_ACEPTADO :
                        for j, a in reversed(s.acciones_hechas):
                            if a is Reglas.Accion.GRITAR:
                                if j is not self.jugador:
                                    result.append(Reglas.Accion.GRITAR)
                                break  # hago break en el primer GRITAR que encuentre en reversa, si no fui yo agrego Gritar pero siempre break
                    elif s.truco == Reglas.EstadoTruco.NADA_DICHO: result.append(Reglas.Accion.GRITAR)
                    elif s.truco == Reglas.EstadoTruco.VALE4_ACEPTADO : pass
                    else:
                        assert False  # WARNING: Si me toca, el estado del truco deberia estar en alguno case de los elif, a menos que permita Re-Raise

                    # solo resta agregar las acciones de jugar cartas aun en mano
                    for c in self.cartas_restantes:
                        result.append(Reglas.Accion(self.cartas_totales.index(c) + 1))

                else:
                    assert False  # caso no posible (no estamos en ciclo de envido o truco y tampoco me toca jugar)

        # VERSION CON FILTRADO DE DUPLICADOS (lo quito para que salten problemas de flujo si los hay)
        #from more_itertools import unique_everseen
        #return list(unique_everseen(result))

        return result

    def Elegir_Accion(self, s, debug=False):
        # Esta version es para agente random, es al azar pero introducimos unhack para reducir un poco la probabalidad de que haga Fold
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

        if a is Reglas.Accion.ENVIDO :
            if s.envido is Reglas.EstadoEnvido.NADA_DICHO : s.envido = Reglas.EstadoEnvido.E_DICHO
            elif s.envido is Reglas.EstadoEnvido.E_DICHO : s.envido = Reglas.EstadoEnvido.EE_DICHO
        elif a is Reglas.Accion.REALENVIDO :
            if s.envido is Reglas.EstadoEnvido.NADA_DICHO : s.envido = Reglas.EstadoEnvido.R_DICHO
            elif s.envido is Reglas.EstadoEnvido.E_DICHO : s.envido = Reglas.EstadoEnvido.ER_DICHO
        elif a is Reglas.Accion.FALTAENVIDO :
            if s.envido is Reglas.EstadoEnvido.NADA_DICHO: s.envido = Reglas.EstadoEnvido.F_DICHO
            elif s.envido is Reglas.EstadoEnvido.E_DICHO : s.envido = Reglas.EstadoEnvido.EF_DICHO
            elif s.envido is Reglas.EstadoEnvido.ER_DICHO : s.envido = Reglas.EstadoEnvido.ERF_DICHO
            elif s.envido is Reglas.EstadoEnvido.EE_DICHO : s.envido = Reglas.EstadoEnvido.EEF_DICHO
            elif s.envido is Reglas.EstadoEnvido.R_DICHO : s.envido = Reglas.EstadoEnvido.RF_DICHO
        elif a is Reglas.Accion.RECHAZAR_TANTO:
            if s.envido is Reglas.EstadoEnvido.E_DICHO : s.envido = Reglas.EstadoEnvido.E_RECHAZADO
            elif s.envido is Reglas.EstadoEnvido.EF_DICHO : s.envido = Reglas.EstadoEnvido.EF_RECHAZADO
            elif s.envido is Reglas.EstadoEnvido.EE_DICHO : s.envido = Reglas.EstadoEnvido.EE_RECHAZADO
            elif s.envido is Reglas.EstadoEnvido.EEF_DICHO: s.envido = Reglas.EstadoEnvido.EEF_RECHAZADO
            elif s.envido is Reglas.EstadoEnvido.ER_DICHO: s.envido = Reglas.EstadoEnvido.ER_RECHAZADO
            elif s.envido is Reglas.EstadoEnvido.ERF_DICHO: s.envido = Reglas.EstadoEnvido.ERF_RECHAZADO
            elif s.envido is Reglas.EstadoEnvido.R_DICHO: s.envido = Reglas.EstadoEnvido.R_RECHAZADO
            elif s.envido is Reglas.EstadoEnvido.RF_DICHO: s.envido = Reglas.EstadoEnvido.RF_RECHAZADO
            elif s.envido is Reglas.EstadoEnvido.F_DICHO: s.envido = Reglas.EstadoEnvido.F_RECHAZADO
        elif a is Reglas.Accion.ACEPTAR_TANTO:
            if s.envido is Reglas.EstadoEnvido.E_DICHO: s.envido = Reglas.EstadoEnvido.E_ACEPTADO
            elif s.envido is Reglas.EstadoEnvido.EF_DICHO: s.envido = Reglas.EstadoEnvido.EF_ACEPTADO
            elif s.envido is Reglas.EstadoEnvido.EE_DICHO: s.envido = Reglas.EstadoEnvido.EE_ACEPTADO
            elif s.envido is Reglas.EstadoEnvido.EEF_DICHO: s.envido = Reglas.EstadoEnvido.EEF_ACEPTADO
            elif s.envido is Reglas.EstadoEnvido.ER_DICHO: s.envido = Reglas.EstadoEnvido.ER_ACEPTADO
            elif s.envido is Reglas.EstadoEnvido.ERF_DICHO: s.envido = Reglas.EstadoEnvido.ERF_ACEPTADO
            elif s.envido is Reglas.EstadoEnvido.R_DICHO: s.envido = Reglas.EstadoEnvido.R_ACEPTADO
            elif s.envido is Reglas.EstadoEnvido.RF_DICHO: s.envido = Reglas.EstadoEnvido.RF_ACEPTADO
            elif s.envido is Reglas.EstadoEnvido.F_DICHO: s.envido = Reglas.EstadoEnvido.F_ACEPTADO

        elif a is Reglas.Accion.GRITAR :
            if s.truco in [Reglas.EstadoTruco.RETRUCO_ACEPTADO, Reglas.EstadoTruco.RETRUCO_DICHO]:
                s.truco = Reglas.EstadoTruco.VALE4_DICHO
            elif s.truco in [Reglas.EstadoTruco.TRUCO_ACEPTADO,Reglas.EstadoTruco.TRUCO_DICHO]:
                s.truco = Reglas.EstadoTruco.RETRUCO_DICHO
            elif s.truco is Reglas.EstadoTruco.NADA_DICHO: s.truco = Reglas.EstadoTruco.TRUCO_DICHO
            elif s.truco is Reglas.EstadoTruco.VALE4_ACEPTADO : assert False # no se puede gritar cuando ya esta dicho el vale4

        elif a is Reglas.Accion.QUIERO_GRITO:
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



class Humano:
    def __init__(self, jugador):
        self.cartas_totales = []
        self.cartas_restantes = []
        self.eps = 0
        self.puntos_envido = 0

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

        self.puntos_envido = Reglas.ContarEnvido(self.cartas_totales)

    def get_acciones_posibles(self,s):
        # Este metodo construye y retorna el vector de acciones posibles (tomados del enum Reglas.Acciones) con base en el estado actual "s"
        result = []

        # ESTAMOS EN PLENO CICLO DE ENVIDO?  (prioritario, debe resolverse antes de hablar de otra cosa)
        if s.envido is Reglas.EstadoEnvido.E_DICHO:
            result.append(Reglas.Accion.ENVIDO)
            result.append(Reglas.Accion.REALENVIDO)
            result.append(Reglas.Accion.FALTAENVIDO)
            result.append(Reglas.Accion.ACEPTAR_TANTO)
            result.append(Reglas.Accion.RECHAZAR_TANTO)
        elif s.envido is Reglas.EstadoEnvido.EE_DICHO:
            result.append(Reglas.Accion.FALTAENVIDO)
            result.append(Reglas.Accion.ACEPTAR_TANTO)
            result.append(Reglas.Accion.RECHAZAR_TANTO)
        elif s.envido in [Reglas.EstadoEnvido.R_DICHO, Reglas.EstadoEnvido.ER_DICHO]:
            result.append(Reglas.Accion.FALTAENVIDO)
            result.append(Reglas.Accion.ACEPTAR_TANTO)
            result.append(Reglas.Accion.RECHAZAR_TANTO)
        elif s.envido in [Reglas.EstadoEnvido.EF_DICHO, Reglas.EstadoEnvido.EEF_DICHO ,
                          Reglas.EstadoEnvido.ERF_DICHO , Reglas.EstadoEnvido.RF_DICHO ,
                          Reglas.EstadoEnvido.F_DICHO]:
            result.append(Reglas.Accion.ACEPTAR_TANTO)
            result.append(Reglas.Accion.RECHAZAR_TANTO)

        else: # NO ESTAMOS EN MEDIO DE UN CICLO DE ENVIDO

            # ESTAMOS EN UN CICLO DE TRUCO?  (prioritario luego del envido)
            if s.truco is Reglas.EstadoTruco.TRUCO_DICHO:
                if (s.envido is Reglas.EstadoEnvido.NADA_DICHO) and (len(self.cartas_restantes) == 3):
                    result.append(Reglas.Accion.ENVIDO)
                    result.append(Reglas.Accion.REALENVIDO)
                    result.append(Reglas.Accion.FALTAENVIDO)
                result.append(Reglas.Accion.QUIERO_GRITO)
                result.append(Reglas.Accion.GRITAR)  # Permitimos Re-Raise (poco lógico, lo podriamos restringir a ultima mano bajo un if len(self.cartas_restantes) == 0)
                result.append(Reglas.Accion.FOLD)
            elif s.truco is Reglas.EstadoTruco.RETRUCO_DICHO:
                result.append(Reglas.Accion.QUIERO_GRITO)
                result.append(Reglas.Accion.GRITAR)  # Permitimos Re-Raise (poco lógico, lo podriamos restringir a ultima mano bajo un if len(self.cartas_restantes) == 0)
                result.append(Reglas.Accion.FOLD)
            elif s.truco == Reglas.EstadoTruco.VALE4_DICHO:
                result.append(Reglas.Accion.QUIERO_GRITO)
                result.append(Reglas.Accion.FOLD)

            # NO ESTAMOS EN MEDIO DE UN CICLO DE TRUCO
            else:
                # ES POSIBLE DECIR ENVIDO: todavia no pasamos por envido y tengo 3 cartas en la mano (si jugue algo ya fui)
                if (s.envido is Reglas.EstadoEnvido.NADA_DICHO) and (len(self.cartas_restantes) == 3):
                    # validar que el truco lo permite (todavia no se dijo el Truco)
                    if s.truco is Reglas.EstadoTruco.NADA_DICHO:
                        result.append(Reglas.Accion.ENVIDO)
                        result.append(Reglas.Accion.REALENVIDO)
                        result.append(Reglas.Accion.FALTAENVIDO)

                # ENVIDO YA GESTIONADO QUEDA TRUCO Y CARTAS
                if s.QuienJugariaCarta() == self.jugador: # me toca
                    # Opciones de Truco : si me gritaron, agregar las acciones de aceptar (call) y subir apuesta (raise)
                    if s.truco is Reglas.EstadoTruco.TRUCO_ACEPTADO :
                        for j, a in reversed(s.acciones_hechas):
                            if a is Reglas.Accion.GRITAR:
                                if j is not self.jugador:
                                    result.append(Reglas.Accion.GRITAR)
                                break  # hago break en el primer GRITAR que encuentre en reversa, si no fui yo agrego Gritar pero siempre break

                    elif s.truco is Reglas.EstadoTruco.RETRUCO_ACEPTADO :
                        for j, a in reversed(s.acciones_hechas):
                            if a is Reglas.Accion.GRITAR:
                                if j is not self.jugador:
                                    result.append(Reglas.Accion.GRITAR)
                                break  # hago break en el primer GRITAR que encuentre en reversa, si no fui yo agrego Gritar pero siempre break
                    elif s.truco == Reglas.EstadoTruco.NADA_DICHO: result.append(Reglas.Accion.GRITAR)
                    elif s.truco == Reglas.EstadoTruco.VALE4_ACEPTADO : pass
                    else:
                        assert False  # WARNING: Si me toca, el estado del truco deberia estar en alguno case de los elif, a menos que permita Re-Raise

                    # solo resta agregar las acciones de jugar cartas aun en mano
                    for c in self.cartas_restantes:
                        result.append(Reglas.Accion(self.cartas_totales.index(c) + 1))

                else:
                    assert False  # caso no posible (no estamos en ciclo de envido o truco y tampoco me toca jugar)

        # VERSION CON FILTRADO DE DUPLICADOS (lo quito para que salten problemas de flujo si los hay)
        #from more_itertools import unique_everseen
        #return list(unique_everseen(result))

        return result

    def Elegir_Accion(self, s, debug=False):
        print("")
        print("###  TE TOCA HUMANO, p" + str(self.jugador) + "  ###")
        print("   Truco: " + s.truco.name + "    Envido: " + s.envido.name)
        print("   Se jugaron las siguientes cartas: " + str(s.cartas_jugadas))
        print("   Cartas en la mano: " + str(self.cartas_restantes))
        print("")
        a_posibles = self.get_acciones_posibles(s)

        print("Debes elegir accion! acciones posibles: ")
        ids_a = []
        for a in a_posibles:
            ids_a.append(a.value)
            print("   " + str(a.value) + ". " + a.name)

        print("")
        opcion = int(get_non_negative_int("   Ingrese accion: ", ids_a))

        return Reglas.Accion(opcion)

    # Ejecuta la accion que le llega, actualizando el estado y el agente de forma acorde
    def EjecutarAccion(self, s, a, DEBUG=False):

        if a is Reglas.Accion.FOLD: s.truco = Reglas.EstadoTruco.FOLD

        if a is Reglas.Accion.ENVIDO :
            if s.envido is Reglas.EstadoEnvido.NADA_DICHO : s.envido = Reglas.EstadoEnvido.E_DICHO
            elif s.envido is Reglas.EstadoEnvido.E_DICHO : s.envido = Reglas.EstadoEnvido.EE_DICHO
        elif a is Reglas.Accion.REALENVIDO :
            if s.envido is Reglas.EstadoEnvido.NADA_DICHO : s.envido = Reglas.EstadoEnvido.R_DICHO
            elif s.envido is Reglas.EstadoEnvido.E_DICHO : s.envido = Reglas.EstadoEnvido.ER_DICHO
        elif a is Reglas.Accion.FALTAENVIDO :
            if s.envido is Reglas.EstadoEnvido.NADA_DICHO: s.envido = Reglas.EstadoEnvido.F_DICHO
            elif s.envido is Reglas.EstadoEnvido.E_DICHO : s.envido = Reglas.EstadoEnvido.EF_DICHO
            elif s.envido is Reglas.EstadoEnvido.ER_DICHO : s.envido = Reglas.EstadoEnvido.ERF_DICHO
            elif s.envido is Reglas.EstadoEnvido.EE_DICHO : s.envido = Reglas.EstadoEnvido.EEF_DICHO
            elif s.envido is Reglas.EstadoEnvido.R_DICHO : s.envido = Reglas.EstadoEnvido.RF_DICHO
        elif a is Reglas.Accion.RECHAZAR_TANTO:
            if s.envido is Reglas.EstadoEnvido.E_DICHO : s.envido = Reglas.EstadoEnvido.E_RECHAZADO
            elif s.envido is Reglas.EstadoEnvido.EF_DICHO : s.envido = Reglas.EstadoEnvido.EF_RECHAZADO
            elif s.envido is Reglas.EstadoEnvido.EE_DICHO : s.envido = Reglas.EstadoEnvido.EE_RECHAZADO
            elif s.envido is Reglas.EstadoEnvido.EEF_DICHO: s.envido = Reglas.EstadoEnvido.EEF_RECHAZADO
            elif s.envido is Reglas.EstadoEnvido.ER_DICHO: s.envido = Reglas.EstadoEnvido.ER_RECHAZADO
            elif s.envido is Reglas.EstadoEnvido.ERF_DICHO: s.envido = Reglas.EstadoEnvido.ERF_RECHAZADO
            elif s.envido is Reglas.EstadoEnvido.R_DICHO: s.envido = Reglas.EstadoEnvido.R_RECHAZADO
            elif s.envido is Reglas.EstadoEnvido.RF_DICHO: s.envido = Reglas.EstadoEnvido.RF_RECHAZADO
            elif s.envido is Reglas.EstadoEnvido.F_DICHO: s.envido = Reglas.EstadoEnvido.F_RECHAZADO
        elif a is Reglas.Accion.ACEPTAR_TANTO:
            if s.envido is Reglas.EstadoEnvido.E_DICHO: s.envido = Reglas.EstadoEnvido.E_ACEPTADO
            elif s.envido is Reglas.EstadoEnvido.EF_DICHO: s.envido = Reglas.EstadoEnvido.EF_ACEPTADO
            elif s.envido is Reglas.EstadoEnvido.EE_DICHO: s.envido = Reglas.EstadoEnvido.EE_ACEPTADO
            elif s.envido is Reglas.EstadoEnvido.EEF_DICHO: s.envido = Reglas.EstadoEnvido.EEF_ACEPTADO
            elif s.envido is Reglas.EstadoEnvido.ER_DICHO: s.envido = Reglas.EstadoEnvido.ER_ACEPTADO
            elif s.envido is Reglas.EstadoEnvido.ERF_DICHO: s.envido = Reglas.EstadoEnvido.ERF_ACEPTADO
            elif s.envido is Reglas.EstadoEnvido.R_DICHO: s.envido = Reglas.EstadoEnvido.R_ACEPTADO
            elif s.envido is Reglas.EstadoEnvido.RF_DICHO: s.envido = Reglas.EstadoEnvido.RF_ACEPTADO
            elif s.envido is Reglas.EstadoEnvido.F_DICHO: s.envido = Reglas.EstadoEnvido.F_ACEPTADO

        elif a is Reglas.Accion.GRITAR :
            if s.truco in [Reglas.EstadoTruco.RETRUCO_ACEPTADO, Reglas.EstadoTruco.RETRUCO_DICHO]:
                s.truco = Reglas.EstadoTruco.VALE4_DICHO
            elif s.truco in [Reglas.EstadoTruco.TRUCO_ACEPTADO,Reglas.EstadoTruco.TRUCO_DICHO]:
                s.truco = Reglas.EstadoTruco.RETRUCO_DICHO
            elif s.truco is Reglas.EstadoTruco.NADA_DICHO: s.truco = Reglas.EstadoTruco.TRUCO_DICHO
            elif s.truco is Reglas.EstadoTruco.VALE4_ACEPTADO : assert False # no se puede gritar cuando ya esta dicho el vale4

        elif a is Reglas.Accion.QUIERO_GRITO:
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
        self.ganadorTruco = None # 4 estados posibles. None si nadie, 0 si empate, p1  o p2
        self.ganadorTotal = None  # 4 estados posibles. None si nadie, 0 si empate, p1  o p2
        self.p1 = None
        self.p2 = None

    def QuienGanoEnvido(self):
        s = self.estados[-1]  # tomo estado final

        if s.envido is Reglas.EstadoEnvido.NADA_DICHO : return None

        # Primero veo si alguien hizo Fold
        for j, a in s.acciones_hechas:
            if a is Reglas.Accion.RECHAZAR_TANTO:
                if j is Reglas.JUGADOR1: return Reglas.JUGADOR2
                if j is Reglas.JUGADOR2: return Reglas.JUGADOR1

        # Finalmente, si se dijo algo y no hay RECHAZAR_TANTO, el que tenga mas puntos
        if self.p1.puntos_envido >= self.p2.puntos_envido : return Reglas.JUGADOR1
        elif self.p1.puntos_envido < self.p2.puntos_envido : return Reglas.JUGADOR2

        assert False  # imposible que calcular el envido llegue aca

    def CalcularPuntosFinales(self):
        p1 = 0
        p2 = 0
        bet_Truco = 1
        bet_Envido = 0

        # PUNTOS ENVIDO
        s = self.estados[-1]
        if s.envido is Reglas.EstadoEnvido.NADA_DICHO : bet_Envido = 0
        elif s.envido is Reglas.EstadoEnvido.E_ACEPTADO : bet_Envido = 2
        elif s.envido is Reglas.EstadoEnvido.E_RECHAZADO : bet_Envido = 1
        elif s.envido is Reglas.EstadoEnvido.EF_RECHAZADO : bet_Envido = 2
        elif s.envido is Reglas.EstadoEnvido.EE_ACEPTADO : bet_Envido = 4
        elif s.envido is Reglas.EstadoEnvido.EE_RECHAZADO : bet_Envido = 2
        elif s.envido is Reglas.EstadoEnvido.EEF_RECHAZADO : bet_Envido = 4
        elif s.envido is Reglas.EstadoEnvido.ER_ACEPTADO : bet_Envido = 5
        elif s.envido is Reglas.EstadoEnvido.ER_RECHAZADO : bet_Envido = 2
        elif s.envido is Reglas.EstadoEnvido.ERF_RECHAZADO : bet_Envido = 5
        elif s.envido is Reglas.EstadoEnvido.R_ACEPTADO : bet_Envido = 3
        elif s.envido is Reglas.EstadoEnvido.R_RECHAZADO : bet_Envido = 1
        elif s.envido is Reglas.EstadoEnvido.RF_RECHAZADO : bet_Envido = 3
        elif s.envido is Reglas.EstadoEnvido.F_RECHAZADO : bet_Envido = 1
        # la Falta por ahora son 10 para dar fuerte peso, mañana puede ser una funcion
        elif s.envido is Reglas.EstadoEnvido.EEF_ACEPTADO : bet_Envido = 10
        elif s.envido is Reglas.EstadoEnvido.RF_ACEPTADO : bet_Envido = 10
        elif s.envido is Reglas.EstadoEnvido.ERF_ACEPTADO : bet_Envido = 10
        elif s.envido is Reglas.EstadoEnvido.EF_ACEPTADO : bet_Envido = 10
        elif s.envido is Reglas.EstadoEnvido.F_ACEPTADO : bet_Envido = 10
        else: assert False  # Todos estados de envido deberian estar cubiertos en algun caso

        # ahora si, asigno los puntos del envido
        if self.QuienGanoEnvido() is Reglas.JUGADOR1 : p1 = p1 + bet_Envido
        elif self.QuienGanoEnvido() is Reglas.JUGADOR2: p2 = p2 + bet_Envido
        # else es que ninguno gano, no hay puntajes que asignar

        # PUNTOS TRUCO
        s = self.estados[-1]
        if s.truco is Reglas.EstadoTruco.FOLD:
            # Foldeo, calcular Truco con base en lo ultimo gritado
            s = self.estados[-2]
            if s.truco is Reglas.EstadoTruco.TRUCO_DICHO : bet_Truco = 1
            elif s.truco is Reglas.EstadoTruco.RETRUCO_DICHO : bet_Truco = 2
            elif s.truco is Reglas.EstadoTruco.VALE4_DICHO : bet_Truco = 3
            elif s.truco is Reglas.EstadoTruco.TRUCO_ACEPTADO : bet_Truco = 2
            elif s.truco is Reglas.EstadoTruco.RETRUCO_ACEPTADO : bet_Truco = 3
            elif s.truco is Reglas.EstadoTruco.VALE4_ACEPTADO : bet_Truco = 4
            elif s.truco is Reglas.EstadoTruco.NADA_DICHO : bet_Truco = 1
            else: assert False
        elif s.truco is Reglas.EstadoTruco.TRUCO_ACEPTADO : bet_Truco = 2
        elif s.truco is Reglas.EstadoTruco.RETRUCO_ACEPTADO : bet_Truco = 3
        elif s.truco is Reglas.EstadoTruco.VALE4_ACEPTADO : bet_Truco = 4
        elif s.truco is Reglas.EstadoTruco.NADA_DICHO : bet_Truco = 1
        else: assert False

        # PUNTOS TRUCO
        if self.ganadorTruco is Reglas.JUGADOR1:
            p1 = p1 + bet_Truco
        elif self.ganadorTruco is Reglas.JUGADOR2:
            p2 = p2 + bet_Truco
        else:
            assert False  # Nadie gano el truco? es imposiblem

        return p1, p2

class Estado:
    def __init__(self):
        self.cartas_jugadas = []
        self.truco = Reglas.EstadoTruco.NADA_DICHO
        self.envido = Reglas.EstadoEnvido.NADA_DICHO
        self.acciones_hechas = []
        self.puntos_envido_p1 = 0
        self.puntos_envido_p2 = 0


    def __repr__(self):
        # override print() oupput a consola
        return " ## cartas jugadas:" + str(self.cartas_jugadas) + ", estado:" + self.truco.name + ", acciones:" + str(self.acciones_hechas) + " ##"

    def __str__(self):  # python
        # override del str()
        return " Partida, cartas jugadas:" + str(self.cartas_jugadas) + ", estadoT:" + self.truco.name + ", estadoE:" + self.envido.name + ", acciones:" + str(self.acciones_hechas)

    def get_last_action_from_player(self, jugador):
        # Devuelve la ultima accion de un jugador
        for i in reversed(self.acciones_hechas):
            if i[0] == jugador:
                return i[1]

    def reset(self):
        self.cartas_jugadas = []
        self.truco = Reglas.EstadoTruco.NADA_DICHO
        #self.ganador = None  # 4 estados posibles. None si nadie, 0 si empate, p1  o p2
        self.acciones_hechas = []

    def QuienActua(self):

        if self.truco is Reglas.EstadoTruco.FOLD: return None

        if (self.envido in [Reglas.EstadoEnvido.NADA_DICHO,
                            Reglas.EstadoEnvido.E_ACEPTADO, Reglas.EstadoEnvido.E_RECHAZADO,
                            Reglas.EstadoEnvido.EE_ACEPTADO, Reglas.EstadoEnvido.EE_RECHAZADO,
                            Reglas.EstadoEnvido.RF_ACEPTADO, Reglas.EstadoEnvido.RF_RECHAZADO,
                            Reglas.EstadoEnvido.EEF_ACEPTADO, Reglas.EstadoEnvido.EEF_RECHAZADO,
                            Reglas.EstadoEnvido.EF_ACEPTADO, Reglas.EstadoEnvido.EF_RECHAZADO,
                            Reglas.EstadoEnvido.ER_ACEPTADO, Reglas.EstadoEnvido.ER_RECHAZADO,
                            Reglas.EstadoEnvido.ERF_ACEPTADO, Reglas.EstadoEnvido.ERF_RECHAZADO,
                            Reglas.EstadoEnvido.R_ACEPTADO, Reglas.EstadoEnvido.R_RECHAZADO,
                            Reglas.EstadoEnvido.F_ACEPTADO, Reglas.EstadoEnvido.F_RECHAZADO ]):
            # ENVIDO YA RESUELTO

            if (self.truco in [Reglas.EstadoTruco.NADA_DICHO, Reglas.EstadoTruco.TRUCO_ACEPTADO,
                               Reglas.EstadoTruco.RETRUCO_ACEPTADO, Reglas.EstadoTruco.VALE4_ACEPTADO]):
                # AMBOS CICLOS (Truco y Envido) RESUELTOS: retornar quien jugaria carta
                return self.QuienJugariaCarta()
            else:
                # EN PLENO CICLO DE TRUCO, devolver el opuesto del juegador que lo grito
                j = self.QuienGritoUltimo()
                if j is Reglas.JUGADOR1: return Reglas.JUGADOR2
                if j is Reglas.JUGADOR2: return Reglas.JUGADOR1

        else:
            # EN PLENO CICLO DE ENVIDO: devolver el opuesto del juegador que hablo último
            j, a = self.acciones_hechas[-1]  # j es el jugador, a es la acion,  -1 toma la ultima accion hecha
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




    def QuienGritoUltimo(self):
        # Primero veo si alguien hizo Fold
        for j, a in reversed(self.acciones_hechas):
            if a is Reglas.Accion.GRITAR:
                return j

        return None

    def QuienGanoManos(self):
        # Calcula quien gano las manos, puede retornar:
        # Reglas.JUGADOR1 or JUGADOR2
        # "None" si no se jugaron todas las manos aun (en esta nueva version esto rara vez se deberia usar, es parte de estado S)
        # p1 si es un triple empate en las 3 manos (por ser mano)

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
        # TODO que termine el partido si alguno ya gano 2 manos (se jugo

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
                    # empataron las 3 manos, gana el mano
                    return Reglas.JUGADOR1

        assert False # no deberia llegar aqui

class Motor:

    STATE_VECTOR_LENGTH = 100

    @staticmethod
    def Construir_Lista_Cartas(lista_id_cartas):
        result = []
        for i in lista_id_cartas:
            result.append(Reglas.MAZO[int(i)])

        return result

    @staticmethod
    def Play_Human_game(p1, p2, con_trampa):

        e = Episodio()
        s = Estado()
        p1.eps = 0
        p2.eps = 0

        # SETUP INICIAL repartir cartas
        cartas_p1, cartas_p2 = Reglas.RepartirCartas()
        p1.TomarCartas(cartas_p1)
        p2.TomarCartas(cartas_p2)
        s.puntos_envido_p1 = p1.puntos_envido
        s.puntos_envido_p2 = p2.puntos_envido
        e.p1 = p1
        e.p2 = p2
        e.estados.append(copy.deepcopy(s))
        print("")
        if con_trampa : print("  Cartas Jugador 1: " + str(p1.cartas_totales) + ",  puntos envido: " + str(p1.puntos_envido))
        if con_trampa : print("  Cartas Jugador 2: " + str(p2.cartas_totales) + ",  puntos envido: " + str(p2.puntos_envido))

        # Accion inicial
        current_player = p1
        a = p1.Elegir_Accion(s, con_trampa)

        # loops until the game is over
        while (s.QuienGanoManos() is None) and (s.truco is not Reglas.EstadoTruco.FOLD) :

            current_player.EjecutarAccion(s, a, True)

            if a is Reglas.Accion.ACEPTAR_TANTO :
                print(" TANTO ACEPTADO, p1:" + str(p1.puntos_envido) + ", p2:" +   str(p2.puntos_envido) )

            # Tomo otro jugador
            if s.QuienActua() == Reglas.JUGADOR1:
                next_player = p1
            else:
                next_player = p2

            # Me fijo si termino, 4 opciones:  Terminal Gane, Terminal empate, Terminal Perdi o No terminal y propago
            if s.QuienGanoEpisodio() is not None:
                quien_gano = s.QuienGanoEpisodio()

                if quien_gano == Reglas.JUGADOR1:
                    print(" GANE EL TRUCO! (jugador 1)")
                    e.ganadorTruco = Reglas.JUGADOR1
                elif quien_gano == Reglas.JUGADOR2:
                    print(" GANE EL TRUCO! (jugador 2)")
                    e.ganadorTruco = Reglas.JUGADOR1
            else:
                # Caso no terminal
                a = next_player.Elegir_Accion(s, con_trampa)

            # Finalmente alterno jugador
            if s.QuienActua() == Reglas.JUGADOR1:
                current_player = p1
            else:
                current_player = p2
            # Termino la mano
            e.estados.append(copy.deepcopy(s))  # Agrego el estado intermedio al episodio

        # Terminó el while gameover
        print("")
        print("Termino la partida, cartas jugadas finales: " + str(s.cartas_jugadas))
        print("Ganó: p" + str(e.ganadorTruco) + "! ,  con puntaje:" + str(e.CalcularPuntosFinales()))
        print("    >las cartas de p1 eran: " + str(p1.cartas_totales))
        print("    >las cartas de p2 eran: " + str(p2.cartas_totales))


    @staticmethod
    def Play_random_games(p1, p2, N, DEBUG):
        # SEEDING (no usar, queda como recordatorio que usarlo afecta las cartas y termina entrenando para el mismo set de cartas cada vez)
        # from numpy.random import seed
        # seed(1)
        assert p1.jugador == Reglas.JUGADOR1
        assert p2.jugador == Reglas.JUGADOR2

        lista_episodios = []

        # Declaro variables de monitoreo
        cont_win_p1 = 0
        cont_win_p2 = 0
        cont_empate = 0

        for i in range(N):
            print("\r" + str(((i+1)/N)*100)[0:5] + " % Training completado ", end="")
            #if DEBUG: printDebug("EPISODIO #" + str(i + 1) + "   ")

            e = Episodio()
            s = Estado()

            # SETUP INICIAL repartir cartas
            cartas_p1, cartas_p2 = Reglas.RepartirCartas()
            p1.TomarCartas(cartas_p1)
            p2.TomarCartas(cartas_p2)
            s.puntos_envido_p1 = p1.puntos_envido
            s.puntos_envido_p2 = p2.puntos_envido

            e.p1 = p1
            e.p2 = p2
            e.estados.append(copy.deepcopy(s))

            if DEBUG: printDebug("  Cartas Jugador 1: " + str(p1.cartas_totales))
            if DEBUG: printDebug("  Cartas Jugador 2: " + str(p2.cartas_totales))

            # Accion inicial
            current_player = p1
            a = p1.Elegir_Accion(s, False)

            # loops until the game is over
            while (s.QuienGanoManos() is None) and (s.truco is not Reglas.EstadoTruco.FOLD) :

                current_player.EjecutarAccion(s, a, DEBUG)
                if DEBUG: printDebug("      Nuevo estado: " + s.truco.name.lower() + ",  cartas: " + str(s.cartas_jugadas))

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
                        if DEBUG: printDebug(" GANE EL TRUCO! (jugador 1)")
                        e.ganadorTruco = Reglas.JUGADOR1
                    elif quien_gano == Reglas.JUGADOR2:
                        # Caso 3: terminal perdí
                        if DEBUG: printDebug(" GANE EL TRUCO! (jugador 2)")
                        e.ganadorTruco = Reglas.JUGADOR2
                else:
                    # Caso no terminal
                    a = next_player.Elegir_Accion(s, False)

                # Finalmente alterno jugador
                if s.QuienActua() == Reglas.JUGADOR1:
                    current_player = p1
                else:
                    current_player = p2
                #Termino la mano
                e.estados.append(copy.deepcopy(s))  # Agrego el estado intermedio al episodio

            # Terminó el while gameover
            lista_episodios.append(e)  # Agrego el episodio a la lista de episodios
            if DEBUG : print("Gano: " + str(e.ganadorTruco) + ",   puntaje:" + str(e.CalcularPuntosFinales()))
            total_p1, total_p2 = e.CalcularPuntosFinales()
            if total_p1 > total_p2: cont_win_p1 = cont_win_p1 + 1
            if total_p1 < total_p2: cont_win_p2 = cont_win_p2 + 1
            if total_p1 == total_p2: cont_empate = cont_empate + 1
            e.p1 = copy.copy(p1) #para evitar malentendidos posteriores. para que la variable e.p1 o e.p2 funcionen bien deberia hacer deepcopy que es muy costoso al tener una Red adentro
            e.p2 = copy.copy(p2) #para evitar malentendidos posteriores. para que la variable e.p1 o e.p2 funcionen bien deberia hacer deepcopy que es muy costoso al tener una Red adentro
        # Terminó el for N

        # Despliego resultados de la corrida
        winratio = cont_win_p1*100/(cont_win_p1+cont_win_p2+cont_empate)
        print("## RESULTADO ##  N= " + str(N) + " - j1: " + str(cont_win_p1) + ", j2: " + str(cont_win_p2) + ", Empates: " + str(cont_empate) + ", Total Win Ratio p1:"+ str(winratio)[0:5] + " ##")

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
    def ConvertStateToVector(jugador, estado, normalized=True): # Aca construimos el vector de largo fijo y normalizado para usar de input a la Red Neuronal
        result = []

        # 1ro ESTADO TRUCO (1 neurona)
        if normalized : result.append((estado.truco.value  - (len(Reglas.EstadoTruco)/2)) / len(Reglas.EstadoTruco) )  # normalizo usando total de estados posibles de truco
        else: result.append(estado.truco.value)

        # 2do ESTADO ENVIDO (3 neuronas: estado, puntos_p1 si aplica, puntos_p2 si aplica)
        if normalized:
            result.append((estado.envido.value - (len(Reglas.EstadoEnvido) / 2)) / len(Reglas.EstadoEnvido))  # normalizo usando total de estados posibles de truco
            if estado.envido in [Reglas.EstadoEnvido.E_ACEPTADO,
                                   Reglas.EstadoEnvido.EE_ACEPTADO,
                                   Reglas.EstadoEnvido.RF_ACEPTADO,
                                   Reglas.EstadoEnvido.EEF_ACEPTADO,
                                   Reglas.EstadoEnvido.EF_ACEPTADO,
                                   Reglas.EstadoEnvido.ER_ACEPTADO,
                                   Reglas.EstadoEnvido.ERF_ACEPTADO,
                                   Reglas.EstadoEnvido.R_ACEPTADO,
                                   Reglas.EstadoEnvido.F_ACEPTADO]:
                # El envido se jugó, agrego p1 seguro y p2 solo si gano el tanto (de lo contrario diria "buenas" y no muestra)
                result.append((estado.puntos_envido_p1 - 16) / 33)  # normalizo
                if estado.puntos_envido_p1 < estado.puntos_envido_p2:
                    result.append((estado.puntos_envido_p2 - 16) / 33)
                else:
                    result.append(0)  # padeo 0 porque p2 dijo "son buenas" y no revelo los puntos
            else:
                # El envido NO se jugó, solo me agrego yo
                if jugador.jugador is Reglas.JUGADOR1 :
                    result.append((estado.puntos_envido_p1 - 16)/33) #normalizo
                    result.append(0) # padeo 0 el otro jugador
                elif jugador.jugador is Reglas.JUGADOR2 :
                    result.append(0) # padeo 0 el otro jugador
                    result.append((estado.puntos_envido_p2 - 16)/33) #normalizo
                else: assert False
        else:
            result.append(estado.envido.value)
            if estado.envido in [Reglas.EstadoEnvido.E_ACEPTADO,
                                   Reglas.EstadoEnvido.EE_ACEPTADO,
                                   Reglas.EstadoEnvido.RF_ACEPTADO,
                                   Reglas.EstadoEnvido.EEF_ACEPTADO,
                                   Reglas.EstadoEnvido.EF_ACEPTADO,
                                   Reglas.EstadoEnvido.ER_ACEPTADO,
                                   Reglas.EstadoEnvido.ERF_ACEPTADO,
                                   Reglas.EstadoEnvido.R_ACEPTADO,
                                   Reglas.EstadoEnvido.F_ACEPTADO]:
                # El envido se jugó, agrego p1 seguro y p2 solo si gano el tanto (de lo contrario diria "buenas" y no muestra)
                result.append(estado.puntos_envido_p1)
                if estado.puntos_envido_p1 < estado.puntos_envido_p2:
                    result.append(estado.puntos_envido_p2)
                else:
                    result.append(0)  # padeo 0 porque p2 dijo "son buenas" y no revelo los puntos
            else:
                # El envido NO se jugó, solo me agrego yo
                if jugador.jugador is Reglas.JUGADOR1 :
                    result.append(estado.puntos_envido_p1)
                    result.append(0) # padeo 0 el otro jugador
                elif jugador.jugador is Reglas.JUGADOR2 :
                    result.append(0) # padeo 0 el otro jugador
                    result.append(estado.puntos_envido_p2)
                else: assert False


        # 3ro CARTAS DEL JUGADOR (18 neuronas:  3 cartas con 6 neuronas por carta: truco 4xPalo y envido  )
        for c in jugador.cartas_totales:
            if normalized :
                result.append((c.ValorTruco -50)/ 100)    # 100 es maximo valortruco de cualquier carta, lo centro en el origen
                result.extend(c.Palo_to_categorical_vector(normalized))
                result.append((c.ValorEnvido - 4) / 8)
            else:
                result.append(c.ValorTruco)
                result.extend(c.Palo_to_categorical_vector(normalized))
                result.append(c.ValorEnvido)

        # 4to CARTAS JUGADAS (36 neuronas, fijo: 6 cartas con 6 neuronas cada una truco, palo y envido)
        for i in range(6):
            if len(estado.cartas_jugadas) > i:
                if normalized :
                    result.append((estado.cartas_jugadas[i].ValorTruco-50)/100)  # 100 es maximo valortruco de cualquier carta, lo centro en el origen
                    result.extend(estado.cartas_jugadas[i].Palo_to_categorical_vector(normalized))
                    result.append((estado.cartas_jugadas[i].ValorEnvido - 4) / 8)
                else:
                    result.append(estado.cartas_jugadas[i].ValorTruco)
                    result.extend(estado.cartas_jugadas[i].Palo_to_categorical_vector(normalized))
                    result.append(estado.cartas_jugadas[i].ValorEnvido)
            else:  # padding (largo fijo 6, el resto completo con 0's)
                result.append(0)
                result.append(0)
                result.append(0)
                result.append(0)
                result.append(0)
                result.append(0)

        # 5to ACCIONES (42 neuronas, fijo = 21 acciones x 2 (jugador + codigo accion) )  secuencia= Jugador, CodigoAccion
        for i in range(21):
            if len(estado.acciones_hechas) > i:
                # Primero agrego el codigo de Jugador que hizo una accion
                if normalized : result.append(estado.acciones_hechas[i][0]-1.5) # codigo de jugador normalizado (a -0,5 y 0,5)
                else: result.append((estado.acciones_hechas[i][0])) # codigo de jugador sin normalizar

                # Segundo agrego el codigo de accion, evitando dataleak (que que un jugador vea accion JugarC1,2,3 del oponente)
                if estado.acciones_hechas[i][0] == jugador.jugador:
                    # si son mis jugadas puedo guardar el detalle (sea normalizado o no)
                    if normalized : result.append((estado.acciones_hechas[i][1].value-len(Reglas.Accion))/(len(Reglas.Accion)+1)) # codigo de accion normalizado
                    else: result.append(estado.acciones_hechas[i][1].value) # codigo de accion sin normalizar
                else:
                    # si son jugadas de otro, ignoro las acciones de jugar la carta agregando un cero
                    if estado.acciones_hechas[i][1].value not in [Reglas.Accion.JUGAR_C1.value,Reglas.Accion.JUGAR_C2.value,Reglas.Accion.JUGAR_C3.value ]:
                        if normalized : result.append((estado.acciones_hechas[i][1].value-len(Reglas.Accion))/(len(Reglas.Accion)+1))
                        else: result.append(estado.acciones_hechas[i][1].value)  # codigo de accion sin normalizar
                    else:
                        result.append(0)
            else: # si me quedo sin acciones que agregar hago padding (largo fijo 20, el resto completo con 0's)
                result.append(0)
                result.append(0)

        return result

