import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
import cargar 
nltk.download('punkt') 

#texto_carga = cargar.openFile2(input("ingrese el filename (sin el .txt): "))
#texto = texto_carga.lower()

#texto_prueba = "defVar get(9) nop (1) nom 0 defVar x 0 defVar y 0 defVar one 0 defProc putCB (c, b) { (0);  (9); turnTo(arriba)}"
texto_prueba2 = "defProc goNorth() jump (1, 2) nop ( { while can(nop ()) { walk (1 , north ) }; putCB (1 ,1) } defProc "
todo = sent_tokenize(texto_prueba2.lower())
tokens = [word_tokenize(cadacosa) for cadacosa in todo]
#print("Tokens:", tokens)

#Direcciones y orientaciones para comandos
Directions = ['front', 'right', 'left', 'back']
Orientations = ['north', 'south', 'west', 'east']
num = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
Comandos = ['walk', 'leap', 'jump', 'turn', 'turnto', 'drop', 'get','grab', 'letgo', 'nop']
Condicion = ['facing', 'can', 'not']

def correccionIndexOOR(element_to_check, position_to_check, Lista):
    diga = (len(Lista)-1) - position_to_check
    check = False
    # position_to_check == 0, ultima posicion
    # position_to_check == 1, penultima posicion, 
    # etc...
    if Lista[diga] == element_to_check:
        check = True
    else:
        check = False
    return check
        
# Funcion para defVar 
# HACER LO DE QUE LOS NOMBRES SE VUELVEN A USAR
def check_defVar(tokens_):
    i = 0
    check = False
    existe = False
    lista_nombres = []
    tokens = tokens_[0]
    while i < len(tokens):
        token = tokens[i]
        if token == "defvar":
            existe = True
            nombre = tokens[i+1]
            lista_nombres.append(nombre)
            valor = tokens[i+2]
            
            if isinstance(nombre, str) and valor.isdigit():
                check = True
                i += 2  # Avanzar el índice para saltar al próximo token

        i += 1
    
    return check,existe,lista_nombres

#Funcion para defProc
def check_defProc(tokens_):
    i= 0
    tokens = tokens_[0]
    dict_nombres = {}
    check = False
    existe = False
    while i<len(tokens):
        token = tokens[i]
        if token == "defproc":
            existe = True
            nombre = tokens[i+1]
            dict_nombres[nombre] = ""
            parentesis_izquierdo = tokens[i+2]
            if isinstance(nombre,str) and parentesis_izquierdo == "(":
                continuacion = tokens[i+3]
                if continuacion == ")": # primer caso 0 parametros
                    check = True
                    dict_nombres[nombre] = [tokens[i+2],continuacion]
                elif isinstance(continuacion,str) and tokens[i+4] == ")": # segundo caso 1 parametro
                    check = True
                    dict_nombres[nombre] = [tokens[i+2],continuacion,tokens[i+4]]
                elif isinstance(continuacion,str) and tokens[i+4] == "," and isinstance(tokens[i+5],str) and tokens[i+6] == ")": # tercer caso 2 parametros
                    check = True
                    dict_nombres[nombre] = [tokens[i+2],continuacion,tokens[i+4],tokens[i+5],tokens[i+5]]
                else:
                    check = False

        i += 1
    return check,existe,dict_nombres  

#COMANDOS
'''
Walk_Leap               FUNCIONA solo
Jump                    FUNCIONA solo
Turn                    FUNCIONA solo
TurnTo                  FUNCIONA solo
Drop_Get_Grab_LetGo     FUNCIONA solo
Nop'''
def Walk_Leap (lista_variables_creadas, Directions, Orientations, num, tokens_):
    '''
    PARAMETROS:
        lista_variables_creadas: las variables creadas en las defVar y defProc
        Directions: f, r, l, b
        Orientations: n, s, w, e
        num: numeros de 0-9
    
    RETURN:
        check: bool para comprobar si esta bien escrita o no el comando de walk o leap
        existe: bool para comprobar si el comando walk o leap existe o no en el programa
        
    '''
    i = 0
    check = False
    existe = False
    tokens = tokens_[0]
    while i < len(tokens):
        if ((tokens[i] == "walk") or (tokens[i] == "leap")):
            existe = True
            if tokens[i+1] == '(' and ((tokens[i+2] in num) or (tokens[i+2] in lista_variables_creadas)) and tokens[i+3] == ')':
                
                check = True
            elif tokens[i+1] == '(' and ((tokens[i+2] in num) or (tokens[i+2] in lista_variables_creadas)) and (tokens[i+3]== ',') and ((tokens[i+4] in Directions) or (tokens[i+4] in Orientations)) and tokens[i+5] == ')':
                check = True
            else:
                check = False
        
        i += 1
    return check, existe

def Jump (lista_variables_creadas, num, tokens_):
    i = 0
    check = False
    existe = False
    tokens = tokens_[0]
    while i < len(tokens):
        if tokens[i] == "jump":
            existe = True
            if tokens[i+1] == '(' and ((tokens[i+2] in num) or (tokens[i+2] in lista_variables_creadas)) and (tokens[i+3]== ',') and ((tokens[i+4] in num) or (tokens[i+4] in lista_variables_creadas)) and tokens[i+5] == ')':
                check = True
            else:
                check = False
        i += 1
    return check, existe
def Turn (Directions, tokens_):
    i = 0
    check = False
    existe = False
    tokens = tokens_[0]
    while i < len(tokens):
        if tokens[i] == "turn":
            existe = True
            if tokens[i+1] == '(' and (tokens[i+2] in Directions) and tokens[i+3] == ')':
                check = True
            else:
                check = False
        i += 1
    return check, existe

def TurnTo (Orientations, tokens_):
    i = 0
    check = False
    existe = False
    tokens = tokens_[0]
    while i < len(tokens):
        if (tokens[i] == "turnto"):
            existe = True
            if tokens[i+1] == '(' and (tokens[i+2] in Orientations) and tokens[i+3] == ')':
                check = True
            else:
                check = False
        i += 1
    return check, existe

def Drop_Get_Grab_LetGo (lista_variables_creadas, num, tokens_):
    i = 0
    check = False
    existe = False
    tokens = tokens_[0]
    lista = ['drop', 'get','grab', 'letgo']
    while i < len(tokens):
        if (tokens[i] == lista[0]) or (tokens[i] == lista[1]) or (tokens[i] == lista[2]) or (tokens[i] == lista[3]):
            existe = True
            if tokens[i+1] == '(' and ((tokens[i+2] in num) or (tokens[i+2] in lista_variables_creadas)) and tokens[i+3] == ')':
                check = True
            else:
                check = False
        i += 1
    return check, existe

def Nop(tokens_):
    i = 0
    check = False
    existe = False
    tokens = tokens_[0]
    while i < len(tokens):
        if tokens[i] == "nop":
            existe = True
            if tokens[i+1] == '(' and tokens[i+2] == ')':
                check = True
            else:
                check = False
        i += 1
    return check, existe
print (Nop (tokens))
'''
Facing                  FUNCIONA solo
Can                     FUNCIONA solo
Not                     pendiente prueba
'''
#CONDICIONES
def Facing (Orientations, tokens_):
    i = 0
    check = False
    existe = False
    tokens = tokens_[0]
    while i < len(tokens):
        if(tokens[i] == "facing"):
            existe = True
            if tokens[i+1] == '(' and (tokens[i+2] in Orientations) and tokens[i+3] == ')':
                check = True
            else:
                check = False
        i += 1
    return check, existe

def Can (Comandos, lista_variables_creadas, Directions, Orientations, num, tokens):
    i = 0
    check = False
    #tokens = tokens_[0]
    while i < len(tokens):
        if tokens[i] == "can":
            if tokens[i+1] == '(' and (tokens[i+2] in Comandos):
                sliced_tokens = tokens[i+2:]
                nuevo_inico = tokens[i+2]
                if (nuevo_inico == 'walk') or (nuevo_inico == 'leap'):
                    check = Walk_Leap (lista_variables_creadas, Directions, Orientations, num, sliced_tokens)
                elif (nuevo_inico == 'jump'):
                    check = Jump (lista_variables_creadas, num, sliced_tokens)
                elif (nuevo_inico == 'turn'):
                    check = Turn (Directions, sliced_tokens)
                elif (nuevo_inico == 'turnto'):
                    check = TurnTo (Orientations, sliced_tokens)
                elif (nuevo_inico == 'drop') or (nuevo_inico == 'get') or (nuevo_inico == 'grab') or (nuevo_inico == 'letgo'):
                    check = Drop_Get_Grab_LetGo (lista_variables_creadas, num, sliced_tokens)
                elif (nuevo_inico == 'nop'):
                    check = Nop(sliced_tokens)
                else:
                    check = False
                    
                if nuevo_inico == ')' or check == False:
                    break
            else:
                check = False
        i += 1
    return check
# PENDIENTE / revisar como se va a comprobar el cierre de este parentesis
#print (Can(Comandos, ['x', 'putcb', 'y'], Directions, Orientations, num, tokens))

def Not (Condiciones, lista_variables_creadas, Directions, Orientations, Comandos, num, tokens):
    i = 0
    check = False
    while i < len(tokens):
        if tokens[i] == "not":
            if tokens[i+1] == '(' and (tokens[i+2] in Condiciones):
                sliced_tokens= tokens[i+2:]
                nuevo_inico = tokens[i+2]
                if nuevo_inico == 'can':
                    check = Can(Comandos, lista_variables_creadas, Directions, Orientations, num, sliced_tokens)
                elif nuevo_inico == 'facing':
                    check = Facing (Orientations, sliced_tokens)
                else:
                    check = False
        i += 1
    return check
# PENDIENTE / revisar como se va a comprobar el cierre de este parentesis

#CONTROL STRUCTURES (condicionales)
        

def blockCommands(dict_nombres_proc,lista_variables_creadas, Directions, Orientations, num, tokens_):
    i = 0 
    check = False
    existe = False
    values_dict_nombres_proc = dict_nombres_proc.values()
    keys_dict_nombres_proc = dict_nombres_proc.keys()
    print(keys_dict_nombres_proc,"what")

    tokens = tokens_[0]
    while i < len(tokens):
        if tokens[i] == "{":
            existe = True
            if isinstance(tokens[i+1],str):

                if Walk_Leap (lista_variables_creadas, Directions, Orientations, num, tokens_) == (True, True) :
                    check = True 
                elif Jump (lista_variables_creadas, num, tokens_) == (True, True) :
                    check = True 
                elif Turn (Directions, tokens_)  == (True, True) :
                    check = True 
                elif TurnTo (Orientations, tokens_) == (True, True) :
                    check = True 
                elif Drop_Get_Grab_LetGo (lista_variables_creadas, num, tokens_) == (True, True) :
                    check = True 
                elif Nop(tokens_) == (True, True) :
                    check = True
                elif tokens[i+1] in keys_dict_nombres_proc:
                    #if tokens[i+1] == dict_nombres_proc[tokens[i+1]]: 
                    check = True                  
                else:
                    check = False
        i+=1
    return check,existe

list_variables_names_tupla = check_defVar(tokens)
list_variables_names = list_variables_names_tupla[2]



dict_nombres_proc_tupla = check_defProc(tokens)
dict_nombres_proc = dict_nombres_proc_tupla[2]

# falta implementar esta funcion en el defProc

# recorro la lista de cada nombre y tiene que ser igual a la estructura que es correcta

# CAMBIAR EL IS INSTANCE POR UNA FUNCION AUXILIAR QUE RECORRA CADA CADENA DEL NOMBRE

# mirar que los metodos que se implementan abajo tienen que tener las mismas variables que la definicion de proc ¿puede entrar cualquier cosa?
