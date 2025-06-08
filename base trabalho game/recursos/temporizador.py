import pygame
import time

class Temporizador:

    def __init__(self):
        self.inicio = time.time()
        self.ativo = True

    def reiniciar(self):
        self.inicio = time.time()
        self.ativo = True

    def pausar(self):
        self.ativo = False
        self.pausa = time.time()

    def continuar(self):
        if not self.ativo:
            pausa_duracao = time.time() - self.pausa
            self.inicio += pausa_duracao
            self.ativo = True

    def tempo_formatado(self):
        if self.ativo:
            tempo = time.time() - self.inicio
        else:
            tempo = self.pausa - self.inicio

        minutos = int(tempo // 60)
        segundos = int(tempo % 60)
        return f"{minutos:02d}:{segundos:02d}"

    def exibir(self, tela, fonte, pos_x=800, pos_y=15):
        texto = fonte.render(f"Tempo: {self.tempo_formatado()}", True, (255, 255, 255))
        tela.blit(texto, (pos_x, pos_y))
