#!/usr/bin/python
#-*- coding: utf-8 -*-
import wx
import time

def GuardarEnArchivo(texto, nombre):
    archivo = open(nombre+'.txt', 'w')
    archivo.write(texto)
    archivo.close()


class panelInicio(wx.Panel):
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.quote = wx.StaticText(self, label="integrantes: \n Erik López - 1430406 \n Alejandro Valencia R - 1427368 \n Juan Jose Varela - 1424388", pos=(10, 10))

        self.logger = wx.TextCtrl(self, pos=(300,20), size=(450,420), style=wx.TE_MULTILINE | wx.TE_READONLY)

        self.botonCargar = wx.Button(self, label="Cargar Datos", pos=(178 , 90), size = (85, 30))
        self.Bind(wx.EVT_BUTTON, self.ClickCargar, self.botonCargar)

        self.lblSeleccionar = wx.StaticText(self, label="Seleccionar Archivo :", pos=(10,90))

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

            sumaTiemposPacerlas = int(self.SumaTiempos.GetValue())

            matrizTextoEntrada =str(self.UtilidadesDeParcelas.GetValue()).split('\r\n')
            print(matrizTextoEntrada)
            matrizUtilidades = []
            for i in range(0, numeroParcelas):
               temp = matrizTextoEntrada[i].split(' ')
               matrizUtilidades.append([])
               for j in range(0, len(TiemposDuracionParcelas)):
                matrizUtilidades[i].append(int(temp[j]))

            print(matrizUtilidades)
            
   




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