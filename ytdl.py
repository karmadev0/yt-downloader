from pytubefix import YouTube

def download_video(url):
  """Descarga un video de YouTube dado una URL utilizando pytubefix.

  Args:
    url: La URL del video de YouTube.
  """

  try:
    yt = YouTube(url)
    video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    video.download()
    print("Descarga completada!")
  except Exception as e:
    print(f"Error durante la descarga: {e}")

