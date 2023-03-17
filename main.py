from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.toast import toast
from kivy.core.window import Window
from kivymd.uix.screen import MDScreen
from kivy.properties import ObjectProperty
from kivymd.uix.screenmanager import MDScreenManager

import bd_info as api

Builder.load_file("gui.kv")

class Sc_Manager(MDScreenManager):
    pass

class Sc_Perfil(MDScreen):
    pass

class Sc_Login(MDScreen):
    def novo_login(self, usuario, senha):
        api.fazer_login(usuario, senha)

class Sc_Cadastro(MDScreen):
    def novo_cadastro(self, un, ua, eu, us1, us2, ps, rs):
        if us1 != "" and us2 != "" and us1 == us2:
            api.cadastro_usuario(un, ua, eu, us2, ps, rs) 
        else:
            toast("Verifique se campos de senhas estão iguais.")

class Sc_Config(MDScreen):
    txt_pergunta = ObjectProperty(None)
    txt_resposta = ObjectProperty(None)
    txt_senha = ObjectProperty(None)
    txt_senha_confirma = ObjectProperty(None)
    txt_email = ObjectProperty(None)

    def verificar_email(self, e):
        api.verificar_email(e)

    def verificar_formulario(self, p, r, s1, s2, e):
        if e != '':            
            if s1 == s2:                
                api.verificar_pergunta(p, r, s2, e)

    def alterar_senha(self, s1, s2, e):
        if s1 != '' and s2 != '' and e != '':
            if s1 == s2:
                api.alterar_senha(s2, e)                
            else: 
                toast("As senhas devem ser iguais.")                

class loginApp(MDApp):  
    def on_stop(self):
        api.desconecte()      
    def build(self):
        self.title = "App de Login"
        Window.size = (320, 460)
        self.sm = Sc_Manager()
        api.criar_tabela()
        return self.sm

if __name__ == "__main__":        
    loginApp().run()
