import nltk
nltk.download('punkt')  # Descargar los recursos necesarios

from nltk.tokenize import word_tokenize, sent_tokenize

# Texto de ejemplo
texto = " defVar nom 0 defVar x 0 defVar y 0 defVar one 0"
# Tokenización de frases
frases = sent_tokenize(texto)
print("Frases:", frases)

# Tokenización de palabras en cada frase
tokens_por_frase = [word_tokenize(frase) for frase in frases]
print("Tokens por frase:", tokens_por_frase)

comandoSolo1Parametro = ["turn","turnto","drop","get","grab","letGo"]
# funcion para las funciones jump walk 

def check_turnto(comando):
    if len(tokens) == 4 and tokens[0] == 'turnto' and tokens[1] == '(' and tokens[3] == ')' and tokens[2] in ['north', 'south', 'east', 'west']:
        return True
    return False 

def check_comandos_1_parametro(lstComandos):
    while comando in lstComandos:
        if comando 





# funcion para def var
# funcion para def proc


"""if oalbea == DROP:
palabras[]"""