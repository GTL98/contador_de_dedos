################################################################################################
#                                                                                              #
#  Toda a lógica mais detalhada está presente no arquivo "Contador de Dedos.ipynb"             #
#                                                                                              #
#  Em caso de dúvidas, consultar a documentação:                                               #
#      - "Aula 1 - Rastramento de mão (Introdução).ipynb" no link abaixo.                      #
#                                                                                              #
#  GitHub: https://github.com/GTL98/curso-completo-de-visao-computacional-avancada-com-python  #
#                                                                                              #
################################################################################################


# Importar as bibliotecas
import cv2
import time
import os
import rastreamento_mao as rm


# Definir o tamanho da tela
largura_tela = 640
altura_tela = 480


# Imagens dos dedos
caminho = 'imagens_dedos'
lista_imagens = os.listdir(caminho)
print(lista_imagens)
lista_fotos = []
for caminho_imagem in lista_imagens:
    foto = cv2.imread(f'{caminho}/{caminho_imagem}')
    lista_fotos.append(foto)
    

# Taxa de frame (FPS)
tempo_atual = 0
tempo_anterior = 0


# Módulo DetectorMao
detector = rm.DetectorMao(max_maos=1, deteccao_confianca=0.75, rastreamento_confianca=0.75)


# Lista das landmarks
# Serão usadas as lankdmarks das pontas dos dedos, em ordem: dedão, indicador, médio, anelar e mindinho
landmarks_ponta_dedos = [4, 8 , 12, 16, 20]


# Captura de vídeo
cap = cv2.VideoCapture(0)
cap.set(3, largura_tela)
cap.set(4, altura_tela)

while True:
    sucesso, imagem = cap.read()
    imagem = detector.encontrar_maos(imagem)
    lista_landmark = detector.encontrar_posicao(imagem, desenho=False)
    
    # Pegar as posições das landmarks que usaremos
    if lista_landmark:
        dedos = []
        # Loop para o dedão (usa o eixo X para verificar se está levantando ou abaixado)
        if lista_landmark[landmarks_ponta_dedos[0]][1] > lista_landmark[landmarks_ponta_dedos[0] - 1][1]:
            dedos.append(1)
        else:
            dedos.append(0)
        
        # Loop para todos os dedos menos o dedão
        for ponta_dedo in range(1, 5):
            # Pegar a posição no eixo Y da ponta de cada dedo
            if (lista_landmark[landmarks_ponta_dedos[ponta_dedo]][2] < 
                lista_landmark[landmarks_ponta_dedos[ponta_dedo] - 2][2]):
                dedos.append(1)
            else:
                dedos.append(0)
        
        # Ver quantos dedos estão levantados
        dedos_levantados = dedos.count(1)
    
        # Personalizar o tamanho da foto, não precisando redimensionar foto por foto
        altura_foto, largura_foto, canal = lista_fotos[dedos_levantados-1].shape

        # Colocar a foto dos dedos na captura de imagem
        imagem[0: altura_foto, 0: largura_foto] = lista_fotos[dedos_levantados-1]
        
        # Colocar o retângulo para mostrar os números
        cv2.rectangle(imagem, (20, 300), (170, 470), (0, 0, 0), cv2.FILLED)
        
        # Colocar os números no retângulo
        cv2.putText(imagem, str(dedos_levantados), (45, 440), cv2.FONT_HERSHEY_PLAIN, 10, (255, 255, 255), 25)
    
    # Configrar o FPS
    tempo_atual = time.time()
    fps = 1/(tempo_atual - tempo_anterior)
    tempo_anterior = tempo_atual
    
    # Mostrar o FPS na tela
    cv2.putText(imagem, f'FPS: {int(fps)}', (425, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 255), 3)
    
    # Mostrar a imagem na tela
    cv2.imshow('Imagem', imagem)
    
    # Terminar o loop
    if cv2.waitKey(1) & 0xFF == ord('s'):
        break
        
# Fechar a tela de captura
cap.release()
cv2.destroyAllWindows()
