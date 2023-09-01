import nltk
from nltk.tokenize import word_tokenize, sent_tokenize, regexp_tokenize
import cargar 
nltk.download('punkt') 

###ARREGLAR TOKENIZADOR###

#texto_carga = cargar.openFile2(input("ingrese el filename (sin el .txt): "))
#texto = texto_carga.lower()

texto_prueba = "defvar n 0 defproc goNorth() {jump ( 1 , 2 )} "
#texto_prueba2 = "defProc goNorth() { while can ( walk (1 , north )) { walk (1 , north ) }; putCB (1 ,1) } defProc hola (cara,de) "

tokens = word_tokenize(texto_prueba)
print(tokens,"estos son los tokens")

#Direcciones y orientaciones para comandos
Directions = ['front', 'right', 'left', 'back']
Orientations = ['north', 'south', 'west', 'east']
num = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
Comandos = ['walk', 'leap', 'jump', 'turn', 'turnto', 'drop', 'get','grab', 'letgo', 'nop']
Condicion = ['facing', 'can', 'not']

# Funcion para defVar 
### HACER LO DE QUE LOS NOMBRES SE VUELVEN A USAR ###
def check_defVar(tokens):
    i = 0
    check = False
    lista_nombres = []
    while i < len(tokens):
        token = tokens[i]
        if token == "defvar":
            nombre = tokens[i+1]
            lista_nombres.append(nombre)
            valor = tokens[i+2]
            
            if isinstance(nombre, str) and valor.isdigit():
                check = True
                i += 2  # Avanzar el índice para saltar al próximo token

        i += 1
    
    return check,lista_nombres

#Funcion para defProc
def check_defProc(tokens):
    i= 0
    tokens = tokens
    dict_nombres = {}
    check = False
    while i<len(tokens):
        token = tokens[i]
        if token == "defproc":
            nombre = tokens[i+1]
            dict_nombres[nombre] = ""
            parentesis_izquierdo = tokens[i+2]
            if isinstance(nombre,str) and parentesis_izquierdo == "(":
                continuacion = tokens[i+3]
                if continuacion == ")": # primer caso 0 parametros
                    check = True
                    dict_nombres[nombre] = [tokens[i+2],continuacion]
                    longitud_l = len(dict_nombres[nombre])
                    dict_nombres[nombre] = longitud_l
                elif isinstance(continuacion,str) and tokens[i+4] == ")": # segundo caso 1 parametro
                    check = True
                    dict_nombres[nombre] = len[tokens[i+2],continuacion,tokens[i+4]]
                    longitud_l = len(dict_nombres[nombre])
                    dict_nombres[nombre] = longitud_l
                elif isinstance(continuacion,str) and tokens[i+4] == "," and isinstance(tokens[i+5],str) and tokens[i+6] == ")": # tercer caso 2 parametros
                    check = True
                    dict_nombres[nombre] = len[tokens[i+2],continuacion,tokens[i+4],tokens[i+5],tokens[i+5]]
                    longitud_l = len(dict_nombres[nombre])
                    dict_nombres[nombre] = longitud_l
                else:
                    check = False

        i += 1
    return check,dict_nombres  


#COMANDOS
def Walk_Leap (lista_variables_creadas, Directions, Orientations, num, tokens):
    '''
    PARAMETROS:
        lista_variables_creadas: las variables creadas en las defVar y defProc
        Directions: f, r, l, b
        Orientations: n, s, w, e
        num: numeros de 0-9
    
    RETURN:
        check: bool para comprobar si esta bien escrita o no el comando de walk o leap
        
    '''
    i = 0
    check = False
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
    return check

def Jump (lista_variables_creadas, num, tokens):
    i = 0
    check = False
    while i < len(tokens):
        if tokens[i] == "jump":
            if tokens[i+1] == '(' and ((tokens[i+2] in num) or (tokens[i+2] in lista_variables_creadas)) and (tokens[i+3]== ',') and ((tokens[i+4] in num) or (tokens[i+4] in lista_variables_creadas)) and tokens[i+5] == ')':
                check = True
            else:
                check = False
        i += 1
    return check

def Turn (Directions, tokens):
    i = 0
    check = False
    while i < len(tokens):
        if tokens[i] == "turn":
            if tokens[i+1] == '(' and (tokens[i+2] in Directions) and tokens[i+3] == ')':
                check = True
            else:
                check = False
        i += 1
    return check

def TurnTo (Orientations, tokens):
    i = 0
    check = False
    while i < len(tokens):
        if tokens[i] == "turnto":
            if tokens[i+1] == '(' and (tokens[i+2] in Orientations) and tokens[i+3] == ')':
                check = True
            else:
                check = False
        i += 1
    return check

def Drop_Get_Grab_LetGo (lista_variables_creadas, num, tokens):
    i = 0
    check = False
    while i < len(tokens):
        if (tokens[i] == "drop") or (tokens[i] == "get") or (tokens[i] == "grab") or (tokens[i] == "letgo"):
            if tokens[i+1] == '(' and ((tokens[i+2] in num) or (tokens[i+2] in lista_variables_creadas)) and tokens[i+3] == ')':
                check = True
            else:
                check = False
        i += 1
    return check

def Nop(tokens):
    i = 0
    check = False
    while i < len(tokens):
        if tokens[i] == "nop":
            if tokens[i+1] == '(' and tokens[i+2] == ')':
                check = True
            else:
                check = False
        i += 1
    return check

def check_funciones_defProc(dict_nombres_proc, tokens):
    i = 0
    keys_dict_nombres_proc = dict_nombres_proc.keys()
    values_dict_nombres_proc = dict_nombres_proc.values()
    #estructura que lleva 1 parametro
    while i < len(tokens):
        for key in keys_dict_nombres_proc:
            if tokens[i] == key and dict_nombres_proc[key] == 2:
                tokens


    #estructura que lleva 2 parametros
    #estructura que lleva 3 parametros   
    return 0  

def blockCommands(dict_nombres_proc,lista_variables_creadas, Directions, Orientations, num, tokens):
    i = 0 
    check = True
    values_dict_nombres_proc = dict_nombres_proc.values()
    keys_dict_nombres_proc = dict_nombres_proc.keys()
    print(keys_dict_nombres_proc,"what")
    print(values_dict_nombres_proc,"que")
    while i < len(tokens):
        if tokens[i] == "{":  ## debe hacerse con slize [i+1]
            print (tokens[i+1:])
            if tokens[i+1] == "walk" or tokens[i+1] == "leap":
                check = Walk_Leap (lista_variables_creadas, Directions, Orientations, num, tokens[i:])

            elif tokens[i+1] == "jump":
                check = Jump (lista_variables_creadas, num,  tokens[i+1:])

            elif tokens[i+1] == "turn":
                check = Turn (Directions,  tokens[i:]) 

            elif tokens[i+1] == "turnto" :
                check = TurnTo (Orientations,  tokens[i:]) 

            elif  tokens[i+1] == "drop" or tokens[i+1] == "get" or tokens[i+1] == "grab" or tokens[i+1] == "letgo" :
                check = Drop_Get_Grab_LetGo (lista_variables_creadas, num,  tokens[i:]) 

            elif tokens[i+1] == "nop" :
                check = Nop( tokens[i:])
            #if tokens[i+2] in keys_dict_nombres_proc:
                #if tokens[i+1] == dict_nombres_proc[tokens[i+1]]: 
                check = True 

            if (tokens[i+1] != "}" and tokens[i+1] not in ['defvar', 'n', '0', 'defproc', 'goNorth', '(', ')', '{', 'jump', '(', '1', ',', '2', ')']) or (check == False) :
                check = False
            else:
                break
        
        i+=1
        print(tokens[i-1])
    return check
###COMAAAAAA###
#arreglar { que si no entra siempre va a ser true 

list_variables_names_tupla = check_defVar(tokens)
list_variables_names = list_variables_names_tupla[1]
#print(list_variables_names,"lol")
dict_nombres_proc_tupla = check_defProc(tokens)
dict_nombres_proc = dict_nombres_proc_tupla[1]
#print(dict_nombres_proc,"loool")
print(blockCommands(dict_nombres_proc,list_variables_names,Directions,Orientations,num,tokens ), "ojala funcione")


### falta implementar esta funcion en el defProc###

#### recorro la lista de cada nombre y tiene que ser igual a la estructura que es correcta, mirar cantidad parametros ###

### CAMBIAR EL IS INSTANCE POR UNA FUNCION AUXILIAR QUE RECORRA CADA CADENA DEL NOMBRE ###
