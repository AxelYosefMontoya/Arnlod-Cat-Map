import os
import requests
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt

def download_image(url, local_path="temp_image.jpg"):
    """Descarga una imagen desde una URL"""
    response = requests.get(url)
    if response.status_code == 200:
        with open(local_path, 'wb') as f:
            f.write(response.content)
        return local_path
    else:
        raise Exception(f"No se pudo descargar la imagen. Código de estado: {response.status_code}")

def arnold_transform(image_path, iterations=3, keep_all=False):
    """Aplica la transformación del gato de Arnold"""
    title = os.path.splitext(os.path.basename(image_path))[0]
    counter = 0
    canvas = None
    
    while counter < iterations:
        with Image.open(image_path) as img:
            width, height = img.size
            canvas = Image.new(img.mode, (width, height))
            
            for x in range(width):
                for y in range(height):
                    nx = (2 * x + y) % width
                    ny = (x + y) % height
                    canvas.putpixel((nx, height-ny-1), img.getpixel((x, height-y-1)))

        counter += 1
        print(f"Iteración {counter}/{iterations} completada")
        
        if not keep_all and counter > 1:
            os.remove(image_path)
            
        image_path = f"arnold_result_{counter}.png"
        canvas.save(image_path)
    
    return canvas

def main():
    image_url = "https://github.com/AxelYosefMontoya/Arnlod-Cat-Map/blob/main/high%20voltage%2001.png"
    
    try:
        # 1. Descargar la imagen
        local_path = download_image(image_url)
        
        # 2. Aplicar transformación
        result = arnold_transform(local_path, iterations=3)
        
        # 3. Mostrar resultado (funciona en Colab/Jupyter)
        plt.imshow(result)
        plt.axis('off')
        plt.show()
        
        print("Transformación completada. Resultado guardado como 'arnold_result_3.png'")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Instalar dependencias si se ejecuta en Colab
    try:
        from google.colab import drive
        print("Ejecutando en Google Colab")
        !pip install requests pillow matplotlib
        main()
    except:
        print("Ejecutando localmente")
        main()
