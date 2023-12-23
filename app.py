from flask import Flask, render_template, request, session, redirect, url_for
from datetime import datetime, timedelta
#Import base de datos 
from database import Rentacarro

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'mysecretkey'

#Comprobar si se puede realizar una reserva
def reserva_comprova(reserva, llista_reserves):
    if 'dia' not in reserva or not reserva['dia']:
        return "Por favor, selecciona una fecha para la reserva."

    data_actual = datetime.now().strftime("%Y-%m-%d")
    if reserva['dia'] < data_actual:
        return "No puedes reservar para una fecha anterior a hoy."

    for r in llista_reserves:
        if (
            r['idcarro'] == reserva['carro_id'] and
            r['dia'] == reserva['dia']
        ):
            return "Este carro ya está reservado para la fecha seleccionada."

    if not reserva['usuario']:
        return "No has ingresado el nombre del usuario."

    return 0

##CLASE CARRO##
class Carro:
    def __init__(self, id, nom, clase, preu, descripcio, img):
        self.id = id
        self.nom = nom
        self.clase = clase
        self.preu = preu
        self.descripcio = descripcio
        self.img = img

class Reserva:
    def __init__(self, idcarro, iniciReserva, finalReserva, usuario):
        self.idcarro = idcarro
        self.iniciReserva = iniciReserva
        self.finalReserva = finalReserva
        self.usuario = usuario


##RUTAS
#Ruta / - Lista de carros-----------------------------------------------------------------
@app.route('/')
def index():
    carros = Rentacarro.get_carros()  #Saco los carros de la DB     
    return render_template('llista_carros.html', carros=carros)



#Ruta /reservar --------------------------------------------------------------------------
@app.route('/reservar', methods=['GET', 'POST'])
def reservar():
    carros= Rentacarro.get_carros()

    if request.method == 'POST':
        # Obtener datos del formulario
        nom = request.form['nom']
        llinatges = request.form['llinatges']
        diareserva = request.form['diareserva']
        horareserva = request.form['horareserva']
        diaretorno = request.form['diaretorno']
        horaretorno = request.form['horaretorno']
        carroreserva = request.form['carroreserva']

        print(llinatges, horareserva, diareserva, horaretorno, diaretorno)

        # Llamar a la función insert_reserva
        Rentacarro.insert_reserva(carroreserva, f'{diareserva} {horareserva}:00:00', f'{diaretorno} {horaretorno}:00:00', f'{nom} {llinatges}')

        # Redirigir a la página principal u otra página según tus necesidades
        return redirect(url_for('index'))
    
    
        
    return render_template('reservar_carro.html', carros=carros)



#Ruta lista de reservas----------------------------------------------------------------
@app.route('/llista_reserves')
def llista_reserves():
    # Obtener todas las reservas de la base de datos
    reserves = Rentacarro.get_reservas_with_carros()

    # Obtener la fecha de inicio y fin de la semana actual
    today = datetime.now().date()
    
    # Obtener el número de semanas a navegar desde los parámetros de la solicitud
    weeks_to_navigate = int(request.args.get('weeks', 0))

    # Obtener la fecha de inicio de la semana actual
    start_of_week = datetime(2023, 11, 19, 18, 0, 0).date()

    # Ajustar la fecha de inicio según el número de semanas a navegar
    start_of_week += timedelta(weeks=weeks_to_navigate)

    # Rango de la semana (desde x día hasta los 7 más)
    date_range = [start_of_week + timedelta(days=i) for i in range(7)]
    
    # Calcula la semana anterior y siguiente
    previous_week = start_of_week - timedelta(weeks=1)
    next_week = start_of_week + timedelta(weeks=1)

    return render_template('llista_reserves.html', reservas=reserves, today=today, date_range=date_range, previous_week=previous_week, next_week=next_week)


#Ruta intranet

@app.route('/intranet', methods=['GET', 'POST'])
def intranet():
    if request.method == 'POST':
        # Obtén los datos del formulario
        nom = request.form.get('nom')
        descripcio = request.form.get('descripcio')
        clase = request.form.get('clase')
        preu = request.form.get('preu')

        # Lógica para insertar el nuevo carro en la base de datos
        # (Utiliza tu propia lógica de base de datos aquí)

        # Después de insertar, redirige a la página principal u otra página según tus necesidades
        return redirect(url_for('intranet'))
    
    # Si es un GET, carga la página normalmente con la lista de carros existentes
    all_carros = Rentacarro.get_carros()
    return render_template('intranet.html', carros=all_carros) 





if __name__ == '__main__':
    app.run(debug=True)
