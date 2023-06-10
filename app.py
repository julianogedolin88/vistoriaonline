from flask import Flask, render_template, request, redirect
import pymysql

app = Flask(__name__)

def get_db_connection():
    db = pymysql.connect(
        host="127.0.0.1",
        user="root",
        password="080818Tj",
        database="crud",
        cursorclass=pymysql.cursors.DictCursor
    )
    return db

def create_table():
    db = get_db_connection()
    cursor = db.cursor()

    table_query = '''
        CREATE TABLE IF NOT EXISTS itens (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(255) NOT NULL,
            descricao VARCHAR(255),
            valor FLOAT
        )
    '''
    cursor.execute(table_query)
    db.commit()

    cursor.close()
    db.close()

@app.route('/')
def index():
    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM itens")
    items = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template('index.html', items=items)

@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        db = get_db_connection()
        cursor = db.cursor()

        nome = request.form['nome']
        descricao = request.form['descricao']
        valor = request.form['valor']
        
        query = "INSERT INTO itens (nome, descricao, valor) VALUES (%s, %s, %s)"
        cursor.execute(query, (nome, descricao, valor))
        db.commit()
        
        cursor.close()
        db.close()
        
        return redirect('/')
    
    return render_template('add.html')

@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    if request.method == 'POST':
        db = get_db_connection()
        cursor = db.cursor()

        nome = request.form['nome']
        descricao = request.form['descricao']
        valor = request.form['valor']
        
        query = "UPDATE itens SET nome=%s, descricao=%s, valor=%s WHERE id=%s"
        cursor.execute(query, (nome, descricao, valor, item_id))
        db.commit()
        
        cursor.close()
        db.close()
        
        return redirect('/')
    
    db = get_db_connection()
    cursor = db.cursor()

    query = "SELECT * FROM itens WHERE id = %s"
    cursor.execute(query, (item_id,))
    item = cursor.fetchone()

    cursor.close()
    db.close()

    return render_template('edit.html', item=item)

@app.route('/delete/<int:item_id>', methods=['GET', 'POST'])
def delete_item(item_id):
    db = get_db_connection()
    cursor = db.cursor()

    query = "DELETE FROM itens WHERE id = %s"
    cursor.execute(query, (item_id,))
    db.commit()
    
    cursor.close()
    db.close()
    
    return redirect('/')

if __name__ == '__main__':
    create_table()
    app.run(debug=True)
