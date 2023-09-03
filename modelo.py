import nltk
from nltk.tokenize import word_tokenize, sent_tokenize, regexp_tokenize
import cargar 
nltk.download('punkt') 

#texto_carga = cargar.openFile2(input("ingrese el filename (sin el .txt): "))
#texto = texto_carga.lower()

texto_prueba = "repeat 3 times {get(1); leap(1,left)} else { get(1); leap(1,left)} wak(1,north)" # solo mira 1 bracket
#texto_prueba2 = "defProc goNorth() { while can ( walk (1 , north )) { walk (1 , north ) }; putCB (1 ,1) } defProc hola (cara,de) "

pattern = r'\w+|[.,(){}\[\]]|\S+'
#pattern = r'\w+|,'
tokens = regexp_tokenize(texto_prueba, pattern)
print(tokens,"estos son los tokens")

#Direcciones y orientaciones para comandos
Directions = ['front', 'right', 'left', 'back']
Orientations = ['north', 'south', 'west', 'east']
num = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
Comandos = ['walk', 'leap', 'jump', 'turn', 'turnto', 'drop', 'get','grab', 'letgo', 'nop']
Condiciones = ['facing', 'can', 'not']
alfabeto = 'abcdefghijklmnopqrstuvwxyz'

#Funcion para rectificar que es un nombre valido
def nombre_correcto(nombre):
    check = True
    for caracter in nombre:
        if caracter not in alfabeto:
            check = False
            break
    return check

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
            
            if nombre_correcto(nombre) and valor.isdigit():
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
            if nombre_correcto(nombre) and parentesis_izquierdo == "(":
                continuacion = tokens[i+3]
                if continuacion == ")": # primer caso 0 parametros
                    check = True
                    dict_nombres[nombre] = 2
                elif nombre_correcto(continuacion) and tokens[i+4] == ")": # segundo caso 1 parametro
                    check = True
                    dict_nombres[nombre] = 3
                elif nombre_correcto(continuacion) and tokens[i+4] == "," and nombre_correcto(tokens[i+5]) and tokens[i+6] == ")": # tercer caso 2 parametros
                    check = True
                    dict_nombres[nombre] = 5
                else:
                    check = False

        i += 1
    return check,dict_nombres  

# Variables y funciones creadas 
list_variables_names_tupla = check_defVar(tokens)
list_variables_names = list_variables_names_tupla[1]
dict_nombres_proc_tupla = check_defProc(tokens)
dict_nombres_proc = dict_nombres_proc_tupla[1]

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
    while i < len(tokens):
        if ((tokens[i] == "walk") or (tokens[i] == "leap")):
            if (correccionIndexOOR('walk', 2, tokens)[0]== True or correccionIndexOOR('leap', 2, tokens)[0]== True) or (correccionIndexOOR('walk', 1, tokens)[0]== True or correccionIndexOOR('leap', 1, tokens)[0]== True) or (correccionIndexOOR('walk', 0, tokens)[0]== True or correccionIndexOOR('leap', 0, tokens)[0]== True):
                return False, tokens[i:]
                
            elif ((correccionIndexOOR('walk', 3, tokens) == (True, i))  or (correccionIndexOOR('leap', 3, tokens) == (True, i))) and tokens[i+1] == '(' and ((tokens[i+2] in num) or (tokens[i+2] in lista_variables_creadas)) and tokens[i+3] == ')':
                return True, tokens[i+4:]
            
            elif tokens[i+1] == '(' and ((tokens[i+2] in num) or (tokens[i+2] in lista_variables_creadas)) and tokens[i+3] == ')':
                return True, tokens[i+4:]
            
            #ya no hay posibles 'walk' o 'leap' con solo un parametro
            
            elif (correccionIndexOOR('walk', 3, tokens)[0]== True or correccionIndexOOR('leap', 3, tokens)[0]== True) or (correccionIndexOOR('walk', 4, tokens)[0]== True or correccionIndexOOR('leap', 4, tokens)[0]== True):
                return False, tokens[i:]
                
            elif ((correccionIndexOOR('walk', 5, tokens) == (True, i))  or (correccionIndexOOR('leap', 5, tokens) == (True, i))) and tokens[i+1] == '(' and ((tokens[i+2] in num) or (tokens[i+2] in lista_variables_creadas)) and (tokens[i+3]== ',') and ((tokens[i+4] in Directions) or (tokens[i+4] in Orientations)) and tokens[i+5] == ')':
                return True, tokens[i+6:]
            
            elif tokens[i+1] == '(' and ((tokens[i+2] in num) or (tokens[i+2] in lista_variables_creadas)) and (tokens[i+3]== ',') and ((tokens[i+4] in Directions) or (tokens[i+4] in Orientations)) and tokens[i+5] == ')':
                return True, tokens[i+6:]
            
            else:
                return False, tokens[i:]
                

        i+=1
def Jump (lista_variables_creadas, num, tokens):
    i = 0
    while i < len(tokens):
        if tokens[i] == "jump":
            if (correccionIndexOOR('jump', 0, tokens)[0]== True) or (correccionIndexOOR('jump', 1, tokens)[0]== True) or (correccionIndexOOR('jump', 2, tokens)[0]== True) or (correccionIndexOOR('jump', 3, tokens)[0]== True) or (correccionIndexOOR('jump', 4, tokens)[0]== True):
                return False, tokens[i:]
                
            elif (correccionIndexOOR('jump', 5, tokens) ==(True, i)) and tokens[i+1] == '(' and ((tokens[i+2] in num) or (tokens[i+2] in lista_variables_creadas)) and (tokens[i+3]== ',') and ((tokens[i+4] in num) or (tokens[i+4] in lista_variables_creadas)) and tokens[i+5] == ')':
                return True, tokens[i+6:]
            
            elif tokens[i+1] == '(' and ((tokens[i+2] in num) or (tokens[i+2] in lista_variables_creadas)) and (tokens[i+3]== ',') and ((tokens[i+4] in num) or (tokens[i+4] in lista_variables_creadas)) and tokens[i+5] == ')':
                return True, tokens[i+6:]
            else:
                return False, tokens[i:]
                
        i += 1
def Turn (Directions, tokens):
    i = 0
    while i < len(tokens):
        if tokens[i] == "turn":
            if  (correccionIndexOOR('turn', 0, tokens)[0]== True) or (correccionIndexOOR('turn', 1, tokens)[0]== True) or (correccionIndexOOR('turn', 2, tokens)[0]== True):
                return False, tokens[i:]
                
            elif (correccionIndexOOR('turn', 3, tokens) == (True, i)) and tokens[i+1] == '(' and (tokens[i+2] in Directions) and tokens[i+3] == ')':
                return True, tokens[i+4:]
            
            elif tokens[i+1] == '(' and (tokens[i+2] in Directions) and tokens[i+3] == ')':
                return True, tokens[i+4:]
            else:
                return False, tokens[i:]
                
        i += 1
def TurnTo (Orientations, tokens):
    i = 0
    while i < len(tokens):
        if tokens[i] == "turnto":
            if  (correccionIndexOOR('turnto', 0, tokens)[0]== True) or (correccionIndexOOR('turnto', 1, tokens)[0]== True) or (correccionIndexOOR('turnto', 2, tokens)[0]== True):
                return False, tokens[i:]
                
            elif (correccionIndexOOR('turnto', 3, tokens) == (True, i)) and tokens[i+1] == '(' and (tokens[i+2] in Orientations) and tokens[i+3] == ')':
                return True, tokens[i+4:]
                
            elif tokens[i+1] == '(' and (tokens[i+2] in Orientations) and tokens[i+3] == ')':
                return True, tokens[i+4:]
                
            else:
                return False, tokens[i:]
                
        i += 1
def Drop_Get_Grab_LetGo (lista_variables_creadas, num, tokens):
    i = 0
    while i < len(tokens):
        if (tokens[i] == "drop") or (tokens[i] == "get") or (tokens[i] == "grab") or (tokens[i] == "letgo"):
            if  (correccionIndexOOR(tokens[i], 0, tokens)[0]== True) or (correccionIndexOOR(tokens[i], 1, tokens)[0]== True) or (correccionIndexOOR(tokens[i], 2, tokens)[0]== True):
                return False, tokens[i:]
                
            elif (correccionIndexOOR(tokens[i], 3, tokens) == (True, i)) and tokens[i+1] == '(' and ((tokens[i+2] in num) or (tokens[i+2] in lista_variables_creadas)) and tokens[i+3] == ')':
                return True, tokens[i+4:]
                
            elif tokens[i+1] == '(' and ((tokens[i+2] in num) or (tokens[i+2] in lista_variables_creadas)) and tokens[i+3] == ')':
                return True, tokens[i+4:]
                
            else:
                return False, tokens[i:]
                
        i+= 1
def Nop(tokens):
    i = 0
    while i < len(tokens):
        if tokens[i] == "nop":
            if correccionIndexOOR('nop', 0, tokens)[0] == True or correccionIndexOOR('nop', 1, tokens)[0]== True:
                return False, tokens[i:]
                
            elif correccionIndexOOR('nop', 2, tokens) == (True, i) and tokens[i+1] == '(' and tokens[i+2] == ')':    
                return True, tokens[i+3:]
            
            elif tokens[i+1] == '(' and tokens[i+2] == ')':
                return True, tokens[i+3:]
            else:
                return False, tokens[i:]
        i += 1

#CONDICIONES
def Facing (Orientations, tokens):
    i = 0
    while i < len(tokens):
        if(tokens[i] == "facing"):
            if (correccionIndexOOR('facing', 0, tokens)[0]== True) or (correccionIndexOOR('facing', 1, tokens)[0]== True) or (correccionIndexOOR('facing', 2, tokens)[0]== True):
                return False, tokens[i:]
            elif tokens[i+1] == '(' and (tokens[i+2] in Orientations) and tokens[i+3] == ')':
                return True, tokens[i+4:]
            else:
                return False, []
        i += 1
def Can (Comandos, lista_variables_creadas, Directions, Orientations, num, tokens):
    i = 0
    while i < len(tokens):
        if tokens[i] == "can":
            j = i+1
            if (correccionIndexOOR('can', 0, tokens)[0] == True) or (correccionIndexOOR('can', 1, tokens)[0]== True) or (correccionIndexOOR('can', 2, tokens)[0] == True):
                return False, []
            while j < len(tokens[i+1:]):
                if tokens[j] =='(':
                    if (tokens[j+1] in Comandos):
                        sliced_tokens = (tokens[j:])
                        nuevo_inico = tokens[j+1]
                        if (nuevo_inico == 'walk') or (nuevo_inico == 'leap'):
                            check=Walk_Leap (lista_variables_creadas, Directions, Orientations, num, sliced_tokens)[0]
                            sliced_sliced = Walk_Leap (lista_variables_creadas, Directions, Orientations, num, sliced_tokens)[1]
                        elif (nuevo_inico == 'jump'):
                            check= Jump (lista_variables_creadas, num, sliced_tokens)[0]
                            sliced_sliced = Jump (lista_variables_creadas, num, sliced_tokens)[1]
                        elif (nuevo_inico == 'turn'):
                            check= Turn (Directions, sliced_tokens)[0]
                            sliced_sliced = Turn (Directions, sliced_tokens)[1]
                        elif (nuevo_inico == 'turnto'):
                            check = TurnTo (Orientations, sliced_tokens)[0]
                            sliced_sliced = TurnTo (Orientations, sliced_tokens)[1]
                        elif (nuevo_inico == 'drop') or (nuevo_inico == 'get') or (nuevo_inico == 'grab') or (nuevo_inico == 'letgo'):
                            check = Drop_Get_Grab_LetGo (lista_variables_creadas, num, sliced_tokens)[0]
                            sliced_sliced = Drop_Get_Grab_LetGo (lista_variables_creadas, num, sliced_tokens)[1]
                        elif (nuevo_inico == 'nop'):
                            check= Nop(sliced_tokens)[0]
                            sliced_sliced = Nop(sliced_tokens)[1]
                        else:
                            check = False, []
                        if check != True or sliced_sliced[0] != ')':
                            return False, []
                        else:
                            return True, sliced_sliced[1:]
                else:
                    return False, []
                j+= 1
        i+=1
def Not (Condiciones, lista_variables_creadas, Directions, Orientations, Comandos, num, tokens):
    i = 0
    while i < len(tokens):
        if tokens[i] == "not":
            if (correccionIndexOOR('not', 0, tokens)[0]== True) or (correccionIndexOOR('not', 1, tokens)[0]== True) or (correccionIndexOOR('not', 2, tokens)[0]== True):
                return False, []
            
            elif tokens[i+1] == ':' and (tokens[i+2] in Condiciones):
                sliced_tokens=(tokens[i+2:])
                nuevo_inico = tokens[i+2]
                if nuevo_inico == 'can':
                    return Can(Comandos, lista_variables_creadas, Directions, Orientations, num, sliced_tokens)
                elif nuevo_inico == 'facing':
                    return Facing (Orientations, sliced_tokens)
                else:
                    return False, []
        i += 1
        
#Funcion para verificar si las funciones de defProc se vuelven a implementar bien
def check_funciones_defProc(dict_nombres_proc, tokens):
    i = 0
    check = True
    keys_dict_nombres_proc = dict_nombres_proc.keys()

    while i < len(tokens):
        for key in keys_dict_nombres_proc:
            if tokens[i] == key and dict_nombres_proc[key] == 2:
                if not (tokens[i+1] == '(' and tokens[i+2] == ')'): #estructura que lleva 1 parametro
                    check = False

            elif tokens[i] == key and dict_nombres_proc[key] == 3:
                if not (tokens[i+1] == '(' and ((tokens[i+2] in num) or (tokens[i+2] in lista_variables_creadas)) and tokens[i+3] == ')'):     #estructura que lleva 2 parametros
                    check = False

            elif tokens[i] == key and dict_nombres_proc[key] == 5:
                if not(tokens[i+1] == '(' and ((tokens[i+2] in num) or (tokens[i+2] in lista_variables_creadas)) and (tokens[i+3]== ',') and ((tokens[i+4] in Directions) or (tokens[i+4] in Orientations)) and tokens[i+5] == ')'):   #estructura que lleva 3 parametros 
                    check = False

        i += 1  
    return check, tokens[i:]
dict_nombres_proc = (check_defProc(tokens))[1]
lista_variables_creadas = (check_defVar(tokens))[1]

#Funcion para cada vez que aparezcan corchetes/ bloques de comandos
def blockCommands(dict_nombres_proc,lista_variables_creadas, Directions, Orientations, num, tokens):
    i = 0 
    check = True
    se_cerro_corchete = False
    se_abrio_corchete = False
    keys_dict_nombres_proc = dict_nombres_proc.keys()

    if tokens[i] == "{":  ## debe hacerse con slize [i+1]
        se_abrio_corchete = True
        i+=1
        while i < len(tokens) :
            print ("tOKEN IS ", tokens[i])
            if tokens[i] == "walk" or tokens[i] == "leap":
                check, tokens= Walk_Leap (lista_variables_creadas, Directions, Orientations, num, tokens[i:])
                i=0  

            elif tokens[i] == "jump":
                check, tokens= Jump (lista_variables_creadas, num,  tokens[i:])
                i=0
            elif tokens[i] == "turn":
                check, tokens= Turn (Directions,  tokens[i:]) # Recibimos el check y el nuevo slice de tokens
                i=0
            elif tokens[i] == "turnto" :
                check, tokens= TurnTo (Orientations,  tokens[i:]) 
                i=0
            elif  tokens[i] == "drop" or tokens[i] == "get" or tokens[i] == "grab" or tokens[i] == "letgo" :
                check , tokens = Drop_Get_Grab_LetGo (lista_variables_creadas, num,  tokens[i:]) 
                i=0

            elif tokens[i] == "nop" :
                check , tokens= Nop( tokens[i:])
                i=0
            elif tokens[i] in keys_dict_nombres_proc: 
                check, tokens= check_funciones_defProc(dict_nombres_proc, tokens, lista_variables_creadas) 
                i=0

            if (check == False)  or (tokens[i] == "}") :
                print(f'breakie con check igual a {check} y mis tokens a actuales son {tokens}')
                break
                
            elif ( tokens[i] != ";"):
                check = False
                print(tokens[i], '  because of this')
                break

            i+=1

        if tokens[i] == "}":
            tokens = tokens[i+1:]
            se_cerro_corchete = True
                
       
    
    check = check and se_cerro_corchete and se_abrio_corchete
    return check, tokens

### al bloque de comandos le falta llamar condicionales y eso ###
###arreglar { } que lo toma como true y tiene que haber algo adentro ### ( EN LA FUNCION GRANDE ) 

print(blockCommands(dict_nombres_proc,list_variables_names,Directions,Orientations,num,tokens ), "comprobado block commands")

#CONTROL STRUCTURES (condicionales)
def If (dict_nombres_proc, lista_variables_creadas, Directions, Orientations, num, tokens):
    i = 0
    while i < len(tokens):
        if(tokens[i] == "if"):
            if (correccionIndexOOR('if', 0, tokens)[0]== True) or (correccionIndexOOR('if', 1, tokens)[0]== True) or (correccionIndexOOR('if', 2, tokens)[0]== True):
                return False, tokens[i:]
            elif tokens[i+1] in Condiciones:
                if tokens[i+1] == 'facing':
                    check, sliced = Facing(Orientations, tokens[i+1:])
                elif tokens[i+1] == 'can':
                    check, sliced = Can(Comandos, lista_variables_creadas, Directions, Orientations, num, tokens[i+1:])
                elif tokens [i+1]== 'not':
                    check, sliced = Not(Condiciones, lista_variables_creadas, Directions, Orientations, Comandos, num, tokens[i+1:])
            else:
                return False, []
            
            if sliced!= [] and check !=False and sliced[0] == '{':
                check, ssliced = blockCommands(dict_nombres_proc,list_variables_names,Directions,Orientations,num, sliced)
                if ssliced !=[] and check!= False and ssliced[0] == 'else':
                    check, sssliced = blockCommands(dict_nombres_proc, lista_variables_creadas, Directions, Orientations, num, ssliced[1:])
                    if check == True:
                        return check, sssliced
                    else:
                        return False, sssliced
                else:
                    return False, sssliced
                
            else:
                return False, []
                
        i += 1
    return check, sliced
def While (dict_nombres_proc, lista_variables_creadas, Directions, Orientations, num, tokens):
    i = 0
    while i < len(tokens):
        if(tokens[i] == "while"):
            if (correccionIndexOOR('while', 0, tokens)[0]== True) or (correccionIndexOOR('while', 1, tokens)[0]== True) or (correccionIndexOOR('while', 2, tokens)[0]== True):
                return False, tokens[i:]
            elif tokens[i+1] in Condiciones:
                if tokens[i+1] == 'facing':
                    check, sliced = Facing(Orientations, tokens[i+1:])
                elif tokens[i+1] == 'can':
                    check, sliced = Can(Comandos, lista_variables_creadas, Directions, Orientations, num, tokens[i+1:])
                elif tokens [i+1]== 'not':
                    check, sliced = Not(Condiciones, lista_variables_creadas, Directions, Orientations, Comandos, num, tokens[i+1:])
            else:
                return False,  []
            if sliced!= [] and check !=False and sliced[0] == '{':
                check, sliced = blockCommands(dict_nombres_proc, lista_variables_creadas, Directions, Orientations, num, sliced)
                if check == True:
                    return True, sliced
                else:
                    return False, []
            else:
                return False, []
            
        i += 1
def RepeatTimes(dict_nombres_proc, lista_variables_creadas, Directions, Orientations, num, tokens):
    i = 0
    while i < len(tokens):
        if(tokens[i] == "repeat"):
            if (correccionIndexOOR('repeat', 0, tokens)[0]== True) or (correccionIndexOOR('repeat', 1, tokens)[0]== True) or (correccionIndexOOR('repeat', 2, tokens)[0]== True):
                return False, []
            elif (tokens[i+1] in num or tokens[i+1] in lista_variables_creadas) and tokens[i+2] == 'times' and tokens[i+3]== '{':
                check, sliced = blockCommands(dict_nombres_proc, lista_variables_creadas, Directions, Orientations, num, tokens[i+3:])
                if check == True:
                    return True, sliced
                else:
                    return False, []
            else:
                return False, []
        i+= 1
