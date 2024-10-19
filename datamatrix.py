import cv2
from pyzbar import pyzbar

def decode_codes(frame):
    # Usa a função decode da pyzbar para encontrar códigos de barras, QR codes e Data Matrix na imagem
    decoded_objects = pyzbar.decode(frame)
    
    for obj in decoded_objects:
        # Pega os dados do código (em bytes, então decodificamos para string)
        code_data = obj.data.decode("utf-8")
        code_type = obj.type
        
        # Desenha um retângulo ao redor do código
        (x, y, w, h) = obj.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Exibe os dados decodificados e o tipo do código (QR code, Data Matrix, etc.)
        text = f"{code_data} ({code_type})"
        cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        print(f"Código detectado: {code_data}, Tipo: {code_type}")

    return frame

def main():
    # Inicializa a captura de vídeo (0 = webcam padrão)
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Erro ao acessar a webcam.")
        return

    while True:
        # Lê o frame da webcam
        ret, frame = cap.read()
        
        if not ret:
            print("Erro ao capturar a imagem.")
            break
        
        # Decodifica QR code e Data Matrix no frame
        frame = decode_codes(frame)
        
        # Mostra o frame com a marcação dos códigos
        cv2.imshow("QR Code e Data Matrix Scanner", frame)
        
        # Fecha o programa se apertar a tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Libera a captura e fecha todas as janelas abertas
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
