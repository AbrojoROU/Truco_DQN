from Truco_Core_v2_r1 import *
import keras
import tensorflow as tf

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
    cartas_j1.append(Reglas.MAZO[9])
    cartas_j1.append(Reglas.MAZO[5])
    cartas_j1.append(Reglas.MAZO[3])
    cartas_j2.append(Reglas.MAZO[8])
    cartas_j2.append(Reglas.MAZO[6])
    cartas_j2.append(Reglas.MAZO[1])

    p1.TomarCartas(cartas_j1)
    p2.TomarCartas(cartas_j2)

    # Prueba
    print("1) p1 juega c1, acciones de p2 disponibles")
    p1.EjecutarAccion(s, Reglas.Accion.JUGAR_C1)
    print(str(p2.get_acciones_posibles(s)))
    print("")

    return p1, p2, s

    print("2) p2 grito Truco, acciones de p1 disponibles")
    p2.EjecutarAccion(s, Reglas.Accion.GRITAR_TRUCO)
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

def Generate_and_Save(nameprefix, batch_size, epochs):
    print("###########################")
    print("##   Generate_and_Save   ##")
    print("###########################")
    print("")

    nameprefixLoad = "value_pickles\_v_"
    p1_DQN = keras.models.load_model(nameprefixLoad + "p1_DQN.h5")
    p2_DQN = keras.models.load_model(nameprefixLoad + "p2_DQN.h5")
    p1 = AgenteDVN(Reglas.JUGADOR1, p1_DQN)
    p2 = AgenteDVN(Reglas.JUGADOR2, p2_DQN)

    print("1. Generando Partidas de entrenamiento")
    (p1_traindata, p1_trainlabels), (p2_traindata, p2_trainlabels) = Motor.Generate_Value_Training_Games(p1, p2, batch_size, epochs)

    print("")
    print("2. Generando Partidas de test")
    (p1_testdata, p1_testlabels), (p2_testdata, p2_testlabels) = Motor.Generate_Value_Training_Games(p1, p2, batch_size, 1)
    print("len p1_traindata: " + str(len(p1_traindata)) + ", len p1_testdata: " + str(len(p1_testdata)))
    print("len p1_trainlabels: " + str(len(p1_trainlabels)) + ", len p1_testlabels: " + str(len(p1_testlabels)))
    print("len p2_traindata: " + str(len(p2_traindata)) + ", len p2_testdata: " + str(len(p2_testdata)))
    print("len p2_trainlabels: " + str(len(p2_trainlabels)) + ", len p2_testlabels: " + str(len(p2_testlabels)))

    print("")
    print("3. Guardando partidas en Disco (pickle) con prefijo:" + nameprefix)
    # train
    Motor.Save_Games_to_Disk(p1_traindata, nameprefix + "p1_traindata.pickle")
    Motor.Save_Games_to_Disk(p1_trainlabels, nameprefix + "p1_trainlabels.pickle")
    Motor.Save_Games_to_Disk(p2_traindata, nameprefix + "p2_traindata.pickle")
    Motor.Save_Games_to_Disk(p2_trainlabels, nameprefix + "p2_trainlabels.pickle")
    # test
    Motor.Save_Games_to_Disk(p1_testdata, nameprefix + "p1_testdata.pickle")
    Motor.Save_Games_to_Disk(p1_testlabels, nameprefix + "p1_testlabels.pickle")
    Motor.Save_Games_to_Disk(p2_testdata, nameprefix + "p2_testdata.pickle")
    Motor.Save_Games_to_Disk(p2_testlabels, nameprefix + "p2_testlabels.pickle")

def Train_Save(nameprefix, eps):
    print("####################")
    print("##   Train_Save   ##")
    print("####################")
    print("")
    print("## Carga de partidas de entrenamiento P1 desde Disco (pickles) con prefijo '" + nameprefix + "'")
    # p1
    p1_traindata = Motor.Load_Games_From_Disk(nameprefix + "p1_traindata.pickle")
    p1_trainlabels = Motor.Load_Games_From_Disk(nameprefix + "p1_trainlabels.pickle")
    p1_testdata = Motor.Load_Games_From_Disk(nameprefix + "p1_testdata.pickle")
    p1_testlabels = Motor.Load_Games_From_Disk(nameprefix + "p1_testlabels.pickle")

    # ENTRENANDO REDES
    from keras import models
    from keras import layers

    #########################
    print("")
    print("## Entrenando Red para P1ayer 1")
    ## ENTRENO RED PARA p1
    p1_DQN = models.Sequential()
    p1_DQN.add(layers.Dense(50, activation='relu', input_shape=(50,)))
    p1_DQN.add(layers.Dense(100, activation='relu'))
    p1_DQN.add(layers.Dense(200, activation='relu'))
    p1_DQN.add(layers.Dense(200, activation='relu'))
    p1_DQN.add(layers.Dense(200, activation='relu'))
    p1_DQN.add(layers.Dense(200, activation='relu'))
    p1_DQN.add(layers.Dense(100, activation='relu'))
    p1_DQN.add(layers.Dense(50, activation='relu'))
    p1_DQN.add(layers.Dense(1))

    p1_DQN.compile(optimizer='adam', loss='mse', metrics=['mae'])

    # Convierto a nparray y reshape a lo especificado en las capas de la red neuronal (shape a 50)
    # Train
    p1_traindata = np.squeeze(np.asarray(p1_traindata))
    p1_traindata = p1_traindata.reshape((len(p1_traindata), 50))
    p1_traindata = p1_traindata.astype('float32')
    #p1_trainlabels = keras.utils.to_categorical(p1_trainlabels)  # los labels van a categorical
    # Test
    p1_testdata = np.squeeze(np.asarray(p1_testdata))
    p1_testdata = p1_testdata.reshape((len(p1_testdata), 50))
    p1_testdata = p1_testdata.astype('float32')
    #p1_testlabels = keras.utils.to_categorical(p1_testlabels)  # los labels van a categorical

    # Fiteo la red
    p1_DQN.fit(p1_traindata, p1_trainlabels, epochs=eps, batch_size=256, shuffle=True, verbose=2)

    # Evaluo contra Test
    test_loss, test_acc = p1_DQN.evaluate(p1_testdata, p1_testlabels, verbose=2)
    print('test_acc:', test_acc)

    print("")
    print("  ...guardando Red DQN de p1 con prefijo '" + nameprefix + "'")
    p1_DQN.save(nameprefix+"p1_DQN.h5")
    print("      " + nameprefix + "p1_DQN.h5 guardado!")

    del p1_traindata

    #########################
    ## ENTRENO RED PARA p2
    print("## Carga de partidas de entrenamiento P2 desde Disco (pickles) con prefijo '" + nameprefix + "'")
    # p2
    p2_traindata = Motor.Load_Games_From_Disk(nameprefix + "p2_traindata.pickle")
    p2_trainlabels = Motor.Load_Games_From_Disk(nameprefix + "p2_trainlabels.pickle")
    p2_testdata = Motor.Load_Games_From_Disk(nameprefix + "p2_testdata.pickle")
    p2_testlabels = Motor.Load_Games_From_Disk(nameprefix + "p2_testlabels.pickle")

    print("")
    print("## Entrenando Red para P1ayer 2")
    p2_DQN = models.Sequential()
    p2_DQN.add(layers.Dense(50, activation='relu', input_shape=(50,)))
    p2_DQN.add(layers.Dense(100, activation='relu'))
    p2_DQN.add(layers.Dense(200, activation='relu'))
    p2_DQN.add(layers.Dense(200, activation='relu'))
    p2_DQN.add(layers.Dense(200, activation='relu'))
    p2_DQN.add(layers.Dense(200, activation='relu'))
    p2_DQN.add(layers.Dense(100, activation='relu'))
    p2_DQN.add(layers.Dense(50, activation='relu'))
    p2_DQN.add(layers.Dense(1))

    p2_DQN.compile(optimizer='adam', loss='mse', metrics=['mae'])

    # Convierto a nparray y reshape a lo especificado en las capas de la red neuronal (shape a 50)
    # Train
    p2_traindata = np.squeeze(np.asarray(p2_traindata))
    p2_traindata = p2_traindata.reshape((len(p2_traindata), 50))
    p2_traindata = p2_traindata.astype('float32')

    # Test
    p2_testdata = np.squeeze(np.asarray(p2_testdata))
    p2_testdata = p2_testdata.reshape((len(p2_testdata), 50))
    p2_testdata = p2_testdata.astype('float32')


    # Fiteo la red
    p2_DQN.fit(p2_traindata, p2_trainlabels, epochs=eps, batch_size=256, shuffle=True, verbose=2)

    # Evaluo contra Test
    test_loss, test_acc = p2_DQN.evaluate(p2_testdata, p2_testlabels, verbose=2)
    print('test_acc:', test_acc)

    print("")
    print("  ...guardando red DQN de p2 con prefijo '" + nameprefix + "'")
    p2_DQN.save(nameprefix + "p2_DQN.h5")
    print("      " + nameprefix + "p2_DQN.h5 guardado!")

    del p2_traindata

def Load_and_Test(nameprefix, DEBUG):
    print("#######################")
    print("##   Load_and_Test   ##")
    print("#######################")
    print("")
    print("## Carga de partidas de Test desde Disco (pickles) con prefijo: " + nameprefix)
    # test
    p1_testdata = Motor.Load_Games_From_Disk(nameprefix + "p1_testdata.pickle")
    p1_testlabels = Motor.Load_Games_From_Disk(nameprefix + "p1_testlabels.pickle")
    p2_testdata = Motor.Load_Games_From_Disk(nameprefix + "p2_testdata.pickle")
    p2_testlabels = Motor.Load_Games_From_Disk(nameprefix + "p2_testlabels.pickle")

    # Convierto a nparray y reshape a lo especificado en las capas de la red neuronal (shape a 50)
    # p1
    p1_testdata = np.squeeze(np.asarray(p1_testdata))
    p1_testdata = p1_testdata.reshape((len(p1_testdata), 50))
    p1_testdata = p1_testdata.astype('float32')

    # p2
    p2_testdata = np.squeeze(np.asarray(p2_testdata))
    p2_testdata = p2_testdata.reshape((len(p2_testdata), 50))
    p2_testdata = p2_testdata.astype('float32')

    print("")
    print("## Loading model from disk")
    # p1
    p1_DQN = keras.models.load_model(nameprefix + "p1_DQN.h5")
    test_loss_p1, test_acc_p1 = p1_DQN.evaluate(p1_testdata, p1_testlabels, verbose=2)
    print('## p1 test_acc:', test_acc_p1)
    # p2
    p2_DQN = keras.models.load_model(nameprefix + "p2_DQN.h5")
    test_loss_p2, test_acc_p2 = p2_DQN.evaluate(p2_testdata, p2_testlabels, verbose=2)
    print('## p2 test_acc:', test_acc_p2)


    p1,p2, s = Get_VectorEstado_Prueba()

    currentplayer = s.QuienActua()
    if s.QuienActua() == Reglas.JUGADOR1: currentplayer = p1
    if s.QuienActua() == Reglas.JUGADOR2 : currentplayer = p2

    print("Le toca a p" + str(currentplayer.jugador))
    print(" cartas jugadas: " + str(s.cartas_jugadas))
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
        _s = Motor.ConverToPolicyVector(_cp, _s, True)
        _s = np.squeeze(np.asarray(_s))# Convierto a array de Red
        _s = _s.reshape(1, 50)
        _s = _s.astype('float32')

        # 4. Estimo
        if _cp.jugador is Reglas.JUGADOR1 : output = p1_DQN.predict(_s)
        if _cp.jugador is Reglas.JUGADOR2 : output = p2_DQN.predict(_s)
        print("p" + str(_cp.jugador) + "> accion posible: " + str(i.name) + ",  valor:" + str(output))




#######################################################
###                    MAIN                         ###
#######################################################
if __name__ == '__main__':
    printDebug("COMIENZO!")
    print("")

    import logging
    logging.getLogger('tensorflow').disabled = True

    # Variables de Entrenamiento
    nameprefix  = "value_pickles v3\_v_"
    DEBUG = False

    # Genero las partidas y guardo los pickles en disco (omitir si ya tengo un buen pickle generado)
    Generate_and_Save(nameprefix,1000,10)

    # Cargo las partidas de Disco, entreno la red y la guardo en disco en h5 (omitir si ya tengo una buena Red entrenada)
    Train_Save(nameprefix, 5)

    # finalmente, cargo una Red de disco (formato h5) y juego/testeo
    Load_and_Test(nameprefix, DEBUG)


    print("")
    printDebug("## TERMINE! ##")