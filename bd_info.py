import hashlib
import mysql.connector
from kivymd.app import MDApp
from datetime import datetime
from kivymd.toast import toast
from kivymd.uix.screen import MDScreen


connect_args = {
"host": "localhost",
"database": "bd_app_login",
"user": "root",
"password": ""
}

class Data(MDScreen):
	conexao = mysql.connector.connect(**connect_args)
	cursor = conexao.cursor(buffered=True)
	
	def __init__(self, **kwargs):
		super(Data, self).__init__(**kwargs)
		self.current_app = MDApp.get_running_app()
		self.criar_tabela_de_login()

	def desconectar(self):		
		self.cursor.close()
		self.conexao.close()
		
	def criar_tabela_de_login(self):
		sql = """CREATE TABLE IF NOT EXISTS tb_usuarios(id integer PRIMARY KEY AUTO_INCREMENT, nome VARCHAR(25) NOT NULL, apelido VARCHAR(25) NOT NULL, email VARCHAR(30) NOT NULL, senha VARCHAR(36) NOT NULL, pergunta VARCHAR(40) NOT NULL, resposta VARCHAR(40) NOT NULL, data_cadastro DATE NULL)"""
		self.cursor.execute(sql)

	def login(self, ua, pw): 		
		txt_name = ua
		hash_pw = hashlib.md5(pw.encode("utf-8")).hexdigest()
		sql = """SELECT nome, apelido, email, senha FROM tb_usuarios WHERE apelido = %s AND senha = %s"""
		self.cursor.execute(sql, (txt_name, hash_pw,))
		data = self.cursor.fetchone()
		if data is not None:				
			if (txt_name == data[1] and hash_pw == data[3]):				
				toast("Login efetuado com sucesso.")
				self.current_app.sm.current = "sc_perfil"
				sc = self.current_app.sm.get_screen("sc_perfil")
				sc.txt_nome.text = data[0]
				sc.txt_apelido.text = data[1]
				sc.txt_email.text= data[2]
				return True
			else:
				toast("Erro. Informações inválidas.")
				return False		
		else:
			toast("Erro. Informações inválidas.")

	def verificar_email(self, e):
		sql = """SELECT id, email, pergunta, resposta FROM tb_usuarios WHERE email = %s"""
		self.cursor.execute(sql, (e,))
		data = self.cursor.fetchone()
		if data is not None:			
			self.current_app.sm.get_screen("sc_config").txt_resposta.disabled = False
			self.current_app.sm.get_screen("sc_config").txt_pergunta.text = data[2]
			self.current_app.sm.get_screen("sc_config").txt_resposta.focus = True
			toast("Agora informe a resposta secreta.")
		elif e == "":
			toast("Digite seu email")
		else:
			toast("Email não encontrado.")

	def verificar_pergunta_secreta(self, p, r, s, e):
		sql = """SELECT id, email, pergunta, resposta FROM tb_usuarios WHERE email = %s"""
		valores = e
		self.cursor.execute(sql, (valores,))
		data = self.cursor.fetchone()
		if data is not None:
			if p == data[2] and r == data[3]:
				self.current_app.sm.get_screen("sc_config").txt_senha.disabled = False
				self.current_app.sm.get_screen("sc_config").txt_senha_confirma.disabled = False
				self.current_app.sm.get_screen("sc_config").txt_senha.focus = True
				toast("Agora informa a nova senha.")
			else:
				toast("Por favor responda corretamente.")				
		else:
			toast("Informações inválidas.")

	def nova_senha(self, s, e):
		sql = """SELECT id, email FROM tb_usuarios WHERE email = %s"""		
		self.cursor.execute(sql, (e,))
		data = self.cursor.fetchone()
		if data is not None:
			query = ("""UPDATE tb_usuarios SET senha = %s WHERE email = %s""")
			us = hashlib.md5(s.encode("utf-8")).hexdigest()
			valores = us, e
			self.cursor.execute(query, (valores))
			self.conexao.commit()
			toast("Informações atualizadas com sucesso.")
		else:
			toast("Informações inválidas.")

	def cadastrar_usuario(self, un, ua, eu, us, ps, rs):
		# nome, apelido, email, senha, pergunta, resposta
		agora = datetime.now()
		verifica_sql = "SELECT apelido, email FROM tb_usuarios WHERE apelido = %s OR email = %s"
		dados_sql = un, eu
		self.cursor.execute(verifica_sql, (dados_sql))
		data = self.cursor.fetchone()
		if data is None:
			query = """INSERT INTO tb_usuarios (nome, apelido, email, senha, pergunta, resposta, data_cadastro) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
			us = hashlib.md5(us.encode("utf-8")).hexdigest()
			valores = un, ua, eu, us, ps, rs, str(agora)
			self.cursor.execute(query, valores)
			self.conexao.commit()
			toast("Usuário Cadastrado com Sucesso!")
		else:
			toast("Impossível Efetuar Cadastro!")

def desconecte():
	dt = Data()
	dt.desconectar()

def criar_tabela():
	dt = Data()
	dt.criar_tabela_de_login()

def fazer_login(us, pw):	
	dt = Data()
	dt.login(us, pw)

def verificar_email(e):
	dt = Data()
	dt.verificar_email(e)

def verificar_pergunta(p, r, s, e):	
	dt = Data()
	dt.verificar_pergunta_secreta(p, r, s, e)

def alterar_senha(s, e):
	dt = Data()
	dt.nova_senha(s, e)

def cadastro_usuario(un, ua, eu, us, ps, rs):	
	dt = Data()
	dt.cadastrar_usuario(un, ua, eu, us, ps, rs)