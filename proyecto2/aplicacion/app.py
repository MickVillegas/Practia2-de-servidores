from flask import Flask, redirect, render_template, request, url_for
from flask_bootstrap import Bootstrap5
from aplicacion import config
from aplicacion.forms import formArticulo, formCategoria, formSINO
from werkzeug.utils import secure_filename
from aplicacion.models import Categorias, Articulos

app = Flask(__name__)
Bootstrap = Bootstrap5(app)
app.config.from_object(config)


from aplicacion.models import Articulos, Categorias, db
db.init_app(app)


@app.route("/")
@app.route("/categorias/<id>")
def inicio (id = '0'):
    categoria = Categorias.query.get(id)
    if id == '0':
        articulos = Articulos.query.all()
    else:
        articulos = Articulos.query.filter_by(CategoriaId = id)
    categorias = Categorias.query.all()
    return render_template("inicio.html", categoria = categoria, articulos = articulos, categorias = categorias)
@app.route('/categorias')
def categorias():
    categorias = Categorias.query.all()
    return render_template('categorias.html', categorias = categorias)
@app.errorhandler(404)
def pageNotFOund(error):
    return render_template("error.html", error = "pagina no encontrada..."), 404

@app.route('/articulos/new/', methods = ['GET', 'POST'])
def articulos_new():
    form = formArticulo()
    categorias = [(c.id, c.nombre) for c in Categorias.query.all()[0:]]
    form.CategoriaId.choices = categorias
    if form.validate_on_submit():
        try:
            f = form.photo.data
            nombre_fichero = secure_filename(f.filename)
            f.save(app.root_path+"static/upload"+nombre_fichero)
        except:
            nombre_fichero = ""
        art = Articulos()
        form.populate_obj(art)
        art.image = nombre_fichero
        db.session.add(art)
        db.session.commit()
        return redirect(url_for("inicio"))
    else:
        return render_template("articulos_new.html", form = form)

@app.route('/categorias/new', methods = ["get", "post"])
def categorias_new():
    form = formCategoria(request.form)
    if form.validate_on_submit():
        cat = Categorias(nombre = form.nombre.data)
        db.session.add(cat)
        db.session.commit()
        return redirect(url_for("categorias"))
    else:
        return render_template("categorias_new.html", form = form)

@app.route('/articulos/<id>/edit', methods = ["get", "post"])
def articulos_edit(id):
    art = Articulos.query.get(id)
    if art is None:
        abort(404)
    form = formArticulo(obj = art)
    categorias = [(c.id, c.nombre) for c in Categorias.query.all()[0:]]
    form.CategoriaId.choices = categorias
    if form.validate_on_submit():
        if form.photo.data:
            os.remove(app.root_path + "/img/upload/" + art.image)
            try:
                f = form.photo.data
                nombre_fichero = secure_filename(f.filename)
                f.save(app.root_path + "/img/upload/" + nombre_fichero)
            except:
                nombre_fichero = ""
        else:
            nombre_fichero = art.image
        form.populate_obj(art)
        art.image = nombre_fichero
        db.session.commit()
        return redirect(url_for("inicio"))
    return render_template("articulos_new.html", form = form)

@app.route('/articulos/<id>/delete', methods = ["get", "post"])
def articulos_delete(id):
    art = Articulos.query.get(id)
    if art is None:
        abort(404)
    form = formSINO()
    if form.validate_on_submit():
        if form.si.data:
            if art.image!="":
                os.remove(app.root_path+"/static/img"+art.image)
            db.session.delete(art)
            db.session.commit()
        return redirect(url_for("inicio"))
    return render_template("articulos_delete.html", form = form, art = art)

@app.route('/categorias/<id>/edit', methods = ["get", "post"])
def categorias_edit(id):
    cat = Categorias.query.get(id)
    if cat is None:
        abort(404)
    form = formCategoria(request.form, obj = cat)
    if form.validate_on_submit():
        form.populate_obj(cat)
        db.session.commit()
        return redirect(url_for("categorias"))
    return render_template("categorias_new.html", form = form)

@app.route('/categorias/<id>/delete', methods = ["get", "post"])
def categorias_delete(id):
    cat = Categorias.query.get(id)
    if cat is None:
        abort(404)
    form = formSINO()
    if form.validate_on_submit():
        if form.si.data:
            db.session.delete(cat)
            db.session.commit()
            return redirect(url_for("categorias"))
    return render_template("categorias_delete.html", form = form, cat = cat)