import random

def generar_id() -> int:

    '''
    Esta funcion se encarga de generar un numero aleatorio que sera utilizado como id 
    
    '''
    return random.randint(100,100000)