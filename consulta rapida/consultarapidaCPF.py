#ATENÇÃO: O CODIGO SÓ ESTA RODANDO NA VERSÃO DO EDGE:
#Versão 131.0.2903.112(64 bits) 11/25

from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
import time
import tkinter as tk
import re

# Função para formatar o CPF ou CNPJ
def formatar_documento(documento, tipo):
    if tipo == 'CPF':
        # Formata como CPF: XXX.XXX.XXX-XX
        return re.sub(r'(\d{3})(\d{3})(\d{3})(\d{2})', r'\1.\2.\3-\4', documento)
    elif tipo == 'CNPJ':
        # Formata como CNPJ: XX.XXX.XXX/XXXX-XX
        return re.sub(r'(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})', r'\1.\2.\3/\4-\5', documento)

# Função para obter o CPF/CNPJ da interface gráfica
def obter_documento():
    global documento, tipo_documento
    documento = entry.get()
    tipo_documento = var_tipo.get()
    documento = formatar_documento(documento, tipo_documento)
    root.destroy()  # Fecha a janela após clicar em enviar

# Função para centralizar a janela Tkinter
def centralizar_janela(janela, largura, altura):
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    pos_x = (largura_tela // 2) - (largura // 2)
    pos_y = (altura_tela // 2) - (altura // 2)
    janela.geometry(f'{largura}x{altura}+{pos_x}+{pos_y}')

# Criação da interface gráfica
root = tk.Tk()
root.title("Escolha o Tipo de Documento")

# Definindo o tamanho e centralizando a janela
centralizar_janela(root, 350, 250)

# Definir uma cor de fundo suave
root.configure(bg="#f0f0f0")

# Variável para armazenar o tipo de documento escolhido (CPF ou CNPJ)
var_tipo = tk.StringVar(value="CPF")

# Criação dos botões de seleção para CPF e CNPJ
frame_tipo = tk.Frame(root, bg="#f0f0f0")
frame_tipo.pack(pady=15)

label_tipo = tk.Label(frame_tipo, text="Escolha o tipo de documento:", font=("Arial", 12), bg="#f0f0f0")
label_tipo.grid(row=0, column=0, columnspan=2, pady=10)

radio_cpf = tk.Radiobutton(frame_tipo, text="CPF", variable=var_tipo, value="CPF", font=("Arial", 12), bg="#f0f0f0")
radio_cpf.grid(row=1, column=0, padx=10)

radio_cnpj = tk.Radiobutton(frame_tipo, text="CNPJ", variable=var_tipo, value="CNPJ", font=("Arial", 12), bg="#f0f0f0")
radio_cnpj.grid(row=1, column=1, padx=10)

# Caixa de entrada para o documento (CPF ou CNPJ)
frame_documento = tk.Frame(root, bg="#f0f0f0")
frame_documento.pack(pady=10)

label_documento = tk.Label(frame_documento, text="Digite o CPF/CNPJ:", font=("Arial", 12), bg="#f0f0f0")
label_documento.grid(row=0, column=0, pady=10)

entry = tk.Entry(frame_documento, font=("Arial", 14), width=20)
entry.grid(row=1, column=0)

# Botão de Enviar (usando tk.Button em vez de ttk)
frame_botao = tk.Frame(root, bg="#f0f0f0")
frame_botao.pack(pady=20)

button_enviar = tk.Button(frame_botao, text="Enviar", command=obter_documento, font=("Arial", 12), bg="#4CAF50", fg="white", width=10)
button_enviar.grid(row=0, column=0)

root.mainloop()

# Caminho para o EdgeDriver
driver_path = r"C:\Users\sousa\OneDrive\Documentos\codigosBiel\msedgedriver.exe"
service = Service(driver_path)

# Definindo as opções para o EdgeDriver
options = Options()
options.add_argument("--ignore-certificate-errors")  # Ignora erros de SSL

# Inicia o driver do Edge
driver = webdriver.Edge(service=service, options=options)

# Abre os três sites em diferentes guias
driver.get("https://")
driver.execute_script("window.open('https://');")    #
driver.execute_script("window.open('https://');")

# Troca para a primeira aba e insere o CPF/CNPJ no primeiro site
driver.switch_to.window(driver.window_handles[0])
wait = WebDriverWait(driver, 30)
text_area1 = wait.until(EC.presence_of_element_located((By.ID, 'NI')))
text_area1.send_keys(documento)
text_area1.send_keys(Keys.RETURN)  # Envia Enter

# Troca para a segunda aba e insere o CPF/CNPJ no segundo site
driver.switch_to.window(driver.window_handles[1])
wait = WebDriverWait(driver, 30)
text_area2 = wait.until(EC.presence_of_element_located((By.ID, 'formEnvio:campoCPFCNPJ')))
text_area2.send_keys(documento)

# Troca para a terceira aba e insere o CPF/CNPJ no terceiro site
driver.switch_to.window(driver.window_handles[2])
wait = WebDriverWait(driver, 30)
text_area3 = wait.until(EC.presence_of_element_located((By.ID, 'dados_documento')))
text_area3.send_keys(documento)

# Aguarda alguns segundos e então fecha o navegador (opcional)
time.sleep(100)
driver.quit()
