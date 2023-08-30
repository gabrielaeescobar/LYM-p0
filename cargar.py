import nltk
import os
nltk.download('punkt')  # Descargar los recursos necesarios

from nltk.tokenize import word_tokenize, sent_tokenize

###########################################         ABRIR ARCHIVO TXT

def openFile2(file_name: str)->list[str]:
    
    """    
    Args:
        file_name: str del archivo <.txt> que se quiere cargar.

    Returns:
        lines (list[str]): lista con los str de cada linea del texto cargado (que es basicamente lo que hace el metodo <readlines()>)
    """
    file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name+'.txt')
    lista = []
    with open(file_name, "r") as cmdFile:
        lineas = cmdFile.readlines()
        texto = ''
        for linea in lineas:
            final = texto+ linea
            texto = final
        
    return texto



