from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///buku.db'
db = SQLAlchemy(app)

class Buku(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tajuk = db.Column(db.String(100), nullable=False)
    pengarang = db.Column(db.String(100), nullable=False)
    penerbit = db.Column(db.String(100), nullable=False)
    tahun_terbit = db.Column(db.String(10), nullable=False)
    kategori = db.Column(db.String(50), nullable=False)

@app.route('/')
def senarai_buku():
    carian = request.args.get('carian', '')
    with app.app_context():
        if carian:
            senarai = Buku.query.filter(
                (Buku.tajuk.contains(carian)) |
                (Buku.pengarang.contains(carian)) |
                (Buku.penerbit.contains(carian)) |
                (Buku.tahun_terbit.contains(carian)) |
                (Buku.kategori.contains(carian))
            ).all()
        else:
            senarai = Buku.query.all()
    return render_template('senarai.html', senarai=senarai, carian=carian)

@app.route('/tambah', methods=['GET', 'POST'])
def tambah_buku():
    if request.method == 'POST':
        tajuk = request.form['tajuk']
        pengarang = request.form['pengarang']
        penerbit = request.form['penerbit']
        tahun_terbit = request.form['tahun_terbit']
        kategori = request.form['kategori']

        buku_baru = Buku(tajuk=tajuk, pengarang=pengarang, penerbit=penerbit, tahun_terbit=tahun_terbit, kategori=kategori)
        with app.app_context():
            db.session.add(buku_baru)
            db.session.commit()
        return redirect(url_for('senarai_buku'))

    return render_template('tambah.html')

@app.route('/padam/<int:buku_id>')
def padam_buku(buku_id):
    with app.app_context():
        buku_padam = Buku.query.get(buku_id)
        if buku_padam:
            db.session.delete(buku_padam)
            db.session.commit()
    return redirect(url_for('senarai_buku'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
