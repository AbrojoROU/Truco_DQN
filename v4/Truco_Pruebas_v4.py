import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # or any {'0', '1', '2'}
os.environ['TF_CPP_MIN_VLOG_LEVEL'] = '0'
from Truco_Core_v4 import *
from Truco_Value_Network_v4 import *
import numpy as np





def prueba_QuienGanoManos():
    print("")
    print("===================================================")
    print("## PRUEBA - Quien Gano Manos - ##")
    print("===================================================")
    print("")

    # Creao estado dummy
    s = Estado()

    # Pruebas
    s.cartas_jugadas = Motor.Construir_Lista_Cartas("985613")  # La de DEBUG
    print("Prueba con (100-80, 30-40, 10-20): " + str(s.QuienGanoManos()))
    s.cartas_jugadas = Motor.Construir_Lista_Cartas("452179")  # Empatan la 1ra
    print("Prueba con (30-30, 20-10, 40-100): " + str(s.QuienGanoManos()))
    s.cartas_jugadas = Motor.Construir_Lista_Cartas("451297")  # Empatan la 1ra
    print("Prueba con (30-30, 10-20,  100-40): "  + str(s.QuienGanoManos()))
    s.cartas_jugadas = Motor.Construir_Lista_Cartas("214579")  # Empatan 2da
    print("Prueba con (20-10, 30-30, 40-100): " + str(s.QuienGanoManos()))
    s.cartas_jugadas = Motor.Construir_Lista_Cartas("124597")  # Empatan 2da
    print("Prueba con (10-20, 30-30, 100-40): " + str(s.QuienGanoManos()))
    s.cartas_jugadas = Motor.Construir_Lista_Cartas("214567")  # Empatan 2da y 3ra
    print("Prueba con (20-10, 30-30, 40-40): " + str(s.QuienGanoManos()))
    s.cartas_jugadas = Motor.Construir_Lista_Cartas("124567")  # Empatan 2da y 3ra
    print("Prueba con (10-20, 30-30, 40-40): " + str(s.QuienGanoManos()))
    s.cartas_jugadas = Motor.Construir_Lista_Cartas("452167")  # Empatan 2da y 3ra
    print("Prueba con (30-30, 20-10, 40-40): " + str(s.QuienGanoManos()))
    s.cartas_jugadas = Motor.Construir_Lista_Cartas("452367")  # Empatan las 3
    print("Prueba con (30-30, 20-20, 40-40): " + str(s.QuienGanoManos()))
    s.cartas_jugadas = Motor.Construir_Lista_Cartas("452317")  # Empatan la 1ra y 2da
    print("Prueba con (30-30, 20-20, 10-40): " + str(s.QuienGanoManos()))
    s.cartas_jugadas = Motor.Construir_Lista_Cartas("452371") # Empatan la 1ra y 2da
    print("Prueba con (30-30, 20-20, 40-10): " + str(s.QuienGanoManos()))
    s.cartas_jugadas = Motor.Construir_Lista_Cartas("45")  # Empatan la 1ra y 2da
    print("Prueba con (30-30, ...): " + str(s.QuienGanoManos()))

def prueba_QuienJugariaCarta():
    print("")
    print("===================================================")
    print("## PRUEBA - Quien Jugaria Carta - ##")
    print("===================================================")
    print("Reglas de prueba: 2-3  4-5   y 6-7  empatan, el resto gana quien tiene ID mas alto ")
    print("")

    # Creao estado dummy
    s = Estado()

    # Pruebas
    s.cartas_jugadas = Motor.Construir_Lista_Cartas("9856")
    print("9856" + " : " + str(s.QuienJugariaCarta()))
    s.cartas_jugadas = Motor.Construir_Lista_Cartas("6")
    print("6" + " : " + str(s.QuienJugariaCarta()))
    s.cartas_jugadas = Motor.Construir_Lista_Cartas("23")  # empate
    print("23" + " : " + str(s.QuienJugariaCarta()))
    s.cartas_jugadas = Motor.Construir_Lista_Cartas("84")  # empate
    print("84" + " : " + str(s.QuienJugariaCarta()))
    s.cartas_jugadas = Motor.Construir_Lista_Cartas("48")  # empate
    print("48" + " : " + str(s.QuienJugariaCarta()))
    s.cartas_jugadas = Motor.Construir_Lista_Cartas("164")  # empate
    print("164" + " : " + str(s.QuienJugariaCarta()))
    s.cartas_jugadas = Motor.Construir_Lista_Cartas("628")  # empate
    print("628" + " : " + str(s.QuienJugariaCarta()))
    s.cartas_jugadas = Motor.Construir_Lista_Cartas("2384")  # primera empatan
    print("2384" + " : " + str(s.QuienJugariaCarta()))
    s.cartas_jugadas = Motor.Construir_Lista_Cartas("2348")  # primera empatan
    print("2348" + " : " + str(s.QuienJugariaCarta()))
    s.cartas_jugadas = Motor.Construir_Lista_Cartas("8423")  # segunda empatan
    print("8423" + " : " + str(s.QuienJugariaCarta()))
    s.cartas_jugadas = Motor.Construir_Lista_Cartas("4823")  # segunda empatan
    print("2348" + " : " + str(s.QuienJugariaCarta()))
    s.cartas_jugadas = Motor.Construir_Lista_Cartas("2345")  # Doble Empate
    print("2345" + " : " + str(s.QuienJugariaCarta()))
    s.cartas_jugadas = Motor.Construir_Lista_Cartas("23845")  # primera empatan
    print("23845" + " : " + str(s.QuienJugariaCarta()))
    s.cartas_jugadas = Motor.Construir_Lista_Cartas("23485") # primera empatan
    print("23485" + " : " + str(s.QuienJugariaCarta()))
    s.cartas_jugadas = Motor.Construir_Lista_Cartas("85234")  # segunda empatan
    print("85234" + " : " + str(s.QuienJugariaCarta()))
    s.cartas_jugadas = Motor.Construir_Lista_Cartas("58234")  # segunda empatan
    print("58234" + " : " + str(s.QuienJugariaCarta()))
    s.cartas_jugadas = Motor.Construir_Lista_Cartas("23457")  # Doble Empate
    print("23457" + " : " + str(s.QuienJugariaCarta()))

def prueba_QuienActua():
    print("")
    print("===================================================")
    print("## PRUEBA - Quien Actua - ##")
    print("===================================================")
    print("prueba 1")

    # PRUEBA 1
    s = Estado()
    print("inicial, le toca a: p" + str(s.QuienActua()))

    s.acciones_hechas.append((Reglas.JUGADOR1, Reglas.Accion.JUGAR_C1))
    s.cartas_jugadas.append(Carta("4-Copa", 10))
    print("p1 jugó carta 1, le toca a: p" + str(s.QuienActua()))

    s.acciones_hechas.append((Reglas.JUGADOR2, Reglas.Accion.GRITAR))
    s.truco = Reglas.EstadoTruco.TRUCO_DICHO
    print("p2 grito Truco, le toca a: p" + str(s.QuienActua()))

    s.acciones_hechas.append((Reglas.JUGADOR1, Reglas.Accion.QUIERO_GRITO))
    s.truco = Reglas.EstadoTruco.TRUCO_ACEPTADO
    print("p1 acepto Truco, le toca a: p" + str(s.QuienActua()))

    s.acciones_hechas.append((Reglas.JUGADOR2, Reglas.Accion.JUGAR_C3))
    s.cartas_jugadas.append(Carta("6-Copa", 20))
    print("p2 jugó carta 3(que gana la mano), le toca a: p" + str(s.QuienActua()))

    s.acciones_hechas.append((Reglas.JUGADOR2, Reglas.Accion.JUGAR_C1))
    s.cartas_jugadas.append(Carta("6-Basto", 20))
    print("p2 jugó carta 1, le toca a: p" + str(s.QuienActua()))

    s.acciones_hechas.append((Reglas.JUGADOR1, Reglas.Accion.GRITAR))
    s.truco = Reglas.EstadoTruco.RETRUCO_DICHO
    print("p1 grito ReTruco, le toca a: p" + str(s.QuienActua()))

    s.acciones_hechas.append((Reglas.JUGADOR2, Reglas.Accion.FOLD))
    s.truco = Reglas.EstadoTruco.FOLD
    print("p2 no quiso, le toca a: p" + str(s.QuienActua()))

    # PRUEBA 2
    print("")
    print("prueba 2")
    s = Estado()
    print("inicial, le toca a: p" + str(s.QuienActua()))

    s.acciones_hechas.append((Reglas.JUGADOR1, Reglas.Accion.GRITAR))
    s.truco = Reglas.EstadoTruco.TRUCO_DICHO
    print("p2 grito Truco, le toca a: p" + str(s.QuienActua()))

    s.acciones_hechas.append((Reglas.JUGADOR2, Reglas.Accion.QUIERO_GRITO))
    s.truco = Reglas.EstadoTruco.TRUCO_ACEPTADO
    print("p2 grito ReTruco, le toca a: p" + str(s.QuienActua()))

    s.acciones_hechas.append((Reglas.JUGADOR1, Reglas.Accion.JUGAR_C3))
    s.cartas_jugadas.append(Carta("6-Copa", 20))
    print("p1 jugó carta 3, le toca a: p" + str(s.QuienActua()))

    s.acciones_hechas.append((Reglas.JUGADOR2, Reglas.Accion.FOLD))
    s.truco = Reglas.EstadoTruco.FOLD
    print("p2 no quiso, le toca a: p" + str(s.QuienActua()))

def prueba_QuienActua2():
    # Pruebo Get Acciones Posibles, no uso ejecutar accion porque no quiero mezclar pruebas
    # CUIDADO CON CIERTAS JUGADAS QUE PUEDEN DAR MAL POR NO EJECUTAR LA ACCION COMPLETAMENTE BIEN
    print("")
    print("===================================================")
    print("## PRUEBA - Acciones Posibles - ##")
    print("===================================================")
    print("")

    # SETUP
    s = Estado()
    p1 = AgenteRandom(Reglas.JUGADOR1)
    p2 = AgenteRandom(Reglas.JUGADOR2)
    cartas_p1, cartas_p2 = Reglas.RepartirCartas()
    p1.TomarCartas(cartas_p1)
    p2.TomarCartas(cartas_p2)

    #Prueba 1
    print("inicial,")
    print("quien actua? " + str(s.QuienActua()))
    print("")

    print("p1 toco Envido,")
    s.acciones_hechas.append((Reglas.JUGADOR1, Reglas.Accion.ENVIDO))
    s.envido = Reglas.EstadoEnvido.E_DICHO
    print("quien actua? " + str(s.QuienActua()))
    print("")

    print("p2 reraise Real Envido,")
    s.acciones_hechas.append((Reglas.JUGADOR2, Reglas.Accion.REALENVIDO))
    s.envido = Reglas.EstadoEnvido.R_DICHO
    print("quien actua? " + str(s.QuienActua()))
    print("")

    print("p1 rereaise Falta,")
    s.acciones_hechas.append((Reglas.JUGADOR1, Reglas.Accion.FALTAENVIDO))
    s.envido = Reglas.EstadoEnvido.F_DICHO
    print("quien actua? " + str(s.QuienActua()))
    print("")


def prueba_QuienActua3():
    # Pruebo Get Acciones Posibles, no uso ejecutar accion porque no quiero mezclar pruebas
    # CUIDADO CON CIERTAS JUGADAS QUE PUEDEN DAR MAL POR NO EJECUTAR LA ACCION COMPLETAMENTE BIEN
    print("")
    print("===================================================")
    print("## PRUEBA - Acciones Posibles - ##")
    print("===================================================")
    print("")

    # SETUP
    s = Estado()
    p1 = AgenteRandom(Reglas.JUGADOR1)
    p2 = AgenteRandom(Reglas.JUGADOR2)
    cartas_p1, cartas_p2 = Reglas.RepartirCartas()
    p1.TomarCartas(cartas_p1)
    p2.TomarCartas(cartas_p2)

    #Prueba 1
    print("inicial")
    print("quien actua? " + str(s.QuienActua()))
    print("")

    print("p1 grito Truco,")
    s.acciones_hechas.append((Reglas.JUGADOR1, Reglas.Accion.GRITAR))
    s.truco = Reglas.EstadoTruco.TRUCO_DICHO
    print("quien actua? " + str(s.QuienActua()))
    print("")

    print("p2 toco Real Envido, ")
    s.acciones_hechas.append((Reglas.JUGADOR2, Reglas.Accion.REALENVIDO))
    s.envido = Reglas.EstadoEnvido.R_DICHO
    print("quien actua? " + str(s.QuienActua()))
    print("")

    print("p1 rereaise RF, ")
    s.acciones_hechas.append((Reglas.JUGADOR1, Reglas.Accion.FALTAENVIDO))
    s.envido = Reglas.EstadoEnvido.F_DICHO
    print("quien actua? " + str(s.QuienActua()))
    print("")

    print("p2 acepta la Falta, ")
    s.acciones_hechas.append((Reglas.JUGADOR2, Reglas.Accion.ACEPTAR_TANTO))
    s.envido = Reglas.EstadoEnvido.F_ACEPTADO
    print("quien actua? " + str(s.QuienActua()))
    print("")

    print("p2 acepta el Grito,")
    s.acciones_hechas.append((Reglas.JUGADOR2, Reglas.Accion.QUIERO_GRITO))
    s.truco = Reglas.EstadoTruco.TRUCO_ACEPTADO
    print("quien actua? " + str(s.QuienActua()))
    print("")


def prueba_QuienActua4():
    # Pruebo Get Acciones Posibles, no uso ejecutar accion porque no quiero mezclar pruebas
    # CUIDADO CON CIERTAS JUGADAS QUE PUEDEN DAR MAL POR NO EJECUTAR LA ACCION COMPLETAMENTE BIEN
    print("")
    print("===================================================")
    print("## PRUEBA - Acciones Posibles - ##")
    print("===================================================")
    print("")

    # SETUP
    s = Estado()
    p1 = AgenteRandom(Reglas.JUGADOR1)
    p2 = AgenteRandom(Reglas.JUGADOR2)
    cartas_p1, cartas_p2 = Reglas.RepartirCartas()
    p1.TomarCartas(cartas_p1)
    p2.TomarCartas(cartas_p2)

    #Prueba 1
    print("inicial, ")
    print("quien actua? " + str(s.QuienActua()))
    print("")

    print("p1 grito Truco, ")
    s.acciones_hechas.append((Reglas.JUGADOR1, Reglas.Accion.GRITAR))
    s.truco = Reglas.EstadoTruco.TRUCO_DICHO
    print("quien actua? " + str(s.QuienActua()))
    print("")

    print("p2 grita ReTruco,")
    s.acciones_hechas.append((Reglas.JUGADOR2, Reglas.Accion.GRITAR))
    s.truco = Reglas.EstadoTruco.RETRUCO_DICHO
    print("quien actua? " + str(s.QuienActua()))
    print("")

    print("p1 grita Vale4, ")
    s.acciones_hechas.append((Reglas.JUGADOR1, Reglas.Accion.GRITAR))
    s.truco= Reglas.EstadoTruco.VALE4_DICHO
    print("quien actua? " + str(s.QuienActua()))
    print("")

    print("p2 acepta el Vale4,")
    s.acciones_hechas.append((Reglas.JUGADOR2, Reglas.Accion.QUIERO_GRITO))
    s.truco = Reglas.EstadoTruco.VALE4_ACEPTADO
    print("quien actua? " + str(s.QuienActua()))
    print("")


    """
    print("p1 acepto, acciones de p2 disponibles")
    s.acciones_hechas.append((Reglas.JUGADOR1, Reglas.Accion.QUIERO_GRITO))
    s.truco = Reglas.EstadoTruco.TRUCO_ACEPTADO
    print(str(p2.get_acciones_posibles(s)))
    print("")

    print("p2 jugo c3, acciones de p1 disponibles")
    s.acciones_hechas.append((Reglas.JUGADOR2, Reglas.Accion.JUGAR_C3))
    s.cartas_jugadas.append(Carta("4-Copa", 10))
    print(str(p1.get_acciones_posibles(s)))
    print("")

    print("p1 hace fold, acciones de p2 disponibles")
    s.acciones_hechas.append((Reglas.JUGADOR1, Reglas.Accion.GRITAR))
    s.truco = Reglas.EstadoTruco.RETRUCO_DICHO
    print(str(p2.get_acciones_posibles(s)))
    print("")
    """


def prueba_AccionesPosibles():
    # Pruebo Get Acciones Posibles, no uso ejecutar accion porque no quiero mezclar pruebas
    # CUIDADO CON CIERTAS JUGADAS QUE PUEDEN DAR MAL POR NO EJECUTAR LA ACCION COMPLETAMENTE BIEN
    print("")
    print("===================================================")
    print("## PRUEBA - Acciones Posibles - ##")
    print("===================================================")
    print("")

    # SETUP
    s = Estado()
    p1 = AgenteRandom(Reglas.JUGADOR1)
    p2 = AgenteRandom(Reglas.JUGADOR2)
    cartas_p1, cartas_p2 = Reglas.RepartirCartas()
    p1.TomarCartas(cartas_p1)
    p2.TomarCartas(cartas_p2)

    #Prueba 1
    print("inicial, acciones posibles de p1")
    print(str(p1.get_acciones_posibles(s)))
    print("")

    print("p1 juega c1, acciones de p2 disponibles")
    s.acciones_hechas.append((Reglas.JUGADOR1, Reglas.Accion.JUGAR_C1))
    s.cartas_jugadas.append(Carta("6-Copa", 20))
    p1.EjecutarAccion(s, Reglas.Accion.JUGAR_C1, False)
    print(str(p2.get_acciones_posibles(s)))
    print("")

    print("p2 grito Truco, acciones de p1 disponibles")
    s.acciones_hechas.append((Reglas.JUGADOR2, Reglas.Accion.GRITAR))
    s.truco = Reglas.EstadoTruco.TRUCO_DICHO
    print(str(p1.get_acciones_posibles(s)))
    print("")

    print("p1 aceptó, acciones de p2 disponibles")
    s.acciones_hechas.append((Reglas.JUGADOR1, Reglas.Accion.QUIERO_GRITO))
    s.truco = Reglas.EstadoTruco.TRUCO_ACEPTADO
    print(str(p2.get_acciones_posibles(s)))
    print("")

    print("p2 jugo c3, acciones de p1 disponibles")
    s.acciones_hechas.append((Reglas.JUGADOR2, Reglas.Accion.JUGAR_C3))
    s.cartas_jugadas.append(Carta("4-Copa", 10))
    print(str(p1.get_acciones_posibles(s)))
    print("")

    print("p1 hace fold, acciones de p2 disponibles")
    s.acciones_hechas.append((Reglas.JUGADOR1, Reglas.Accion.GRITAR))
    s.truco = Reglas.EstadoTruco.RETRUCO_DICHO
    print(str(p2.get_acciones_posibles(s)))
    print("")

def prueba_AccionesPosibles2():
    # Pruebo Get Acciones Posibles, no uso ejecutar accion porque no quiero mezclar pruebas
    # CUIDADO CON CIERTAS JUGADAS QUE PUEDEN DAR MAL POR NO EJECUTAR LA ACCION COMPLETAMENTE BIEN
    print("")
    print("===================================================")
    print("## PRUEBA - Acciones Posibles - ##")
    print("===================================================")
    print("")

    # SETUP
    s = Estado()
    p1 = AgenteRandom(Reglas.JUGADOR1)
    p2 = AgenteRandom(Reglas.JUGADOR2)
    cartas_p1, cartas_p2 = Reglas.RepartirCartas()
    p1.TomarCartas(cartas_p1)
    p2.TomarCartas(cartas_p2)

    #Prueba 1
    print("inicial, acciones posibles de p1")
    print(str(p1.get_acciones_posibles(s)))
    print("")

    print("p1 toco Envido, acciones de p2 disponibles")
    s.acciones_hechas.append((Reglas.JUGADOR1, Reglas.Accion.ENVIDO))
    s.envido = Reglas.EstadoEnvido.E_DICHO
    print(str(p2.get_acciones_posibles(s)))
    print("")

    print("p2 reraise Real Envido, acciones de p1 disponibles")
    s.acciones_hechas.append((Reglas.JUGADOR2, Reglas.Accion.REALENVIDO))
    s.envido = Reglas.EstadoEnvido.R_DICHO
    print(str(p1.get_acciones_posibles(s)))
    print("")

    print("p1 rereaise Falta, acciones de p2 disponibles")
    s.acciones_hechas.append((Reglas.JUGADOR1, Reglas.Accion.FALTAENVIDO))
    s.envido = Reglas.EstadoEnvido.F_DICHO
    print(str(p2.get_acciones_posibles(s)))
    print("")

    """
    print("p1 acepto, acciones de p2 disponibles")
    s.acciones_hechas.append((Reglas.JUGADOR1, Reglas.Accion.QUIERO_GRITO))
    s.truco = Reglas.EstadoTruco.TRUCO_ACEPTADO
    print(str(p2.get_acciones_posibles(s)))
    print("")

    print("p2 jugo c3, acciones de p1 disponibles")
    s.acciones_hechas.append((Reglas.JUGADOR2, Reglas.Accion.JUGAR_C3))
    s.cartas_jugadas.append(Carta("4-Copa", 10))
    print(str(p1.get_acciones_posibles(s)))
    print("")

    print("p1 hace fold, acciones de p2 disponibles")
    s.acciones_hechas.append((Reglas.JUGADOR1, Reglas.Accion.GRITAR))
    s.truco = Reglas.EstadoTruco.RETRUCO_DICHO
    print(str(p2.get_acciones_posibles(s)))
    print("")
    """

def prueba_AccionesPosibles3():
    # Pruebo Get Acciones Posibles, no uso ejecutar accion porque no quiero mezclar pruebas
    # CUIDADO CON CIERTAS JUGADAS QUE PUEDEN DAR MAL POR NO EJECUTAR LA ACCION COMPLETAMENTE BIEN
    print("")
    print("===================================================")
    print("## PRUEBA - Acciones Posibles - ##")
    print("===================================================")
    print("")

    # SETUP
    s = Estado()
    p1 = AgenteRandom(Reglas.JUGADOR1)
    p2 = AgenteRandom(Reglas.JUGADOR2)
    cartas_p1, cartas_p2 = Reglas.RepartirCartas()
    p1.TomarCartas(cartas_p1)
    p2.TomarCartas(cartas_p2)

    #Prueba 1
    print("inicial, acciones posibles de p1")
    print(str(p1.get_acciones_posibles(s)))
    print("")

    print("p1 grito Truco, acciones de p2 disponibles")
    s.acciones_hechas.append((Reglas.JUGADOR1, Reglas.Accion.GRITAR))
    s.truco = Reglas.EstadoTruco.TRUCO_DICHO
    print(str(p2.get_acciones_posibles(s)))
    print("")

    print("p2 toco Real Envido, acciones de p1 disponibles")
    s.acciones_hechas.append((Reglas.JUGADOR2, Reglas.Accion.REALENVIDO))
    s.envido = Reglas.EstadoEnvido.R_DICHO
    print(str(p1.get_acciones_posibles(s)))
    print("")

    print("p1 rereaise RF, acciones de p2 disponibles")
    s.acciones_hechas.append((Reglas.JUGADOR1, Reglas.Accion.FALTAENVIDO))
    s.envido = Reglas.EstadoEnvido.RF_DICHO
    print(str(p2.get_acciones_posibles(s)))
    print("")

    print("p2 acepta la Falta, acciones de p2 disponibles")
    s.acciones_hechas.append((Reglas.JUGADOR2, Reglas.Accion.ACEPTAR_TANTO))
    s.envido = Reglas.EstadoEnvido.RF_ACEPTADO
    print(str(p2.get_acciones_posibles(s))) # p2 le queda por responder el truco
    print("")

    print("p2 acepta el Grito, acciones de p1 disponibles")
    s.acciones_hechas.append((Reglas.JUGADOR2, Reglas.Accion.QUIERO_GRITO))
    s.truco = Reglas.EstadoTruco.TRUCO_ACEPTADO
    print(str(p1.get_acciones_posibles(s)))  # p2 le queda por responder el truco
    print("")

    """
    print("p1 acepto, acciones de p2 disponibles")
    s.acciones_hechas.append((Reglas.JUGADOR1, Reglas.Accion.QUIERO_GRITO))
    s.truco = Reglas.EstadoTruco.TRUCO_ACEPTADO
    print(str(p2.get_acciones_posibles(s)))
    print("")

    print("p2 jugo c3, acciones de p1 disponibles")
    s.acciones_hechas.append((Reglas.JUGADOR2, Reglas.Accion.JUGAR_C3))
    s.cartas_jugadas.append(Carta("4-Copa", 10))
    print(str(p1.get_acciones_posibles(s)))
    print("")

    print("p1 hace fold, acciones de p2 disponibles")
    s.acciones_hechas.append((Reglas.JUGADOR1, Reglas.Accion.GRITAR))
    s.truco = Reglas.EstadoTruco.RETRUCO_DICHO
    print(str(p2.get_acciones_posibles(s)))
    print("")
    """

def prueba_AccionesPosibles4():
    # Pruebo Get Acciones Posibles, no uso ejecutar accion porque no quiero mezclar pruebas
    # CUIDADO CON CIERTAS JUGADAS QUE PUEDEN DAR MAL POR NO EJECUTAR LA ACCION COMPLETAMENTE BIEN
    print("")
    print("===================================================")
    print("## PRUEBA - Acciones Posibles - ##")
    print("===================================================")
    print("")

    # SETUP
    s = Estado()
    p1 = AgenteRandom(Reglas.JUGADOR1)
    p2 = AgenteRandom(Reglas.JUGADOR2)
    cartas_p1, cartas_p2 = Reglas.RepartirCartas()
    p1.TomarCartas(cartas_p1)
    p2.TomarCartas(cartas_p2)

    #Prueba 1
    print("inicial, acciones posibles de p1")
    print(str(p1.get_acciones_posibles(s)))
    print("")

    print("p1 grito Truco, acciones de p2 disponibles")
    s.acciones_hechas.append((Reglas.JUGADOR1, Reglas.Accion.GRITAR))
    s.truco = Reglas.EstadoTruco.TRUCO_DICHO
    print(str(p2.get_acciones_posibles(s)))
    print("")

    print("p2 grita ReTruco, acciones de p1 disponibles")
    s.acciones_hechas.append((Reglas.JUGADOR2, Reglas.Accion.GRITAR))
    s.truco = Reglas.EstadoTruco.RETRUCO_DICHO
    print(str(p1.get_acciones_posibles(s)))
    print("")

    print("p1 grita Vale4, acciones de p2 disponibles")
    s.acciones_hechas.append((Reglas.JUGADOR1, Reglas.Accion.GRITAR))
    s.truco= Reglas.EstadoTruco.VALE4_DICHO
    print(str(p2.get_acciones_posibles(s)))
    print("")

    print("p2 acepta el Vale4, acciones de p1 disponibles")
    s.acciones_hechas.append((Reglas.JUGADOR2, Reglas.Accion.QUIERO_GRITO))
    s.truco = Reglas.EstadoTruco.VALE4_ACEPTADO
    print(str(p1.get_acciones_posibles(s))) # p2 le queda por responder el truco
    print("")


    """
    print("p1 acepto, acciones de p2 disponibles")
    s.acciones_hechas.append((Reglas.JUGADOR1, Reglas.Accion.QUIERO_GRITO))
    s.truco = Reglas.EstadoTruco.TRUCO_ACEPTADO
    print(str(p2.get_acciones_posibles(s)))
    print("")

    print("p2 jugo c3, acciones de p1 disponibles")
    s.acciones_hechas.append((Reglas.JUGADOR2, Reglas.Accion.JUGAR_C3))
    s.cartas_jugadas.append(Carta("4-Copa", 10))
    print(str(p1.get_acciones_posibles(s)))
    print("")

    print("p1 hace fold, acciones de p2 disponibles")
    s.acciones_hechas.append((Reglas.JUGADOR1, Reglas.Accion.GRITAR))
    s.truco = Reglas.EstadoTruco.RETRUCO_DICHO
    print(str(p2.get_acciones_posibles(s)))
    print("")
    """


def prueba_EjecutarAccion():
    print("")
    print("===================================================")
    print("## PRUEBA - Ejecutar Accion - ##")
    print("===================================================")
    print("")

    # SETUP
    s = Estado()
    p1 = AgenteRandom(Reglas.JUGADOR1)
    p2 = AgenteRandom(Reglas.JUGADOR2)
    cartas_j1 = []
    cartas_j2 = []
    cartas_j1.append(Reglas.MAZO[9])
    cartas_j1.append(Reglas.MAZO[5])
    cartas_j1.append(Reglas.MAZO[3])
    cartas_j2.append(Reglas.MAZO[8])
    cartas_j2.append(Reglas.MAZO[6])
    cartas_j2.append(Reglas.MAZO[1])

    p1.TomarCartas(cartas_j1)
    p2.TomarCartas(cartas_j2)

    #Prueba 1
    print("inicial")
    print("")

    print("1) p1 juega c1, acciones de p2 disponibles")
    p1.EjecutarAccion(s,Reglas.Accion.JUGAR_C1)
    print(str(p2.get_acciones_posibles(s)))
    print("")

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

    print("6) p2 hace fold, acciones de p1 disponibles")
    p2.EjecutarAccion(s, Reglas.Accion.JUGAR_C2)
    print(str(p1.get_acciones_posibles(s)))
    print("")

    print("Fin de prueba, estado S final")
    print("")
    print("Cartas Jugadas:")
    print(str(s.cartas_jugadas))
    print("")
    print("Acciones Hechas Jugadas:")
    print(str(s.acciones_hechas))
    print("")
    print("p1, cartas restantes:")
    print(str(p1.cartas_restantes))
    print("")
    print("p2, cartas restantes:")
    print(str(p2.cartas_restantes))

def prueba_EjecutarAccion2():
    print("")
    print("===================================================")
    print("## PRUEBA - Ejecutar Accion 2 - ##")
    print("===================================================")
    print("")

    # SETUP
    s = Estado()
    p1 = AgenteRandom(Reglas.JUGADOR1)
    p2 = AgenteRandom(Reglas.JUGADOR2)
    cartas_j1 = []
    cartas_j2 = []
    cartas_j1.append(Reglas.MAZO[9])
    cartas_j1.append(Reglas.MAZO[5])
    cartas_j1.append(Reglas.MAZO[3])
    cartas_j2.append(Reglas.MAZO[8])
    cartas_j2.append(Reglas.MAZO[6])
    cartas_j2.append(Reglas.MAZO[1])

    p1.TomarCartas(cartas_j1)
    p2.TomarCartas(cartas_j2)

    #Prueba 1
    print("inicial")
    print("")

    print("1) p1 juega c1, acciones de p2 disponibles")
    p1.EjecutarAccion(s,Reglas.Accion.JUGAR_C1)
    print(str(p2.get_acciones_posibles(s)))
    print("")

    print("2) p2 Envido, acciones de p1 disponibles")
    p2.EjecutarAccion(s, Reglas.Accion.ENVIDO)
    print("estado envido: " + s.envido.name)
    print(str(p1.get_acciones_posibles(s)))
    print("")

    print("3) p1 acepto, acciones de p2 disponibles")
    p1.EjecutarAccion(s, Reglas.Accion.ACEPTAR_TANTO)
    print(str(p2.get_acciones_posibles(s)))
    print("")

    print("5) p2 jugo c2, acciones de p1 disponibles")
    p2.EjecutarAccion(s, Reglas.Accion.JUGAR_C2)
    print(str(p1.get_acciones_posibles(s)))
    print("")

    print("6) p1 jugo c2, acciones de p2 disponibles")
    p1.EjecutarAccion(s, Reglas.Accion.JUGAR_C2)
    print(str(p2.get_acciones_posibles(s)))
    print("")

    print("Fin de prueba, estado S final")
    print("")
    print("Cartas Jugadas:")
    print(str(s.cartas_jugadas))
    print("")
    print("Acciones Hechas Jugadas:")
    print(str(s.acciones_hechas))
    print("")
    print("p1, cartas restantes:")
    print(str(p1.cartas_restantes))
    print("")
    print("p2, cartas restantes:")
    print(str(p2.cartas_restantes))

#poner ciclos retruco a ver si anda el grito regritar sin un aceptar en el medio
def prueba_EjecutarAccion3():
    print("")
    print("===================================================")
    print("## PRUEBA - Ejecutar Accion 3 - ##")
    print("===================================================")
    print("")

    # SETUP
    s = Estado()
    p1 = AgenteRandom(Reglas.JUGADOR1)
    p2 = AgenteRandom(Reglas.JUGADOR2)
    cartas_j1 = []
    cartas_j2 = []
    cartas_j1.append(Reglas.MAZO[9])
    cartas_j1.append(Reglas.MAZO[5])
    cartas_j1.append(Reglas.MAZO[3])
    cartas_j2.append(Reglas.MAZO[8])
    cartas_j2.append(Reglas.MAZO[6])
    cartas_j2.append(Reglas.MAZO[1])

    p1.TomarCartas(cartas_j1)
    p2.TomarCartas(cartas_j2)

    #Prueba 1
    print("inicial")
    print("")

    print("1) p1 juega c1, acciones de p2 disponibles")
    p1.EjecutarAccion(s,Reglas.Accion.JUGAR_C1)
    print("estadoT: " + s.truco.name)
    print(str(p2.get_acciones_posibles(s)))
    print("")

    print("2) p2 grito Truco, acciones de p1 disponibles")
    p2.EjecutarAccion(s, Reglas.Accion.GRITAR)
    print("estadoT: " + s.truco.name)
    print(str(p1.get_acciones_posibles(s)))
    print("")

    print("3) p1 GRITA, acciones de p2 disponibles")
    p1.EjecutarAccion(s, Reglas.Accion.GRITAR)
    print("estadoT: " + s.truco.name)
    print(str(p2.get_acciones_posibles(s)))
    print("")

    print("4) p2 GRITA, acciones de p1 disponibles")
    p2.EjecutarAccion(s, Reglas.Accion.GRITAR)
    print("estadoT: " + s.truco.name)
    print(str(p1.get_acciones_posibles(s)))
    print("")

    print("5) p1 quiere grito, acciones de p2 disponibles")
    p1.EjecutarAccion(s, Reglas.Accion.QUIERO_GRITO)
    print("estadoT: " + s.truco.name)
    print(str(p2.get_acciones_posibles(s)))
    print("")

    print("6) p2 juega C2, acciones de p1 disponibles")
    p2.EjecutarAccion(s, Reglas.Accion.JUGAR_C2)
    print("estadoT: " + s.truco.name)
    print(str(p1.get_acciones_posibles(s)))
    print("")

    print("Fin de prueba, estado S final")
    print("")
    print("Cartas Jugadas:")
    print(str(s.cartas_jugadas))
    print("")
    print("Acciones Hechas Jugadas:")
    print(str(s.acciones_hechas))
    print("")
    print("p1, cartas restantes:")
    print(str(p1.cartas_restantes))
    print("")
    print("p2, cartas restantes:")
    print(str(p2.cartas_restantes))

def prueba_HastaVALE4():
    print("")
    print("===================================================")
    print("## PRUEBA - Ejecutar Accion - ##")
    print("===================================================")
    print("")

    # SETUP
    s = Estado()
    p1 = AgenteRandom(Reglas.JUGADOR1)
    p2 = AgenteRandom(Reglas.JUGADOR2)
    cartas_j1 = []
    cartas_j2 = []
    cartas_j1.append(Reglas.MAZO[9])
    cartas_j1.append(Reglas.MAZO[5])
    cartas_j1.append(Reglas.MAZO[3])
    cartas_j2.append(Reglas.MAZO[8])
    cartas_j2.append(Reglas.MAZO[6])
    cartas_j2.append(Reglas.MAZO[1])

    p1.TomarCartas(cartas_j1)
    p2.TomarCartas(cartas_j2)

    #Prueba 1
    print("inicial")
    print("")

    print("1) p1 GRITA TRUCO, acciones de p2 disponibles")
    p1.EjecutarAccion(s,Reglas.Accion.GRITAR)
    print(str(p2.get_acciones_posibles(s)))
    print("")

    print("2) p2 QUIERE TRUCO, acciones de p1 disponibles")
    p2.EjecutarAccion(s, Reglas.Accion.QUIERO_GRITO)
    print(str(p1.get_acciones_posibles(s)))
    print("")

    print("3) p1 juega C3, acciones de p2 disponibles")
    p1.EjecutarAccion(s, Reglas.Accion.JUGAR_C3)
    print(str(p2.get_acciones_posibles(s)))
    print("")

    print("4) p2 GRITA RETRUCO, acciones de p1 disponibles")
    p2.EjecutarAccion(s, Reglas.Accion.GRITAR)
    print(str(s.QuienActua()))
    print("Acciones posibles p1" + str(p1.get_acciones_posibles(s)))
    #print("Acciones posibles p2" + str(p2.get_acciones_posibles(s)))
    print("")



    print("Fin de prueba, estado S final")
    print("")
    print("Cartas Jugadas:")
    print(str(s.cartas_jugadas))
    print("")
    print("Acciones Hechas Jugadas:")
    print(str(s.acciones_hechas))
    print("")
    print("p1, cartas restantes:")
    print(str(p1.cartas_restantes))
    print("")
    print("p2, cartas restantes:")
    print(str(p2.cartas_restantes))

def prueba_Elegir_Accion_Random():
    print("")
    print("===================================================")
    print("## PRUEBA - Elegir Accion Random- ##")
    print("===================================================")
    print("")

    # SETUP
    s = Estado()
    p1 = AgenteRandom(Reglas.JUGADOR1)
    p2 = AgenteRandom(Reglas.JUGADOR2)
    cartas_j1 = []
    cartas_j2 = []
    cartas_j1.append(Reglas.MAZO[9])
    cartas_j1.append(Reglas.MAZO[5])
    cartas_j1.append(Reglas.MAZO[3])
    cartas_j2.append(Reglas.MAZO[8])
    cartas_j2.append(Reglas.MAZO[6])
    cartas_j2.append(Reglas.MAZO[1])

    p1.TomarCartas(cartas_j1)
    p2.TomarCartas(cartas_j2)

    #Prueba 1
    print("inicial")
    print("")

    print("1) p1 juega c1, acciones de p2 disponibles")
    p1.EjecutarAccion(s,Reglas.Accion.JUGAR_C1)
    print(str(p2.get_acciones_posibles(s)))
    print("")

    print("2) p2 grito Truco, acciones de p1 disponibles")
    p2.EjecutarAccion(s, Reglas.Accion.GRITAR)
    print(str(p1.get_acciones_posibles(s)))
    print("")

    print("3) p1 acepto, acciones de p2 disponibles")
    p1.EjecutarAccion(s, Reglas.Accion.QUIERO_GRITO)
    print(str(p2.get_acciones_posibles(s)))
    print("")

    print("sampleo de estas acciones:")
    print(str(p2.Elegir_Accion(s)))
    print(str(p2.Elegir_Accion(s)))
    print(str(p2.Elegir_Accion(s)))
    print(str(p2.Elegir_Accion(s)))
    print(str(p2.Elegir_Accion(s)))
    print(str(p2.Elegir_Accion(s)))
    print(str(p2.Elegir_Accion(s)))
    print(str(p2.Elegir_Accion(s)))

def prueba_PlayRandomGames():
    print("")
    print("===================================================")
    print("## PRUEBA - Play Random Games - ##")
    print("===================================================")
    print("")
    p1 = AgenteRandom(Reglas.JUGADOR1)
    p2 = AgenteRandom(Reglas.JUGADOR2)

    Motor.Play_random_games(p1,p2,2,True)

def prueba_Save_Load_Games():
    print("")
    print("===================================================")
    print("## PRUEBA - Saven and Load Games - ##")
    print("===================================================")
    print("")
    p1 = AgenteRandom(Reglas.JUGADOR1)
    p2 = AgenteRandom(Reglas.JUGADOR2)

    print("")
    print(" Playing games...")
    print("")
    lista_episodios = Motor.Play_random_games(p1,p2,2,True)
    print("")
    print("print de lista_episodios:")
    print(str(lista_episodios))

    print("")
    print("Comenzando SAVE de lista_episodios")
    Motor.Save_Games_to_Disk(lista_episodios, "prueba_le.pickle")

    print("Comenzando LOAD")
    pruebaLoad = Motor.Load_Games_From_Disk("prueba_le.pickle")
    print("")
    print("print de lista_episodios:")
    print(str(pruebaLoad))
    print("")

def prueba_ConvertVector():
    print("")
    print("===================================================")
    print("## PRUEBA - Convert to Vector - ##")
    print("===================================================")
    print("")

    # SETUP
    s = Estado()
    p1 = AgenteRandom(Reglas.JUGADOR1)
    p2 = AgenteRandom(Reglas.JUGADOR2)
    cartas_j1 = []
    cartas_j2 = []
    cartas_j2.append(Reglas.MAZO[9])
    cartas_j2.append(Reglas.MAZO[5])
    cartas_j2.append(Reglas.MAZO[3])
    cartas_j1.append(Reglas.MAZO[8])
    cartas_j1.append(Reglas.MAZO[6])
    cartas_j1.append(Reglas.MAZO[1])

    p1.TomarCartas(cartas_j1)
    p2.TomarCartas(cartas_j2)
    print("cartas p1: " + str(p1.cartas_totales))
    print("cartas p2: " + str(p2.cartas_totales))
    s.puntos_envido_p1 = p1.puntos_envido
    s.puntos_envido_p2 = p2.puntos_envido

    # Prueba 1
    print("")
    print("inicial")
    print("")

    print("1) p1 juega c1, acciones de p2 disponibles")
    p1.EjecutarAccion(s, Reglas.Accion.JUGAR_C1)
    print(str(p2.get_acciones_posibles(s)))
    print("")

    print("2) p2 Envido, acciones de p1 disponibles")
    p2.EjecutarAccion(s, Reglas.Accion.ENVIDO)
    print("estado envido: " + s.envido.name)
    print(str(p1.get_acciones_posibles(s)))
    print("")

    print("3) p1 acepto, acciones de p2 disponibles")
    p1.EjecutarAccion(s, Reglas.Accion.ACEPTAR_TANTO)
    print(str(p2.get_acciones_posibles(s)))
    print("")

    print("5) p2 jugo c2, acciones de p1 disponibles")
    p2.EjecutarAccion(s, Reglas.Accion.JUGAR_C2)
    print(str(p1.get_acciones_posibles(s)))
    print("")

    print("6) p1 jugo c2, acciones de p2 disponibles")
    p1.EjecutarAccion(s, Reglas.Accion.JUGAR_C2)
    print(str(p2.get_acciones_posibles(s)))
    print("")

    print(str(Motor.ConvertStateToVector(p1, s, True)))
    print("")
    print(len(Motor.ConvertStateToVector(p1, s, True)))

def prueba_CalcularPuntos():
    print("")
    print("===================================================")
    print("## PRUEBA - CalcularPuntos - ##")
    print("===================================================")
    print("")

    p1 = AgenteRandom(Reglas.JUGADOR1)
    p2 = AgenteRandom(Reglas.JUGADOR2)

    episodios = Motor.Play_random_games(p1, p2, 1, False)
    print("cartas p1: " + str(p1.cartas_totales) + ",   puntos envido:" + str(p1.puntos_envido))
    print("cartas p2: " + str(p2.cartas_totales) + ",   puntos envido:" + str(p2.puntos_envido))
    for e in episodios:
        for s in e.estados:
            print("estadoT: " + str(s))
        print("")
        print("puntos" + str(e.CalcularPuntosFinales()))

    print("puntos: " + str(e.CalcularPuntosFinales()[0]))
    print("puntos: " + str(e.CalcularPuntosFinales()[1]))


def prueba_CalcularPuntosEnvido():
    print("")
    print("===================================================")
    print("## PRUEBA - CalcularPuntos - ##")
    print("===================================================")
    print("")

    p1 = AgenteRandom(Reglas.JUGADOR1)
    p2 = AgenteRandom(Reglas.JUGADOR2)

    cartas_p1, cartas_p2 = Reglas.RepartirCartas()
    p1.TomarCartas(cartas_p1)
    p2.TomarCartas(cartas_p2)

    print("cartas p1: " + str(p1.cartas_totales) + ",   puntos envido:" + str(p1.puntos_envido))
    print("cartas p2: " + str(p2.cartas_totales) + ",   puntos envido:" + str(p2.puntos_envido))


def prueba_MultiProcess_Value_Training_Games():
    print("")
    print("===================================================")
    print("## PRUEBA - Generate_Value_Training_Games - ##")
    print("===================================================")
    print("")
    #p1 = AgenteRandom(Reglas.JUGADOR1)
    #p2 = AgenteRandom(Reglas.JUGADOR2)

    genX = "value_pickles\gen2_"
    p1_DQN = keras.models.load_model(genX + "p1_DQN.h5")
    p2_DQN = keras.models.load_model(genX + "p2_DQN.h5")

    p1 = AgenteGreedyDVN(Reglas.JUGADOR1, p1_DQN)
    p2 = AgenteGreedyDVN(Reglas.JUGADOR2, p2_DQN)


    (p1_data, p1_labels), (p2_data, p2_labels) = Motor.MP_Generate_Value_Training_Games(p1, p2, 20000, False)

    print("")
    print("p1 data")
    print(*p1_data, sep='\n')
    print("")
    print("p1 labels")
    print(p1_labels)
    print("")
    print("p2 data")
    print(*p2_data, sep='\n')
    print("")
    print("p2 labels")
    print(p2_labels)
    print("")

def prueba_Generate_Value_Training_Games(gen):
    print("")
    print("===================================================")
    print("## PRUEBA - Generate_Value_Training_Games - ##")
    print("===================================================")
    print("")

    if gen == 0:
        p1 = AgenteRandom(Reglas.JUGADOR1)
        p2 = AgenteRandom(Reglas.JUGADOR2)
    else:
        gen_n = "value_pickles\gen" + str(gen) + "_"
        p1_DQN = keras.models.load_model(gen_n + "p1_DVN.h5")
        p2_DQN = keras.models.load_model(gen_n + "p2_DVN.h5")
        p1 = AgenteGreedyDVN(Reglas.JUGADOR1, p1_DQN)
        p2 = AgenteGreedyDVN(Reglas.JUGADOR2, p2_DQN)


    (p1_data, p1_labels), (p2_data, p2_labels) = Motor.Generate_Value_Training_Games(p1, p2, 2, True)

    print("")
    print("p1 data")
    print(*p1_data, sep='\n')
    print("")
    print("p1 labels")
    print(p1_labels)
    print("")
    print("p2 data")
    print(*p2_data, sep='\n')
    print("")
    print("p2 labels")
    print(p2_labels)
    print("")

def prueba_Play_DVN_RandomGames(gen):
    print("")
    print("===================================================")
    print("## PRUEBA - Play DVN Games - ##")
    print("===================================================")
    print("")
    genV = "value_pickles\gen" + str(gen) + "_"
    p1_DVN = keras.models.load_model(genV + "p1_DQN.h5")
    p2_DVN = keras.models.load_model(genV + "p2_DQN.h5")
    p1 = AgenteGreedyDVN(Reglas.JUGADOR1, p1_DVN)
    p2 = AgenteGreedyDVN(Reglas.JUGADOR2, p2_DVN)

    Motor.Play_random_games(p1, p2, 10000, True)

def prueba_Play_HUMAN():
    print("")
    print("===================================================")
    print("## PRUEBA - Play HUMAN - ##")
    print("===================================================")
    print("")


    # RANDOM AGENTS
    #random_p1 = AgenteRandom(Reglas.JUGADOR1)
    #random_p2 = AgenteRandom(Reglas.JUGADOR2)

    # VALUE AGENTS
    #genV = "value_pickles\gen2_"
    #p1_DVN = keras.models.load_model(genV + "p1_DQN.h5")
    #p2_DVN = keras.models.load_model(genV + "p2_DQN.h5")
    #value_p1 = AgenteGreedyDVN(Reglas.JUGADOR1, p1_DVN)
    #value_p2 = AgenteGreedyDVN(Reglas.JUGADOR2, p2_DVN)

    # POLICY AGENTS
    #genP = "policy_pickles\gen2_"
    #p1_DPN = keras.models.load_model(genP + "p1_DQN.h5")
    #p2_DPN = keras.models.load_model(genP + "p2_DQN.h5")
    #policy_p1 = AgenteDPN(Reglas.JUGADOR1, p1_DPN)
    #policy_p2 = AgenteDPN(Reglas.JUGADOR2, p2_DPN)

    # PARTIDAS
    #Motor.Play_random_games(random_p1, random_p2, 1, True)
    #Motor.Play_random_games(value_p1, value_p2, 1, True)
    #Motor.Play_random_games(policy_p1, policy_p2, 1, True)

    # MIXTA
    print("")
    Motor.Play_Human_game(Humano(Reglas.JUGADOR1),
                            AgenteGreedyDVN(Reglas.JUGADOR2, keras.models.load_model("value_pickles\gen2_p2_DVN.h5")),
                            True)


def prueba_Play_VERSUS():
    print("")
    print("===================================================")
    print("## PRUEBA - Play VERSUS Games - ##")
    print("===================================================")
    print("")
    # RANDOM AGENTS
    random_p1 = AgenteRandom(Reglas.JUGADOR1)
    random_p2 = AgenteRandom(Reglas.JUGADOR2)

    # VALUE AGENTS
    genV = "value_pickles\gen2_"
    p1_DVN = keras.models.load_model(genV + "p1_DQN.h5")
    p2_DVN = keras.models.load_model(genV + "p2_DQN.h5")
    value_p1 = AgenteGreedyDVN(Reglas.JUGADOR1, p1_DVN)
    value_p2 = AgenteGreedyDVN(Reglas.JUGADOR2, p2_DVN)

    # PARTIDAS
    #Motor.Play_random_games(random_p1, random_p2, 1, True)
    #Motor.Play_random_games(value_p1, value_p2, 1, True)
    #Motor.Play_random_games(policy_p1, policy_p2, 1, True)

    # MIXTA
    print("random vs gen2")
    Motor.Play_random_games(AgenteRandom(Reglas.JUGADOR1),
                            AgenteGreedyDVN(Reglas.JUGADOR2, keras.models.load_model("value_pickles\gen2_p2_DQN.h5")),
                            2000, False)
    print("random vs gen12")
    Motor.Play_random_games(AgenteRandom(Reglas.JUGADOR1),
                            AgenteGreedyDVN(Reglas.JUGADOR2, keras.models.load_model("value_pickles\gen12_p2_DQN.h5")),
                            2000, False)

    print("gen2 vs gen12")
    Motor.Play_random_games(AgenteGreedyDVN(Reglas.JUGADOR1, keras.models.load_model("value_pickles\gen2_p1_DQN.h5")),
                            AgenteGreedyDVN(Reglas.JUGADOR2, keras.models.load_model("value_pickles\gen12_p2_DQN.h5")),
                            2000, False)

    print("gen12 vs gen2")
    Motor.Play_random_games(AgenteGreedyDVN(Reglas.JUGADOR1, keras.models.load_model("value_pickles\gen12_p1_DQN.h5")),
                            AgenteGreedyDVN(Reglas.JUGADOR2, keras.models.load_model("value_pickles\gen2_p2_DQN.h5")),
                            2000, False)


#######################################################
###                    MAIN                         ###
#######################################################
if __name__ == '__main__':

    ### PRUEBAS ESTADO
    #prueba_QuienGanoManos()
    #prueba_QuienJugariaCarta()
    #prueba_QuienActua()
    #prueba_QuienActua2()
    #prueba_QuienActua3()
    #prueba_QuienActua4()
    #prueba_CalcularPuntos()
    #prueba_CalcularPuntosEnvido()

    ### PRUEBAS AGENTE
    #prueba_AccionesPosibles()
    #prueba_AccionesPosibles2()
    #prueba_AccionesPosibles3()
    #prueba_AccionesPosibles4()
    #prueba_EjecutarAccion()
    #prueba_EjecutarAccion2()
    #prueba_EjecutarAccion3()
    # prueba_Elegir_Accion_Random()
    # prueba_HastaVALE4()

    ### PRUEBAS MOTOR
    #prueba_PlayRandomGames()
    # prueba_Save_Load_Games()
    #prueba_ConvertVector()

    # REDES
    #prueba_Generate_Value_Training_Games(0)
    # prueba_MultiProcess_Value_Training_Games()
    # prueba_Play_DVN_RandomGames()we
    # prueba_Play_DPN_RandomGames()

    # PARTIDAS DE PRUEBA
    # prueba_Play_VERSUS()
    # PolicyNetworkEngine.PolicyNetworkTrainer(10000, 3)


    ##############
    # AHORA
    ##############

    #trainer

    ##  parametros de trainer ( start_gen 0?, number_of_generations,  iterations_per_generation, multiprocess=False)
    ## start_gen ultima version donde debe existir el DVN.h5. Primer output sera la startgen+1
    #ValueNetworkEngine.ValueNetworkTrainer(21, 3, 500000, True)


    #ValueNetworkEngine.HeadToHead_PlayTest(21, 66, 50000, False)
    #ValueNetworkEngine.HeadToHead_PlayTest(66, 21, 50000, False)
    #ValueNetworkEngine.HeadToHead_PlayTest(21, 77, 50000, False)
    #ValueNetworkEngine.HeadToHead_PlayTest(77, 21, 50000, False)



    #gen_next = "value_pickles\gen1_"
    #ValueNetworkEngine.Load_and_Test(gen_next)
    #prueba_Generate_Value_Training_Games(0)

    # para entrenar la red con los pickles de la generacion ya generados (nextgen, maxepocs, loadprecvious)
    #ValueNetworkEngine.Train_Save("value_pickles\gen16_", ValueNetworkEngine.MAX_EPOCHS_PERGEN, True)


    #gen_next = "value_pickles\gen2_"
    #ValueNetworkEngine.Generate_and_Save(gen_n, gen_next, games_per_gen)
    #ValueNetworkEngine.Train_Save(gen_next, 50, True)
    #ValueNetworkEngine.Load_and_Test("value_pickles\gen16_")

    # versus

    """
    print("stock 16 vs greed 66")
    Motor.Play_random_games(AgenteSoftmaxDVN(Reglas.JUGADOR1, keras.models.load_model("value_pickles\gen16_p1_DVN.h5")),
                            AgenteGreedyDVN(Reglas.JUGADOR2, keras.models.load_model("value_pickles\gen66_p2_DVN.h5")),
                            50000, False)
    """



    #ValueNetworkEngine.HeadToHead_PlayTest(16, 77, 50000, False)
    #ValueNetworkEngine.HeadToHead_PlayTest(16, 16, 50000, False)

    #ValueNetworkEngine.HeadToHead_PlayTest(16, 15, 50000, False)
    #ValueNetworkEngine.HeadToHead_PlayTest(15, 16, 50000, False)

    # pruebas acidas
    #ValueNetworkEngine.Load_and_Test("value_pickles\gen5_")
    #ValueNetworkEngine.Load_and_Test("value_pickles\gen11_")
    #prueba_Play_HUMAN()

    # CODE TO CHECK GPU



    print("")
    printDebug("## TERMINE! ##")