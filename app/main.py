from flask import Blueprint, render_template, request, url_for
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from . import db
import os

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    now = datetime.now()
    cam_name = []
    for i in os.scandir('./app/static/streams'):
        if i.is_dir():
            cam_name.append(i.name)
    date = [(now - timedelta(i)).strftime('%d/%m/%Y')
 for i in range(7)]
    return render_template('profile.html',
	date = date, cam_name = cam_name, name=current_user.name)

@main.route('/profile', methods=['POST'])
@login_required
def profile_post():
    data = request.form
    cam_name = []
    for i in os.scandir('./app/static/streams'):
        if i.is_dir():
            cam_name.append(i.name)
    #time to count chosen weekday
    chosen = str((datetime.now().weekday() - int(data["date"]))%7 + 1)
    cam_index = int(data['cam']) - 1
    dir_name = cam_name[cam_index]
    # BIG dir name means there is only one weekday
    if dir_name.isupper:
        chosen = ''
    file_list ={}
    for filename in os.scandir('./app/static/streams/' + dir_name):
        if filename.is_file() and filename.name.endswith(f'{chosen}.mkv'):
           file_list.update({filename.name:datetime.fromtimestamp(filename.stat()[-1]).strftime('%d%m%Y: %H%M')})
    file_list = sorted(file_list.items())
    urls = [url_for('static', filename='streams/' + dir_name + '/' +i[0]) for i in file_list]
    times = [i[1] for i in file_list]
    print(f'urls:{urls}')
    return render_template('playback.html', filename=urls, times=times)    
