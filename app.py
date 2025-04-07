from flask import Flask,request,redirect,url_for,render_template
import os
from funcionessql import *

app= Flask(__name__)
@app.route('/<msj>/<color>',methods=['GET','POST'])
@app.route('/<msj>',methods=['GET','POST'])
@app.route('/')
def index(msj='',color=''):
    return render_template('index.html',msj=msj,color=color)


@app.route('/form',methods=['GET','POST'])
def form():
   if request.method=='POST':
       nombre_carpeta=request.form['nombre_producto']
       if nombre_carpeta=="":
           msj='nombre no valido'
           color='rojo'
           return redirect(url_for('index', msj=msj,color=color))
       url = f'uploads/{nombre_carpeta}'
       if os.path.exists(url):
            color='rojo'
            msj='ese producto ya existe'
            
            return redirect(url_for('index',msj=msj,color=color))
       else:
            os.mkdir(f'uploads/{nombre_carpeta}')
            imagenes_subidas=request.files.getlist('imagenes[]')
            for img in imagenes_subidas:
                if img != '':
                    nombre_img=img.filename
                    url = f'uploads/{nombre_carpeta}/{nombre_img}'
                    img.save(f'uploads/{nombre_carpeta}/{nombre_img}')
                    guardarproducto_db(nombre_carpeta)
                    id_producto=obtenerid_db(nombre_carpeta)
                    id_producto=str(id_producto[0])
                    guardarimg_db(url,id_producto)
            msj='producto agregado exitosamente'
            color='azul'
            return redirect(url_for('index',msj=msj,color=color))
   return redirect(url_for('index'))








if __name__ == '__main__':
    app.run(debug=True)