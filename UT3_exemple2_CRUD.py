from flask import Flask, render_template, request, session
import numpy as np
from database import biblioteca
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'


@app.route('/')
def index():
	llistaEditors=biblioteca.carregaEditors()
	print(llistaEditors)
	return render_template('UT3_exemple2_editors.html',editors=llistaEditors)

@app.route('/formulari') #arriba aquí tant si volem modificar com si volem afegir un nou
def formulari():
	ideditor= request.args.get('id_edit')
	nom= request.args.get('nom')
	return render_template('UT3_exemple2_modifica.html',idedit=ideditor,nom=nom)

# This page will have the sign up form
@app.route('/elimina')
def elimina():
	idedit= request.args.get('id_edit')
	biblioteca.eliminaEditor(idedit)
	llistaEditors=biblioteca.carregaEditors()
	return render_template('UT3_exemple2_editors.html',editors=llistaEditors)

@app.route('/executacanvis')
def executacanvis():
	ideditor= request.args.get('id_edit')
	nom= request.args.get('nom')
	#Si no tenim ideditor es que es un NOU editor. si SI que el tenim, es una modificacio
	if ideditor!='None': #es una modificacio
		biblioteca.modificaEditor(nom,ideditor)
	else:#es un editor nou
		biblioteca.afegeixEditor(nom)
	llistaEditors=biblioteca.carregaEditors()
	return render_template('UT3_exemple2_editors.html',editors=llistaEditors)



if __name__ == '__main__':
	app.run(debug=True)
