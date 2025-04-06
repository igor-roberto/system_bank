import customtkinter as ctk
import mysql.connector # Biblioteca para se conectar ao banco de dados


ctk.set_appearance_mode('light') #light para modo claro, e dark para modo escuro do app

# Função para validar acesso
def validar_acesso():
    ag_user = ag_entry.get()
    conta_user = conta_entry.get()
    pw_user = pw_entry.get()

    try:
        # Convertendo valores numéricos
        ag_user = int(ag_user)  # Transforma em INT
        pw_user = int(pw_user)  # Transforma em INT

        # Conectar ao banco de dados
        conexao = mysql.connector.connect(
            host="dbitalux1.cmvqca8o25u9.us-east-1.rds.amazonaws.com", #endpoint da AWS
            user="admin",
            password="ysMkRlKKvvrd5PlAXGMC",
            database="dbitalux",
            port=3305  #Se deixar a porta padrão que é a 3306, nem precisa colocar isso
        )

        cursor = conexao.cursor()

        # Consultando o banco de dados
        query = "SELECT * FROM conta WHERE agencia = %s AND `conta` = %s AND senha = %s"
        valores = (ag_user, conta_user, pw_user)

        cursor.execute(query, valores)
        resultado = cursor.fetchone()  # Pega apenas um resultado

        if resultado: #Se a variavel resultado for verdadeiro vai acontecer oq esta abaixo, caso contrario vai dar login incorreto
            login_access.configure(text='✅ Login feito com sucesso!', text_color='green') #Na linha 75 tem a variavel login_acess com o texto vazio, dai aqui eu uso o configure para adicionar um texto
        else:
            login_access.configure(text='❌ Login incorreto!', text_color='red')

        # Fechar cursor e conexão
        cursor.close()
        conexao.close()

    except ValueError:
        login_access.configure(text='❌ Erro: Agência e senha devem ser números!', text_color='red')

    except mysql.connector.Error as err:
        login_access.configure(text=f'⚠ Erro no banco: {err}', text_color='red')

app = ctk.CTk() #inicializando o app
app.title('Italux Bank') #colocando o nome em cima
app.geometry("320x170") #definindo o tamanho da janela
app.resizable(False, False) #Colocando false em tudo quero dizer que não quero dar a opção de ficar redimensionando a janela


ag = ctk.CTkLabel(app, text="Agência") #Definindo o titulo da Agencia com o label
ag.grid(row=0, column=0, padx=10,sticky='w') # o grid, eu coloco a posição que vai ficar row=0(linha zero), column=0(coluna zero)
ag_entry= ctk.CTkEntry(app, placeholder_text='1234') # Aqui estou criando a caixinha e no placeholder coloco oq vai escrito dentro
ag_entry.grid(row=1, column=0, padx=10)

conta = ctk.CTkLabel(app, text="Conta")
conta.grid(row=0, column=1, padx=10, sticky='w')
conta_entry= ctk.CTkEntry(app, placeholder_text='12345-6')
conta_entry.grid(row=1, column=1, padx=10)

pw= ctk.CTkLabel(app, text="Senha")
pw.grid(row=2, column=0,padx=10, sticky='w')
pw_entry= ctk.CTkEntry(app, placeholder_text='6 dígitos', show='●')
pw_entry.grid(row=3, column=0, padx=10)

enter= ctk.CTkButton(app, text="Entrar",hover_color='#dd5500', fg_color= "#ff6200",text_color='#fff',command=validar_acesso) #criando o botão entrar
enter.grid(row=3, column=1,padx=10, sticky='w')

login_access= ctk.CTkLabel(app, text='') #Aqui é onde vai ficar a escrita de 'Login feito com sucesso!' ou 'Login incorreto!', eu deixo vazio pois o texto que vai aqui irá depender se os dados do usuário irá estar na base de dados
login_access.grid(row=5, column=0, columnspan=2)


app.mainloop() #Iniciando a aplicação
