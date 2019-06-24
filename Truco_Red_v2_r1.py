from Truco_Core_v2_r1 import *
import keras

#######################################################
###                    MAIN                         ###
#######################################################
if __name__ == '__main__':
    print("COMIENZO!")
    print("")

    p1 = Agente(Reglas.JUGADOR1)
    p2 = Agente(Reglas.JUGADOR2)
    print("")


    name = "pruebas"
    batch_size = 20000
    epochs = 5
    DEBUG = True

    # print("1. Cargo partidas de disco (opcional)")

    print("")
    print("2. Generando Partidas de entrenamiento (opcional)")
    (p1_traindata, p1_trainlabels), (p2_traindata, p2_trainlabels) = Motor.Generate_Training_Games(batch_size, epochs, DEBUG)

    print("")
    print("3. Generando Partidas de test (opcional)")
    (p1_testdata, p1_testlabels), (p2_testdata, p2_testlabels) = Motor.Generate_Training_Games(batch_size, 1, DEBUG)

    print("len p1_traindata: " + str(len(p1_traindata)) + ", len p1_testdata: " + str(len(p1_testdata)))
    print("len p1_trainlabels: " + str(len(p1_trainlabels)) + ", len p1_testlabels: " + str(len(p1_testlabels)))

    print("len p2_traindata: " + str(len(p2_traindata)) + ", len p2_testdata: " + str(len(p2_testdata)))
    print("len p2_trainlabels: " + str(len(p2_trainlabels)) + ", len p2_testlabels: " + str(len(p2_testlabels)))

    print("")
    print("3. RED ")
    from keras import models
    from keras import layers

    network = models.Sequential()
    network.add(layers.Dense(50, activation='relu', input_shape=(50,)))
    network.add(layers.Dense(50, activation='relu'))
    network.add(layers.Dense(8, activation='softmax'))

    network.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])

    # ajusto formas de datos a lo especificado en las capas de la red neuronal (shape a 3*3)
    # divido los numeros en los datos para que los valores esten todos entre [0,1]

    p1_traindata = np.squeeze(np.asarray(p1_traindata))
    p1_traindata = p1_traindata.reshape((len(p1_traindata), 50))
    p1_traindata = p1_traindata.astype('float32')

    p1_testdata = np.squeeze(np.asarray(p1_testdata))
    p1_testdata = p1_testdata.reshape((len(p1_testdata), 50))
    p1_testdata = p1_testdata.astype('float32')

    from keras.utils import to_categorical

    p1_trainlabels = to_categorical(p1_trainlabels)
    p1_testlabels = to_categorical(p1_testlabels)

    network.fit(p1_traindata, p1_trainlabels, epochs=2, batch_size=64)

    test_loss, test_acc = network.evaluate(p1_testdata, p1_testlabels)
    print('test_acc:', test_acc)

    print("")
    print("## TERMINE! ##")