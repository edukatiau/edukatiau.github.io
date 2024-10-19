import cv2
from pyzbar import pyzbar

def decode_qr_code(frame):
    # Usa a função decode da pyzbar para encontrar códigos de barras ou QR codes na imagem
    decoded_objects = pyzbar.decode(frame)
    
    for obj in decoded_objects:
        # Pega os dados do QR code (normalmente em bytes, então decodificamos para string)
        qr_data = obj.data.decode("utf-8")
        qr_type = obj.type
        
        # Desenha um retângulo em volta do QR code
        (x, y, w, h) = obj.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Exibe os dados decodificados
        text = f"{qr_data} ({qr_type})"
        cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        print(f"QR Code detected: {qr_data}")

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
        
        # Decodifica QR code no frame
        frame = decode_qr_code(frame)
        
        # Mostra o frame com a marcação do QR code
        cv2.imshow("QR Code Scanner", frame)
        
        # Fecha o programa se apertar a tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Libera a captura e fecha todas as janelas abertas
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
