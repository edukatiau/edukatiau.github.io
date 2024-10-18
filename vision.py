import cv2
import numpy as np

# Inicia a captura de vídeo da webcam (0 é o ID da webcam padrão)
cap = cv2.VideoCapture(0)

# Verifica se a webcam foi inicializada corretamente
if not cap.isOpened():
    print("Erro ao acessar a webcam")
    exit()

while True:
    # Captura frame por frame da webcam
    ret, frame = cap.read()

    if not ret:
        print("Falha ao capturar frame")
        break

    # Converte o frame para escala de cinza
    frame_cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Aplica um filtro Gaussiano para suavizar a imagem
    blur = cv2.GaussianBlur(frame_cinza, (5, 5), 0)

    # Aplica limiarização (threshold) para binarizar a imagem
    _, binaria = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY_INV)

    # Detecta os contornos das peças no frame
    contornos, _ = cv2.findContours(binaria, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Desenha os contornos no frame original
    cv2.drawContours(frame, contornos, -1, (0, 255, 0), 2)

    # Exibe o número de peças detectadas no frame atual
    cv2.putText(frame, f'Pecas detectadas: {len(contornos)}', (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    # Exibe o frame com as peças detectadas
    cv2.imshow('Deteccao de Pecas', frame)

    # Sai do loop ao pressionar a tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera o objeto de captura e fecha as janelas
cap.release()
cv2.destroyAllWindows()
