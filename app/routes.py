from app import app
from datetime import datetime
from datetime import timedelta
from flask import render_template
from flask import request, url_for
import os

@app.route('/')
#@app.route('/index')
def index():
#    date = { 'today': datetime.now().strftime('%d/%m/%Y'),'yesterday'}
    now = datetime.now()
    date = [(now - timedelta(i)).strftime('%d/%m/%Y')
 for i in range(7)]
    return render_template('index.html',
	date = date)

@app.route('/', methods = ['POST'])
def parse_request():
    data = request.form
    #time to count chosen weekday
    chosen = str((datetime.now().weekday() - int(data["date"]))%7 + 1)
    file_list ={} 
    for filename in os.scandir('./app/static/streams'):
        if filename.is_file() and filename.name.endswith(f'{chosen}.mkv'):
           file_list.update({filename.name:datetime.fromtimestamp(filename.stat()[-1]).strftime('%d%m%Y: %H%M')}) 
    file_list = sorted(file_list.items()) 
    urls = [url_for('static', filename='streams/'+i[0]) for i in file_list]
    times = [i[1] for i in file_list]
    print(f'urls:{urls}')
    return render_template('playback.html', filename=urls, times=times) #have to make return exit and separate html template
