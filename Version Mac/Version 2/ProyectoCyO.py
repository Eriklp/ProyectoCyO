#!/usr/bin/python
#-*- coding: utf-8 -*-
import wx
import time
from pulp import *
def GuardarEnArchivo(texto, nombre):
    archivo = open(nombre+'.txt', 'w')
    archivo.write(texto)
    archivo.close()


class panelInicio(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.quote = wx.StaticText(self, label="integrantes: \n Erik López - 1430406 \n Alejandro Valencia R - 1427368 \n Juan Jose Varela - 1424388 \n Edgar Mauricio Ceron Florez - 1427918", pos=(10, 10))

        self.logger = wx.TextCtrl(self, pos=(300,20), size=(450,420), style=wx.TE_MULTILINE | wx.TE_READONLY)

        self.botonCargar = wx.Button(self, label="Cargar Datos", pos=(178 , 95), size = (85, 30))
        self.Bind(wx.EVT_BUTTON, self.ClickCargar, self.botonCargar)

        self.lblSeleccionar = wx.StaticText(self, label="Seleccionar Archivo :", pos=(10,95))

        self.lblNumParcelas = wx.StaticText(self, label="Numero de parcelas :", pos=(10, 130))
        self.NumParcelas = wx.TextCtrl(self, value= '', pos=(150, 130), size=(120, 30))

        self.lblTiemposDuracion = wx.StaticText(self, label = 'Tiempos de duración: ', pos = (10, 165))
        self.TiemposDuracion = wx.TextCtrl(self, value = '', pos = (150, 165), size = (120, 30))

        self.lblSumaTiempos = wx.StaticText(self, label = 'Suma de los tiempos: ', pos = (10, 200))
        self.SumaTiempos = wx.TextCtrl(self, value = '', pos = (150, 200), size = (120, 30))

        self.lblUtilidadesDePacelas = wx.StaticText(self, label = 'Utilidades De Las Parcelas: ', pos = (10, 240))
        self.UtilidadesDeParcelas = wx.TextCtrl(self, value = '', pos = (50, 260), size = (200, 120), style=wx.TE_MULTILINE | wx.TE_READONLY)

        self.buttonSolucionar = wx.Button(self, label = 'Solucionar', pos = (110, 390), size = (75, 30))
        self.Bind(wx.EVT_BUTTON, self.ClickSolucionar, self.buttonSolucionar)





    def ClickCargar(self,event):
        openFileDialog = wx.FileDialog(self, "Open", "", "", "Text files (*.txt)|*.txt", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        openFileDialog.ShowModal()
        ruta = openFileDialog.GetPath()
        self.logger.SetValue("ruta del archivo: " + ruta + '\n')
        archivo = open(ruta, "r")
        NumeroDeParcelas = int(archivo.readline())
        self.NumParcelas.SetValue(str(NumeroDeParcelas))
        tiemposdeduraciondeparcelas = archivo.readline().split(" ")
        TiemposDeDuracionDeParcelas = []
        for i in tiemposdeduraciondeparcelas:
            TiemposDeDuracionDeParcelas.append(int(i))
        info = "Numero De Parcelas: " + str(NumeroDeParcelas) + "\n" + "Tiempos de duracion: " + str(TiemposDeDuracionDeParcelas) + "\n"
        TiempoDuracionmostrar = ""
        for i in range(0, len(TiemposDeDuracionDeParcelas)):
            TiempoDuracionmostrar += str(TiemposDeDuracionDeParcelas[i])
            if i < (len(TiemposDeDuracionDeParcelas) - 1):
                TiempoDuracionmostrar += " "

        self.TiemposDuracion.SetValue(str(TiempoDuracionmostrar))
        SumaDeLosTiempos = int(archivo.readline())
        self.SumaTiempos.SetValue(str(SumaDeLosTiempos))
        info += "Suma de los tiempos: " + str(SumaDeLosTiempos) + "\n"
        matrizUtilidad = []
        matrizUtilidadMostrar = ""
        for i in range(0, NumeroDeParcelas):
            linea = archivo.readline().split(' ')
            #print(linea)
            matrizUtilidad.append([])
            for j in range(0,SumaDeLosTiempos):
                matrizUtilidad[i].append(int(linea[j]))
                matrizUtilidadMostrar += linea[j]
                #print(matrizUtilidadMostrar, '- ', j)
                if j < (SumaDeLosTiempos - 1):
                    matrizUtilidadMostrar += " "

        self.UtilidadesDeParcelas.SetValue(matrizUtilidadMostrar)
        info += "Utilidades de las parcelas: \n" + matrizUtilidadMostrar
        self.logger.SetValue(info)
        ##GuardarEnArchivo(info, matrizUtilidadMostrar)

    def ClickSolucionar(self, event):
            numeroParcelas = int(self.NumParcelas.GetValue())

            tiempoduracionparcelas = str(self.TiemposDuracion.GetValue()).split(' ')
            #print(tiempoduracionparcelas)
            TiemposDuracionParcelas = []
            for i in range(0, len(tiempoduracionparcelas)):
                #print(TiemposDuracionParcelas)
                TiemposDuracionParcelas.append(int(tiempoduracionparcelas[i]))
            ##print(TiemposDuracionParcelas)

            sumaTiemposParcelas = int(self.SumaTiempos.GetValue())

            matrizTextoEntrada =str(self.UtilidadesDeParcelas.GetValue()).split('\n')

            matrizUtilidades = []
            indice = 0;
            for i in range(0, numeroParcelas + (numeroParcelas - 1)):

                if matrizTextoEntrada[i] != '':
                    temp = matrizTextoEntrada[i].split(' ')
                    matrizUtilidades.append([])
                    for j in range(0, sumaTiemposParcelas):
                        matrizUtilidades[indice].append(int(temp[j]))
                    indice = indice + 1;

            tiempoInicio = time.time()
            numeroDeParcelas = numeroParcelas
            duracionCosecha = sumaTiemposParcelas
            D = TiemposDuracionParcelas

            U = matrizUtilidades

            cosecha = LpProblem('Cosecha', LpMaximize)

            X = [[ pulp.LpVariable('X_%s_%s'%(i,j), lowBound=0, upBound=1, cat="Integer") for j in range(duracionCosecha)] for i in range(numeroDeParcelas)]
            P = [ pulp.LpVariable('P_%s'%(i), lowBound=0, upBound=(duracionCosecha - D[i]), cat="Integer") for i in range(numeroDeParcelas)]

            FuncionObjetivo = [(U[i][j])*(X[i][j]) for i in range(numeroDeParcelas) for j in range(duracionCosecha)]

            cosecha += lpSum(FuncionObjetivo)

            for i in range(numeroDeParcelas):
                cosecha += lpSum(X[i][j] for j in range(duracionCosecha)) == 1

            for j in range(duracionCosecha):
                cosecha += lpSum(X[i][j] for i in range(numeroDeParcelas)) <= 1

            for i in range(numeroDeParcelas):
                for j in range(duracionCosecha):
                    cosecha += X[i][j]*(j + D[i] - 1) <= duracionCosecha - D[i] + 1
            """"
            for i in range(numeroDeParcelas):
                for j in range(duracionCosecha - D[i] + 1):
                    for fila in range(numeroDeParcelas):
                        if (fila != i):
                            y1 = pulp.LpVariable('Y1_%s_%s_%s'%(i,j,fila), lowBound=0, upBound=1, cat="Integer")
                            y2 = pulp.LpVariable('Y2_%s_%s_%s'%(i,j,fila), lowBound=0, upBound=1, cat="Integer")
                            restriccion = [X[fila][columna]*(columna + 1) for columna in range(duracionCosecha)]
                            cosecha += X[i][j]*((j + 2) + D[i] - 1) <= lpSum(restriccion) + (2*duracionCosecha)*(1 - y1)
                            cosecha += X[i][j]*j >= lpSum(restriccion) - (2*duracionCosecha)*(1 - y2)
                            cosecha += y1 + y2 == 1
            """

            for i in range(numeroDeParcelas):
                for parcela in range(numeroParcelas):
                    if i != parcela:
                        restriccion = [(X[i][columna])*(columna) for columna in range(duracionCosecha)]
                        cosecha += P[i] == lpSum(restriccion)

            indice = 0

            for i in range(numeroDeParcelas):
                for parcela in range(numeroDeParcelas):
                    if i != parcela:
                        y1 = pulp.LpVariable('Y1_%s_%s_%s'%(i,parcela, indice), lowBound=0, upBound=1, cat="Integer")
                        y2 = pulp.LpVariable('Y2_%s_%s_%s'%(i,parcela, indice), lowBound=0, upBound=1, cat="Integer")
                        cosecha += P[i] + D[i] <= P[parcela] + (2*duracionCosecha)*(1 - y1)
                        cosecha += P[i] >= P[parcela] - (2*duracionCosecha)*(1 - y2)
                        cosecha += y1 + y2 == 1
                        indice = indice + 1;

            cosecha.solve()
            tiempoFinal = time.time()

            tiempoTotal = tiempoFinal - tiempoInicio

            info = 'Variables de decision: \n\n'
            textoArchivo = ''
            for v in X:
                for dato in v:
                    info += '\t' + dato.name +  '=' +  str(dato.varValue) + '\n'
            for v in P:
                info += '\t' + v.name +  '=' +  str(v.varValue) + '\n'


            resultadoCosecha = []
            sumaDeUtilidades = 0
            indiceParcela = 0;

            for i in P:
                dato = i.varValue
                resultadoCosecha.append(int(dato))
                sumaDeUtilidades = sumaDeUtilidades + U[indiceParcela][int(dato)]
                indiceParcela = indiceParcela + 1;



            str1 = ' '.join(str(e) for e in resultadoCosecha)
            info += '\nSuma Utilidades: ' + str(sumaDeUtilidades) + '\n'
            info += 'Tiempos Cosechas ' + str1 + '\n'
            info += 'Tiempo Ejecución: ' + str(tiempoTotal*1000) + 'ms'

            textoArchivo = str(sumaDeUtilidades) + '\n' + str1

            GuardarEnArchivo(textoArchivo, 'SalidaResultados')

            self.logger.SetValue(info)







app = wx.App(False)
# Creamos el frame padre
frame = wx.Frame(None, title="Proyecto CyO", size=(780,520))
# Creamos el contenedor de pestañas
nb = wx.Notebook(frame)
# Añadimos los paneles con Addpage
nb.AddPage(panelInicio(nb), "Inicio")
#nb.AddPage(panelResultado(nb), "Resultados")
frame.Show()
app.MainLoop()
