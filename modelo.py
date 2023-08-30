import nltk
nltk.download('punkt') 

from nltk.tokenize import word_tokenize, sent_tokenize


texto = " defVar nom 0 defVar x 0 defVar y 0 defVar one 0 defProc putCB (c, b) { drop(c); letGo (b) ; walk(n) }"
todo = sent_tokenize(texto)
tokens = [word_tokenize(cadacosa) for cadacosa in todo]
print("Tokens:", tokens)

#constantes
parent_izq = "("

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

print(check_defVar(tokens), "defvar")

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