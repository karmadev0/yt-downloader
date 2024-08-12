from pytubefix import YouTube
from flask import Flask, render_template, request, send_file
import requests
import os
import time  # For simulated file deletion (can't directly control server)
from tqdm import tqdm
from flask import Flask
import time

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/descargar', methods=['POST'])
def descargar():
    url = request.form['url']

    # Validate URL
    try:
        response = requests.head(url)
        response.raise_for_status()  # Raise exception for failed requests
        if not (url.startswith('https://www.youtube.com/') or url.startswith('https://youtu.be/')):
            return 'URL inválida. Debe ser una URL de YouTube (youtube.com o youtu.be).'
    except requests.exceptions.RequestException:
        return 'Error al verificar la URL.'

    yt = YouTube(url)
    video_title = yt.title.replace('/', '_').replace(':', '_')
    thumbnail_url = yt.thumbnail_url

    try:
        audio = yt.streams.filter(only_audio=True).order_by('bitrate').desc().first()
        with tqdm(total=audio.filesize, desc=f"Descargando {video_title}") as bar:
            out_file = audio.download(filename=f"{video_title}.mp3")

            # Update progress bar if `pytubefix` provides chunk size information
            if hasattr(audio, 'chunk_size'):  # Check if chunk_size is available
                for chunk in audio.download_chunks(chunk_size=audio.chunk_size):
                    if chunk:
                        bar.update(len(chunk))
                    else:
                        break

        # **Comentar la sección de eliminación:**
        # Simulated deletion (can't directly control server)
        # print(f"Simulando eliminación del archivo {out_file} después de 1 minuto...")
        # time.sleep(60)  # Simulate 1 minute wait
        # try:
        #     os.remove(out_file)
        #     print(f"Archivo {out_file} eliminado (simulado).")
        # except OSError as e:
        #     print(f"Error al eliminar el archivo (simulado): {e}")

    except Exception as e:
        return f"Error al descargar el audio: {str(e)}"

    # Send MP3 directly (no ZIP)
    return send_file(out_file, as_attachment=True,
                     mimetype='audio/mpeg',
                     download_name=f"{video_title}.mp3")
    # para eliminar en un minuto
    r
    try:
        print(f"{out_file} se eliminara en 60 segundos")
        time.sleep(60)
        os.remove(out_file)
        print(f"Archivo {out_file} eliminado.")
    except Exception as e:
        return f"error al eliminar el archivo: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
