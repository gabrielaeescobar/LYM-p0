import nltk
nltk.download('punkt') 

from nltk.tokenize import word_tokenize, sent_tokenize
import cargar 

texto_carga = cargar.openFile2(input("ingrese el filename (sin el .txt): "))
texto = texto_carga.lower()

#texto_prueba = " defVar nom 0 defVar x 0 defVar y 0 defVar one 0 defProc putCB (c, b) { drop(c); letGo (b) ; walk(n) }"
#texto_prueba2 = "defProc goNorth() { while can ( walk (1 , north )) { walk (1 , north ) }; putCB (1 ,1) } defProc hola (cara,de) "
todo = sent_tokenize(texto)
tokens = [word_tokenize(cadacosa) for cadacosa in todo]
#print("Tokens:", tokens)

#Comandos por cantidad de parametros

comando_vacio = ["nop"]
comando_solo_1 = ["turn","turnto","drop","get","grab","letGo", "facing","can","not"]
comando_1_o_mas =[] 

#Direcciones y orientaciones para comandos
Directions = ['front', 'right', 'left', 'back']
Orientations = ['north', 'south', 'west', 'east']
num = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']



# Funcion para defVar 

# MIRAR SI LOS NOMBRES SE VUELVEN A USAR
def check_defVar(tokens_):
    i = 0
    check = False
    hubo = "no_hubo"
    tokens = tokens_[0]
    while i < len(tokens):
        token = tokens[i]
        if token == "defvar":
            hubo = "si_hubo"
            nombre = tokens[i+1]
            valor = tokens[i+2]
            
            if isinstance(nombre, str) and valor.isdigit():
                check = True
                i += 2  # Avanzar el índice para saltar al próximo token

        i += 1
    
    return check,hubo



    #Funcion para defProc
def check_defProc(tokens_):
    i= 0
    tokens = tokens_[0]
    lista_nombres = []
    check = False
    hubo = "no_hubo"
    while i<len(tokens):
        token = tokens[i]
        if token == "defproc":
            hubo = "si_hubo"
            nombre = tokens[i+1]
            lista_nombres.append(nombre)
            parentesis_izquierdo = tokens[i+2]
            if isinstance(nombre,str) and parentesis_izquierdo == "(":
                continuacion = tokens[i+3]
                if continuacion == ")": # primer caso 0 parametros
                    check = True
                elif isinstance(continuacion,str) and tokens[i+4] == ")": # segundo caso 1 parametro
                    check = True
                elif isinstance(continuacion,str) and tokens[i+4] == "," and isinstance(tokens[i+5],str) and tokens[i+6] == ")": # tercer caso 2 parametros
                    check = True
                else:
                    check = False

        i += 1
    return check,hubo,lista_nombres    

#def block_commands(tokens_)-> bool:
     
    """                    lista_nueva_tokens = []
                    check_corchetes = dos_corchetes()
                    if token"""
                
        
print(check_defProc(tokens), "defproc")


#COOOOOMAAANNNDDOOOOSSSSS

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
        if tokens[i] == "turnto":
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
    while i < len(tokens):
        if (tokens[i] == "drop") or (tokens[i] == "get") or (tokens[i] == "grab") or (tokens[i] == "letgo"):
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
