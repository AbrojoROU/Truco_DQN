from Truco_Core_v2_r1 import *


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

    s.acciones_hechas.append((Reglas.JUGADOR2, Reglas.Accion.GRITAR_TRUCO))
    s.truco = Reglas.EstadoTruco.TRUCO_DICHO
    print("p2 grito Truco, le toca a: p" + str(s.QuienActua()))

    s.acciones_hechas.append((Reglas.JUGADOR1, Reglas.Accion.QUIERO_GRITO))
    s.truco = Reglas.EstadoTruco.TRUCO_ACEPTADO
    print("p1 acepto Truco, le toca a: p" + str(s.QuienActua()))

    s.acciones_hechas.append((Reglas.JUGADOR2, Reglas.Accion.JUGAR_C3))
    s.cartas_jugadas.append(Carta("6-Copa", 20))
    print("p2 jugó carta 3, le toca a: p" + str(s.QuienActua()))

    s.acciones_hechas.append((Reglas.JUGADOR2, Reglas.Accion.JUGAR_C1))
    s.cartas_jugadas.append(Carta("6-Basto", 20))
    print("p2 jugó carta 1, le toca a: p" + str(s.QuienActua()))

    s.acciones_hechas.append((Reglas.JUGADOR1, Reglas.Accion.GRITAR_RETRUCO))
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

    s.acciones_hechas.append((Reglas.JUGADOR1, Reglas.Accion.GRITAR_TRUCO))
    s.truco = Reglas.EstadoTruco.TRUCO_DICHO
    print("p2 grito Truco, le toca a: p" + str(s.QuienActua()))

    s.acciones_hechas.append((Reglas.JUGADOR2, Reglas.Accion.GRITAR_RETRUCO))
    s.truco = Reglas.EstadoTruco.RETRUCO_DICHO
    print("p2 grito ReTruco, le toca a: p" + str(s.QuienActua()))

    s.acciones_hechas.append((Reglas.JUGADOR1, Reglas.Accion.QUIERO_GRITO))
    s.truco = Reglas.EstadoTruco.RETRUCO_ACEPTADO
    print("p1 acepto ReTruco, le toca a: p" + str(s.QuienActua()))

    s.acciones_hechas.append((Reglas.JUGADOR1, Reglas.Accion.JUGAR_C3))
    s.cartas_jugadas.append(Carta("6-Copa", 20))
    print("p1 jugó carta 3, le toca a: p" + str(s.QuienActua()))

    s.acciones_hechas.append((Reglas.JUGADOR2, Reglas.Accion.FOLD))
    s.truco = Reglas.EstadoTruco.FOLD
    print("p2 no quiso, le toca a: p" + str(s.QuienActua()))

def prueba_AccionesPosibles():
    print("")
    print("===================================================")
    print("## PRUEBA - Acciones Posibles - ##")
    print("===================================================")
    print("")

    # SETUP
    s = Estado()
    p1 = Agente(Reglas.JUGADOR1)
    p2 = Agente(Reglas.JUGADOR2)
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
    print(str(p2.get_acciones_posibles(s)))
    print("")

    print("p2 grito Truco, acciones de p1 disponibles")
    s.acciones_hechas.append((Reglas.JUGADOR2, Reglas.Accion.GRITAR_TRUCO))
    s.truco = Reglas.EstadoTruco.TRUCO_DICHO
    print(str(p1.get_acciones_posibles(s)))
    print("")

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
    s.acciones_hechas.append((Reglas.JUGADOR1, Reglas.Accion.FOLD))
    s.truco = Reglas.EstadoTruco.FOLD
    print(str(p2.get_acciones_posibles(s)))
    print("")

def prueba_EjecutarAccion():
    print("")
    print("===================================================")
    print("## PRUEBA - Ejecutar Accion - ##")
    print("===================================================")
    print("")

    # SETUP
    s = Estado()
    p1 = Agente(Reglas.JUGADOR1)
    p2 = Agente(Reglas.JUGADOR2)
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
    print(str(p2.get_acciones_posibles(s)))
    print("")

    print("p2 grito Truco, acciones de p1 disponibles")
    s.acciones_hechas.append((Reglas.JUGADOR2, Reglas.Accion.GRITAR_TRUCO))
    s.truco = Reglas.EstadoTruco.TRUCO_DICHO
    print(str(p1.get_acciones_posibles(s)))
    print("")

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

    print("p1 jugo c1, acciones de p2 disponibles")
    s.acciones_hechas.append((Reglas.JUGADOR1, Reglas.Accion.JUGAR_C2))
    s.cartas_jugadas.append(Carta("6-Basto", 20))
    print(str(p2.get_acciones_posibles(s)))
    print("")

    print("p2 hace fold, acciones de p1 disponibles")
    s.acciones_hechas.append((Reglas.JUGADOR2, Reglas.Accion.FOLD))
    s.truco = Reglas.EstadoTruco.FOLD
    print(str(p1.get_acciones_posibles(s)))
    print("")


if __name__ == '__main__':
    print("COMIENZO!")
    print("")

    # PRUEBAS ESTADO
    #prueba_QuienGanoManos()
    #prueba_QuienJugariaCarta()
    #prueba_QuienActua()

    # PRUEBAS AGENTE
    #prueba_AccionesPosibles()
    prueba_EjecutarAccion()


    print("")
    print("## TERMINE! ##")
