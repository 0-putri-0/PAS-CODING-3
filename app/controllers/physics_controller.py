from flask import Blueprint, render_template, request, redirect
from ..models.models import Calculation

physics_bp = Blueprint('physics_bp', __name__)

@physics_bp.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
    
        voltage = float(request.form["voltage"])
        current = float(request.form["current"])
        if current == 0:
            return "Arus tidak boleh nol.", 400
        resistance = voltage / current
        calc = Calculation(voltage=voltage, current=current, resistance=resistance)
        calc.save()
        return redirect('/')
    calculations = Calculation.query.all()
    return render_template("index.html", calculations=calculations)

@physics_bp.route('/gabung', methods=["GET", "POST"])
def gabung():
    calculations = Calculation.query.all()
    if request.method == "POST":
        id1 = int(request.form["calc1"])
        id2 = int(request.form["calc2"])
        jenis = request.form["jenis"]
        calc1 = Calculation.query.get(id1)
        calc2 = Calculation.query.get(id2)
        if not calc1 or not calc2:
            return "Perhitungan tidak ditemukan.", 404
        r1 = calc1.resistance
        r2 = calc2.resistance
        if jenis == "seri":
            r_total = r1 + r2
        elif jenis == "paralel":
            r_total = 1 / (1/r1 + 1/r2)
        else:
            return "Jenis rangkaian tidak valid.", 400
        

        return render_template("gabung.html", r_total=r_total, jenis=jenis, calc1=calc1, calc2=calc2)
    return render_template("gabung.html", calculations=calculations)
@physics_bp.route('/update/<id>', methods=["GET", "POST"])
def kategori_update(id):
    kategori = Calculation.get_by_id(id)
    if request.method == "POST":
        kategori.name = request.form["name"]
        kategori.save()
        return redirect("/kategori")
    return render_template("update.html", kategori=kategori)

@physics_bp.route('/hapus/<id>')
def kategori_hapus(id):
    kategori = Calculation.get_by_id(id)
    if kategori:
        kategori.delete()
    return redirect("/kategori")
