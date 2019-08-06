from Truco_Core_v4 import *
from matplotlib import pyplot
import keras
from keras import models, layers
from keras.callbacks import EarlyStopping, ModelCheckpoint
from itertools import chain
from scipy.special import softmax
import multiprocessing as mp


class HiperParametros:
    MAX_EPOCHS_PERGEN = 70
    PATIENCE_PERGEN = 6
    BATCH_SIZE = 256
    VALIDATION_RATIO = 0.40  # as % of the total amount of training games
    TRAINING_EPSILON = 0.05
    PLAYING_EPSILON = 0
    MULTIPROCESS_WORKER_POOL_COUNT = 2  # Ovearhead warning (y no funciona bien en entornos con GPU habilitadas)


# Este agente usa su Red de Valor para decidir acciones
class AgenteGreedyDVN:
    def __init__(self, jugador, dvn):
        self.eps = 0
        self.cartas_totales = []
        self.cartas_restantes = []
        self.DVN = dvn
        self.puntos_envido = 9

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

        if debug: print("")
        if debug: print(" p" + str(self.jugador) + " me toca!")
        # choose an action based on epsilon-greedy strategy
        r = np.random.rand()

        # podemos usar decaying epsilon (usando variable interna de clase) para el agente que vaya reduciendo eps. Esto me sirve porque cada training agent es nuevo.
        if r < self.eps:
            # take a random action
            if debug: print("  Taking a random action")
            idx = np.random.choice(len(self.get_acciones_posibles(s)))  # random 0,1 y 2
            a = self.get_acciones_posibles(s)[idx]

        else:
            a = None
            best = -10000

            _cp = AgenteGreedyDVN(self.jugador, self.DVN)
            _cp.cartas_totales = self.cartas_totales

            for i in self.get_acciones_posibles(s):
                # 1. copio
                _cp.cartas_restantes = copy.deepcopy(self.cartas_restantes)
                _s = copy.deepcopy(s)

                # 2. muevo
                _cp.EjecutarAccion(_s, i)

                # 3. convierto
                _s = Motor.ConvertStateToVector(_cp, _s, True)
                _s = np.squeeze(np.asarray(_s))  # Convierto a array de Red
                _s = _s.reshape(1, Motor.STATE_VECTOR_LENGTH)
                _s = _s.astype('float32')

                # 4. Estimo
                value = _cp.DVN.predict(_s)
                if value > best :
                    best = value
                    a = i
                if debug : print("     @p" + str(_cp.jugador) + " pensando en: " + str(i.name) + ",  valor: " + str(value[0][0])[0:6])
        if debug: print("     <p" + str(self.jugador) + "> accion elegida: " + str(a.name) + ",  valor: " + str(best))
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
        if DEBUG : print("  <<p" + str(self.jugador) + " - ejecutando accion: " + str(a) + ">>")
        s.acciones_hechas.append((self.jugador, a))

class AgenteSoftmaxDVN:
    def __init__(self, jugador, dvn):
        self.eps = 0
        self.cartas_totales = []
        self.cartas_restantes = []
        self.DVN = dvn
        self.puntos_envido = 9

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

        if debug: print("")
        if debug: print(" p" + str(self.jugador) + " me toca!")
        # choose an action based on epsilon-greedy strategy
        r = np.random.rand()

        # podemos usar decaying epsilon (usando variable interna de clase) para el agente que vaya reduciendo eps. Esto me sirve porque cada training agent es nuevo.
        if r < self.eps:
            # take a random action
            if debug: print("  Taking a random action")
            idx = np.random.choice(len(self.get_acciones_posibles(s)))  # random 0,1 y 2
            a = self.get_acciones_posibles(s)[idx]

        else:
            a = None
            best = -10000

            _cp = AgenteSoftmaxDVN(self.jugador, self.DVN)
            _cp.cartas_totales = self.cartas_totales

            acciones_posibles = self.get_acciones_posibles(s)
            valores_candidatos = []

            for i in acciones_posibles:
                # 1. copio
                _cp.cartas_restantes = copy.deepcopy(self.cartas_restantes)
                _s = copy.deepcopy(s)

                # 2. muevo
                _cp.EjecutarAccion(_s, i)

                # 3. convierto
                _s = Motor.ConvertStateToVector(_cp, _s, True)
                _s = np.squeeze(np.asarray(_s))  # Convierto a array de Red
                _s = _s.reshape(1, Motor.STATE_VECTOR_LENGTH)
                _s = _s.astype('float32')

                # 4. Estimo
                value = _cp.DVN.predict(_s)
                valores_candidatos.append(value)
                if debug : print("     @p" + str(_cp.jugador) + " pensando en: " + str(i.name) + ",  valor: " + str(value[0][0])[0:6])
            assert len(valores_candidatos) == len(acciones_posibles)
            valores_candidatos = softmax(valores_candidatos)
            a = random.choices(population=acciones_posibles, weights=valores_candidatos)[0]

        if debug: print("     <p" + str(self.jugador) + "> accion elegida: " + str(a.name) + ",  valor: " + str(best))
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
        if DEBUG : print("  <<p" + str(self.jugador) + " - ejecutando accion: " + str(a) + ">>")
        s.acciones_hechas.append((self.jugador, a))

class ValueNetworkEngine:

    @staticmethod  # Version SingleProcess de Generar Juegos de Entrenamiento
    def Generate_Value_Training_Games(p1, p2, batch_size, normalized=True):
        print("")
        print("#########################################")
        print("  DEPRECATED, USE MULTIPROCESS VERSION")
        print("(unless you are using GPU, then its fine)")
        print("#########################################")
        print("")

        p1_data = []
        p1_labels = []
        p2_data = []
        p2_labels = []
        print("Generando Partidas.. ( batch_size=" + str(batch_size) + " )")
        print("")

        # Corremos
        episodios = Motor.Play_random_games(p1, p2, batch_size, False)
        for e in episodios:
            for s in reversed(range(len(e.estados))):
                # logica: "si en [s-1] me toca a mi, en [s] ya jugue yo. Guardo ese estado con mi movimiento hecho y el puntaje total
                if s > 0 and e.estados[s - 1].QuienActua() is Reglas.JUGADOR1:
                    p1_data.append(Motor.ConvertStateToVector(e.p1, e.estados[s], normalized))
                    p1_labels.append(e.CalcularPuntosFinales()[0] - e.CalcularPuntosFinales()[1])

                if s > 0 and e.estados[s - 1].QuienActua() is Reglas.JUGADOR2:
                    p2_data.append(Motor.ConvertStateToVector(e.p2, e.estados[s], normalized))
                    p2_labels.append(e.CalcularPuntosFinales()[1] - e.CalcularPuntosFinales()[0])

        return (p1_data, p1_labels), (p2_data, p2_labels)

    @staticmethod  # Version MultiProcess de Generar Juegos: Worker helper function
    def MP_value_worker(p1, p2, N, queue):
        print("")
        # Los clono para evitar que se ensucie con otros threads de generacion de partidas
        p1 = copy.deepcopy(p1)
        p2 = copy.deepcopy(p2)
        episodios = Motor.Play_random_games(p1, p2, N, False)
        queue.put(episodios)
        # import sys
        # sys.stdout.flush()

    @staticmethod  # Version MultiProcess de Generar Juegos: Main Function
    def MP_Generate_Value_Training_Games(p1, p2, batch_size, normalized=True):
        p1_data = []
        p1_labels = []
        p2_data = []
        p2_labels = []
        process_count = HiperParametros.MULTIPROCESS_WORKER_POOL_COUNT

        assert process_count >= 1
        assert batch_size >= process_count

        print("Generando Partidas.. ( batch_size=" + str(batch_size) + " )")
        print("")

        # Me divido la partidas entre la cantidad de workers
        N = round(batch_size / process_count )
        # creo las colas de retorno
        listaQueues = []
        for q in range(process_count):
            listaQueues.append(mp.Queue())

        # creo los 4 workers
        listaProcess = []
        for q in listaQueues:
            listaProcess.append(mp.Process(target=ValueNetworkEngine.MP_value_worker, args=(p1, p2, N, q)))

        for p in listaProcess:
            p.start()

        listaEpisodios = []
        for q in listaQueues:
            # obtengo el retorno de los 4 workers
            listaEpisodios.append(q.get())

        for p in listaProcess:
            # espero que retornen
            p.join()

        # sumo los resultados
        for e in list(itertools.chain.from_iterable(listaEpisodios)):
            # for e in chain(episodios1, episodios2):
            # pero quizas esto sea con otra Red de Value (esta es policy)
            for s in reversed(range(len(e.estados))):
                # logica: "si en [s-1] me toca a mi, en [s] ya jugue yo. Guardo ese estado con mi movimiento hecho y el puntaje total

                if s > 0 and e.estados[s - 1].QuienActua() is Reglas.JUGADOR1:
                    p1_data.append(Motor.ConvertStateToVector(e.p1, e.estados[s], normalized))
                    p1_labels.append(e.CalcularPuntosFinales()[0] - e.CalcularPuntosFinales()[1])

                if s > 0 and e.estados[s - 1].QuienActua() is Reglas.JUGADOR2:
                    p2_data.append(Motor.ConvertStateToVector(e.p2, e.estados[s], normalized))
                    p2_labels.append(e.CalcularPuntosFinales()[1] - e.CalcularPuntosFinales()[0])

        return (p1_data, p1_labels), (p2_data, p2_labels)

    @staticmethod  #Version Multiprocess de Testear Agentes: NO ACTUALIZADA (REVISAR!! la deja para no perderla por si la quiero terminar luego)
    def MP_TestDVNAgents(p1, p2, N, debug):  ## DEPRECRATED
        # Me divido la partidas entre la cantidad de workers

        N = round(N / 4)
        # creo las colas de retorno
        queue1 = mp.Queue()
        queue2 = mp.Queue()
        queue3 = mp.Queue()
        queue4 = mp.Queue()
        # creo los 4 workers
        process1 = mp.Process(target=Motor.MP_value_worker, args=(p1, p2, N, queue1))
        process2 = mp.Process(target=Motor.MP_value_worker, args=(p1, p2, N, queue2))
        process3 = mp.Process(target=Motor.MP_value_worker, args=(p1, p2, N, queue3))
        process4 = mp.Process(target=Motor.MP_value_worker, args=(p1, p2, N, queue4))
        # comienzo la ejecucion de los 4 workers en paralelo
        process1.start()
        process2.start()
        process3.start()
        process4.start()
        # obtengo el retorno de los 4 workers
        episodios1 = queue1.get()
        episodios2 = queue2.get()
        episodios3 = queue3.get()
        episodios4 = queue4.get()
        # espero que retornen
        process1.join()
        process2.join()
        process3.join()
        process4.join()
        # sumo los resultados
        # print("eps totales:" + str(len(episodios))+ ", ep1:" + str(len(episodios1))+", ep2:" + str(len(episodios2))+", ep3:" + str(len(episodios3))+", ep4:" + str(len(episodios4)))

        cont_p1 = 0
        cont_p2 = 0

        for e in chain(episodios1, episodios2, episodios3, episodios4):
            puntos_p1, puntos_p2 = e.CalcularPuntosFinales()
            if puntos_p1 > puntos_p2: cont_p1 = cont_p1 + 1
            if puntos_p1 < puntos_p2: cont_p2 = cont_p2 + 1

        winratio = cont_p1 * 100 / (cont_p1 + cont_p2)

        if debug:
            print("")
            print("#############")
            print("#############")
            print("## RESULTADO ##  N= " + str(N * 4) + " - j1: " + str(cont_p1) + ", j2: " + str(cont_p2) + ", Empates: " + str(
                (N * 4) - cont_p1 - cont_p2) + ", WINRATIO p1:" + str(winratio)[0:5] + " ##")
            print("#############")
            print("#############")
            print("")
        return winratio

    @staticmethod  #Generar Red Deep Value Network usada por los agentes (ya sea Greedy o Softmax)
    def Generate_Player_DVN():
        from keras.layers import LeakyReLU

        player_DVN = models.Sequential()
        player_DVN.add(layers.Dense(100, input_shape=(Motor.STATE_VECTOR_LENGTH,)))
        player_DVN.add(LeakyReLU(alpha=0.1))
        player_DVN.add(layers.Dense(100, kernel_regularizer=keras.regularizers.l2(0.01)))
        player_DVN.add(LeakyReLU(alpha=0.1))
        #player_DVN.add(layers.Dropout(0.2))  # DROPOUT
        player_DVN.add(layers.Dense(100, kernel_regularizer=keras.regularizers.l2(0.01)))
        player_DVN.add(LeakyReLU(alpha=0.1))
        player_DVN.add(layers.Dense(100, kernel_regularizer=keras.regularizers.l2(0.01)))
        player_DVN.add(LeakyReLU(alpha=0.1))
        #player_DVN.add(layers.Dropout(0.2)) # DROPOUT
        player_DVN.add(layers.Dense(100, kernel_regularizer=keras.regularizers.l2(0.01)))
        player_DVN.add(LeakyReLU(alpha=0.1))
        player_DVN.add(layers.Dense(100, kernel_regularizer=keras.regularizers.l2(0.01)))
        player_DVN.add(LeakyReLU(alpha=0.1))
        #player_DVN.add(layers.Dropout(0.2))  # DROPOUT
        player_DVN.add(layers.Dense(100, kernel_regularizer=keras.regularizers.l2(0.01)))
        player_DVN.add(LeakyReLU(alpha=0.1))
        player_DVN.add(layers.Dense(100, kernel_regularizer=keras.regularizers.l2(0.01)))
        player_DVN.add(LeakyReLU(alpha=0.1))
        player_DVN.add(layers.Dense(1))

        #version alternativa para tunear el optimizer mejor
        #r_optimizer = keras.optimizers.Adam(lr=0.0001, decay=.02)
        #player_DVN.compile(optimizer=r_optimizer, loss='mse', metrics=['mae'])

        player_DVN.compile(optimizer='adam', loss='mse', metrics=['mae'])

        return player_DVN

    @staticmethod  # Genero un vector de prueba acida (lo uso al terminar de entrenar una generacion)
    def Get_VectorEstado_Prueba():
        print("###########################")
        print("##   Partida de Prueba   ##")
        print("###########################")
        print("")

        # SETUP
        s = Estado()
        p1 = AgenteRandom(Reglas.JUGADOR1)
        p2 = AgenteRandom(Reglas.JUGADOR2)
        cartas_j1 = []
        cartas_j2 = []
        cartas_j1.append(Reglas.MAZO[40])  # Carta("1-Espada", 98
        cartas_j1.append(Reglas.MAZO[21])  # Carta("11-Basto", 42)
        cartas_j1.append(Reglas.MAZO[10])  # Carta("6-Oro", 21)
        cartas_j2.append(Reglas.MAZO[39])  # Carta("1-Basto", 91)
        cartas_j2.append(Reglas.MAZO[30])  # Carta("2-Oro", 63)
        cartas_j2.append(Reglas.MAZO[3])  # Carta("4-Basto", 7)

        p1.TomarCartas(cartas_j1)
        p2.TomarCartas(cartas_j2)
        s.puntos_envido_p1 = p1.puntos_envido
        s.puntos_envido_p2 = p2.puntos_envido

        # Prueba
        print("1) p1 juega c1, acciones de p2 disponibles")
        p1.EjecutarAccion(s, Reglas.Accion.JUGAR_C1)
        print(str(p2.get_acciones_posibles(s)))
        print("")
        return p1, p2, s  # poner esta linea donde quiera testear predict de la red

        print("2) p2 grito Truco, acciones de p1 disponibles")
        p2.EjecutarAccion(s, Reglas.Accion.GRITAR)
        print(str(p1.get_acciones_posibles(s)))
        print("")

        print("3) p1 acepto, acciones de p2 disponibles")
        p1.EjecutarAccion(s, Reglas.Accion.QUIERO_GRITO)
        print(str(p2.get_acciones_posibles(s)))
        print("")

        print("4) p2 jugo c3, acciones de p1 disponibles")
        p2.EjecutarAccion(s, Reglas.Accion.JUGAR_C3)
        print(str(p1.get_acciones_posibles(s)))
        print("")

        print("5) p1 jugo c2, acciones de p2 disponibles")
        p1.EjecutarAccion(s, Reglas.Accion.JUGAR_C2)
        print(str(p2.get_acciones_posibles(s)))
        print("")
        print(">> Cartas jugadas hasta ahora: " + str(s.cartas_jugadas))

        return p1, p2, s # poner esta linea donde quiera testear predict de la red

    @staticmethod  # Genera partidas de entrenamiento (1. carga los DVN.h5 ; 2. creo los agentes ; 3. los hago jugar ; 4. Save pickle a disco)
    def Generate_and_Save(input_prefix, output_prefix, games_per_gen, multi_process=False):

        print("  ##   Generate_and_Save   ##")
        print("")

        if input_prefix is not None:
            # Si input prefix es None, entonces es generacion inicial Random, de lo contrario cargamos generacion anterior
            p1_DQN = keras.models.load_model(input_prefix + "p1_DVN.h5")
            p2_DQN = keras.models.load_model(input_prefix + "p2_DVN.h5")
            p1 = AgenteSoftmaxDVN(Reglas.JUGADOR1, p1_DQN)
            p1.eps = HiperParametros.TRAINING_EPSILON
            p2 = AgenteSoftmaxDVN(Reglas.JUGADOR2, p2_DQN)
            p2.eps = HiperParametros.TRAINING_EPSILON
        else:
            p1 = AgenteRandom(Reglas.JUGADOR1)
            p2 = AgenteRandom(Reglas.JUGADOR2)

        print("1. Generando Partidas de entrenamiento")
        if multi_process is True : (p1_traindata, p1_trainlabels), (p2_traindata, p2_trainlabels) = ValueNetworkEngine.MP_Generate_Value_Training_Games(p1, p2, games_per_gen)
        else : (p1_traindata, p1_trainlabels), (p2_traindata, p2_trainlabels) = ValueNetworkEngine.Generate_Value_Training_Games(p1, p2, games_per_gen)

        print("")
        print("2. Generando Partidas de test")
        if multi_process is True :
            (p1_testdata, p1_testlabels), (p2_testdata, p2_testlabels) = ValueNetworkEngine.MP_Generate_Value_Training_Games(
                    p1, p2, round(games_per_gen*HiperParametros.VALIDATION_RATIO)) # Usamos Ratio del Trainign set para determinar tamaño de validation
        else:
            (p1_testdata, p1_testlabels), (p2_testdata, p2_testlabels) = ValueNetworkEngine.Generate_Value_Training_Games(
                    p1, p2, round(games_per_gen*HiperParametros.VALIDATION_RATIO)) # Usamos Ratio del Trainign set para determinar tamaño de validation

        print("len p1_traindata: " + str(len(p1_traindata)) + ", len p1_testdata: " + str(len(p1_testdata)))
        print("len p1_trainlabels: " + str(len(p1_trainlabels)) + ", len p1_testlabels: " + str(len(p1_testlabels)))
        print("len p2_traindata: " + str(len(p2_traindata)) + ", len p2_testdata: " + str(len(p2_testdata)))
        print("len p2_trainlabels: " + str(len(p2_trainlabels)) + ", len p2_testlabels: " + str(len(p2_testlabels)))

        print("")
        print("3. Guardando partidas en Disco (pickle) con prefijo:" + output_prefix + "...")
        # train
        Motor.Save_Games_to_Disk(p1_traindata, output_prefix + "p1_traindata.pickle")
        Motor.Save_Games_to_Disk(p1_trainlabels, output_prefix + "p1_trainlabels.pickle")
        Motor.Save_Games_to_Disk(p2_traindata, output_prefix + "p2_traindata.pickle")
        Motor.Save_Games_to_Disk(p2_trainlabels, output_prefix + "p2_trainlabels.pickle")
        # test
        Motor.Save_Games_to_Disk(p1_testdata, output_prefix + "p1_testdata.pickle")
        Motor.Save_Games_to_Disk(p1_testlabels, output_prefix + "p1_testlabels.pickle")
        Motor.Save_Games_to_Disk(p2_testdata, output_prefix + "p2_testdata.pickle")
        Motor.Save_Games_to_Disk(p2_testlabels, output_prefix + "p2_testlabels.pickle")
        print("  ...guardado!")
        print("")

    @staticmethod  # Entrena las Redes (1. carga los pickles de disco ; 2. Fit p1 DVN ; 3. Fit p2 DVN ; 4. Save DVN.h5 a disco)
    def Train_Save(gen_prefix, training_epochs, load_previous = False):

        print("  ##   Train_Save   ##")
        print("")

        #########################
        ## ENTRENO RED PARA p1

        print("  ## Carga de partidas de entrenamiento P1 desde Disco (pickles) con prefijo '" + gen_prefix + "'")
        # p1
        p1_traindata = Motor.Load_Games_From_Disk(gen_prefix + "p1_traindata.pickle")
        p1_trainlabels = Motor.Load_Games_From_Disk(gen_prefix + "p1_trainlabels.pickle")
        p1_testdata = Motor.Load_Games_From_Disk(gen_prefix + "p1_testdata.pickle")
        p1_testlabels = Motor.Load_Games_From_Disk(gen_prefix + "p1_testlabels.pickle")


        if load_previous is True:
            if len(gen_prefix) == 19:
                prev_gen = int(gen_prefix[-2]) - 1  # tomo el numero de generacion del string, lo parseo a int y le resto 1
                prev_gen = gen_prefix[:-2] + str(prev_gen) + gen_prefix[-1:]  #vuelvo a recrear el string
            elif len(gen_prefix) == 20:
                prev_gen = int(gen_prefix[-3:-1:]) - 1  # tomo el numero de generacion del string, lo parseo a int y le resto 1
                prev_gen = gen_prefix[:-3] + str(prev_gen) + gen_prefix[-1:]  # vuelvo a recrear el string
            else:
                assert False # length of string gen_prefix unexpected
            # cargo y anexo
            p1_traindata = p1_traindata + Motor.Load_Games_From_Disk(prev_gen + "p1_traindata.pickle")
            p1_trainlabels = p1_trainlabels + Motor.Load_Games_From_Disk(prev_gen + "p1_trainlabels.pickle")


        ## VALIDO LEN VECTORES
        assert len(p1_traindata) == len(p1_trainlabels)
        assert len(p1_testdata) == len(p1_testlabels)

        print("")
        print("  ## Entrenando Red para P1ayer 1")
        p1_DVN = ValueNetworkEngine.Generate_Player_DVN()

        # Convierto a nparray y reshape a lo especificado en las capas de la red neuronal (shape a Motor.STATE_VECTOR_LENGTH)
        # Train
        p1_traindata = np.squeeze(np.asarray(p1_traindata))
        p1_traindata = p1_traindata.reshape((len(p1_traindata), Motor.STATE_VECTOR_LENGTH))
        p1_traindata = p1_traindata.astype('float32')
        # Test
        p1_testdata = np.squeeze(np.asarray(p1_testdata))
        p1_testdata = p1_testdata.reshape((len(p1_testdata), Motor.STATE_VECTOR_LENGTH))
        p1_testdata = p1_testdata.astype('float32')

        # patient early stopping
        callbacks = [EarlyStopping(monitor='val_loss', patience=HiperParametros.PATIENCE_PERGEN),
                     ModelCheckpoint(filepath=gen_prefix+"p1_DVN.h5", monitor='val_loss', save_best_only=True)]

        # Fiteo la red ACA
        history = p1_DVN.fit(p1_traindata, p1_trainlabels, validation_data=(p1_testdata, p1_testlabels),
                             callbacks=callbacks, epochs=training_epochs, batch_size=HiperParametros.BATCH_SIZE,
                             shuffle=True, verbose=2)

        # evaluate the model ACA
        _, train_acc = p1_DVN.evaluate(p1_traindata, p1_trainlabels, verbose=0)
        _, test_acc = p1_DVN.evaluate(p1_testdata, p1_testlabels, verbose=0)
        print('Train: %.3f, Test: %.3f' % (train_acc, test_acc))
        # plot training history ACA
        #pyplot.clf()
        pyplot.figure(1)
        pyplot.plot(history.history['loss'], label=('train p1 (gen '+str(gen_prefix)+")"))
        pyplot.plot(history.history['val_loss'], label=('test p1 (gen '+str(gen_prefix)+")"))
        pyplot.legend()
        pyplot.draw()
        pyplot.pause(0.001)


        print("")
        #print("  ...guardando Red DVN de p1 con prefijo '" + gen_prefix + "'")
        #p1_DVN.save(gen_prefix+"p1_DVN.h5")
        print("    ..." + gen_prefix + "p1_DVN.h5 guardado!")

        # Free memory explicit
        del p1_traindata
        del p1_DVN



        #########################
        ## ENTRENO RED PARA p2
        print("## Carga de partidas de entrenamiento P2 desde Disco (pickles) con prefijo '" + gen_prefix + "'")
        # p2
        p2_traindata = Motor.Load_Games_From_Disk(gen_prefix + "p2_traindata.pickle")
        p2_trainlabels = Motor.Load_Games_From_Disk(gen_prefix + "p2_trainlabels.pickle")
        p2_testdata = Motor.Load_Games_From_Disk(gen_prefix + "p2_testdata.pickle")
        p2_testlabels = Motor.Load_Games_From_Disk(gen_prefix + "p2_testlabels.pickle")

        if load_previous is True:
            #este IF es para corregir el string del path cuando la generacion cambia de 1 digito a 2 digitos
            if len(gen_prefix) == 19:
                prev_gen = int(gen_prefix[-2]) - 1  # tomo el numero de generacion del string, lo parseo a int y le resto 1
                prev_gen = gen_prefix[:-2] + str(prev_gen) + gen_prefix[-1:]  # vuelvo a recrear el string
            elif len(gen_prefix) == 20:
                prev_gen = int(gen_prefix[-3:-1:]) - 1  # tomo el numero de generacion del string, lo parseo a int y le resto 1
                prev_gen = gen_prefix[:-3] + str(prev_gen) + gen_prefix[-1:]  # vuelvo a recrear el string
            else:
                assert False  # length of string gen_prefix unexpected
            # cargo y anexo
            p2_traindata = p2_traindata + Motor.Load_Games_From_Disk(prev_gen + "p1_traindata.pickle")
            p2_trainlabels = p2_trainlabels + Motor.Load_Games_From_Disk(prev_gen + "p1_trainlabels.pickle")

        ## VALIDO LEN VECTORES
        assert len(p2_traindata) == len(p2_trainlabels)
        assert len(p2_testdata) == len(p2_testlabels)

        print("")
        print("## Entrenando Red para P1ayer 2")
        p2_DVN = ValueNetworkEngine.Generate_Player_DVN()

        # Convierto a nparray y reshape a lo especificado en las capas de la red neuronal (shape a Motor.STATE_VECTOR_LENGTH)
        # Train
        p2_traindata = np.squeeze(np.asarray(p2_traindata))
        p2_traindata = p2_traindata.reshape((len(p2_traindata), Motor.STATE_VECTOR_LENGTH))
        p2_traindata = p2_traindata.astype('float32')

        # Test
        p2_testdata = np.squeeze(np.asarray(p2_testdata))
        p2_testdata = p2_testdata.reshape((len(p2_testdata), Motor.STATE_VECTOR_LENGTH))
        p2_testdata = p2_testdata.astype('float32')

        # patient early stopping
        callbacks = [EarlyStopping(monitor='val_loss', patience=HiperParametros.PATIENCE_PERGEN),
                     ModelCheckpoint(filepath=gen_prefix + "p2_DVN.h5", monitor='val_loss', save_best_only=True)]

        # Fiteo la red
        p2_DVN.fit(p2_traindata, p2_trainlabels, validation_data=(p2_testdata, p2_testlabels),
                   callbacks=callbacks, epochs=training_epochs, batch_size=HiperParametros.BATCH_SIZE,
                   shuffle=True, verbose=2)

        # evaluate the model ACA
        _, train_acc = p2_DVN.evaluate(p2_traindata, p2_trainlabels, verbose=0)
        _, test_acc = p2_DVN.evaluate(p2_testdata, p2_testlabels, verbose=0)
        print('Train: %.3f, Test: %.3f' % (train_acc, test_acc))
        # plot training history ACA
        pyplot.figure(2)
        pyplot.plot(history.history['loss'], label=('train p2 (gen '+str(gen_prefix)+")"))
        pyplot.plot(history.history['val_loss'], label=('test p2 (gen '+str(gen_prefix)+")"))
        pyplot.legend()
        pyplot.draw()
        pyplot.pause(0.001)

        print("")
        #print("  ...guardando red DVN de p2 con prefijo '" + gen_prefix + "'")
        #p2_DVN.save(gen_prefix + "p2_DVN.h5")
        print("    ..." + gen_prefix + "p2_DVN.h5 guardado!")

        # Free memory explicit
        del p2_traindata
        del p2_DVN

    @staticmethod  # Levanta las Redes de y les hace una prueba acida
    def Load_and_Test(gen_prefix):
        print("  ##   Load_and_Test   ##")
        print("")
        print("  ## Carga de partidas de Test desde Disco (pickles) con prefijo: " + gen_prefix)

        print("")
        print("## Loading model from disk")
        # p1
        p1_DVN = keras.models.load_model(gen_prefix + "p1_DVN.h5")
        # p2
        p2_DVN = keras.models.load_model(gen_prefix + "p2_DVN.h5")

        # AHORA SI, EJECUTO PRUEBA
        p1,p2, s = ValueNetworkEngine.Get_VectorEstado_Prueba()

        currentplayer = s.QuienActua()
        if s.QuienActua() == Reglas.JUGADOR1: currentplayer = p1
        if s.QuienActua() == Reglas.JUGADOR2 : currentplayer = p2

        print("Le toca a p" + str(currentplayer.jugador))
        print(" cartas en mesa: " + str(s.cartas_jugadas))
        print(" cartas totales: " + str(currentplayer.cartas_totales))
        print(" cartas restates: " + str(currentplayer.cartas_restantes))
        print("")

        for i in currentplayer.get_acciones_posibles(s):
            # 1. copio
            _p1 = copy.deepcopy(p1)
            _p2 = copy.deepcopy(p2)
            _s = copy.deepcopy(s)
            if currentplayer.jugador is Reglas.JUGADOR1 : _cp = _p1
            if currentplayer.jugador is Reglas.JUGADOR2 : _cp = _p2

            # 2. muevo
            _cp.EjecutarAccion(_s, i)

            # 3. convierto
            _s = Motor.ConvertStateToVector(_cp, _s, True)
            _s = np.squeeze(np.asarray(_s))# Convierto a array de Red
            _s = _s.reshape(1, Motor.STATE_VECTOR_LENGTH)
            _s = _s.astype('float32')

            # 4. Estimo
            if _cp.jugador is Reglas.JUGADOR1 : output = p1_DVN.predict(_s)
            if _cp.jugador is Reglas.JUGADOR2 : output = p2_DVN.predict(_s)
            print("p" + str(_cp.jugador) + "> accion posible: " + str(i.name) + ",  valor:" + str(output))

            # Free memory explicit
            #del _p1
            #del _p2
            #del _s

        #Free memory explicit
        del p1
        del p2
        del s
        del p1_DVN
        del p2_DVN

    @staticmethod  # Pone 2 agentes a competir entre si con N partidas de entrenamiento
    def HeadToHead_PlayTest(gen_p1, gen_p2, N, debug):
        gen1 = gen_p1
        gen2 = gen_p2

        print("")
        print("(warning, versus test usa greedy agent, not stockastic )")
        print("JUGANDO gen" + str(gen_p1) + " versus gen" + str(gen_p2))
        if gen_p1 > 0:
            gen_p1 = "value_pickles\gen" + str(gen_p1) + "_"
            p1_DVN = keras.models.load_model(gen_p1 + "p1_DVN.h5")
            value_p1 = AgenteGreedyDVN(Reglas.JUGADOR1, p1_DVN)
            value_p1.eps = HiperParametros.PLAYING_EPSILON
        else:
            value_p1 = AgenteRandom(Reglas.JUGADOR1)

        if gen_p2 > 0:
            gen_p2 = "value_pickles\gen" + str(gen_p2) + "_"
            p2_DVN = keras.models.load_model(gen_p2 + "p2_DVN.h5")
            value_p2 = AgenteGreedyDVN(Reglas.JUGADOR2, p2_DVN)
            value_p2.eps = HiperParametros.PLAYING_EPSILON
        else:
            value_p2 = AgenteRandom(Reglas.JUGADOR2)

        Motor.Play_random_games(value_p1, value_p2, N, debug)
        print("### JUGANDO gen" + str(gen_p1) + " versus gen" + str(gen_p2))
        print("############################################################")
        print("############################################################")
        print("############################################################")
        print("")

        # Free memory explicit
        del value_p1
        del value_p2
        #FINMETODO

    @staticmethod  # Metodo principal para entrenar generaciones de Agentes (el a su vez llama los distintos metodos como Generate y Train)
    def ValueNetworkTrainer(start_gen, generations, games_per_gen, multi_process=False):
        # WARNING: Debe existir start_gen tanto en h5 como pickles
        # Detalle: Los start_gen.h5 los levanta en Generate_and_Save para generar juegos de aprendizaje
        # Los pickles son necesarios porque el entrenamiento de start_gen + 1 los tambien (a menos que deshabilitemos load_previous)
        printDebug("COMIENZO!")
        print("")

        for i in range(start_gen, start_gen+generations):
            print("")
            print("##########################")
            print("##     GENERACION " + str(i+1) + "     ##")
            print("##########################")
            print("")
            gen_n = "value_pickles\gen" + str(i) + "_"
            gen_next = "value_pickles\gen" + str(i + 1) + "_"
            if i == 0: gen_n = None

            # Genero las partidas y guardo los pickles en disco (omitir si ya tengo un buen pickle generado)
            ValueNetworkEngine.Generate_and_Save(gen_n, gen_next, games_per_gen, multi_process)
            # Cargo las partidas de Disco, entreno la red y la guardo en disco en h5 (omitir si ya tengo una buena Red entrenada)
            if i == 0:
                ValueNetworkEngine.Train_Save(gen_next, HiperParametros.MAX_EPOCHS_PERGEN, False)
            else:
                ValueNetworkEngine.Train_Save(gen_next, HiperParametros.MAX_EPOCHS_PERGEN, True)
            # finalmente, cargo una Red de disco (formato h5) y juego/testeo
            ValueNetworkEngine.Load_and_Test(gen_next)

        print("")
        printDebug("## TERMINE! ##")