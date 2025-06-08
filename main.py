import pygame
import random
import os
import tkinter as tk
from tkinter import messagebox
from recursos.funcoes import inicializarBancoDeDados
from recursos.funcoes import escreverDados
from recursos.temporizador import Temporizador
from datetime import datetime
import json
import speech_recognition as sr
import pyttsx3

print("Inicializando o Jogo! Criado por Ariel!")
print("Aperte Enter para iniciar o jogo")
pygame.init()
inicializarBancoDeDados()
tamanho = (1000,700)
relogio = pygame.time.Clock()
tela = pygame.display.set_mode( tamanho ) 
pygame.display.set_caption("NinjaX")

icone  = pygame.image.load("base/assets/icone.png")
pygame.display.set_icon(icone)
branco = (255,255,255)
preto = (0, 0 ,0 )
ninja = pygame.image.load("base/assets/ninja.png")
fundoStart = pygame.image.load("base/assets/inicioJogo.png")
fundoJogo = pygame.image.load("base/assets/fundoJogo.jpeg")
fundoDead = pygame.image.load("base/assets/fundoDead.jpeg")
kunai = pygame.image.load("base/assets/kunai.png")
shuriken = pygame.image.load("base/assets/shuriken.png")
objeto = pygame.image.load("base/assets/icone.png")
kunaiSound = pygame.mixer.Sound("base/assets/somkunai.mp3")
gameoverSound = pygame.mixer.Sound("base/assets/gameOver.mp3")
fonteMenu = pygame.font.SysFont("comicsans",18)
fonteMorte = pygame.font.SysFont("arial",120)
pygame.mixer.music.load("base/assets/musicaNinja.mp3")
nome = ""
engine = pyttsx3.init()
engine.setProperty('rate', 150)

def falar(texto):
    engine.say(texto)
    engine.runAndWait()

def ouvir_comando():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Diga algo...")
        audio = r.listen(source)
        try:
            comando = r.recognize_google(audio, language="pt-BR")
            print("Você disse:", comando)
            return comando.lower()
        except sr.UnknownValueError:
            print("Não entendi o que você disse.")
            return ""
        except sr.RequestError:
            print("Erro ao acessar o serviço de reconhecimento.")
            return ""
def boas_vindas(nome):
    larguraBotao = 300
    alturaBotao = 50
    fonteGrande = pygame.font.SysFont("arial", 40)
    fonteMedia = pygame.font.SysFont("comicsans", 24)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if botaoStart.collidepoint(evento.pos):
                    jogar()

        tela.fill((30, 30, 60))  # Cor de fundo

        # Texto de boas-vindas
        texto1 = fonteGrande.render(f"Bem-vindo, {nome}!", True, branco)
        tela.blit(texto1, (tamanho[0]//2 - texto1.get_width()//2, 100))

        # Instruções
        instrucoes = [
            "Evite ser atingido pelas kunais que caem do céu.",
            "Use as SETAS para se mover.",
            "Pressione ESPAÇO para pausar o jogo.",
            "Ganhe pontos sobrevivendo mais tempo!"
        ]
        for i, linha in enumerate(instrucoes):
            texto_instrucao = fonteMedia.render(linha, True, branco)
            tela.blit(texto_instrucao, (tamanho[0]//2 - texto_instrucao.get_width()//2, 200 + i * 40))

        # Botão central
        botaoStart = pygame.draw.rect(tela, branco, (tamanho[0]//2 - larguraBotao//2, 450, larguraBotao, alturaBotao), border_radius=15)
        textoBotao = fonteMenu.render("Começar Jogo", True, preto)
        tela.blit(textoBotao, (tamanho[0]//2 - textoBotao.get_width()//2, 460))

        pygame.display.update()
        relogio.tick(60)
def obter_nome():
    
    global nome
    largura_janela = 300
    altura_janela = 50

    def enviar():
        nonlocal root
        nome_digitado = entry_nome.get()
        if not nome_digitado:
            messagebox.showwarning("Aviso", "Por favor, digite seu nome!")
        else:
            globals()['nome'] = nome_digitado
            root.destroy()

    root = tk.Tk()
    root.title("Informe seu nickname")
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()
    pos_x = (largura_tela - largura_janela) // 2
    pos_y = (altura_tela - altura_janela) // 2
    root.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")
    root.protocol("WM_DELETE_WINDOW", enviar)

    entry_nome = tk.Entry(root)
    entry_nome.pack()

    botao = tk.Button(root, text="Enviar", command=enviar)
    botao.pack()

    root.mainloop()
    
def exibir_logs_na_tela(tela, fonte, dados):
    logs_formatados = []
    
    for nick, valores in dados.items():
        if len(valores) == 3:
            pontos, data, hora = valores
        elif len(valores) == 2:
            pontos, data  = valores
            
        else:
            continue  # dado inválido

        logs_formatados.append(f"{nick} - {pontos} pts em {data} às {hora}")

   # Pega apenas os últimos 5 logs
    ultimos_logs = logs_formatados[-5:]

    # Exibir na tela
    y = 500
    for log in ultimos_logs:
        texto = fonte.render(log, True, (255, 255, 255))
        tela.blit(texto, (50, y))
        y += 30

def pausar_jogo(temporizador):
    temporizador.pausar()
    pygame.mixer.music.pause()  # pausa música
    pausado = True
    while pausado:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    pausado = False
                    pygame.mixer.music.unpause()  # retoma música
                    temporizador.continuar()
        tela.fill((50, 50, 50))  # fundo escuro para tela de pausa
        texto_pausa = fonteMorte.render("PAUSADO", True, (255, 255, 255))
        subtexto = fonteMenu.render("Pressione ESPAÇO para continuar", True, (255, 255, 255))
        tela.blit(texto_pausa, (tamanho[0]//2 - 300, tamanho[1]//4 + 100))
        tela.blit(subtexto, (tamanho[0]//2 - 170, tamanho[1]//3 + 180))
        pygame.display.update()
        relogio.tick(30)

def jogar():
    temporizador = Temporizador()
    
    posicaoXPersona = 400
    posicaoYPersona = 700
    movimentoXPersona  = 0
    movimentoYPersona  = 0
    posicaoXkunai = 400
    posicaoYkunai = -240
    velocidadekunai = 1
    pygame.mixer.Sound.play(kunaiSound)
    pygame.mixer.music.play(-1)
    pontos = 0
    posicaoXInimigo = random.randint(0, 900)
    posicaoYInimigo = random.randint(0, 600)
    velocidadeXInimigo = random.choice([-2, 2])
    velocidadeYInimigo = random.choice([-2, 2])
    larguraPersona = 200
    alturaPersona = 250
    larguakunai  = 100
    alturakunai  = 152
    dificuldade  = 30
    tamanho_pulso = 50
    aumentando = True

    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RIGHT:
                movimentoXPersona = 15
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_LEFT:
                movimentoXPersona = -15
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_RIGHT:
                movimentoXPersona = 0
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_LEFT:
                movimentoXPersona = 0
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    pausar_jogo(temporizador)
                 
        posicaoXPersona = posicaoXPersona + movimentoXPersona            
        posicaoYPersona = posicaoYPersona + movimentoYPersona            
        
        if posicaoXPersona < 0 :
            posicaoXPersona = 15
        elif posicaoXPersona >790:
            posicaoXPersona = 780
            
        if posicaoYPersona < 0 :
            posicaoYPersona = 15
        elif posicaoYPersona > 473:
            posicaoYPersona = 463
        # Animação de pulso
        if aumentando:
            tamanho_pulso += 1
            if tamanho_pulso >= 50:
                aumentando = False
        else:
            tamanho_pulso -= 1
            if tamanho_pulso <= 30:
                aumentando = True
        # Redimensiona imagem com base no pulso
        objeto_redimensionado = pygame.transform.scale(objeto, (tamanho_pulso, tamanho_pulso))

        # Desenha no canto superior direito
        pos_x = tamanho[0] - tamanho_pulso - 10
        pos_y = 10
            
        tela.fill(branco)
        tela.blit(fundoJogo, (0,0) )
        tela.blit(shuriken, (posicaoXInimigo, posicaoYInimigo))
        tela.blit( ninja, (posicaoXPersona, posicaoYPersona) )
        temporizador.exibir(tela, fonteMenu)
        posicaoYkunai = posicaoYkunai + velocidadekunai
        if posicaoYkunai > 700:
            posicaoYkunai = -240
            pontos = pontos + 1
            velocidadekunai = velocidadekunai + 1
            posicaoXkunai = random.randint(0,900)
            pygame.mixer.Sound.play(kunaiSound)
        # Movimento randômico do inimigo
        posicaoXInimigo += velocidadeXInimigo
        posicaoYInimigo += velocidadeYInimigo
        if posicaoXInimigo < 0 or posicaoXInimigo > 950:
            velocidadeXInimigo *= -1
        if posicaoYInimigo < 0 or posicaoYInimigo > 650:
             velocidadeYInimigo *= -1    
                   
        tela.blit( kunai, (posicaoXkunai, posicaoYkunai) )
        tela.blit(objeto_redimensionado, (pos_x, pos_y))
        
        texto = fonteMenu.render("Pressione Espaço para pausar o jogo! Pontos: " +str(pontos), True, branco ) 
        tela.blit(texto, (15,15)) 
        
        
        pixelsPersonaX = list(range(posicaoXPersona, posicaoXPersona+larguraPersona))
        pixelsPersonaY = list(range(posicaoYPersona, posicaoYPersona+alturaPersona))
        pixelskunaiX = list(range(posicaoXkunai, posicaoXkunai + larguakunai))
        pixelskunaiY = list(range(posicaoYkunai, posicaoYkunai + alturakunai))
        
        os.system("cls")
        if  len( list( set(pixelskunaiY).intersection(set(pixelsPersonaY))) ) > dificuldade:
            if len(list(set(pixelskunaiX).intersection(set(pixelsPersonaX)))) > dificuldade:
                from recursos.funcoes import escreverDados
                escreverDados(nome, pontos)  
                dead()

                
        else:
            print("Ainda Vivo, mas por pouco!")
        
        
            
        pygame.display.update()
        relogio.tick(60)
         

def start():
    larguraButtonStart = 150
    alturaButtonStart  = 40
    larguraButtonQuit = 150
    alturaButtonQuit  = 40
    

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 140
                    alturaButtonStart  = 35
                if quitButton.collidepoint(evento.pos):
                    larguraButtonQuit = 140
                    alturaButtonQuit  = 35

                
            elif evento.type == pygame.MOUSEBUTTONUP:
                # Verifica se o clique foi dentro do retângulo
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 150
                    alturaButtonStart  = 40
                    obter_nome()
                    boas_vindas(nome)
                    jogar()
                if quitButton.collidepoint(evento.pos):
                    larguraButtonQuit = 150
                    alturaButtonQuit  = 40
                    quit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_v:
                    comando = ouvir_comando()
                if "iniciar" in comando:
                    falar("Iniciando o jogo")
                    obter_nome()
                    boas_vindas(nome)
                    jogar()
                elif "sair" in comando:
                    falar("Saindo do jogo")
                    quit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    pausar_jogo()      
            
        tela.fill(branco)
        tela.blit(fundoStart, (0,0) )

        startButton = pygame.draw.rect(tela, branco, (10,10, larguraButtonStart, alturaButtonStart), border_radius=15)
        startTexto = fonteMenu.render("Iniciar Game", True, preto)
        tela.blit(startTexto, (25,12))
        
        quitButton = pygame.draw.rect(tela, branco, (10,60, larguraButtonQuit, alturaButtonQuit), border_radius=15)
        quitTexto = fonteMenu.render("Sair do Game", True, preto)
        tela.blit(quitTexto, (25,62))
        
        pygame.display.update()
        relogio.tick(60)

def dead():
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(gameoverSound)

    larguraButtonStart = 150
    alturaButtonStart = 40
    larguraButtonQuit = 150
    alturaButtonQuit = 40
    
    try:
     with open("log.dat", "r") as arquivo:
            dados = json.load(arquivo)
    except (json.JSONDecodeError, FileNotFoundError):
        dados = {}
        
    fonteLog = pygame.font.SysFont("comicsans", 20)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 140
                    alturaButtonStart = 35
                if quitButton.collidepoint(evento.pos):
                    larguraButtonQuit = 140
                    alturaButtonQuit = 35
            elif evento.type == pygame.MOUSEBUTTONUP:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 150
                    alturaButtonStart = 40
                    obter_nome()
                    boas_vindas(nome)
                    jogar()
                if quitButton.collidepoint(evento.pos):
                    larguraButtonQuit = 150
                    alturaButtonQuit = 40
                    quit()
                    
        tela.fill(preto)
        tela.blit(fundoDead, (0, 0))
    
        startButton = pygame.draw.rect(tela, branco, (10, 10, larguraButtonStart, alturaButtonStart), border_radius=15)
        startTexto = fonteMenu.render("Iniciar Game", True, preto)
        tela.blit(startTexto, (25, 12))

        quitButton = pygame.draw.rect(tela, branco, (10, 60, larguraButtonQuit, alturaButtonQuit), border_radius=15)
        quitTexto = fonteMenu.render("Sair do Game", True, preto)
        tela.blit(quitTexto, (25, 62))
        
        exibir_logs_na_tela(tela, fonteLog, dados)

        pygame.display.update()
        relogio.tick(60)

start()

