import random

def generar_id() -> int:

    '''
    Esta funcion se encarga de generar un numero aleatorio que sera utilizado como id. 
    
    '''
    return random.randint(100,100000)

def numero_ganador() -> int:

    '''
    Esta funcion se encarga de generar un numero ganador.
    
    '''

    return random.randint(0, 36)


def color_ganador(numero_ganador) -> str:

    '''
    Esta funcion se encarga de generar un color ganador.
    
    '''
    
    return 'rojo' if numero_ganador % 2 == 0 else 'negro'

