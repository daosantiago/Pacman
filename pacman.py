import random
import pygame as pg
from abc import ABCMeta, abstractmethod

LARANJA = (255, 140,0)
ROSA = (255, 15, 192)
CIANO = (0, 255, 255)
BRANCO = (255, 255, 255)
AMARELO = (255, 255, 0)
AZUL = (0, 0, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
VELOCIDADE = 1
RAIO = 10
VEL_BOCA = 3
CIMA = 1
BAIXO = 2
DIREITA = 3
ESQUERDA = 4


class ElementoJogo(metaclass=ABCMeta):
    @abstractmethod
    def pintar(self, tela):
        pass

    @abstractmethod
    def calcular_regras(self):
        pass

    @abstractmethod
    def processar_eventos(self, eventos):
        pass


class Movivel(metaclass=ABCMeta):
    @abstractmethod
    def aceitar_movimento(self):
        pass

    @abstractmethod
    def recusar_movimento(self, direcoes):
        pass

    @abstractmethod
    def esquina(self, direcoes):
        pass


class Cenario(ElementoJogo):
    def __init__(self, tamanho, pac):
        self.pac = pac
        self.vidas = 5
        self.vidas = 5
        self.moviveis = []
        self.tamanho = tamanho
        self.pontos = 0
        # Estados possíveis 0-Jogando, 1-Pausado, 2-GameOver, 3- Vitoria
        self.estado = 0
        self.matrix = [
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
             2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2,
             1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2,
             1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1,
             1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2,
             1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2,
             1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2,
             2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2,
             2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2,
             1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2,
             1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2,
             1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1,
             1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 0, 0, 0,
             0, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 0, 0, 0, 0,
             0, 0, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 2, 0, 0, 0, 0,
             0, 0, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 0, 0, 0, 0,
             0, 0, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2,
             2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1,
             1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2,
             1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2,
             1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2,
             1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2,
             2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2,
             2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2,
             1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2,
             1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1,
             1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2,
             1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2,
             1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
             2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
        ]

    def adicionar_movivel(self, movivel: Movivel) -> None:
        self.moviveis.append(movivel)

    def processar_eventos(self, eventos):
        for e in eventos:
            if e.type == pg.QUIT or (e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE):
                exit()

            if e.type == pg.KEYDOWN:
                if e.key == pg.K_p:
                    if self.estado == 0:
                        self.estado = 1
                    elif self.estado == 1:
                        self.estado = 0

    def pintar_pontos(self, tela):
        pontos_x = 30 * self.tamanho
        img_pontos = fonte.render(f"Score: {self.pontos}", True, AMARELO)
        vidas_img = fonte.render(f"Vidas {self.vidas}", True, AMARELO)
        tela.blit(img_pontos, (pontos_x, 50))
        tela.blit(vidas_img, (pontos_x, 100))

    def pintar_linha(self, tela, numero_linha, linha):
        for numero_coluna, coluna in enumerate(linha):
            x = numero_coluna * self.tamanho
            y = numero_linha * self.tamanho
            cor = PRETO

            if coluna == 2:
                cor = AZUL

            pg.draw.rect(tela, cor, (x, y, self.tamanho, self.tamanho), 0)

            if coluna == 1:
                half = self.tamanho // 2
                pg.draw.circle(tela, AMARELO, (x + half, y + half),
                               self.tamanho // 10, 0)

    def pintar(self, tela):
        self.pintar_jogando(tela)

        if self.estado == 1:
            self.pintar_pausado(tela)
        elif self.estado == 2:
            self.pintar_gameover(tela)
        elif self.estado == 3:
            self.pintar_vitoria(tela)

    def pintar_vitoria(self, tela):
        self.pintar_texto_centro(tela, "P A R A B É N S  V O C Ê  V E N C E U")


    def pintar_texto_centro(self, tela, texto):
        texto_img = fonte.render(texto, True, AMARELO)
        texto_x = (tela.get_width() - texto_img.get_width()) // 2
        texto_y = (tela.get_height() - texto_img.get_height()) // 2
        tela.blit(texto_img, (texto_x, texto_y))

    def pintar_gameover(self, tela):
        self.pintar_texto_centro(tela, "G A M E  O V E R")

    def pintar_pausado(self, tela):
        self.pintar_texto_centro(tela, "P A U S A D O")


    def pintar_jogando(self, tela):
        for numero_linha, linha in enumerate(self.matrix):
            self.pintar_linha(tela, numero_linha, linha)

        self.pintar_pontos(tela)

    def get_direcoes(self, linha, coluna):
        direcoes = []
        if self.matrix[int(linha - 1)][int(coluna)] != 2:
            direcoes.append(CIMA)
        if self.matrix[int(linha + 1)][int(coluna)] != 2:
            direcoes.append(BAIXO)
        if self.matrix[int(linha)][int(coluna - 1)] != 2:
            direcoes.append(ESQUERDA)
        if self.matrix[int(linha)][int(coluna + 1)] != 2:
            direcoes.append(DIREITA)

        return direcoes

    def calcular_regras(self):
        if self.estado == 0:
            self.calcular_regras_jogando()
        elif self.estado == 1:
            self.calcular_regras_pausado()
        elif self.estado == 2:
            self.calcular_regras_gameover()

    def calcular_regras_gameover(self):
        pass

    def calcular_regras_pausado(self):
        pass

    def calcular_regras_jogando(self):
        for mov in self.moviveis:
            lin = int(mov.linha)
            col = int(mov.coluna)
            lin_intencao = int(mov.linha_intencao)
            col_intencao = int(mov.coluna_intencao)
            direcoes = self.get_direcoes(lin, col)

            if len(direcoes) >= 3:
                mov.esquina(direcoes)
            if isinstance(mov, Fantasma) and mov.linha == self.pac.linha and mov.coluna == self.pac.coluna:
                self.vidas -= 1
                if self.vidas <= 0:
                    self.estado = 2
                else:
                    self.pac.linha = 1
                    self.pac.coluna = 1
            else:
                if 0 <= col_intencao < 28 and 0 <= lin_intencao < 29 and self.matrix[lin_intencao][col_intencao] != 2:
                    mov.aceitar_movimento()
                    if isinstance(mov, Pacman) and self.matrix[lin][col] == 1:
                        self.pontos += 1
                        self.matrix[lin][col] = 0
                        if self.pontos >= 306:
                            self.estado = 3
                else:
                    mov.recusar_movimento(direcoes)



class Pacman(Movivel, ElementoJogo):
    def __init__(self, tamanho):
        self.coluna = 1
        self.linha = 1
        self.centro_x = 400
        self.centro_y = 300
        self.tamanho = tamanho
        self.raio = int(self.tamanho // 2)
        self.abertura = 0
        self.velocidade_abertura = 10
        self.vel_x = 0
        self.vel_y = 0
        self.coluna_intencao = self.coluna
        self.linha_intencao = self.linha
        self.direcao = DIREITA
        self.direcao_intencao = 0

    def recusar_movimento(self, direcoes):
        self.linha_intencao = self.linha

    def esquina(self, direcoes):
        pass

    def aceitar_movimento(self):
        if self.linha_intencao != self.linha or self.coluna_intencao != self.coluna:
            self.linha = self.linha_intencao
            self.coluna = self.coluna_intencao
            self.direcao = self.direcao_intencao

    def processar_eventos_mouse(self, eventos):
        delay = 100000
        for e in eventos:
            if e.type == pg.MOUSEMOTION:
                mouse_x, mouse_y = e.pos
                self.coluna = (mouse_x - self.centro_x) / delay
                self.linha = (mouse_y - self.centro_y) / delay

    def processar_eventos(self, eventos):
        for e in eventos:
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_RIGHT:
                    self.vel_x = VELOCIDADE
                elif e.key == pg.K_LEFT:
                    self.vel_x = -VELOCIDADE
                elif e.key == pg.K_UP:
                    self.vel_y = -VELOCIDADE
                elif e.key == pg.K_DOWN:
                    self.vel_y = VELOCIDADE

            if e.type == pg.KEYUP:
                self.vel_x = 0
                self.vel_y = 0

    def calcular_regras(self):
        self.coluna_intencao = self.coluna + self.vel_x
        self.linha_intencao = self.linha + self.vel_y
        self.direcao_intencao = self.calcular_direcao_intencao()

        self.centro_x = int(self.coluna * self.tamanho + self.raio)
        self.centro_y = int(self.linha * self.tamanho + self.raio)
        self.calcular_direcao_intencao()

    def calcular_direcao_intencao(self):
        if self.coluna_intencao > self.coluna:
            self.direcao_intencao = DIREITA
        elif self.linha_intencao > self.linha:
            self.direcao_intencao = BAIXO
        elif self.coluna_intencao < self.coluna:
            self.direcao_intencao = ESQUERDA
        elif self.linha_intencao < self.linha:
            self.direcao_intencao = CIMA

    def pintar(self, tela):
        self.abertura += self.velocidade_abertura
        if self.abertura >= self.raio:
            self.velocidade_abertura = -10
        if self.abertura <= 0:
            self.velocidade_abertura = 10

        # Desenhar o corpo do pacman
        pg.draw.circle(tela, AMARELO, (self.centro_x,
                                       self.centro_y), self.raio, 0)

        canto_boca = (self.centro_x, self.centro_y)
        labio_superior, labio_inferior = self.calcular_boca()
        pontos_boca = [canto_boca, labio_superior, labio_inferior]

        pg.draw.polygon(tela, PRETO, pontos_boca, 0)

        olho_x = int(self.centro_x + self.raio / 3)
        olho_y = int(self.centro_y - self.raio * 0.70)
        olho_raio = int(self.raio / 10)
        pg.draw.circle(tela, PRETO, (olho_x, olho_y), olho_raio, 0)

    def calcular_boca(self):
        if self.direcao == DIREITA:
            labio_superior = (self.centro_x + self.raio, self.centro_y - self.abertura)
            labio_inferior = (self.centro_x + self.raio, self.centro_y + self.abertura)
        elif self.direcao == ESQUERDA:
            labio_superior = (self.centro_x - self.raio, self.centro_y - self.abertura)
            labio_inferior = (self.centro_x - self.raio, self.centro_y + self.abertura)
        elif self.direcao == CIMA:
            labio_superior = (self.centro_x - self.abertura, self.centro_y - self.raio)
            labio_inferior = (self.centro_x + self.abertura, self.centro_y - self.raio)
        elif self.direcao == BAIXO:
            labio_superior = (self.centro_x - self.abertura, self.centro_y + self.raio)
            labio_inferior = (self.centro_x + self.abertura, self.centro_y + self.raio)

        return labio_superior, labio_inferior



class Fantasma(ElementoJogo):
    def __init__(self, cor, tamanho):
        self.coluna = 6
        self.linha = 2
        self.tamanho = tamanho
        self.cor = cor
        self.velocidade = 0.5
        self.direcao = BAIXO
        self.linha_intencao = self.linha
        self.coluna_intencao = self.coluna

    def pintar(self, tela):
        fatia = self.tamanho // 8
        px = int(self.coluna * self.tamanho)
        py = int(self.linha * self.tamanho)
        contorno = [(px, py + self.tamanho),
                    (px + fatia, py + fatia * 2),
                    (px + fatia * 3, py + fatia // 2),
                    (px + fatia * 3, py),
                    (px + fatia * 5, py),
                    (px + fatia * 6, py + fatia // 2),
                    (px + fatia * 7, py + fatia * 2),
                    (px + self.tamanho, py + self.tamanho)]
        pg.draw.polygon(tela, self.cor, contorno, 0)

        olho_raio_ext = fatia
        olho_raio_int = fatia // 2

        olho_e_x = int(px + fatia * 2.5)
        olho_e_y = int(py + fatia * 2.5)

        olho_d_x = int(px + fatia * 5.5)
        olho_d_y = int(py + fatia * 2.5)

        pg.draw.circle(tela, BRANCO, (olho_e_x, olho_e_y), olho_raio_ext, 0)
        pg.draw.circle(tela, PRETO, (olho_e_x, olho_e_y), olho_raio_int, 0)

        pg.draw.circle(tela, BRANCO, (olho_d_x, olho_d_y), olho_raio_ext, 0)
        pg.draw.circle(tela, PRETO, (olho_d_x, olho_d_y), olho_raio_int, 0)

    def calcular_regras(self):
        if self.direcao == CIMA:
            self.linha_intencao -= self.velocidade
        elif self.direcao == BAIXO:
            self.linha_intencao += self.velocidade
        elif self.direcao == ESQUERDA:
            self.coluna_intencao -= self.velocidade
        elif self.direcao == DIREITA:
            self.coluna_intencao += self.velocidade

    def mudar_direcao(self, direcoes):
        self.direcao = random.choice(direcoes)

    def esquina(self, direcoes):
        self.mudar_direcao(direcoes)

    def aceitar_movimento(self):
        self.linha = self.linha_intencao
        self.coluna = self.coluna_intencao

    def recusar_movimento(self, direcoes):
        self.linha_intencao = self.linha
        self.coluna_intencao = self.coluna
        self.mudar_direcao(direcoes)

    def processar_eventos(self, eventos):
        pass


if __name__ == '__main__':
    pg.init()

    tela = pg.display.set_mode((800, 640), 0)
    fonte = pg.font.SysFont('arial', 24, True, False)
    clock = pg.time.Clock()

    size = 600 // 30
    pac = Pacman(size)
    blinky = Fantasma(VERMELHO, size)
    inky = Fantasma(CIANO, size)
    clyde = Fantasma(LARANJA, size)
    pinky = Fantasma(ROSA, size)
    cenario = Cenario(size, pac)
    cenario.adicionar_movivel(pac)
    cenario.adicionar_movivel(blinky)
    cenario.adicionar_movivel(inky)
    cenario.adicionar_movivel(clyde)
    cenario.adicionar_movivel(pinky)

    while True:
        clock.tick(24)
        # Calcular as regras
        pac.calcular_regras()
        blinky.calcular_regras()
        inky.calcular_regras()
        clyde.calcular_regras()
        pinky.calcular_regras()
        cenario.calcular_regras()

        # Renderiza
        tela.fill(PRETO)
        cenario.pintar(tela)
        pac.pintar(tela)
        blinky.pintar(tela)
        inky.pintar(tela)
        clyde.pintar(tela)
        pinky.pintar(tela)
        pg.display.update()
        pg.time.delay(50)

        eventos = pg.event.get()

        pac.processar_eventos(eventos)
        cenario.processar_eventos(eventos)