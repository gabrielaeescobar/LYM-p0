import nltk
from nltk.tokenize import word_tokenize, sent_tokenize, regexp_tokenize
import cargar 
nltk.download('punkt') 

###ARREGLAR TOKENIZADOR###

#texto_carga = cargar.openFile2(input("ingrese el filename (sin el .txt): "))
#texto = texto_carga.lower()

texto_prueba = "defvar n 0 defproc goNorth() turn(north) {jump ( 1 , 2 )} turn(right"
texto_prueba2 = " can ( nop () ) can (turnto(north))"
tokens = word_tokenize(texto_prueba2)
#print(tokens,"estos son los tokens")

#Direcciones y orientaciones para comandos y condiciones
Directions = ['front', 'right', 'left', 'back']
Orientations = ['north', 'south', 'west', 'east']
num = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
Comandos = ['walk', 'leap', 'jump', 'turn', 'turnto', 'drop', 'get','grab', 'letgo', 'nop']
Condicion = ['facing', 'can', 'not']
lo_d_maria = []

def correccionIndexOOR(element_to_check, position_to_check, Lista):
    pos = (len(Lista)-1) - position_to_check
    check = False
    # position_to_check == 0,               ultima posicion
    # position_to_check == 1,               penultima posicion, 
    # etc...
    # position_to_check == len(Lista)- 1,   primera posicion
    # position_to_check == len(Lista)- 2,   segunda posicion 
    if Lista[pos] == element_to_check:
        check = True
    else:
        check = False
    return check, pos

def CanEnComandos(pos, num_parametros: int):
    check_Can = None
    sliced_tok = []
    if num_parametros == 1:
        sliced_tok = tokens[pos+4:]
    elif num_parametros == 2:
        sliced_tok = tokens[pos+6:]
    elif num_parametros == 0:
        sliced_tok = tokens[pos+3:]
        
    if (correccionIndexOOR(tokens[pos], (len(tokens)- 1), tokens)[0] == False) and (correccionIndexOOR(tokens[pos], (len(tokens)-2), tokens)[0] == False):      
        if tokens[pos-2] == 'can':
            if tokens[pos-1] == '(':    
                if sliced_tok != [] and sliced_tok[0] == ')':
                    check_Can = True
                else:
                    check_Can = False
            else:
                check_Can = False
    
    return check_Can

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
    checkCan = None
    while i < len(tokens):
        if ((tokens[i] == "walk") or (tokens[i] == "leap")):
            if (correccionIndexOOR('walk', 2, tokens)[0]== True or correccionIndexOOR('leap', 2, tokens)[0]== True) or (correccionIndexOOR('walk', 1, tokens)[0]== True or correccionIndexOOR('leap', 1, tokens)[0]== True) or (correccionIndexOOR('walk', 0, tokens)[0]== True or correccionIndexOOR('leap', 0, tokens)[0]== True):
                return False, lo_d_maria, checkCan
                
            elif ((correccionIndexOOR('walk', 3, tokens) == (True, i))  or (correccionIndexOOR('leap', 3, tokens) == (True, i))) and tokens[i+1] == '(' and ((tokens[i+2] in num) or (tokens[i+2] in lista_variables_creadas)) and tokens[i+3] == ')':
                return True, lo_d_maria, checkCan
            
            elif tokens[i+1] == '(' and ((tokens[i+2] in num) or (tokens[i+2] in lista_variables_creadas)) and tokens[i+3] == ')':
                return True, lo_d_maria, checkCan
            
            #ya no hay posibles 'walk' o 'leap' con solo un parametro
            
            elif (correccionIndexOOR('walk', 3, tokens)[0]== True or correccionIndexOOR('leap', 3, tokens)[0]== True) or (correccionIndexOOR('walk', 4, tokens)[0]== True or correccionIndexOOR('leap', 4, tokens)[0]== True):
                return False, lo_d_maria, checkCan
                
            elif ((correccionIndexOOR('walk', 5, tokens) == (True, i))  or (correccionIndexOOR('leap', 5, tokens) == (True, i))) and tokens[i+1] == '(' and ((tokens[i+2] in num) or (tokens[i+2] in lista_variables_creadas)) and (tokens[i+3]== ',') and ((tokens[i+4] in Directions) or (tokens[i+4] in Orientations)) and tokens[i+5] == ')':
                return True, lo_d_maria, checkCan
            
            elif tokens[i+1] == '(' and ((tokens[i+2] in num) or (tokens[i+2] in lista_variables_creadas)) and (tokens[i+3]== ',') and ((tokens[i+4] in Directions) or (tokens[i+4] in Orientations)) and tokens[i+5] == ')':
                return True, lo_d_maria, checkCan
            
            else:
                return False, lo_d_maria, checkCan
                

        i+=1

def Jump (lista_variables_creadas, num, tokens):
    i = 0
    checkCan = None
    while i < len(tokens):
        if tokens[i] == "jump":
            if (correccionIndexOOR('jump', 0, tokens)[0]== True) or (correccionIndexOOR('jump', 1, tokens)[0]== True) or (correccionIndexOOR('jump', 2, tokens)[0]== True) or (correccionIndexOOR('jump', 3, tokens)[0]== True) or (correccionIndexOOR('jump', 4, tokens)[0]== True):
                return False, lo_d_maria, checkCan
                
            elif (correccionIndexOOR('jump', 5, tokens) ==(True, i)) and tokens[i+1] == '(' and ((tokens[i+2] in num) or (tokens[i+2] in lista_variables_creadas)) and (tokens[i+3]== ',') and ((tokens[i+4] in num) or (tokens[i+4] in lista_variables_creadas)) and tokens[i+5] == ')':
                return True, lo_d_maria, checkCan
            
            elif tokens[i+1] == '(' and ((tokens[i+2] in num) or (tokens[i+2] in lista_variables_creadas)) and (tokens[i+3]== ',') and ((tokens[i+4] in num) or (tokens[i+4] in lista_variables_creadas)) and tokens[i+5] == ')':
                return True, lo_d_maria, checkCan
            else:
                return False, lo_d_maria, checkCan
                
        i += 1
    

def Turn (Directions, tokens):
    i = 0
    checkCan = None
    while i < len(tokens):
        if tokens[i] == "turn":
            if  (correccionIndexOOR('turn', 0, tokens)[0]== True) or (correccionIndexOOR('turn', 1, tokens)[0]== True) or (correccionIndexOOR('turn', 2, tokens)[0]== True):
                return False, lo_d_maria, checkCan
                
            elif (correccionIndexOOR('turn', 3, tokens) == (True, i)) and tokens[i+1] == '(' and (tokens[i+2] in Directions) and tokens[i+3] == ')':
                return True, lo_d_maria, checkCan
            
            elif tokens[i+1] == '(' and (tokens[i+2] in Directions) and tokens[i+3] == ')':
                return True, lo_d_maria, checkCan
            else:
                return False, lo_d_maria, checkCan
                
        i += 1

def TurnTo (Orientations, tokens):
    i = 0
    checkCan = None
    while i < len(tokens):
        if tokens[i] == "turnto":
            if  (correccionIndexOOR('turnto', 0, tokens)[0]== True) or (correccionIndexOOR('turnto', 1, tokens)[0]== True) or (correccionIndexOOR('turnto', 2, tokens)[0]== True):
                return False, lo_d_maria, checkCan
                
            elif (correccionIndexOOR('turnto', 3, tokens) == (True, i)) and tokens[i+1] == '(' and (tokens[i+2] in Orientations) and tokens[i+3] == ')':
                checkCan =CanEnComandos(i, 1)
                if checkCan != True:
                    return False, lo_d_maria, checkCan
                    
                return True, lo_d_maria, checkCan
                
            elif tokens[i+1] == '(' and (tokens[i+2] in Orientations) and tokens[i+3] == ')':
                checkCan =CanEnComandos(i, 1)
                if checkCan != True:
                    return False, lo_d_maria, checkCan
                    
                return True, lo_d_maria, checkCan
                
            else:
                return False, lo_d_maria, checkCan
                break
        i += 1

def Drop_Get_Grab_LetGo (lista_variables_creadas, num, tokens):
    i = 0
    checkCan = None
    while i < len(tokens):
        if (tokens[i] == "drop") or (tokens[i] == "get") or (tokens[i] == "grab") or (tokens[i] == "letgo"):
            if  (correccionIndexOOR(tokens[i], 0, tokens)[0]== True) or (correccionIndexOOR(tokens[i], 1, tokens)[0]== True) or (correccionIndexOOR(tokens[i], 2, tokens)[0]== True):
                return False, lo_d_maria, checkCan
                
            elif (correccionIndexOOR(tokens[i], 3, tokens) == (True, i)) and tokens[i+1] == '(' and ((tokens[i+2] in num) or (tokens[i+2] in lista_variables_creadas)) and tokens[i+3] == ')':
                checkCan =CanEnComandos(i, 1) 
                if checkCan != True:
                    return False, lo_d_maria, checkCan
                    
                return True, lo_d_maria, checkCan
                
            elif tokens[i+1] == '(' and ((tokens[i+2] in num) or (tokens[i+2] in lista_variables_creadas)) and tokens[i+3] == ')':
                checkCan =CanEnComandos(i, 1) 
                if checkCan != True:
                    return False, lo_d_maria, checkCan
                return True, lo_d_maria, checkCan
                
            else:
                return False
                
        i+= 1
        
def Nop(tokens):
    i = 0
    checkCan = None
    while i < len(tokens):
        if tokens[i] == "nop":
            if correccionIndexOOR('nop', 0, tokens)[0] == True or correccionIndexOOR('nop', 1, tokens)[0]== True:
                return False, lo_d_maria, checkCan
                
            elif correccionIndexOOR('nop', 2, tokens) == (True, i) and tokens[i+1] == '(' and tokens[i+2] == ')':
                checkCan =CanEnComandos(i, 0) 
                if checkCan != True:
                    return False, lo_d_maria, checkCan
                    
                return True, lo_d_maria, checkCan
            
            elif tokens[i+1] == '(' and tokens[i+2] == ')':
                checkCan =CanEnComandos(i, 0) 
                if checkCan != True:
                    return False, lo_d_maria, checkCan
                    
                return True, lo_d_maria, checkCan
            else:
                return False, lo_d_maria, checkCan
        i += 1

#CONDICIONES
def Facing (Orientations, tokens):
    i = 0
    check = False
    while i < len(tokens):
        if(tokens[i] == "facing"):
            if (correccionIndexOOR('facing', 0, tokens)[0]== True) or (correccionIndexOOR('facing', 1, tokens)[0]== True) or (correccionIndexOOR('facing', 2, tokens)[0]== True):
                check = False
                break
            elif tokens[i+1] == '(' and (tokens[i+2] in Orientations) and tokens[i+3] == ')':
                check = True
            else:
                check = False
        i += 1
    return check
'''def Can (Comandos, lista_variables_creadas, Directions, Orientations, num, tokens):
    if 'can' in tokens:
   '''     

def Can (Comandos, lista_variables_creadas, Directions, Orientations, num, tokens):
    i = 0
    check = False
    while i < len(tokens):
        
        if tokens[i] == "can":
            if (correccionIndexOOR('can', 0, tokens)[0] == True) or (correccionIndexOOR('can', 1, tokens)[0]== True) or (correccionIndexOOR('can', 2, tokens)[0] == True):
                check == False
                break
            elif tokens[i+1] == '(':
                if (tokens[i+2] in Comandos):
                    sliced_tokens = (tokens[i:])
                    nuevo_inico = tokens[i+2]
                    if (nuevo_inico == 'walk') or (nuevo_inico == 'leap'):
                        check = Walk_Leap (lista_variables_creadas, Directions, Orientations, num, sliced_tokens)
                    elif (nuevo_inico == 'jump'):
                        check = Jump (lista_variables_creadas, num, sliced_tokens)
                    elif (nuevo_inico == 'turn'):
                        check = Turn (Directions, sliced_tokens)
                    elif (nuevo_inico == 'turnto'):
                        check, maria, checkCan = TurnTo (Orientations, sliced_tokens)
                        if checkCan!= True or check != True:
                            check = False
                            break
                    elif (nuevo_inico == 'drop') or (nuevo_inico == 'get') or (nuevo_inico == 'grab') or (nuevo_inico == 'letgo'):
                        check, maria, checkCan = Drop_Get_Grab_LetGo (lista_variables_creadas, num, sliced_tokens)
                        if checkCan != True or check != True:
                            check = False
                            break
                    elif (nuevo_inico == 'nop'):
                        check, maria, checkCan = Nop(sliced_tokens)
                        if checkCan != True or check != True:
                            check = False
                            break
                    else:
                        check = False
            else:
                check = False
                break
        i+=1
    return check
print (Can(Comandos, [], Directions, Orientations, num, tokens))
################################################################            parentesis de cierre queda pendiente
def Not (Condiciones, lista_variables_creadas, Directions, Orientations, Comandos, num, tokens):
    i = 0
    check = False
    while i < len(tokens):
        if tokens[i] == "not":
            if (correccionIndexOOR('not', 0, tokens)[0]== True) or (correccionIndexOOR('not', 1, tokens)[0]== True) or (correccionIndexOOR('not', 2, tokens)[0]== True):
                check = False
                break
            
            elif tokens[i+1] == ':' and (tokens[i+2] in Condiciones):
                sliced_tokens=(tokens[i+2:])
                nuevo_inico = tokens[i+2]
                if nuevo_inico == 'can':
                    check = Can(Comandos, lista_variables_creadas, Directions, Orientations, num, sliced_tokens)[0]
                elif nuevo_inico == 'facing':
                    check = Facing (Orientations, sliced_tokens)[0]
                else:
                    check = False
        i += 1
    return check

#CONTROL STRUCTURES (condicionales)
#def IfYElse (dict_nombres_proc,lista_variables_creadas, Directions, Orientations, num, tokens):


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
    #print(keys_dict_nombres_proc,"what")
    #print(values_dict_nombres_proc,"que")
    while i < len(tokens):
        if tokens[i] == "{":  ## debe hacerse con slize [i+1]
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
            
            if i not in Comandos:
                
            #if tokens[i+2] in keys_dict_nombres_proc:
                #if tokens[i+1] == dict_nombres_proc[tokens[i+1]]: 
                check = True 

            if (tokens[i+1] != "}" and tokens[i+1] not in ['defvar', 'n', '0', 'defproc', 'goNorth', '(', ')', '{', 'jump', '(', '1', ',', '2', ')']) or (check == False) :
                check = False
            else:
                break
        
        i+=1
        #print(tokens[i-1])
    return check
###COMAAAAAA###
#arreglar { que si no entra siempre va a ser true 

list_variables_names_tupla = check_defVar(tokens)
list_variables_names = list_variables_names_tupla[1]
#print(list_variables_names,"lol")
dict_nombres_proc_tupla = check_defProc(tokens)
dict_nombres_proc = dict_nombres_proc_tupla[1]
#print(dict_nombres_proc,"loool")
#print(blockCommands(dict_nombres_proc,list_variables_names,Directions,Orientations,num,tokens ), "ojala funcione")


### falta implementar esta funcion en el defProc###

#### recorro la lista de cada nombre y tiene que ser igual a la estructura que es correcta, mirar cantidad parametros ###

### CAMBIAR EL IS INSTANCE POR UNA FUNCION AUXILIAR QUE RECORRA CADA CADENA DEL NOMBRE ###
