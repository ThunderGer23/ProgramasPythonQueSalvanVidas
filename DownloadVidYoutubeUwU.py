from pytube import YouTube
link = input("Ingresa el link del video: ")
video = YouTube(link)
print("Descargando" + video.title)
video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()