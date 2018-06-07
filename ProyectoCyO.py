#!/usr/bin/python
#-*- coding: utf-8 -*-
import wx
import time


class panelInicio(wx.Panel):
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.quote = wx.StaticText(self, label="integrantes: \n Erik López - 1430406 \n Alejandro Valencia R - 14----- \n Juan Jose Varela - 14-----", pos=(10, 10))

        self.logger = wx.TextCtrl(self, pos=(300,20), size=(450,420), style=wx.TE_MULTILINE | wx.TE_READONLY)

        self.botonCargar =wx.Button(self, label="Cargar", pos=(240, 100), size = (50, 30))
        self.Bind(wx.EVT_BUTTON, self.ClickCargar, self.botonCargar)

        self.lblnum = wx.StaticText(self, label="Numero de procedimientos :", pos=(10,100))
        self.numProc = wx.TextCtrl(self, value="", pos=(195, 100), size=(40,-1))

        self.lblproc = wx.StaticText(self, label="Procedimiento # :", pos=(95, 140))

        self.lblnomproc = wx.StaticText(self, label = 'nombre: ', pos = (10, 160))
        self.nomProc = wx.TextCtrl(self, value = '', pos = (10, 180), size = (120, -1))
        self.lblhoraini = wx.StaticText(self, label = 'Hora inicio: ', pos = (135, 160))
        self.horaini = wx.TextCtrl(self, value = '', pos = (135, 180), size = (75, -1))
        self.lblhorafin = wx.StaticText(self, label = 'Hora fin: ', pos = (220, 160))
        self.horafin = wx.TextCtrl(self, value = '', pos = (220, 180), size = (75, -1))

        self.buttonAgg = wx.Button(self, label = 'añadir', pos = (110, 210), size = (75, -1))
        self.Bind(wx.EVT_BUTTON, self.ClickAnadir, self.buttonAgg)

        self.buttonInge = wx.Button(self, label = 'Solucion Ingenua o Exhaustiva', pos = (45, 260))
        self.Bind(wx.EVT_BUTTON, self.ClickIngenuo, self.buttonInge)
        self.buttonInge.Disable()
        self.buttonVor = wx.Button(self, label = 'Solucion Voraz', pos = (95, 290))
        self.Bind(wx.EVT_BUTTON, self.ClickVoraz, self.buttonVor)
        self.buttonVor.Disable()
        self.buttonDim = wx.Button(self, label = 'Solucion Dinámica', pos = (85, 320))
        self.Bind(wx.EVT_BUTTON, self.ClickDinamico, self.buttonDim)
        self.buttonDim.Disable()

        #parte de abrir archivos ¬¬
        self.buttonArchivo = wx.Button(self, label = 'archivo', pos = (8, 132))
        self.Bind(wx.EVT_BUTTON, self.ClickArchivo, self.buttonArchivo)
        #fin de parte de abrir archivo ¬¬
    def ClickArchivo(self, event):
        archivo = open("procedimientos.txt", "r")
        linea1 = archivo.readline()
        global numeroProcedimientos
        numeroProcedimientos = int(linea1)
        lineas = archivo.readlines()
        global ListProc
        for i  in range(0, len(lineas), 1):
            lin = lineas[i].split(' ')
            ListProc.append(lin)
        for i in range(numeroProcedimientos):
            ListProc[i][2] = ListProc[i][2].replace('\n', '')
        for i in range(numeroProcedimientos):
            for j in range(1, 3):
                ListProc[i][j] = time.strptime(ListProc[i][j], "%H:%M")
        self.buttonInge.Enable()
        self.buttonVor.Enable()
        self.buttonDim.Enable()
        self.buttonAgg.Disable()
        self.buttonOk.Disable()
        self.numProc.SetValue(str(numeroProcedimientos))
        self.numProc.SetEditable(False)
        self.numProc.Disable()
    def ClickCargar(self,event):
        openFileDialog = wx.FileDialog(self, "Open", "", "", "Text files (*.txt)|*.txt", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        openFileDialog.ShowModal()
        ruta = openFileDialog.GetPath()
        print ruta
        self.logger.SetValue("ruta del archivo: " + ruta + '\n')
        #self.lblproc.SetLabel('Procedimiento: 0')
        self.numProc.SetEditable(False)
    def ClickAnadir(self, event):
        global numeroProcedimientos
        global np
        if np < numeroProcedimientos:
            nombre_tem = self.nomProc.GetValue()
            horain_tem = time.strptime(self.horaini.GetValue(), "%H:%M")
            horafin_tem = time.strptime(self.horafin.GetValue(), "%H:%M")
            ListProc[np][0] = str(nombre_tem)
            ListProc[np][1] = horain_tem
            ListProc[np][2] = horafin_tem
            self.logger.SetValue('Se añadio el procedimiento: ' + ListProc[np][0] + '\nhora inicio: ' + str(ListProc[np][1].tm_hour) +':'+str(ListProc[np][1].tm_min) + '\nhora fin : ' + str(ListProc[np][2].tm_hour) + ':' + str(ListProc[np][1].tm_min) +'\n' )
            infoProc = '[nombre_proc] \t [hora_ini] \t [hora_fin] \n'
            for i in range(np + 1):
                for j in range(3):
                    if j == 0:
                        infoProc += str(ListProc[i][j]) +'                      \t'
                    else:
                        infoProc += str(ListProc[i][j].tm_hour) + ':' + str(ListProc[i][j].tm_min) +'             \t'

                infoProc += '\n'
            self.logger.AppendText(infoProc)
            self.nomProc.SetValue('')
            self.horaini.SetValue('')
            self.horafin.SetValue('')
            np += 1
            if np != numeroProcedimientos:
                self.lblproc.SetLabel('Procedimiento: ' + str(np))
            elif np == numeroProcedimientos:
                msj = wx.MessageDialog(self, 'ya lleno todos los procedimientos!', 'Proyecto', style = wx.OK)
                msj.ShowModal()
                self.lblproc.SetLabel('Procedimientos: ' + str(numeroProcedimientos))
                self.nomProc.SetEditable(False)
                self.horaini.SetEditable(False)
                self.horafin.SetEditable(False)
                self.buttonAgg.Disable()
                self.buttonOk.Disable()
                self.buttonInge.Enable()
                self.buttonVor.Enable()
                self.buttonDim.Enable()
    def ClickIngenuo(self, event):
        self.logger.SetValue('solucion ingenua: \n')

        infoProc = '[nombre_proc] \t [hora_ini] \t [hora_fin] \n'
        for i in range(numeroProcedimientos):
            for j in range(3):
                if j == 0:
                    infoProc += str(ListProc[i][j]) +'                      \t'
                else:
                    infoProc += str(ListProc[i][j].tm_hour) + ':' + str(ListProc[i][j].tm_min) +'             \t'
            infoProc += '\n'
        self.logger.AppendText(infoProc)

        aux=0
        ProcedimientosARealizar = []
        ProcedimientosARealizar.append(ListProc[0])
        #print (len(ListProc))
        ListProc.remove(ListProc[0])
        #print (len(ListProc))
        print(len(ProcedimientosARealizar)-1)

        for i in range (len(ListProc)):
            print(i)
            if not cruzan(ProcedimientosARealizar[len(ProcedimientosARealizar)-1],ListProc[i]):
                ProcedimientosARealizar.append(ListProc[i])
                ListProc.remove(ListProc[i])
            else:
                ListProc.remove(ListProc[i])





        info = '[nombre_proc] \t [hora_ini] \t [hora_fin] \n'
        for i in range(len(ProcedimientosARealizar)):
            for j in range(3):
                if j == 0:
                    info += str(ProcedimientosARealizar[i][j]) +'                      \t'
                else:
                    info += str(ProcedimientosARealizar[i][j].tm_hour) + ':' + str(ProcedimientosARealizar[i][j].tm_min) +'             \t'
            info += '\n'
        self.logger.AppendText(info)
    def ClickVoraz(self, event):
        self.logger.SetValue('solucion voraz: \n')
        infoProc = '[nombre_proc] \t [hora_ini] \t [hora_fin] \n'
        for i in range(numeroProcedimientos):
            for j in range(3):
                if j == 0:
                    infoProc += str(ListProc[i][j]) +'                      \t'
                else:
                    infoProc += str(ListProc[i][j].tm_hour) + ':' + str(ListProc[i][j].tm_min) +'             \t'
            infoProc += '\n'
        self.logger.AppendText(infoProc)
        tiempo_inicio = time.time()
        listaDePesos = []
        for i in range(numeroProcedimientos):
            peso = HorasAminutos(ListProc[i][2].tm_hour, ListProc[i][2].tm_min) - HorasAminutos(ListProc[i][1].tm_hour, ListProc[i][1].tm_min)
            listaDePesos.append(peso)
        ProcedimientosARealizar = []
        sum = 0
        maxx = 0
        aux = 0
        aux2 = 0
        while len(listaDePesos)>0:

            if sum == 0:
                maxx = max(listaDePesos)
                ind = listaDePesos.index(maxx)
                ProcedimientosARealizar.append(ListProc[ind])
                ListProc.remove(ListProc[ind])
                listaDePesos.remove(maxx)
                sum = sum + maxx
            else :
                maxx = max(listaDePesos)
                ind = listaDePesos.index(maxx)

                if not cruzan(ProcedimientosARealizar[aux],ListProc[ind]):
                    ProcedimientosARealizar.append(ListProc[ind])
                    ListProc.remove(ListProc[ind])
                    listaDePesos.remove(maxx)
                    sum = sum + maxx
                    aux = len(ProcedimientosARealizar) - 1
                else :
                    if not cruzan(ListProc[ind],ProcedimientosARealizar[aux2]):
                        ProcedimientosARealizar.append(ListProc[ind])
                        ListProc.remove(ListProc[ind])
                        listaDePesos.remove(maxx)
                        sum = sum + maxx
                        aux2 = len(ProcedimientosARealizar)-1
                    else:
                        ListProc.remove(ListProc[ind])
                        listaDePesos.remove(maxx)


        info = '[nombre_proc] \t [hora_ini] \t [hora_fin] \n'
        for i in range(len(ProcedimientosARealizar)):
            for j in range(3):
                if j == 0:
                    info += str(ProcedimientosARealizar[i][j]) +'                      \t'
                else:
                    info += str(ProcedimientosARealizar[i][j].tm_hour) + ':' + str(ProcedimientosARealizar[i][j].tm_min) +'             \t'
            info += '\n'
        self.logger.AppendText(info)
        tiempo_fin = time.time()
        tiempo_ejecucion = tiempo_fin - tiempo_inicio
        self.logger.AppendText("El tiempo de ejecucion para esta solucion voraz fue de: " +  str(tiempo_ejecucion))
    def ClickDinamico(self,event):
        self.logger.SetValue('Hola, aqui va la solucion dinamica del problema')
        ListProcMin = []
        for i in range(numeroProcedimientos):
            ListProcMin.insert(i, list((i, HorasAminutos(ListProc[i][1].tm_hour, ListProc[i][1].tm_min), HorasAminutos(ListProc[i][2].tm_hour, ListProc[i][2].tm_min))))
        print(ListProcMin)
        #quicksort(ListProcMin, 0, (len(ListProcMin) - 1))
        ListProcMin.sort(key =  lambda x: x[2])
        print(ListProcMin)
        listaBeneficios = []
        listaCostos = []
        #se llena la lista de beneficios con las duraciones de cada procedimiento
        for i in range(numeroProcedimientos):
            beneficio = HorasAminutos(ListProc[i][2].tm_hour, ListProc[i][2].tm_min) - HorasAminutos(ListProc[i][1].tm_hour, ListProc[i][1].tm_min)
            listaBeneficios.append(beneficio)

        ProcedimientosARealizar = []

        #se llena la lista de costos buscando el maximo de los beneficios
        listaCostos.append(0)
        for i in range(1, numeroProcedimientos):
            listaCostos.insert(i, maximo((listaBeneficios[i - 1] + listaCostos[i - 1]), listaCostos[i - 1], (i - 1)))
        print(listaCostos)
"""
SE DEFINEN LA INTERFAZ Y METODOS DEl PANEL LIBROS
"""
arrayPaginas=[]
arrayNombres=[]
cantEscritores = 0
cantLibros = 0
posiblesSol = []
solLibros = []

def suma(arreglo):
    global arrayPaginas
    summ = 0
    for i in arreglo:
        summ = summ + arrayPaginas[int(i)-1]
    return summ

def calcTiempo(solucion):
    global solLibros
    tiempo = 0
    for i in solucion:
        taux = suma(i)
        if(taux > tiempo):
        	solLibros = i
        	tiempo = taux
    return tiempo

def genSol(ini,fin):
    sol = []

    for i in range(ini,fin+1,1):
        sol.append(i)
    return sol

def generarSol(escritor, libro, array):
    global posiblesSol
    if(not(escritor==0 and libro!=0) and not(escritor!=0 and libro==0)):
        if(escritor==0 and libro==0):
            posiblesSol.append(array)

        else:
            iterator = 1
            while(iterator<=libro):
                arregloAux = array
                solAux = genSol(iterator,libro)
                arregloAux.append(solAux)
                generarSol(escritor-1,iterator-1,arregloAux)
                iterator = iterator + 1

class panelResultado(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.logger = wx.TextCtrl(self, pos=(260,20), size=(450,400), style=wx.TE_MULTILINE | wx.TE_READONLY)

        self.buttonCargar =wx.Button(self, label="Cargar Archivo", pos=(20, 20), size = (120, 30))
        self.Bind(wx.EVT_BUTTON, self.ClickCargar, self.buttonCargar)

	self.buttonInge = wx.Button(self, label = 'Solucion Ingenua o Exhaustiva', pos = (45, 260))
        self.Bind(wx.EVT_BUTTON, self.ClickIngenuo, self.buttonInge)
        self.buttonInge.Disable()
        self.buttonVor = wx.Button(self, label = 'Solucion Voraz', pos = (95, 300))
        self.Bind(wx.EVT_BUTTON, self.CLickVoraz, self.buttonVor)
        self.buttonVor.Disable()
        self.buttonDim = wx.Button(self, label = 'Solucion Dinámica', pos = (85, 340))
        self.Bind(wx.EVT_BUTTON, self.ClickDinamico, self.buttonDim)
        self.buttonDim.Disable()


    def ClickIngenuo(self,event):
        global arrayNombres
        global cantEscritores
        global cantLibros
        global solLibros
        global posiblesSol
        generarSol(int(cantEscritores), int(cantLibros), [])
        #tiempo = calcTiempo(posiblesSol)

        print posiblesSol


        self.logger.SetValue('Se mostrara la solucion ingenua del problema')
    def CLickVoraz(self,event):
	    self.logger.SetValue('Se mostrara la solucion voraz del problema')
    def ClickDinamico(self,event):
	    self.logger.SetValue('Se mostrara la solucion dinamica del problema')



    def ClickCargar(self,event):
        archivo = open("infoLibros.txt","r")
        linea1 = archivo.readline()
        global cantEscritores
        global cantLibros
        cantEscritores = linea1.split(" ")[0]
        cantLibros = linea1.split(" ")[1]
        global arrayPaginas
        del arrayPaginas[:]
        global arrayNombres
        del arrayNombres[:]


        for i in archivo.readlines():
            arrayNombres.append(i.split(" ")[0])
            arrayPaginas.append(int(i.split(" ")[1]))

        carga = "La información cargada es la siguiente:\nCantidad de Escritores: "+cantEscritores+"\nCantidad de Libros: "+ cantLibros

        for i in range(0,len(arrayNombres)):
            carga = carga + "Titulo del libro: " + arrayNombres[i] + "--Cantidad de paginas: "+ str(arrayPaginas[i])+"\n"
        self.logger.SetValue(carga)
        self.buttonInge.Enable()
    	self.buttonVor.Enable()
    	self.buttonDim.Enable()




app = wx.App(False)
# Creamos el frame padre
frame = wx.Frame(None, title="Proyecto CyO", size=(780,520))
# Creamos el contenedor de pestañas
nb = wx.Notebook(frame)
# Añadimos los paneles con Addpage
nb.AddPage(panelInicio(nb), "Inicio")
nb.AddPage(panelResultado(nb), "Resultados")
frame.Show()
app.MainLoop()