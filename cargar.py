import nltk
import os
nltk.download('punkt')  # Descargar los recursos necesarios

from nltk.tokenize import word_tokenize, sent_tokenize

###########################################         ABRIR ARCHIVO TXT
def openFile(file_name: str)->list[str]:
    
    """    
    Args:
        file_name: str del archivo <.txt> que se quiere cargar.

    Returns:
        lines (list[str]): lista con los str de cada linea del texto cargado (que es basicamente lo que hace el metodo <readlines()>)
    """
    file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name+'.txt')
    
    with open(file_name, "r") as cmdFile:
        linea = cmdFile.readlines()
        linea.append("\n")                                                          # sin esto en la siguiente funcion no se imprimen todos los datos
    return linea

###########################################         PARA QUITARLE ESPACIOS, PONER TOOODO ELEGANTE
###########################################         Y DEJAR TODOS LOS COMANDOS EN EL MISMO STR
def filterByCommand(lineas: list[str])->list[str]:
    """
    Args:
        lines (list[str]): lista con los str de cada linea del texto cargado (que es basicamente lo que hace el metodo <readlines()>)

    Returns:
        list[str]: cada indice (str de la lista) es un comando :)
    """
    indice = 0                                                                      # primer indice de 'lineas'
    indiceDelComando = indice + 1                                                   # segundo indice de 'lineas' // ultimo de cada comando
    nuevaLista = []                                                                 # lista final
    while (indiceDelComando < len(lineas)):

        if (lineas[indiceDelComando] == "\n"):
            strDelComando = ""                                                      #el comando <str> que se le va a añadir a la lista final

            for numero in range(indice, indiceDelComando):                          #itera hasta tener todos los comandos del texto
                strDelComando = strDelComando + lineas[numero]

            if strDelComando != '':
                nuevaLista.append(" ".join(strDelComando.split()))

            indice = indiceDelComando
            indiceDelComando = indice + 1

        
        if (indiceDelComando < len(lineas) and lineas[indice]=="\n" and lineas[indiceDelComando] == "\n" and lineas[0] != 'd'):
            indice += 2
            indiceDelComando += 2

        
        else:
            indiceDelComando += 1
    return nuevaLista
print(filterByCommand(openFile(input('file_name= '))))
print ('---------------------------------')
print (openFile(input('file_name= ')))