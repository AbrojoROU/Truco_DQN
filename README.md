# Truco_DQN
Implementación de Truco aplicando distintos tipos de redes neuronales (ej: deep Q networks)

v1: Aprendizaje Reforzado Tradicional. Concretamente Temporal Difference (0), aplicando basicamente SARSA + epsilon greedy. Sin envido o truco, mazo reducido, juega las cartas sabiendo cuando matar y con que. 
Buenos resultados pero muy costoso de entrenar (300 Millones de partidas) y con altisimo costo de memoria.

v2: Agentes profundos. Inspirado en AlphaGo, se intentan dos tecnicas diferentes para entrenar los Agentes a ver cual daba mejores resultados: Una Deep Policy Network que dado el estado me retorna las acciones con probabilidades asignadas (problema de clasificacion) y una Deep Value Network que dado un estado me da el valor esperado final de la posicion en puntos de truco. A diferencia del anterior hecho con TD(0), este no actualiza en linea con lo cual buscamos alcanzar equilibrio de Nash generando diferentes generaciones de Agentes que evolucionan su policy aprendiendo de sus padres. 

v3: Refactoring the la solucion de Agentes Profundos con multiples optimizaciones. Cada Agente aprende viendo los juegos del padre, y genera juegos para que su hijo entrene. Aqui la version de Agentes que usan una Deep Policy Network ya es descartada por performar peor que la Deep Value Network lo cual hace sentido para este caso donde la cantidad de acciones posibles es relativamente pequeña. Logra jugar al truco (sin envido) bastante bien, mostrando bluffs y otros comportamientos no triviales.

v4: Agregamos envido, incontables optimizaciones y correcciones de bug adicionales.

v5: Versional final(?) mejor documentada y con notebooks para uso mas facil. Ver presentacion de powerpoint "Proyecto Truco" para mas detalles 
