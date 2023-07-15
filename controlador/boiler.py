# consulta de manera periodica el servidor para determinar si se ha encendido el boiler
import time

fileProgram = "program.txt"

def getCurrentProgram():
    import requests
    try:
        URL = 'http://127.0.0.1:8000/current'
        data = requests.get(URL)
        data = data.json() 
        if data==[]:
            return 0
        data = data[0]
        return data['startTime'],data['endTime']
    except Exception as e:
        return -1

def postCurrentProgram(duration=15):
    import requests
    try:
        URL = 'http://127.0.0.1:8000/current'
        data = {'duration': duration}
        result = requests.post(URL,data={"duration":duration})
        # regresa un 201 si todo está bien
        return result.status_code
    except Exception as e:
        return False

def currentTimeCount():
    import time
    t = time.localtime()
    return t.tm_hour*60+t.tm_min

def programExists():
    import os.path
    return  os.path.isfile(fileProgram)

def programDelete():
    import os
    if os.path.isfile(fileProgram):
        os.remove(fileProgram)


def main():
    while True:
        res = getCurrentProgram()
        if res == 0:
            #nada en curso
            print("Noting to do")
            programDelete()
            pass
        elif res == -1:
            #no pudo conectarese
            if programExists():
                with open(fileProgram,"r") as reader:
                    end = reader.readline()
                end = int(end)
                now = currentTimeCount()
                if now<=end:
                    with open(fileProgram,"w") as writer:
                        writer.write(str(end))
                    print(f"[no connection]{now}: Boiler prendido, se apaga a las {end}")
                else:
                    print(f"[no connection] {now}: Boiler se apaga ahora {end}")
                    programDelete()
        else:
            # el servidor entrego un programa
            start,end = res
            now = currentTimeCount()
            if now<=end:
                with open(fileProgram,"w") as writer:
                    writer.write(str(end))
                print(f"{now}: Boiler prendido, se apaga a las {end}")
            else:
                print(f"{now}: Boiler se apaga ahora {end}")
                programDelete()
            pass
        # duerme 5 segundos
        time.sleep(5)



    pass

main()



