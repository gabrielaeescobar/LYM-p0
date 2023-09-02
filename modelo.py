import nltk
from nltk.tokenize import word_tokenize, sent_tokenize, regexp_tokenize
import cargar 
nltk.download('punkt') 

#texto_carga = cargar.openFile2(input("ingrese el filename (sin el .txt): "))
#texto = texto_carga.lower()

texto_prueba = "{(walk(1)); can(jump (3 ,9)); walk(2,north); turn(front); get(1); leap(1,left)}" # solo mira brackets
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
Condicion = ['facing', 'can', 'not']

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
    checkCan = None
    while i < len(tokens):
        if ((tokens[i] == "walk") or (tokens[i] == "leap")):
            if (correccionIndexOOR('walk', 2, tokens)[0]== True or correccionIndexOOR('leap', 2, tokens)[0]== True) or (correccionIndexOOR('walk', 1, tokens)[0]== True or correccionIndexOOR('leap', 1, tokens)[0]== True) or (correccionIndexOOR('walk', 0, tokens)[0]== True or correccionIndexOOR('leap', 0, tokens)[0]== True):
                return False, tokens[i:], checkCan
                
            elif ((correccionIndexOOR('walk', 3, tokens) == (True, i))  or (correccionIndexOOR('leap', 3, tokens) == (True, i))) and tokens[i+1] == '(' and ((tokens[i+2] in num) or (tokens[i+2] in lista_variables_creadas)) and tokens[i+3] == ')':
                return True, tokens[i+4:], checkCan
            
            elif tokens[i+1] == '(' and ((tokens[i+2] in num) or (tokens[i+2] in lista_variables_creadas)) and tokens[i+3] == ')':
                return True, tokens[i+4:], checkCan
            
            #ya no hay posibles 'walk' o 'leap' con solo un parametro
            
            elif (correccionIndexOOR('walk', 3, tokens)[0]== True or correccionIndexOOR('leap', 3, tokens)[0]== True) or (correccionIndexOOR('walk', 4, tokens)[0]== True or correccionIndexOOR('leap', 4, tokens)[0]== True):
                return False, tokens[i:], checkCan
                
            elif ((correccionIndexOOR('walk', 5, tokens) == (True, i))  or (correccionIndexOOR('leap', 5, tokens) == (True, i))) and tokens[i+1] == '(' and ((tokens[i+2] in num) or (tokens[i+2] in lista_variables_creadas)) and (tokens[i+3]== ',') and ((tokens[i+4] in Directions) or (tokens[i+4] in Orientations)) and tokens[i+5] == ')':
                return True, tokens[i+6:], checkCan
            
            elif tokens[i+1] == '(' and ((tokens[i+2] in num) or (tokens[i+2] in lista_variables_creadas)) and (tokens[i+3]== ',') and ((tokens[i+4] in Directions) or (tokens[i+4] in Orientations)) and tokens[i+5] == ')':
                return True, tokens[i+6:], checkCan
            
            else:
                return False, tokens[i:], checkCan
                

        i+=1
#print(Walk_Leap([], Directions, Orientations, num, tokens))
def Jump (lista_variables_creadas, num, tokens):
    i = 0
    checkCan = None
    while i < len(tokens):
        if tokens[i] == "jump":
            if (correccionIndexOOR('jump', 0, tokens)[0]== True) or (correccionIndexOOR('jump', 1, tokens)[0]== True) or (correccionIndexOOR('jump', 2, tokens)[0]== True) or (correccionIndexOOR('jump', 3, tokens)[0]== True) or (correccionIndexOOR('jump', 4, tokens)[0]== True):
                return False, tokens[i:], checkCan
                
            elif (correccionIndexOOR('jump', 5, tokens) ==(True, i)) and tokens[i+1] == '(' and ((tokens[i+2] in num) or (tokens[i+2] in lista_variables_creadas)) and (tokens[i+3]== ',') and ((tokens[i+4] in num) or (tokens[i+4] in lista_variables_creadas)) and tokens[i+5] == ')':
                return True, tokens[i+6:], checkCan
            
            elif tokens[i+1] == '(' and ((tokens[i+2] in num) or (tokens[i+2] in lista_variables_creadas)) and (tokens[i+3]== ',') and ((tokens[i+4] in num) or (tokens[i+4] in lista_variables_creadas)) and tokens[i+5] == ')':
                return True, tokens[i+6:], checkCan
            else:
                return False, tokens[i:], checkCan
                
        i += 1
    

def Turn (Directions, tokens):
    i = 0
    checkCan = None
    while i < len(tokens):
        if tokens[i] == "turn":
            if  (correccionIndexOOR('turn', 0, tokens)[0]== True) or (correccionIndexOOR('turn', 1, tokens)[0]== True) or (correccionIndexOOR('turn', 2, tokens)[0]== True):
                return False, tokens[i:], checkCan
                
            elif (correccionIndexOOR('turn', 3, tokens) == (True, i)) and tokens[i+1] == '(' and (tokens[i+2] in Directions) and tokens[i+3] == ')':
                return True, tokens[i+4:], checkCan
            
            elif tokens[i+1] == '(' and (tokens[i+2] in Directions) and tokens[i+3] == ')':
                return True, tokens[i+4:], checkCan
            else:
                return False, tokens[i:], checkCan
                
        i += 1

def TurnTo (Orientations, tokens):
    i = 0
    checkCan = None
    while i < len(tokens):
        if tokens[i] == "turnto":
            if  (correccionIndexOOR('turnto', 0, tokens)[0]== True) or (correccionIndexOOR('turnto', 1, tokens)[0]== True) or (correccionIndexOOR('turnto', 2, tokens)[0]== True):
                return False, tokens[i:], checkCan
                
            elif (correccionIndexOOR('turnto', 3, tokens) == (True, i)) and tokens[i+1] == '(' and (tokens[i+2] in Orientations) and tokens[i+3] == ')':
                return True, tokens[i+4:], checkCan
                
            elif tokens[i+1] == '(' and (tokens[i+2] in Orientations) and tokens[i+3] == ')':
                return True, tokens[i+4:], checkCan
                
            else:
                return False, tokens[i:], checkCan
                
        i += 1

def Drop_Get_Grab_LetGo (lista_variables_creadas, num, tokens):
    i = 0
    checkCan = None
    while i < len(tokens):
        if (tokens[i] == "drop") or (tokens[i] == "get") or (tokens[i] == "grab") or (tokens[i] == "letgo"):
            if  (correccionIndexOOR(tokens[i], 0, tokens)[0]== True) or (correccionIndexOOR(tokens[i], 1, tokens)[0]== True) or (correccionIndexOOR(tokens[i], 2, tokens)[0]== True):
                return False, tokens[i:], checkCan
                
            elif (correccionIndexOOR(tokens[i], 3, tokens) == (True, i)) and tokens[i+1] == '(' and ((tokens[i+2] in num) or (tokens[i+2] in lista_variables_creadas)) and tokens[i+3] == ')':
                return True, tokens[i+4:], checkCan
                
            elif tokens[i+1] == '(' and ((tokens[i+2] in num) or (tokens[i+2] in lista_variables_creadas)) and tokens[i+3] == ')':
                return True, tokens[i+4:], checkCan
                
            else:
                return False
                
        i+= 1
def Nop(tokens):
    i = 0
    checkCan = None
    while i < len(tokens):
        if tokens[i] == "nop":
            if correccionIndexOOR('nop', 0, tokens)[0] == True or correccionIndexOOR('nop', 1, tokens)[0]== True:
                return False, tokens[i:], checkCan
                
            elif correccionIndexOOR('nop', 2, tokens) == (True, i) and tokens[i+1] == '(' and tokens[i+2] == ')':    
                return True, tokens[i+3:], checkCan
            
            elif tokens[i+1] == '(' and tokens[i+2] == ')':
                return True, tokens[i+3:], checkCan
            else:
                return False, tokens[i:], checkCan
        i += 1
print (Nop(tokens), '///////////////////////////')
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

def Can (Comandos, lista_variables_creadas, Directions, Orientations, num, tokens):
    i = 0
    check = False
    while i < len(tokens):

        if tokens[i] == "can":
            
            j = i+1
            if (correccionIndexOOR('can', 0, tokens)[0] == True) or (correccionIndexOOR('can', 1, tokens)[0]== True) or (correccionIndexOOR('can', 2, tokens)[0] == True):
                return False
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
                            check = False
                            
                        if check != True or sliced_sliced[0] != ')':
                            return False
                        else:
                            return True
                        
                    
                else:
                    return False
                j+= 1

        i+=1
        
        
    return check
#print (Can(Comandos, [], Directions, Orientations, num, tokens), '///////////////////////')
################################################################            parentesis de cierre esta pendiente
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

            elif tokens[i] == key and dict_nombres_proc[key] == 4:
                if not(tokens[i+1] == '(' and ((tokens[i+2] in num) or (tokens[i+2] in lista_variables_creadas)) and (tokens[i+3]== ',') and ((tokens[i+4] in Directions) or (tokens[i+4] in Orientations)) and tokens[i+5] == ')'):   #estructura que lleva 3 parametros 
                    check = False

        i += 1  
    return check, tokens[i:]
dict_nombres_proc = (check_defProc(tokens))[1]
lista_variables_creadas = (check_defVar(tokens))[1]

#Funcion para cada vez que aparezcan corchetes
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
                print(f'Voy a entrar a walk con { tokens[i:]}')
                check, tokens, _ = Walk_Leap (lista_variables_creadas, Directions, Orientations, num, tokens[i:])
                i=0  

            elif tokens[i] == "jump":
                check, tokens, _ = Jump (lista_variables_creadas, num,  tokens[i:])
                i=0
            elif tokens[i] == "turn":
                check, tokens, _ = Turn (Directions,  tokens[i:]) # Recibimos el check y el nuevo slice de tokens
                i=0
            elif tokens[i] == "turnto" :
                check, tokens, _ = TurnTo (Orientations,  tokens[i:]) 
                i=0
            elif  tokens[i] == "drop" or tokens[i] == "get" or tokens[i] == "grab" or tokens[i] == "letgo" :
                check , tokens,_ = Drop_Get_Grab_LetGo (lista_variables_creadas, num,  tokens[i:]) 
                i=0

            elif tokens[i] == "nop" :
                check , tokens, _ = Nop( tokens[i:])
                i=0
            elif tokens[i] in keys_dict_nombres_proc: 
                check, tokens, _ = check_funciones_defProc(dict_nombres_proc, tokens, lista_variables_creadas) 
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
            se_cerro_corchete = True
                
       
    
    check = check and se_cerro_corchete and se_abrio_corchete
    return check

### al bloque de comandos le falta llamar condicionales y eso ###
###arreglar { } que lo toma como true y tiene que haber algo adentro ### ( EN LA FUNCION GRANDE ) 
### CAMBIAR EL IS INSTANCE POR UNA FUNCION AUXILIAR QUE RECORRA CADA CADENA DEL NOMBRE ###

print(blockCommands(dict_nombres_proc,list_variables_names,Directions,Orientations,num,tokens ), "comprobado block commands")
