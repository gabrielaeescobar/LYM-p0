import nltk
nltk.download('punkt') 

from nltk.tokenize import word_tokenize, sent_tokenize
import cargar 


texto = cargar.openFile2(input("ingrese el filename (sin el .txt): "))

texto_prueba = "defVar nom 0 defVar x 0 defVar y 0 defVar one 0 defProc putCB (c, b) { drop(c); letGo (b) ; walk(n) walk(p, north) }"
todo = sent_tokenize(texto)
tokens = [word_tokenize(cadacosa) for cadacosa in todo]
#print("Tokens:", tokens)

comandoSolo1Parametro = ["turn","turnto","drop","get","grab","letGo"]
# funcion para las funciones jump walk 

# Funcion para defVar
def check_defVar(tokens_):
    i = 0
    check = False
    tokens = tokens_[0]
    while i < len(tokens):
        token = tokens[i]
        if token == "defVar":
            nombre = tokens[i+1]
            valor = tokens[i+2]
            
            if isinstance(nombre, str) and valor.isdigit():
                check = True
                i += 2  # Avanzar el índice para saltar al próximo token

        i += 1
    
    return check

#print(check_defVar(tokens), "defvar")

    #Funcion para defProc
"""    def defProc(tokens):
        i= 0
        check = False
        while i<=len(tokens):
         token = tokens[i]
         if token == "defProc":
             List_defProc = ["defProc"]
             nombre = tokens[i+1]
             if isinstance(nombre,str):
                 List_defProc.append(nombre)
                 if tokens[i+2] == parent_izq:
                     List_defProc.append(parent_izq)
                 parametro1 = tokens[i+3]
                 if isinstance(parametro1)
             """
        




"""""def check_turnto(comando):
    if len(tokens) == 4 and tokens[0] == 'turnto' and tokens[1] == '(' and tokens[3] == ')' and tokens[2] in ['north', 'south', 'east', 'west']:
        return True
    return False """""

""""def check_comandos_1_parametro(lstComandos):
    while comando in lstComandos:
        if comando """




# funcion para def var
# funcion para def proc


"""if oalbea == DROP:
palabras[]"""



#Direcciones y orientaciones para comandos
Directions = ['front', 'right', 'left', 'back']
Orientations = ['north', 'south', 'west', 'east']
num = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

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
        if (tokens[i] == "drop") or (tokens[i] == "get") or (tokens[i] == "grab") or (tokens[i] == "letGo"):
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
