import speech_recognition as sr
import os
from time import sleep

dirName = input("escriba el nombre de la carpeta a procesar, o pulse enter para procesar los wavs de la carpeta 'audio'")
if dirName == "":
    dirName="audio"

class FormatError(Exception):
    pass
    
class Recognize():
    def __init__(self):
        self.re = sr.Recognizer()
    
    def run(self, audio, lang="es"):
        with sr.AudioFile(audio) as source:
            info_audio = self.re.record(source)
            return self.re.recognize_google(info_audio, language=lang)
    
    def processFile(self, dir, name):
        root=dir+"/"+name
        ext = name[-3:]
        name = name[:-4]
        if ext == "wav":
            return self.run(root)
        else:
            raise FormatError()
    
    def processDir(self, name):
        print("procesando... "+name)
        num=0
        data = {}
        dir='./'+name
        files = os.listdir(dir)
        for f in files:
            try:
                data[name+"/"+f] = self.processFile(dir, f)
            except FormatError:
                pass
            sleep(0.1)
        num=len(data)
        f=open("list.txt", "w")
        lista = list(data.keys())
        lista.sort()
        for root in lista:
            text=data[root]
            f.write(root+"|"+text+".\n")
        f.close()
        print("fin del proceso. "+str(num)+" archivos procesados.")

r=Recognize()
try:
    r.processDir(dirName)
except FileNotFoundError:
    print("Error: la carpeta: '"+dirName+"' no existe.")