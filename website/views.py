
from flask import Blueprint, render_template, flash, request, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
import pandas 
import subprocess
import random
views = Blueprint('views', __name__)



@views.route('/')
def home():

    return render_template('index.html', user=current_user,  variable='12345')

@views.route('/home')
def home1():

    return render_template('info.html', user=current_user,  variable='12345')




@views.route('/notes', methods=['GET', 'POST'])
@login_required
def notes ():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
    return render_template('notes.html', user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})



e_cities = ['City name: Seattle: Covid cases: 184473', 'City name: New York: Covid cases: 3065699', 'City name: London: Covid cases: 10011650', 'City name: Sydney: Covid cases: 118074', 'City name: Boston: Covid cases: 124585', 'City name: Chicago: Covid cases: 749730', 'City name: New Orleans: Covid cases: 50836', 'City name: Bangkok: Covid cases: 2204672', 'City name: Seoul: Covid cases: 136376', 'City name: Japan: Covid cases: 99208', 'City name: Singapore: Covid cases: 277042', 'City name: Taipei: Covid cases: 16873', 'City name: Maldives: Covid cases: 94444', ]
ne_cities = ['City name: Jakarta: Covid cases: 4261208', 'City name: Kuala Lumpur: Covid cases: 2731713', 'City name: Bali: Covid cases: 4261208', 'City name: Moscow: Covid cases: 887636']
m_cities = ['City name: Phuket: Covid cases: 2204672', 'City name: Bangkok: Covid cases: 2204672', 'City name: Jaipur: Covid cases: 955331', 'City name: Delhi: Covid cases: 1442633']

@views.route('/result',methods=['POST', 'GET'])
def result():
    output = request.form.to_dict()
    print(output)
    budget = output["budget"]
    desc = output["desc"]
    return render_template('index.html', user=current_user, budget=int(budget), desc=desc, e_city=random.choice(e_cities), ne_city=random.choice(ne_cities), m_city=random.choice(m_cities))


