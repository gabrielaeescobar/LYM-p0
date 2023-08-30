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
# funcion para nop




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


"""""def check_turnto(comando):
    if len(tokens) == 4 and tokens[0] == 'turnto' and tokens[1] == '(' and tokens[3] == ')' and tokens[2] in ['north', 'south', 'east', 'west']:
        return True
    return False """""
