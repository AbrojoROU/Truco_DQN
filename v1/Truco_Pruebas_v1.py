from Truco_Core_v1_r4 import *
import matplotlib.pyplot as plt
import random
# %matplotlib inline

def prueba_General():
    # PRUEBAS GENERALES ENTIDADES
    print("")
    print("=======================")
    print("## PRUEBAS GENERALES ##")
    print("=======================")
    # Reglas = Reglas()
    print(Reglas.MAZO)
    print(Reglas.ACCIONES)
    c1 = Carta("Carta A", 10)
    print(c1)
    str(c1)
    a1 = Agente(Reglas.JUGADOR2)
    print(a1.jugador)
    # a2 = Agente("123") #a ver si da error como debe
    a3 = Agente(Reglas.JUGADOR1)
    a4 = Agente(Reglas.JUGADOR2)



def prueba_GetHash():
    # PRUEBA HASH
    print("")
    print("====================")
    print("## PRUEBA HASHING ##")
    print("====================")
    Carta.ResetContCarta()
    cartas_jugadas = []
    cartas_jugadas.append(Carta("6-Copa", 10))
    cartas_jugadas.append(Carta("6-Basto", 10))
    print("Estado a hashear" + str(cartas_jugadas))
    result = ""
    for i in cartas_jugadas:
        result = result + str(i.ID)
    for j in range(6 - len(cartas_jugadas)):
        result = result + "0"
    print("codigo levantado:  " + str(int(result)))


def prueba_GetStateFromHash():
    # PRUEBA RECONSTRUCCION DESDE UN HASH
    print("")
    print("==========================================")
    print("## PRUEBA RECONSTRUIR ESTADO DESDE HASH ##")
    print("==========================================")
    Carta.ResetContCarta()
    Reglas.MAZO = GenerarMazo()
    print("total cartas en MAZO: " + str(len(Reglas.MAZO)))
    cartas_jugadas = []
    idEstado = "123450"
    print("Hashcode a Levantar: " + str(idEstado))
    for c in str(idEstado):
        if int(c) > 0:
            cartas_jugadas.append(Reglas.MAZO[int(c) - 1])
    print("Lista de Cartas buscadas" + str(cartas_jugadas))

    # Debo reconstruir el mazo antes de levantar el estado, no anda sin esto
    Carta.ResetContCarta()
    Reglas.MAZO = GenerarMazo()
    # Ahora si, finalmente levanto el estado
    cartas_jugadas = LoadEstado_FromHash(idEstado)
    print("ESTADO LEVANTADO: " + str(cartas_jugadas))
    print("cantidad de cartas en estado levantado: " + str(len(cartas_jugadas)))

def prueba_GetAllStateCodes():
    # PRUEBA GET ALL STATES CODES
    print("")
    print("==============================================================")
    print("## PRUEBA METODO QUE CONSTRUYE TODOS LOS CODIGOS DE ESTADOS ##")
    print("==============================================================")
    Carta.ResetContCarta()
    Reglas.MAZO = GenerarMazo()
    lista_codigos = GetAllStatesCodes(Reglas.MAZO, 2)  #6 jugadas, 3 por jugador
    lista_codigos.sort()
    print("cantidad de codigos posibles (solo largo especifico 2, para total acumular) : " + str(len(lista_codigos)))
    cont = 0
    for i in lista_codigos:
        cont = cont + 1
        #print(str(cont) + " nro" + str(int(i)))
    print("cantidad de codigos posibles (solo largo especifico 2) : " + str(len(lista_codigos)))

def prueba_GetAllStates():
    # PRUEBA GET ALL STATES
    print("")
    print("===================================================")
    print("## PRUEBA METODO QUE CONSTRUYE TODOS LOS ESTADOS ##")
    print("===================================================")
    Carta.ResetContCarta()
    Reglas.MAZO = GenerarMazo()
    print("total cartas en MAZO: " + str(len(Reglas.MAZO)))

    lista_estados = GetAllStates()  # solo usar cuando este listo el getallstatecodes
    print("cantidad de estados posibles: " + str(len(lista_estados)))
    cont = 0
    print("Muestreo los de un largo especifico (2)")
    for i in lista_estados:
        if len(i) == 2:
            # no imprimir todos los elementos
            cont = cont + 1
            # print("#" + str(cont) + ", Estado-" + str(i))
    print("imprimi de largo especifico (2): " + str(cont))

def prueba_QuienLeToca():
    print("")
    print("===================================================")
    print("## PRUEBA - Quien le Toca - ##")
    print("===================================================")
    print("Reglas de prueba: 2-3  4-5   y 6-7  empatan, el resto gana quien tiene ID mas alto ")
    print("")

    # Pruebas
    casos_a_probar = []
    casos_a_probar.append("9856")
    casos_a_probar.append("6")
    casos_a_probar.append("23") # empate
    casos_a_probar.append("84")
    casos_a_probar.append("48")
    casos_a_probar.append("164")
    casos_a_probar.append("628")
    casos_a_probar.append("2384") # primera empatan
    casos_a_probar.append("2348") # primera empatan
    casos_a_probar.append("8423") # segunda empatan
    casos_a_probar.append("4823") # segunda empatan, TODO CHEQUEAR REGLA TRUCO
    casos_a_probar.append("2345") # Doble Empate
    casos_a_probar.append("23845")  # primera empatan
    casos_a_probar.append("23485")  # primera empatan
    casos_a_probar.append("85234")  # segunda empatan
    casos_a_probar.append("58234")  # segunda empatan
    casos_a_probar.append("23457")  # Doble Empate

    for i in casos_a_probar:
        print("Prueba con estado: " + i[3::] + "  , le toca a j" + str(QuienLeToca(i)))

def prueba_QueHayEnQ(player = None, DEBUG= False):

    # Creamos el Agente de Prueba
    if player is None:
        player = Agente(Reglas.JUGADOR1, 0.1, 0.1, 0.9)
        player.InicializarQ()

    print("")
    print("===================================================")
    print("## PRUEBA - Que hay en Q - ##")
    print("===================================================")
    print("Formato de Prueba")
    print("")

    s_count = len(player.Q)
    cont_ceros = 0
    cont_non_cero = 0

    if DEBUG: print("Largo de Q = " + str(s_count) )
    if DEBUG: print("Tamaño teorico de Q[s,a} = " + str(s_count*3))

    for i in player.Q.values():
        for j in i:
            #print("output.  i:" + str(j) + "    j: " +str(i[j]))
            if i[j] == 0:
                cont_ceros = cont_ceros +1
            else:
                cont_non_cero = cont_non_cero +1

    if DEBUG:print("Elementos totales contados = " + str(cont_ceros + cont_non_cero))
    if DEBUG:print("De ellos, cantidad en cero = " + str(cont_ceros))
    if DEBUG:print("De ellos, cantidad NO en cero = " + str(cont_non_cero))
    if DEBUG:print("Ratio en cero: " + str(cont_ceros /(cont_ceros + cont_non_cero)))

    return cont_ceros /(cont_ceros + cont_non_cero)

def prueba_QuienGano():
    print("")
    print("===================================================")
    print("## PRUEBA - Quien Gano - ##")
    print("===================================================")
    s = ""
    print("Prueba con nuevo Estado: " + str(QuienGano(s)))
    # Cartas de prueba
    Carta.ResetContCarta()
    Reglas.MAZO = []
    Reglas.MAZO.append(Carta("4-Copa", 10))
    Reglas.MAZO.append(Carta("6-Copa", 20))
    Reglas.MAZO.append(Carta("6-Basto", 20))
    Reglas.MAZO.append(Carta("11-Copa", 30))
    Reglas.MAZO.append(Carta("11-Basto", 30))
    Reglas. MAZO.append(Carta("2-Basto", 40))
    Reglas.MAZO.append(Carta("2-Copa", 40))
    Reglas.MAZO.append(Carta("1-Basto", 80))
    Reglas.MAZO.append(Carta("1-Espada", 100))

    # Pruebas
    s = "985613"  # La de DEBUG
    print("Prueba con 985613 (100-80, 30-40, 10-20): " + str(QuienGano(s)))
    s = "452179"  # Empatan la 1ra
    print("Prueba con (30-30, 20-10, 40-100): " + str(QuienGano(s)))
    s = "451297"  # Empatan la 1ra
    print("Prueba con (30-30, 10-20,  100-40): " + str(QuienGano(s)))
    s = "214579"  # Empatan la 2da
    print("Prueba con (20-10, 30-30, 40-100): " + str(QuienGano(s)))
    s = "124597"  # Empatan la 2da
    print("Prueba con (10-20, 30-30, 100-40): " + str(QuienGano(s)))
    s = "124567"  # Empatan la 2da y 3ra
    print("Prueba con (10-20, 30-30, 40-40): " + str(QuienGano(s)))
    s = "214567"  # Empatan la 2da y 3ra
    print("Prueba con (20-10, 30-30, 40-40): " + str(QuienGano(s)))
    s = "452167"  # Empatan la 1ra y 3ra
    print("Prueba con (30-30, 20-10, 40-40): " + str(QuienGano(s)))
    s = "452367"  # Empatan la 1ra y 3ra
    print("Prueba con (30-30, 20-20, 40-40): " + str(QuienGano(s)))
    s = "452317"  # Empatan la 1ra y 2da
    print("Prueba con (30-30, 20-20, 10-40): " + str(QuienGano(s)))
    s = "452371"  # Empatan la 1ra y 2da
    print("Prueba con (30-30, 20-20, 40-10): " + str(QuienGano(s)))
    s = "45"
    print("Prueba con (30-30, ...): " + str(QuienGano(s)))

def prueba_Save_Load(train_size, DEBUG=False):
    # TRAIN AND SAVE TWO AGENTS
    print("")
    print("===================================================")
    print("## PRUEBA - Train and Save two Agents - ##")
    print("===================================================")
    print("")
    print("1) entrenando agentes..")
    p1, p2 = train_agents(train_size, DEBUG)
    play_game(p1, p2, 100, DEBUG)
    print("p1.Q[0] = " + str(p1.Q[0]))
    # Guardando Q
    print("")
    print("2) Guardando Pickles en p1_qa.pickle y p2_qa.pickle..")
    p1.Save_Q_to_Disk("p1_qa.pickle")
    p2.Save_Q_to_Disk("p2_qa.pickle")
    print("")
    print("3) Cargando Pickles en nuevos players a ver como juegan.")
    # Cargando Q
    nuevo_p1 = Agente(Reglas.JUGADOR1)
    nuevo_p2 = Agente(Reglas.JUGADOR2)
    nuevo_p1.Load_Q_From_Disk("p1_qa.pickle")
    nuevo_p2.Load_Q_From_Disk("p2_qa.pickle")

    play_game(nuevo_p1, nuevo_p2, 100, DEBUG)
    print("nuevo p1.Q[0] = " + str(nuevo_p1.Q[0]))

def DEMO_Random_vs_Trained(p2, sample_size, DEBUG=False):
    # RANDOM AGENTE vs AGENTE
    print("")
    print("===================================================")
    print("## DEMO - Random Agent vs Trained Agent - ##")
    print("===================================================")
    print("")
    # Creo agente random
    print("1) Creando y muestreando Agente Random..")
    p1_r = AgenteRandom(Reglas.JUGADOR1)
    p2_r = AgenteRandom(Reglas.JUGADOR2)
    #p1_r, p2_r = train_agents(0, DEBUG, p1_r, p2_r)
    # muestreo agentes random
    win_ratio_1 = play_game(p1_r, p2_r, sample_size, DEBUG)


    # los hago jugar
    print("")
    print("2) Jugando p1(Random) vs p2(Trained)")
    win_ratio_3 = play_game(p1_r, p2, sample_size, DEBUG)
    print("")

    print("3) TERMINADO! Trained Agent mejora (versus Random Agent): " + str(win_ratio_1 - win_ratio_3))

def DEMO_Human_vs_Trained(p1,p2, DEBUG=False):
    # RANDOM AGENTE vs AGENTE
    print("")
    print("===================================================")
    print("## DEMO - Humano vs Trained Agent - ##")
    print("===================================================")
    print("(primero como p2 y luego como p1")
    print("")
    h1 = Humano(Reglas.JUGADOR1)
    h2 = Humano(Reglas.JUGADOR2)

    print("Jugando p1(ai) vs h2 (Humano)")
    play_game(p1, h2, 1,DEBUG)  #  Humano como p2
    print("")
    print("Jugando h1 (Humano) vs p2(ai) ")
    play_game(h1, p2, 1,DEBUG)  #  Humano como p1

def DEMO_Trained_vs_Trained(train_size_1, train_size_2, DEBUG=False):
    print("")
    print("===================================================")
    print("## DEMO - Trained Agent vs Trained Agent - ##")
    print("===================================================")
    print("")
    p1_w, p2_w = train_agents(train_size_1, DEBUG)
    #print("Jugando p1(medium) vs p2(medium)")
    #play_game(p1_w, p2_w, 100)

    print("")
    p1_m, p2_m = train_agents(train_size_2, DEBUG)
    #print("Jugando p1(medium) vs p2(medium)")
    #play_game(p1_m, p2_m, 100)

    print("")
    print("Jugando p1 vs p2")
    winrate = play_game(p1_w, p2_m, 100,DEBUG)
    print("Winrate player 1: " + str(winrate))

def DEMO_TrainSize_vs_Saved(p1_train_size, p2, samplesize, DEBUG=False):
    print("")
    print("===================================================")
    print("## DEMO - Saved Agent vs Saved Agent - ##")
    print("===================================================")
    print("")
    # Entrenando p1
    p1_t, p2_t = train_agents(p1_train_size, DEBUG)

    # Muestreo p1 Trainsize
    winrate1 = play_game(p1_t, p2_t, samplesize, DEBUG)

    # Ahora si juegan NewTrained vs Saved
    print("Jugando p1 vs p2")
    winrate2 = play_game(p1_t, p2, samplesize, DEBUG)

    print("3) TERMINADO! Trained Agent mejora (versus Saved): " + str(winrate1 - winrate2))

def DEMO_TrainAgent_vs_Random(train_size,DEBUG=False):
    # RANDOM AGENTE vs AGENTE
    print("")
    print("===================================================")
    print("## DEMO - Random Agent vs Trained Agent - ##")
    print("===================================================")
    print("")
    # Creo agente random
    print("1) Creando y muestreando Agente Random..")
    p1_r = AgenteRandom(Reglas.JUGADOR1)
    p2_r = AgenteRandom(Reglas.JUGADOR2)
    # muestreo agentes random
    win_ratio_1 = play_game(p1_r, p2_r, 40000, DEBUG)

    print("2) Entrenando p2 versus el random")
    p1_r = AgenteRandom(Reglas.JUGADOR1)
    p2 = Agente(Reglas.JUGADOR2)
    _, p2 = train_agents(train_size, DEBUG, p1_r, p2)



    # los hago jugar
    print("")
    print("2) Jugando p1(Random) vs p2(Trained)")
    win_ratio_3 = play_game(p1_r, p2, 40000, DEBUG)
    print("")
    print("3) TERMINADO! Trained Agent mejora (versus Random Agent): " + str(win_ratio_1 - win_ratio_3))


def prueba_CurvePropagacion_Q():
    results = []

    # inicial
    p1, p2 = train_agents(1, False)
    results.append(prueba_QueHayEnQ(p2))

    # Otros
    p1, p2 = train_agents(100, False, p1,p2,)
    results.append(prueba_QueHayEnQ(p2))

    p1, p2 = train_agents(1000, False, p1,p2,)
    results.append(prueba_QueHayEnQ(p2))

    p1, p2 = train_agents(10000, False, p1,p2,)
    results.append(prueba_QueHayEnQ(p2))

    p1, p2 = train_agents(100000, False, p1,p2,)
    results.append(prueba_QueHayEnQ(p2))

    print(results)


if __name__ == '__main__':


    print("COMIENZO v1 rel.4 !!")

    # PRUEBAS Unitarias
    """
    prueba_General()
    prueba_GetHash()
    prueba_GetStateFromHash()
    prueba_GetAllStateCodes()
    prueba_GetAllStates()
    print(Reglas.RepartirCartas())
    prueba_QueHayEnQ(loaded_p2, True)
    prueba_QuienGano()
    prueba_QuienLeToca()
    prueba_CurvePropagacion_Q()
    prueba_Save_Load()
    prueba_Save_Load(10000, False)    
    """

    # BIG TRAIN
    # Caso 1) entrenando p1 y p2 entre ellos (Nash equilibrium)
    print("")
    print("# Training Start #")
    print("")


    # Caso 2) Entrenando p2 versus un p1 Random
    # p1_r = AgenteRandom(Reglas.JUGADOR1)
    # p2_t = Agente(Reglas.JUGADOR2)
    # p1_r.InicializarQ()
    # p2_t.InicializarQ()
    # _, p2_t = train_agents(50000000, False, p1_r, p2_t)
    # p2_t.Save_Q_to_Disk("p2_vsRandom.pickle")

    print("")
    print("# Training Finish #")
    print("")


    # Cargando Q de Disco
    printDebug("comienzo carga de Qs de hdd")
    loaded_p1 = Agente(Reglas.JUGADOR1)
    loaded_p2 = Agente(Reglas.JUGADOR2)
    loaded_p2_vsRandom = Agente(Reglas.JUGADOR2)
    loaded_p1.Load_Q_From_Disk("p1.pickle")
    loaded_p2.Load_Q_From_Disk("p2.pickle")
    loaded_p2_vsRandom.Load_Q_From_Disk("p2_vsRandom.pickle")
    printDebug("Termine carga de Qs de hdd")
    print("")

    # Continuar entrenando los AgenteNash
    # sequential_Train_and_Save(20, 2000000, True, loaded_p1, loaded_p2)  # entrenamiento sequential

    # Chequear Status
    print("AgenteNash p1 detalles de Q:")
    loaded_p1.ZeroRatio_en_Q(True)
    print("")
    print("AgenteNash p2 detalles de Q:")
    loaded_p2.ZeroRatio_en_Q(True)
    print("")
    print("Agente_AntiRandom p2 detalles de Q:")
    loaded_p2_vsRandom.ZeroRatio_en_Q(True)
    print("")

    # TODOS CONTRA TODOS!!!
    print("Random vs Random = " + str(play_game(AgenteRandom(Reglas.JUGADOR1), AgenteRandom(Reglas.JUGADOR2), 100000, False)) + " %")  # Random vs randomT
    print("AgenteNash vs Random   = " + str(play_game(loaded_p1, AgenteRandom(Reglas.JUGADOR2), 100000, False)) + " %")  # Random vs nashT
    print("AgenteNash vs AgenteNash = " + str(play_game(loaded_p1, loaded_p2, 100000, False)) + " %") # nashT vs nashT
    print("AgenteNash  vs Agente_AntiRandom = " + str(play_game(loaded_p1,loaded_p2_vsRandom,100000,False)) + " %") # nashT vs randomT
    print("Random vs Agente_AntiRandom = " + str(play_game(AgenteRandom(Reglas.JUGADOR1), loaded_p2_vsRandom, 100000, False)) + " %") # Random vs randomT
    print("Random vs AgenteNash  = "  + str(play_game(AgenteRandom(Reglas.JUGADOR1), loaded_p2, 100000, False)) + " %")  # Random vs nashT


    # DEMO_Human_vs_Trained(loaded_p1, loaded_p2, False)  # Prueba de Agente vs Humano


    # PRUEBAS VIEJAS
    # DEMO_Random_vs_Trained(loaded_p2_vsRandom, 100000)  # Prueba de p1(Random) vs Agent (x parametro)
    # DEMO_Human_vs_Trained(loaded_p1,loaded_p2, False)    # Prueba de Agente vs Humano
    # DEMO_Trained_vs_Trained(100,1000)
    # DEMO_Train_and_Save(1000, False)
    # DEMO_Random_vs_Saved(2000)
    # DEMO_TrainSize_vs_Saved(100000, loaded_p2, 10000)
    # DEMO_TrainAgent_vs_Random(1000000) # entrenamiento rapido de un agente vs random

    # FIN
    print("")
    print("")
    print("TERMINE!!")
