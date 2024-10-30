import cv2
import numpy as np
import tkinter as tk
from tkinter import messagebox, simpledialog, Toplevel
from PIL import Image, ImageTk

# Variáveis globais
fotos_padroes = []  # Lista de tuplas (nome, imagem, miniatura)
threshold_diferenca = 50  # Parâmetro inicial de diferença média
foto_tk = None  # Imagem capturada atual
historico = []  # Histórico de comparações (OK/NOK e imagem)
janela_webcam = None  # Janela da webcam em tempo real
feed_ativo = False  # Controle do feed da webcam

# Função para capturar imagem da webcam
def capturar_imagem():
    global foto_tk
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    if ret:
        # Converte a imagem para o formato compatível com tkinter
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        imagem_pil = Image.fromarray(frame_rgb)
        foto_tk = ImageTk.PhotoImage(imagem_pil)
        label_imagem.config(image=foto_tk)
        return frame
    else:
        messagebox.showerror("Erro", "Não foi possível capturar a imagem.")
        return None

# Função para adicionar uma nova imagem padrão
def adicionar_imagem_padrao():
    imagem_padrao = capturar_imagem()
    if imagem_padrao is not None:
        nome = simpledialog.askstring("Nome da Imagem Padrão", "Digite um nome para a imagem padrão:")
        if nome:
            # Criar miniatura para exibição
            frame_rgb = cv2.cvtColor(imagem_padrao, cv2.COLOR_BGR2RGB)
            imagem_pil = Image.fromarray(frame_rgb)
            imagem_pil.thumbnail((80, 80))
            miniatura = ImageTk.PhotoImage(imagem_pil)

            # Armazenar a imagem padrão com seu nome e miniatura
            fotos_padroes.append((nome, imagem_padrao, miniatura))

            # Atualizar a exibição no menu lateral
            botao_miniatura = tk.Button(frame_lateral, image=miniatura, text=nome, compound="top")
            botao_miniatura.pack(pady=5)

# Função para capturar uma nova imagem e comparar com todas as imagens padrão
def capturar_e_comparar():
    global threshold_diferenca
    nova_imagem = capturar_imagem()
    if fotos_padroes and nova_imagem is not None:
        resultados = []

        # Comparar com cada imagem padrão
        for nome, imagem_padrao, _ in fotos_padroes:
            nova_imagem_resized = cv2.resize(nova_imagem, (imagem_padrao.shape[1], imagem_padrao.shape[0]))
            diferenca = cv2.absdiff(imagem_padrao, nova_imagem_resized)
            media_diferenca = np.mean(diferenca)
            resultado = "OK" if media_diferenca < threshold_diferenca else "NOK"
            resultados.append((nome, resultado, media_diferenca))

        # Atualizar a última comparação na exibição de status
        atualizar_status_ultima_comparacao(resultados)

        # Adicionar a imagem e o resultado ao histórico
        adicionar_historico(nova_imagem, resultados)

        # Exibir os resultados em uma mensagem
        resultados_texto = "\n".join([f"{nome}: {resultado} (Diferença Média: {media:.2f})" for nome, resultado, media in resultados])
        messagebox.showinfo("Resultados da Comparação", resultados_texto)
    else:
        messagebox.showwarning("Aviso", "Capture ao menos uma imagem padrão antes de comparar.")

# Função para atualizar o status da última comparação
def atualizar_status_ultima_comparacao(resultados):
    cor_status = "green" if all(r[1] == "OK" for r in resultados) else "red"
    texto_status = "OK" if cor_status == "green" else "NOK"
    label_status.config(text=texto_status, bg=cor_status)

# Função para adicionar uma miniatura ao histórico
def adicionar_historico(imagem, resultados):
    frame_rgb = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
    imagem_pil = Image.fromarray(frame_rgb)
    imagem_pil.thumbnail((80, 80))
    miniatura = ImageTk.PhotoImage(imagem_pil)

    historico.append((miniatura, imagem, resultados))

    cor_geral = "green" if all(r[1] == "OK" for r in resultados) else "red"
    botao_miniatura = tk.Button(frame_historico, image=miniatura, bg=cor_geral, command=lambda: visualizar_imagem(imagem, resultados))
    botao_miniatura.pack(side="left", padx=5, pady=5)

# Função para abrir uma nova janela e visualizar a imagem em tamanho completo e os resultados
def visualizar_imagem(imagem, resultados):
    janela_visualizar = Toplevel(root)
    janela_visualizar.title("Visualização dos Resultados")
    frame_rgb = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
    imagem_pil = Image.fromarray(frame_rgb)
    imagem_tk = ImageTk.PhotoImage(imagem_pil)
    label_imagem_grande = tk.Label(janela_visualizar, image=imagem_tk)
    label_imagem_grande.image = imagem_tk
    label_imagem_grande.pack()

    resultados_texto = "\n".join([f"{nome}: {resultado} (Diferença Média: {media:.2f})" for nome, resultado, media in resultados])
    label_resultados = tk.Label(janela_visualizar, text=resultados_texto, justify="left")
    label_resultados.pack(pady=10)

# Função para abrir a janela de visualização em tempo real da webcam
def abrir_janela_webcam():
    global janela_webcam, feed_ativo
    if not feed_ativo:
        janela_webcam = Toplevel(root)
        janela_webcam.title("Visualização em Tempo Real")
        janela_webcam.protocol("WM_DELETE_WINDOW", fechar_janela_webcam)

        label_video = tk.Label(janela_webcam)
        label_video.pack()

        feed_ativo = True
        atualizar_feed(label_video)

# Função para atualizar o feed da webcam
def atualizar_feed(label_video):
    global feed_ativo
    if feed_ativo:
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            cv2.imshow("teste", frame)
            #cap.release()

            # Sai do loop ao pressionar a tecla 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


# Função para fechar a janela de visualização da webcam
def fechar_janela_webcam():
    global feed_ativo
    feed_ativo = False
    if janela_webcam:
        janela_webcam.destroy()

# Interface com tkinter
root = tk.Tk()
root.title("Comparação de Imagens com Webcam")

# Navbar superior
navbar = tk.Menu(root)
root.config(menu=navbar)

# Menu "Auxiliar" com visualização da webcam
menu_auxiliar = tk.Menu(navbar, tearoff=0)
navbar.add_cascade(label="Auxiliar", menu=menu_auxiliar)
menu_auxiliar.add_command(label="Visualizar Webcam", command=abrir_janela_webcam)

# Frame lateral para as imagens padrão
frame_lateral = tk.Frame(root, width=200, height=400)
frame_lateral.pack(side="left", fill="y")
frame_lateral.pack_propagate(False)

titulo_imagem_padrao = tk.Label(frame_lateral, text="Imagens Padrão")
titulo_imagem_padrao.pack(pady=5)

frame_principal = tk.Frame(root)
frame_principal.pack(side="top", fill="both", expand=True)

label_imagem = tk.Label(frame_principal)
label_imagem.pack(pady=10)

# Frame de status no canto superior direito
frame_status = tk.Frame(root, width=100, height=50)
frame_status.place(relx=0.85, rely=0.05)

label_status = tk.Label(frame_status, text="---", bg="gray", fg="white", font=("Helvetica", 16), width=8, height=2)
label_status.pack()

# Botões para capturar imagens
botao_definir_imagem_padrao = tk.Button(frame_principal, text="Adicionar Imagem Padrão", command=adicionar_imagem_padrao)
botao_definir_imagem_padrao.pack(pady=5)

botao_comparar = tk.Button(frame_principal, text="Capturar e Comparar", command=capturar_e_comparar)
botao_comparar.pack(pady=5)

# Slider para ajuste do threshold de comparação
def ajustar_threshold(valor):
    global threshold_diferenca
    threshold_diferenca = int(valor)

slider_threshold = tk.Scale(frame_principal, from_=0, to=255, orient="horizontal", label="Threshold de Diferença", command=ajustar_threshold)
slider_threshold.set(threshold_diferenca)
slider_threshold.pack(pady=5)

# Frame inferior para o histórico de resultados
frame_historico = tk.Frame(root, height=100)
frame_historico.pack(side="bottom", fill="x")
frame_historico.pack_propagate(False)

titulo_historico = tk.Label(frame_historico, text="Histórico de Comparações", bg="gray", fg="white")
titulo_historico.pack(fill="x")

root.mainloop()
