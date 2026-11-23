
import pygame
import random
import math

# Inicialização
pygame.init()

LARGURA = 800
ALTURA = 800
FPS = 60

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Brick Breaker Youtube")

relogio = pygame.time.Clock()

# Cores
cores = {
    "branca": (255, 255, 255),
    "preta": (0, 0, 0),
    "amarela": (255, 255, 0),
    "azul": (0, 100, 255),
    "verde": (0, 200, 0),
    "vermelha": (255, 0, 0),
    "cinza": (100, 100, 100)
}

# Fontes
fonte = pygame.font.Font(None, 40)
fonte_grande = pygame.font.Font(None, 70)

# Jogador
tamanho_jogador = 110
altura_jogador = 15
velocidade_jogador = 8

# Bola
tamanho_bola = 15
velocidade_bola = 6

# Blocos
qtde_blocos_linha = 8
qtde_linhas_blocos = 5
qtde_total_blocos = (
    qtde_blocos_linha * qtde_linhas_blocos
)


def criar_blocos():
    distancia = 5
    altura_bloco = 20

    largura_bloco = (
        LARGURA - (qtde_blocos_linha + 1) * distancia
    ) / qtde_blocos_linha

    blocos = []

    for j in range(qtde_linhas_blocos):
        for i in range(qtde_blocos_linha):

            x = distancia + i * (
                largura_bloco + distancia
            )

            y = 70 + j * (
                altura_bloco + distancia
            )

            bloco = pygame.Rect(
                x, y, largura_bloco, altura_bloco
            )

            blocos.append(bloco)

    return blocos


def iniciar_jogo():

    jogador = pygame.Rect(
        LARGURA // 2 - tamanho_jogador // 2,
        ALTURA - 50,
        tamanho_jogador,
        altura_jogador
    )

    bola = pygame.Rect(
        LARGURA // 2,
        ALTURA - 100,
        tamanho_bola,
        tamanho_bola
    )

    movimento_bola = [
        random.choice([-4, 4]),
        -velocidade_bola
    ]

    blocos = criar_blocos()

    pontuacao = 0

    return jogador, bola, movimento_bola, blocos, pontuacao


def desenhar_texto(texto, fonte, cor, x, y):
    imagem = fonte.render(texto, True, cor)
    tela.blit(imagem, (x, y))


def desenhar_jogo(jogador, bola, blocos, pontuacao):

    tela.fill(cores["preta"])

    # Jogador
    pygame.draw.rect(
        tela, cores["azul"], jogador,
        border_radius=8
    )

    # Bola
    pygame.draw.ellipse(
        tela, cores["branca"], bola
    )

    # Blocos
    for i, bloco in enumerate(blocos):

        cor = [
            (255, 70, 70),
            (255, 150, 0),
            (255, 255, 0),
            (0, 200, 100),
            (0, 150, 255)
        ][i // qtde_blocos_linha]

        pygame.draw.rect(
            tela, cor, bloco,
            border_radius=3
        )

    # Pontuação
    desenhar_texto(
        f"Pontuacao: {pontuacao}",
        fonte,
        cores["amarela"],
        20,
        ALTURA - 35
    )


def movimentar_jogador(jogador):

    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_RIGHT]:
        jogador.x += velocidade_jogador

    if teclas[pygame.K_LEFT]:
        jogador.x -= velocidade_jogador

    # Impedir que saia da tela
    if jogador.left < 0:
        jogador.left = 0

    if jogador.right > LARGURA:
        jogador.right = LARGURA


def movimentar_bola(
    bola, movimento_bola, jogador, blocos
):

    bola_anterior = bola.copy()

    # Movimento horizontal e vertical
    bola.x += movimento_bola[0]
    bola.y += movimento_bola[1]

    # Colisão com parede esquerda
    if bola.left <= 0:
        bola.left = 0
        movimento_bola[0] = abs(movimento_bola[0])

    # Colisão com parede direita
    if bola.right >= LARGURA:
        bola.right = LARGURA
        movimento_bola[0] = -abs(movimento_bola[0])

    # Colisão com teto
    if bola.top <= 0:
        bola.top = 0
        movimento_bola[1] = abs(movimento_bola[1])

    # Colisão com jogador
    if (
        bola.colliderect(jogador)
        and movimento_bola[1] > 0
        and bola_anterior.bottom <= jogador.top
    ):

        bola.bottom = jogador.top

        # Calcular o ângulo conforme o local do impacto
        centro_bola = bola.centerx
        centro_jogador = jogador.centerx

        diferenca = (
            centro_bola - centro_jogador
        ) / (tamanho_jogador / 2)

        diferenca = max(-1, min(1, diferenca))

        movimento_bola[0] = diferenca * 7

        movimento_bola[1] = -math.sqrt(
            max(
                1,
                velocidade_bola ** 2
                - movimento_bola[0] ** 2
            )
        )

    # Colisão com blocos
    for bloco in blocos[:]:

        if bola.colliderect(bloco):

            blocos.remove(bloco)

            # Verificar o lado da colisão
            if bola_anterior.bottom <= bloco.top:
                movimento_bola[1] = -abs(
                    movimento_bola[1]
                )

            elif bola_anterior.top >= bloco.bottom:
                movimento_bola[1] = abs(
                    movimento_bola[1]
                )

            elif bola_anterior.right <= bloco.left:
                movimento_bola[0] = -abs(
                    movimento_bola[0]
                )

            elif bola_anterior.left >= bloco.right:
                movimento_bola[0] = abs(
                    movimento_bola[0]
                )

            else:
                movimento_bola[1] *= -1

            break

    # Verificar se a bola caiu
    if bola.top > ALTURA:
        return False

    return True


def mostrar_fim_jogo(vitoria):

    tela.fill(cores["preta"])

    if vitoria:
        mensagem = "VITORIA!"
        cor = cores["verde"]
    else:
        mensagem = "GAME OVER!"
        cor = cores["vermelha"]

    texto = fonte_grande.render(
        mensagem, True, cor
    )

    tela.blit(
        texto,
        texto.get_rect(
            center=(LARGURA // 2, ALTURA // 2 - 40)
        )
    )

    desenhar_texto(
        "Pressione R para reiniciar",
        fonte,
        cores["branca"],
        220,
        ALTURA // 2 + 30
    )

    desenhar_texto(
        "Pressione ESC para sair",
        fonte,
        cores["branca"],
        245,
        ALTURA // 2 + 80
    )


# Iniciar jogo
jogador, bola, movimento_bola, blocos, pontuacao = (
    iniciar_jogo()
)

fim_jogo = False
vitoria = False
jogo_terminado = False

# Loop principal
while not fim_jogo:

    relogio.tick(FPS)

    # Eventos
    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            fim_jogo = True

        if evento.type == pygame.KEYDOWN:

            if evento.key == pygame.K_ESCAPE:
                fim_jogo = True

            if (
                evento.key == pygame.K_r
                and jogo_terminado
            ):

                (
                    jogador,
                    bola,
                    movimento_bola,
                    blocos,
                    pontuacao
                ) = iniciar_jogo()

                jogo_terminado = False
                vitoria = False

    if not jogo_terminado:

        # Atualizar jogador
        movimentar_jogador(jogador)

        # Atualizar bola
        bola_em_jogo = movimentar_bola(
            bola,
            movimento_bola,
            jogador,
            blocos
        )

        # Atualizar pontuação
        pontuacao = qtde_total_blocos - len(blocos)

        # Verificar derrota
        if not bola_em_jogo:
            jogo_terminado = True
            vitoria = False

        # Verificar vitória
        if len(blocos) == 0:
            jogo_terminado = True
            vitoria = True

        desenhar_jogo(
            jogador,
            bola,
            blocos,
            pontuacao
        )

    else:

        mostrar_fim_jogo(vitoria)

    pygame.display.flip()


pygame.quit()
