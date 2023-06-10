import unittest
from flask import Flask
from flask_testing import TestCase
from app import app, get_db_connection

class AppTest(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def setUp(self):
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

        insert_query = "INSERT INTO itens (nome, descricao, valor) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, ("Item 1", "Descrição do Item 1", 10.99))
        cursor.execute(insert_query, ("Item 2", "Descrição do Item 2", 15.99))
        db.commit()

        cursor.close()
        db.close()

    def tearDown(self):
        db = get_db_connection()
        cursor = db.cursor()

        cursor.execute("DROP TABLE itens")
        db.commit()

        cursor.close()
        db.close()

    def test_list_items(self):
        response = self.client.get('/')
        self.assert200(response)
        self.assertTemplateUsed('index.html')
        items = self.get_context_variable('items')
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]['nome'], 'Item 1')
        self.assertEqual(items[1]['descricao'], 'Descrição do Item 2')

if __name__ == '__main__':
    unittest.main()