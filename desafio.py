import requests 
import pytesseract
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
from PIL import ImageEnhance
from PIL import Image, ImageOps

url = "http://localhost:8080/"

requisicao = requests.get(url)

soup = BeautifulSoup(requisicao.content, 'html.parser')

hidden_field = soup.find('input', {'type': 'hidden', 'name': 'captcha_id'})

if hidden_field:
    valor_hidden = hidden_field.get('value')
    print(valor_hidden)
else:
    print("Campo hidden não encontrado.")

captcha_img = url + "captcha/" + valor_hidden + ".png"
print(captcha_img)

# Função para baixar a imagem da URL e extrair caracteres usando OCR
def extrair_caracteres_da_imagem(url):
    # Baixar a imagem da URL
    response = requests.get(url)
    print (f"*** {response.content}")

    img = Image.open(BytesIO(response.content))
    print (f"*** -> {img.mode}")
    
    img = img.convert('P')
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2)  # Ajuste o valor conforme necessário
    img = img.convert('L')  # Converta para escala de cinza
    threshold = 200  # Ajuste o valor do limiar conforme necessário
    img = img.point(lambda p: p > threshold and 255)

    print (f"*** {img}")

    # Converter a imagem para texto usando OCR
    texto_na_imagem = pytesseract.image_to_string(img)
    print (f"*** {texto_na_imagem}")

    return texto_na_imagem


# Chamar a função para extrair caracteres da imagem
caracteres_na_imagem = extrair_caracteres_da_imagem(captcha_img)

# Imprimir os caracteres reconhecidos
print(f"Caracteres na imagem: {caracteres_na_imagem}")