from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)
app.secret_key = 'secretkey'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'musik'

mysql = MySQL(app)

def insert_sample_data():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM lagu")
    count = cursor.fetchone()[0]

    if count == 0:
        try:
            cursor.execute("""
                INSERT INTO lagu (judul, penyanyi, genre, tahun_rilis)
                VALUES
                ('Shape of You', 'Ed Sheeran', 'Pop', 2017),
                ('Blinding Lights', 'The Weeknd', 'Pop', 2020),
                ('Bohemian Rhapsody', 'Queen', 'Rock', 1975)
            """)
            mysql.connection.commit()
        except Exception as e:
            print(f'Error saat menambahkan data: {str(e)}')
        finally:
            cursor.close()

@app.before_request
def before_request():
    insert_sample_data()

@app.route('/')
def index():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM lagu")
        lagu = cursor.fetchall()
        return render_template('index.html', lagu=lagu)
    except Exception as e:
        flash(f'Error: {str(e)}')
        return redirect(url_for('index'))

@app.route('/tambah', methods=['GET', 'POST'])
def tambah():
    if request.method == 'POST':
        try:
            judul = request.form['judul']
            penyanyi = request.form['penyanyi']
            genre = request.form['genre']
            tahun_rilis = request.form['tahun_rilis']

            if not judul or not penyanyi or not genre or not tahun_rilis:
                flash('Semua field harus diisi!')
                return redirect(url_for('tambah'))

            cursor = mysql.connection.cursor()
            cursor.execute(
                "INSERT INTO lagu (judul, penyanyi, genre, tahun_rilis) VALUES (%s, %s, %s, %s)",
                (judul, penyanyi, genre, tahun_rilis)
            )
            mysql.connection.commit()
            flash('Lagu berhasil ditambahkan!')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Error: {str(e)}')
            return redirect(url_for('tambah'))
    return render_template('tambah.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM lagu WHERE id = %s", (id,))
        lagu = cursor.fetchone()

        if request.method == 'POST':
            judul = request.form['judul']
            penyanyi = request.form['penyanyi']
            genre = request.form['genre']
            tahun_rilis = request.form['tahun_rilis']

            if not judul or not penyanyi or not genre or not tahun_rilis:
                flash('Semua field harus diisi!')
                return redirect(url_for('edit', id=id))

            cursor.execute(
                "UPDATE lagu SET judul = %s, penyanyi = %s, genre = %s, tahun_rilis = %s WHERE id = %s",
                (judul, penyanyi, genre, tahun_rilis, id)
            )
            mysql.connection.commit()
            flash('Lagu berhasil diperbarui!')
            return redirect(url_for('index'))
        return render_template('edit.html', lagu=lagu)
    except Exception as e:
        flash(f'Error: {str(e)}')
        return redirect(url_for('index'))

@app.route('/hapus/<int:id>')
def hapus(id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM lagu WHERE id = %s", (id,))
        mysql.connection.commit()
        flash('Lagu berhasil dihapus!')
        return redirect(url_for('index'))
    except Exception as e:
        flash(f'Error: {str(e)}')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
