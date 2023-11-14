from flask import Flask,render_template,request,url_for,redirect
import requests
import json
import datetime

app = Flask(__name__)

def format_size(size):
    sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']
    if size == 0:
        return '0 Byte'

    i = 0
    while size >= 1024 and i < len(sizes)-1:
        size /= 1024.0
        i += 1

    return f"{size:.2f} {sizes[i]}"

def format_time(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d  %H:%M:%S')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get',methods=['POST'])
def redirectLink():
    url = request.form["link"]
    
    api = "https://api.ibeng.tech/api/downloader/terabox?apikey=C9eLLoQZvX&url="+url
    
    response = requests.get(api)
    
    if response.status_code == 200:
        response_json = response.text
        data = json.loads(response_json)
        filename = data['data']['list'][0]['filename']
        link = data['data']['list'][0]['downloadLink']
        timestamp = int(data['data']['list'][0]['create_time'])
        ukuran = float(data['data']['list'][0]['size'])
        tanggal = format_time(timestamp)
        size = format_size(ukuran)
        return render_template('index.html',filename=filename,tanggal=tanggal,size=size,link=link)
    else:
        eror = "gagal mendapatakan direct url"
        return render_template('index.html',eror=eror)


if __name__ == "__main__":
    app.run(debug=True , host='0.0.0.0')