from Truco_Core_v2_r1 import *
import keras
import tensorflow as tf


def Generate_and_Save(nameprefix, batch_size, epochs, DEBUG):
    print("")
    print("## Generate_and_Save ##")
    print("")
    print("1. Generando Partidas de entrenamiento")
    (p1_traindata, p1_trainlabels), (p2_traindata, p2_trainlabels) = Motor.Generate_Training_Games(batch_size, epochs, DEBUG)

    print("")
    print("2. Generando Partidas de test")
    (p1_testdata, p1_testlabels), (p2_testdata, p2_testlabels) = Motor.Generate_Training_Games(batch_size, 1, DEBUG)
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




def Train_Save(nameprefix, batch_size, epochs, DEBUG):
    print("")
    print("## Train_Save ##")
    print("")
    print("1. Carga de partidas de entrenamiento desde Disco (pickles) con prefijo:" + nameprefix)
    # train
    p1_traindata = Motor.Load_Games_From_Disk(nameprefix + "p1_traindata.pickle")
    p1_trainlabels = Motor.Load_Games_From_Disk(nameprefix + "p1_trainlabels.pickle")
    p2_traindata = Motor.Load_Games_From_Disk(nameprefix + "p2_traindata.pickle")
    p2_trainlabels = Motor.Load_Games_From_Disk(nameprefix + "p2_trainlabels.pickle")
    # test
    p1_testdata = Motor.Load_Games_From_Disk(nameprefix + "p1_testdata.pickle")
    p1_testlabels = Motor.Load_Games_From_Disk(nameprefix + "p1_testlabels.pickle")
    p2_testdata = Motor.Load_Games_From_Disk(nameprefix + "p2_testdata.pickle")
    p2_testlabels = Motor.Load_Games_From_Disk(nameprefix + "p2_testlabels.pickle")

    print("")
    print("2. Entrenando Red:")
    from keras import models
    from keras import layers

    p1_DQN = models.Sequential()
    p1_DQN.add(layers.Dense(50, activation='relu', input_shape=(50,)))
    p1_DQN.add(layers.Dense(50, activation='relu'))
    p1_DQN.add(layers.Dense(8, activation='softmax'))

    p1_DQN.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])

    # Convierto a nparray y reshape a lo especificado en las capas de la red neuronal (shape a 50)
    # Train
    p1_traindata = np.squeeze(np.asarray(p1_traindata))
    p1_traindata = p1_traindata.reshape((len(p1_traindata), 50))
    p1_traindata = p1_traindata.astype('float32')
    p1_trainlabels = keras.utils.to_categorical(p1_trainlabels)  # los labels van a categorical
    # Test
    p1_testdata = np.squeeze(np.asarray(p1_testdata))
    p1_testdata = p1_testdata.reshape((len(p1_testdata), 50))
    p1_testdata = p1_testdata.astype('float32')
    p1_testlabels = keras.utils.to_categorical(p1_testlabels)  # los labels van a categorical

    # Fiteo la red
    p1_DQN.fit(p1_traindata, p1_trainlabels, epochs=2, batch_size=64)

    # Evaluo contra Test
    test_loss, test_acc = p1_DQN.evaluate(p1_testdata, p1_testlabels)
    print('test_acc:', test_acc)

    print("")
    print("2. Guardando Red DQN con prefijo:" + nameprefix)
    p1_DQN.save(nameprefix+"p1_DQN.h5")
    print("Saved model to disk")


def Load_and_Test(nameprefix, DEBUG):
    print("")
    print("## Load_and_Test ##")
    print("")
    print("1. Carga de partidas de Test desde Disco (pickles) con prefijo:" + nameprefix)
    # test
    p1_testdata = Motor.Load_Games_From_Disk(nameprefix + "p1_testdata.pickle")
    p1_testlabels = Motor.Load_Games_From_Disk(nameprefix + "p1_testlabels.pickle")
    #p2_testdata = Motor.Load_Games_From_Disk(nameprefix + "p2_testdata.pickle")
    #p2_testlabels = Motor.Load_Games_From_Disk(nameprefix + "p2_testlabels.pickle")

    # Convierto a nparray y reshape a lo especificado en las capas de la red neuronal (shape a 50)
    p1_testdata = np.squeeze(np.asarray(p1_testdata))
    p1_testdata = p1_testdata.reshape((len(p1_testdata), 50))
    p1_testdata = p1_testdata.astype('float32')
    p1_testlabels = keras.utils.to_categorical(p1_testlabels)  # los labels van a categorical


    print("Loading model from disk")
    p1_DQN = keras.models.load_model(nameprefix + "p1_DQN.h5")
    test_loss, test_acc = p1_DQN.evaluate(p1_testdata, p1_testlabels)
    print('test_acc:', test_acc)




#######################################################
###                    MAIN                         ###
#######################################################
if __name__ == '__main__':
    print("COMIENZO!")
    print("")

    tf.logging.set_verbosity(tf.logging.ERROR)  # esta linea deshabilita los warnings de tensfor, deja los errors

    # Variables de Entrenamiento
    nameprefix  = ""
    batch_size = 20000
    epochs = 5
    DEBUG = True

    # Genero las partidas y guardo los pickles en disco (omitir si ya tengo un buen pickle generado)
    Generate_and_Save(nameprefix,batch_size,epochs,DEBUG)

    # Cargo las partidas de Disco, entreno la red y la guardo en disco en h5 (omitir si ya tengo una buena Red entrenada)
    Train_Save(nameprefix,batch_size,epochs,DEBUG)

    # finalmente, cargo una Red de disco (formato h5) y juego/testeo
    Load_and_Test(nameprefix, DEBUG)


    print("")
    print("## TERMINE! ##")