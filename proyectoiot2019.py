import pyrebase
import serial
import time

config = {
    "apiKey": "AIzaSyDmlBKVnFw_A8ZszvLwMmULqFbKolKJt5g",
    "authDomain": "iot2019-8c58f.firebaseapp.com",
    "databaseURL": "https://iot2019-8c58f.firebaseio.com",
    "storageBucket": "iot2019-8c58f.appspot.com",
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

cSer = serial.Serial('/dev/ttyACM0', 9600)

instV = "2"
instRsRo = "4"
instTemp = "5"
instHum = "6"
cont = 0
Sumco2=0
Sumco=0

while True:
    cSer.write(instV.encode())
    voltaje=cSer.readline()
    cSer.write(instRsRo.encode())
    RsRo=cSer.readline()
    cSer.write(instTemp.encode())
    temp=cSer.readline()
    cSer.write(instHum.encode())
    hum=cSer.readline()
    humedad=float(hum)
    temperatura=float(temp)
    Aco2=109.53915*(float(RsRo)**(-2.85894))
    Aco=45.09508*(float(RsRo)**(-4.25009))
    print("ppm de co2:", Aco2)
    print("ppm de co:", Aco)
    print(cont)
    cont+=1
    Sumco2=Sumco2+Aco2
    Sumco=Sumco+Aco
    time.sleep(10)
    tiempo = db.child("sensores/tiempoA").get()
    ciclo=int(tiempo.val())
    if cont > ciclo:
        cont=0
        Sumco=0
        Sumco2=0
        Aco=0
        Aco2=0
    if cont == ciclo:
        cont = 0
        co = Sumco/ciclo
        print(co)
        if co <= 5.5:
            imeca = int(co*50/5.5)
            calidad = "buena"
        else:
            if co >= 5.51 and co <= 11:
                imeca = int(1.82+co*49/5.49)
                calidad = "regular"
            else:
                if co >= 11.01 and co <= 16.5:
                    imeca = int(2.73+co*49/5.49)
                    calidad = "mala"
                else:
                    if co >= 16.51 and co <= 22:
                        imeca = int(3.64+co*49/5.49)
                        calidad = "muy mala"
                    else:
                        imeca = int(co*201/22.01)
                        calidad = "extremadamente mala"
        print("IMECA:", imeca)
        dimeca = {"imeca": imeca}
        print("Calidad de Aire", calidad)
        dcalidad = {"calidad": calidad}
        co2=round(Sumco2/ciclo, 2)
        print("Particulas de CO2 en el aire:", co2)
        dco2 = {"ppmco2": co2}
        print("Temperatura:", temperatura)
        dtemp = {"temperatura": temperatura}
        print("Humedad", humedad)
        dhum = {"humedad": humedad}
        dco = {"ppmco": co}
        db.child("sensores/sensor1").update(dcalidad)
        db.child("sensores/sensor1").update(dimeca)
        db.child("sensores/sensor1").update(dco)
        db.child("sensores/sensor1").update(dco2)
        db.child("sensores/sensor2").update(dhum)
        db.child("sensores/sensor2").update(dtemp)
        Sumco=0
        Sumco2=0
        Aco=0
        Aco2=0
        
cSer.close()