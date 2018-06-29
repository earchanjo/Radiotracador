#IMPORT DOS MODULOS A SER USADOS
from tkinter import* #PARA INTERFACE GRAFICA
import matplotlib.pyplot as plt#PARA PLOTAGEM DO GRAFICO
from mpl_toolkits.mplot3d import Axes3D#PLOTAGEM 3D
import numpy as np#AUXILIO EM FUNCOES MATEMATICAS

gui = Tk()
#JANELA É A INTERFACE PRINCIPAL DO PROGRAMA QUE VAI INICIAR OS GRAFICOS PARA ANALISE
class Janela():
    def __init__(self,gui):
        self.cria_widgets()
        self.packs()

    def cria_widgets(self):#CRIACAO DOS WIDGETS
        self.f1 = Frame(gui,width=300,height=300,bg='white')
        self.f2 = Frame(gui)
        #self.c1 = Canvas(self.f1,width=300,height=300,bg="white")

        #Buttons
        self.plot = Button(self.f2,text='Plotar',command=self.funcao)
        self.tempo_real = Button(self.f2,text='Tempo Real',command=self.funcao2)
        #Labels
        self.titulo = Label(self.f1,text='Tracer',font=('Verdana',20,'bold'),bg='white',fg='black')
        self.opcoes = Label(self.f2,text='Analise',font=('Verdana',20,'bold'))
        self.aviso = Label(self.f1,text='Nenhum dado selecionado para analise...',font=('Verdana',20,'bold'),fg='blue',bg='white')
        #Entrys
        self.ent = Entry(self.f2)#Entrada para o usuario entrar com o arquivo de resultados do sensor

        #Como nosso projeto não tem a possibilidade de ter dados diretamente dos sensores de radiação,
        #Criamos um simulador de dados para diferentes situações encontradas no transporte
    def funcao(self):
        arq = open('/home/chamelon/Hackathon/sensor1/'+str(self.ent.get()),'r')
        linhas = arq.readlines()
        x=[]
        y=[]
        z=[]
        rad=[]
        for l in linhas:
            lista = l.split()
            x.append(float(lista[0]))
            y.append(float(lista[1]))
            z.append(float(lista[2]))
            rad.append(float(lista[3]))
        fig = plt.figure()
        ax = fig.add_subplot(2,2,1,projection='3d')
        ax.plot(x,y,z, label='curva parametrizada')
        ax.legend()
        ax.set_xlabel('Eixo X')
        ax.set_ylabel('Eixo Y')
        ax.set_zlabel('Eixo Z')
        arq.close()
        #grafico da radiacao
        ax = fig.add_subplot(2,2,2)
        ax.plot(x,rad,'r-')
        #coordenadas polares
        pol = fig.add_subplot(2,2,3,projection='polar')
        tetha = np.linspace(0,2*np.pi)
        pol.plot(tetha,y[0:50])
        ###########
        plt.show()
        plt.ion()
    def funcao2(self):
        #Funcao2 é responsavel por plotar os graficos em tempo real, para auxiliar na observação do comportamento do fluido.
        plt.ion() ## Note this correction
        fig= plt.figure()
        #plt.axis([0,1000,0,1,0,1])
        arq = open('/home/chamelon/Hackathon/sensor1/'+str(self.ent.get()),'r')
        arq_res = open('/home/chamelon/Hackathon/Resultados/resultados.txt','w')
        i=0
        x = list()
        y = list()
        z = list()
        ax = fig.add_subplot(projection='3d')
        inicio_anomalia = 0
        final_anomalia = 0
        la = [0]
        s = [20*4**n for n in range(len(la))]
        while i <1000:
            dados = arq.readline().split()
            x.append(float(dados[0]))
            y.append(float(dados[1]))
            z.append(float(dados[2]))
            plt.scatter(x,y,c='black',marker='^',s=s)
            #ax.plot(x,y,z)
            plt.show()
            plt.pause(0.0001)
            if i >=7:
                refx = (x[2]-x[1]) #valor de referencia para a taxa de variacao da coordenada, para poder reconhecer a anomalia no instante de acontecimento e no final
                refy = (y[2]-y[1]) ####
                if ((x[i]-x[i-1]) != (x[i-1]-x[i-2])) or ((y[i]-y[i-1]) != (y[i-1]-y[i-2])):# checa se a taxa de variacao das coordenadas se alterou
                    self.aviso.configure(text="AVISO:Alteração do fluxo em (" + str(x[i])+","+str(y[i])+","+str(z[i])+")",fg='red')#altera o banner de avisos quando encontra uma coordenada onde há anomalia no movimento
                    self.aviso.pack()
                    arq_res.write("Anomalia: "+ str(dados)+"\n")
                if (x[i]-x[i-1]) == refx:
                    self.aviso.configure(text="AVISO:Fluxo regular em (" + str(x[i])+","+str(y[i])+","+str(z[i])+")",fg='blue')
                    self.aviso.pack()
                    arq_res.write(str(dados)+"\n")




            i+=1
        arq_res.close()



        #Funcao que irá gerenciar as montagens de widgets na tela do programa
    def packs(self):
        self.f1.pack(side=TOP)
        self.f2.pack(side=TOP)
        self.titulo.pack(side=TOP)
        self.aviso.pack()
        #self.c1.pack(side=TOP)

        self.opcoes.pack(side=TOP)
        self.plot.pack(side=LEFT)
        self.ent.pack(side=LEFT)
        self.tempo_real.pack(side=LEFT)



Janela(gui)
gui.mainloop()
