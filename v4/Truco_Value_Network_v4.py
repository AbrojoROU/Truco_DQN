import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # or any {'0', '1', '2'}
os.environ['TF_CPP_MIN_VLOG_LEVEL'] = '0'
from Truco_Core_v4 import *
import keras
from keras import models
from keras import layers
from keras.callbacks import EarlyStopping, ModelCheckpoint
from matplotlib import pyplot


class ValueNetworkEngine:
    MAX_EPOCHS_PERGEN = 50
    PATIENCE_PERGEN = 5
    BATCH_SIZE = 256
    VALIDATION_RATIO = 0.10 # as % of the total amount of training games

    @staticmethod
    def Generate_Player_DVN():
        player_DVN = models.Sequential()
        player_DVN.add(layers.Dense(100, activation='relu', input_shape=(Motor.STATE_VECTOR_LENGTH,)))
        player_DVN.add(layers.Dense(120, activation='relu', kernel_regularizer=keras.regularizers.l2(0.01)))
        player_DVN.add(layers.Dropout(0.2))
        player_DVN.add(layers.Dense(120, activation='relu', kernel_regularizer=keras.regularizers.l2(0.01)))
        player_DVN.add(layers.Dropout(0.2))
        player_DVN.add(layers.Dense(120, activation='relu', kernel_regularizer=keras.regularizers.l2(0.01)))
        player_DVN.add(layers.Dropout(0.2))
        player_DVN.add(layers.Dense(120, activation='relu', kernel_regularizer=keras.regularizers.l2(0.01)))
        player_DVN.add(layers.Dropout(0.2))
        player_DVN.add(layers.Dense(120, activation='relu', kernel_regularizer=keras.regularizers.l2(0.01)))
        player_DVN.add(layers.Dropout(0.2))
        player_DVN.add(layers.Dense(120, activation='relu', kernel_regularizer=keras.regularizers.l2(0.01)))
        player_DVN.add(layers.Dropout(0.2))
        player_DVN.add(layers.Dense(120, activation='relu', kernel_regularizer=keras.regularizers.l2(0.01)))
        player_DVN.add(layers.Dropout(0.2))
        player_DVN.add(layers.Dense(120, activation='relu', kernel_regularizer=keras.regularizers.l2(0.01)))
        player_DVN.add(layers.Dropout(0.2))
        player_DVN.add(layers.Dense(120, activation='relu', kernel_regularizer=keras.regularizers.l2(0.01)))
        player_DVN.add(layers.Dense(1))

        player_DVN.compile(optimizer='adam', loss='mse', metrics=['mae'])

        return player_DVN


    @staticmethod
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

    @staticmethod
    def Generate_and_Save(input_prefix, output_prefix, games_per_gen):
        import logging
        logging.getLogger('tensorflow').disabled = True
        from tensorflow.python.util import deprecation
        deprecation._PRINT_DEPRECATION_WARNINGS = False
        print("  ##   Generate_and_Save   ##")
        print("")

        if input_prefix is not None:
            # Si input prefix es None, entonces es generacion inicial Random, de lo contrario cargamos generacion anterior
            p1_DQN = keras.models.load_model(input_prefix + "p1_DVN.h5")
            p2_DQN = keras.models.load_model(input_prefix + "p2_DVN.h5")
            p1 = AgenteDVN(Reglas.JUGADOR1, p1_DQN)
            p1.eps = 0.2
            p2 = AgenteDVN(Reglas.JUGADOR2, p2_DQN)
            p2.eps = 0.2
        else:
            p1 = AgenteRandom(Reglas.JUGADOR1)
            p2 = AgenteRandom(Reglas.JUGADOR2)

        print("1. Generando Partidas de entrenamiento")
        (p1_traindata, p1_trainlabels), (p2_traindata, p2_trainlabels) = Motor.MP_Generate_Value_Training_Games(p1, p2, games_per_gen)

        print("")
        print("2. Generando Partidas de test")
        (p1_testdata, p1_testlabels), (p2_testdata, p2_testlabels) = Motor.MP_Generate_Value_Training_Games(
            p1, p2, round(games_per_gen*ValueNetworkEngine.VALIDATION_RATIO)) # Usamos Ratio del Trainign set para determinar tamaño de validation
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

    @staticmethod
    def Train_Save(gen_prefix, training_epochs, load_previous = False):
        print("  ##   Train_Save   ##")
        print("")
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


        #########################
        ## ENTRENO RED PARA p1
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
        callbacks = [EarlyStopping(monitor='val_loss', patience=ValueNetworkEngine.PATIENCE_PERGEN),
                     ModelCheckpoint(filepath=gen_prefix+"p1_DVN.h5", monitor='val_loss', save_best_only=True)]

        # Fiteo la red ACA
        history = p1_DVN.fit(p1_traindata, p1_trainlabels, validation_data=(p1_testdata, p1_testlabels),
                             callbacks=callbacks, epochs=training_epochs, batch_size=ValueNetworkEngine.BATCH_SIZE,
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

        # Free memory
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
        callbacks = [EarlyStopping(monitor='val_loss', patience=ValueNetworkEngine.PATIENCE_PERGEN),
                     ModelCheckpoint(filepath=gen_prefix + "p2_DVN.h5", monitor='val_loss', save_best_only=True)]

        # Fiteo la red
        p2_DVN.fit(p2_traindata, p2_trainlabels, validation_data=(p2_testdata, p2_testlabels),
                   callbacks=callbacks, epochs=training_epochs, batch_size=ValueNetworkEngine.BATCH_SIZE,
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

        # Free memory
        del p2_traindata
        del p2_DVN


    @staticmethod
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

            # Free memory
            del _p1
            del _p2
            del _s

        #Free memory
        del p1
        del p2
        del s
        del p1_DVN
        del p2_DVN


    @staticmethod
    def ValueTrainingTest(gen_p1,gen_p2, N, debug):
        print("")
        print("JUGANDO gen" + str(gen_p1) + " versus gen" + str(gen_p2))

        if gen_p1 > 0:
            gen_p1 = "value_pickles\gen" + str(gen_p1) + "_"
            p1_DVN = keras.models.load_model(gen_p1 + "p1_DVN.h5")
            value_p1 = AgenteDVN(Reglas.JUGADOR1, p1_DVN)
            value_p1.eps = 0
        else:
            value_p1 = AgenteRandom(Reglas.JUGADOR1)

        if gen_p2 > 0:
            gen_p2 = "value_pickles\gen" + str(gen_p2) + "_"
            p2_DVN = keras.models.load_model(gen_p2 + "p2_DVN.h5")
            value_p2 = AgenteDVN(Reglas.JUGADOR2, p2_DVN)
            value_p2.eps = 0
        else:
            value_p2 = AgenteRandom(Reglas.JUGADOR2)

        Motor.Play_random_games(value_p1, value_p2, N, debug)

    @staticmethod
    def ValueNetworkTrainer(start_gen, generations, games_per_gen, load_previous=False):
        # WARNING: Debe existir start_gen tanto en h5 como pickles
        # Detalle: Los start_gen.h5 los levanta en Generate_and_Save para generar juegos de aprendizaje
        # Los pickles son necesarios porque el entrenamiento de start_gen + 1 los tambien (a menos que deshabilitemos load_previous)
        printDebug("COMIENZO!")
        print("")

        import os
        import logging
        logging.getLogger('tensorflow').disabled = True
        from tensorflow.python.util import deprecation
        deprecation._PRINT_DEPRECATION_WARNINGS = False
        import tensorflow as tf
        if type(tf.contrib) != type(tf): tf.contrib._warning = None
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # or any {'0', '1', '2'}

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
            ValueNetworkEngine.Generate_and_Save(gen_n, gen_next, games_per_gen)
            # Cargo las partidas de Disco, entreno la red y la guardo en disco en h5 (omitir si ya tengo una buena Red entrenada)
            if i == 0:
                ValueNetworkEngine.Train_Save(gen_next, ValueNetworkEngine.MAX_EPOCHS_PERGEN, False)
            else:
                ValueNetworkEngine.Train_Save(gen_next, ValueNetworkEngine.MAX_EPOCHS_PERGEN, load_previous)
            # finalmente, cargo una Red de disco (formato h5) y juego/testeo
            ValueNetworkEngine.Load_and_Test(gen_next)

        print("")
        printDebug("## TERMINE! ##")