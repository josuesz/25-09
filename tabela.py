import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# Função para criar o banco de dados e as tabelas
def criar_banco():
    conn = sqlite3.connect('sistema.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            senha TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cidades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            estado TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

class SistemaCadastro:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Cadastro")

        # Variáveis para usuários
        self.nome_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.senha_var = tk.StringVar()

        # Variáveis para cidades
        self.nome_cidade_var = tk.StringVar()
        self.estado_var = tk.StringVar()

        # Frame para cadastro de usuários
        user_frame = tk.LabelFrame(root, text="Cadastro de Usuários")
        user_frame.pack(pady=10, padx=10, fill="both")

        tk.Label(user_frame, text="Nome:").grid(row=0, column=0)
        tk.Entry(user_frame, textvariable=self.nome_var).grid(row=0, column=1)

        tk.Label(user_frame, text="Email:").grid(row=1, column=0)
        tk.Entry(user_frame, textvariable=self.email_var).grid(row=1, column=1)

        tk.Label(user_frame, text="Senha:").grid(row=2, column=0)
        tk.Entry(user_frame, textvariable=self.senha_var, show='*').grid(row=2, column=1)

        tk.Button(user_frame, text="Incluir", command=self.incluir_usuario).grid(row=3, column=0)
        tk.Button(user_frame, text="Alterar", command=self.alterar_usuario).grid(row=3, column=1)
        tk.Button(user_frame, text="Excluir", command=self.excluir_usuario).grid(row=3, column=2)

        # TreeView para usuários
        self.tree_usuario = ttk.Treeview(root, columns=("ID", "Nome", "Email"), show='headings')
        self.tree_usuario.heading("ID", text="ID")
        self.tree_usuario.heading("Nome", text="Nome")
        self.tree_usuario.heading("Email", text="Email")
        self.tree_usuario.pack(pady=10)

        self.tree_usuario.bind("<ButtonRelease-1>", self.on_tree_select_usuario)

        self.listar_usuarios()

        # Frame para cadastro de cidades
        city_frame = tk.LabelFrame(root, text="Cadastro de Cidades")
        city_frame.pack(pady=10, padx=10, fill="both")

        tk.Label(city_frame, text="Nome da Cidade:").grid(row=0, column=0)
        tk.Entry(city_frame, textvariable=self.nome_cidade_var).grid(row=0, column=1)

        tk.Label(city_frame, text="Estado:").grid(row=1, column=0)
        tk.Entry(city_frame, textvariable=self.estado_var).grid(row=1, column=1)

        tk.Button(city_frame, text="Incluir", command=self.incluir_cidade).grid(row=2, column=0)
        tk.Button(city_frame, text="Alterar", command=self.alterar_cidade).grid(row=2, column=1)
        tk.Button(city_frame, text="Excluir", command=self.excluir_cidade).grid(row=2, column=2)

        # TreeView para cidades
        self.tree_cidade = ttk.Treeview(root, columns=("ID", "Nome", "Estado"), show='headings')
        self.tree_cidade.heading("ID", text="ID")
        self.tree_cidade.heading("Nome", text="Nome")
        self.tree_cidade.heading("Estado", text="Estado")
        self.tree_cidade.pack(pady=10)

        self.tree_cidade.bind("<ButtonRelease-1>", self.on_tree_select_cidade)

        self.listar_cidades()

    # Funções para usuários
    def listar_usuarios(self):
        for i in self.tree_usuario.get_children():
            self.tree_usuario.delete(i)
        conn = sqlite3.connect('sistema.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios")
        for row in cursor.fetchall():
            self.tree_usuario.insert("", "end", values=row)
        conn.close()

    def incluir_usuario(self):
        nome = self.nome_var.get()
        email = self.email_var.get()
        senha = self.senha_var.get()
        if nome and email and senha:
            conn = sqlite3.connect('sistema.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)", (nome, email, senha))
            conn.commit()
            conn.close()
            self.listar_usuarios()
            self.limpar_campos_usuario()
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos!")

    def alterar_usuario(self):
        selected_item = self.tree_usuario.selection()
        if selected_item:
            id_usuario = self.tree_usuario.item(selected_item[0])["values"][0]
            nome = self.nome_var.get()
            email = self.email_var.get()
            senha = self.senha_var.get()
            if nome and email and senha:
                conn = sqlite3.connect('sistema.db')
                cursor = conn.cursor()
                cursor.execute("UPDATE usuarios SET nome=?, email=?, senha=? WHERE id=?", (nome, email, senha, id_usuario))
                conn.commit()
                conn.close()
                self.listar_usuarios()
                self.limpar_campos_usuario()
            else:
                messagebox.showwarning("Atenção", "Preencha todos os campos!")
        else:
            messagebox.showwarning("Atenção", "Selecione um usuário para alterar!")

    def excluir_usuario(self):
        selected_item = self.tree_usuario.selection()
        if selected_item:
            id_usuario = self.tree_usuario.item(selected_item[0])["values"][0]
            conn = sqlite3.connect('sistema.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM usuarios WHERE id=?", (id_usuario,))
            conn.commit()
            conn.close()
            self.listar_usuarios()
            self.limpar_campos_usuario()
        else:
            messagebox.showwarning("Atenção", "Selecione um usuário para excluir!")

    def on_tree_select_usuario(self, event):
        selected_item = self.tree_usuario.selection()
        if selected_item:
            id_usuario, nome, email = self.tree_usuario.item(selected_item[0])["values"]
            self.nome_var.set(nome)
            self.email_var.set(email)
            self.senha_var.set("")  # Mantenha a senha em branco ao selecionar

    def limpar_campos_usuario(self):
        self.nome_var.set("")
        self.email_var.set("")
        self.senha_var.set("")

    # Funções para cidades
    def listar_cidades(self):
        for i in self.tree_cidade.get_children():
            self.tree_cidade.delete(i)
        conn = sqlite3.connect('sistema.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cidades")
        for row in cursor.fetchall():
            self.tree_cidade.insert("", "end", values=row)
        conn.close()

    def incluir_cidade(self):
        nome = self.nome_cidade_var.get()
        estado = self.estado_var.get()
        if nome and estado:
            conn = sqlite3.connect('sistema.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO cidades (nome, estado) VALUES (?, ?)", (nome, estado))
            conn.commit()
            conn.close()
            self.listar_cidades()
            self.limpar_campos_cidade()
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos!")

    def alterar_cidade(self):
        selected_item = self.tree_cidade.selection()
        if selected_item:
            id_cidade = self.tree_cidade.item(selected_item[0])["values"][0]
            nome = self.nome_cidade_var.get()
            estado = self.estado_var.get()
            if nome and estado:
                conn = sqlite3.connect('sistema.db')
                cursor = conn.cursor()
                cursor.execute("UPDATE cidades SET nome=?, estado=? WHERE id=?", (nome, estado, id_cidade))
                conn.commit()
                conn.close()
                self.listar_cidades()
                self.limpar_campos_cidade()
            else:
                messagebox.showwarning("Atenção", "Preencha todos os campos!")
        else:
            messagebox.showwarning("Atenção", "Selecione uma cidade para alterar!")

    def excluir_cidade(self):
        selected_item = self.tree_cidade.selection()
        if selected_item:
            id_cidade = self.tree_cidade.item(selected_item[0])["values"][0]
            conn = sqlite3.connect('sistema.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM cidades WHERE id=?", (id_cidade,))
            conn.commit()
            conn.close()
            self.listar_cidades()
            self.limpar_campos_cidade()
        else:
            messagebox.showwarning("Atenção", "Selecione uma cidade para excluir!")

    def on_tree_select_cidade(self, event):
        selected_item = self.tree_cidade.selection()
        if selected_item:
            id_cidade, nome, estado = self.tree_cidade.item(selected_item[0])["values"]
            self.nome_cidade_var.set(nome)
            self.estado_var.set(estado)

    def limpar_campos_cidade(self):
        self.nome_cidade_var.set("")
        self.estado_var.set("")

if __name__ == "__main__":
    criar_banco()
    root = tk.Tk()
    app = SistemaCadastro(root)
    root.mainloop()
