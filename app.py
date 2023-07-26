from flask import Flask, request, jsonify
import requests
from pytube import YouTube

app = Flask(__name__)

def obter_urls_streaming(url):
    try:
        yt = YouTube(url)
        streams = yt.streams.filter(file_extension='mp4')
        resolucoes = set()
        urls_e_resolucoes = []

        for stream in streams:
            if stream.resolution not in resolucoes:
                resolucoes.add(stream.resolution)
                tem_audio = "sim" if stream.includes_audio_track else "não"
                url_streaming = stream.url
                url_streaming = encurtar_url(url_streaming)
                urls_e_resolucoes.append({"resolucao": stream.resolution, "url_streaming": url_streaming, "audio": tem_audio})

        return urls_e_resolucoes
    except Exception as e:
        return []

def encurtar_url(url):
    try:
        response = requests.get(f"http://tinyurl.com/api-create.php?url={url}")
        if response.ok:
            return response.text.strip()
        else:
            return url
    except Exception as e:
        return url

@app.route('/api/obter_resolucoes', methods=['POST'])
def obter_resolucoes():
    try:
        data = request.get_json()
        video_url = data.get('video_url')
        urls_e_resolucoes = obter_urls_streaming(video_url)

        if not urls_e_resolucoes:
            return jsonify({"message": "Não foi possível encontrar uma stream válida para o vídeo."}), 404

        return jsonify(urls_e_resolucoes), 200

    except Exception as e:
        return jsonify({"message": "Ocorreu um erro ao processar a solicitação."}), 500

if __name__ == "__main__":
    app.run(debug=True)
