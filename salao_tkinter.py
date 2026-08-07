import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

# Arquivos de dados
ARQUIVO_CLIENTES = "clientes.json"
ARQUIVO_AGENDAMENTOS = "agendamentos.json"

# Serviços disponíveis
SERVICOS = {
    "Manicure": 25.00,
    "Pedicure": 30.00,
    "Manicure + Pedicure": 50.00,
    "Hidratação Capilar": 60.00,
    "Corte Feminino": 70.00,
    "Coloração": 90.00,
    "Escova": 35.00,
    "Outro": 0.00
}

# ---------- Funções de Dados ----------
def carregar_dados(arquivo):
    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def salvar_dados(dados, arquivo):
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

# ---------- Aplicativo Principal ----------
class AppSalao:
    def __init__(self, root):
        self.root = root
        self.root.title("💄 Sistema Salão de Beleza")
        self.root.geometry("750x550")  # Tamanho da janela

        # ---------- Abas ----------
        self.abas = ttk.Notebook(root)
        self.aba_clientes = ttk.Frame(self.abas)
        self.aba_agendar = ttk.Frame(self.abas)
        self.aba_agendamentos = ttk.Frame(self.abas)

        self.abas.add(self.aba_clientes, text="📋 Clientes")
        self.abas.add(self.aba_agendar, text="📅 Agendar")
        self.abas.add(self.aba_agendamentos, text="📅 Agendamentos")
        self.abas.pack(expand=1, fill="both")

        # ---------- ABA 1: Clientes ----------
        self.criar_aba_clientes()

        # ---------- ABA 2: Agendar ----------
        self.criar_aba_agendar()

        # ---------- ABA 3: Lista Agendamentos ----------
        self.criar_aba_lista_agendamentos()

        # Carregar dados na inicialização
        self.atualizar_lista_clientes()
        self.atualizar_lista_agendamentos()

    # ===== ABA CLIENTES =====
    def criar_aba_clientes(self):
        frame_cadastro = ttk.LabelFrame(self.aba_clientes, text="Cadastrar Cliente")
        frame_cadastro.pack(padx=10, pady=10, fill="x")

        ttk.Label(frame_cadastro, text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_nome = ttk.Entry(frame_cadastro, width=40)
        self.entry_nome.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_cadastro, text="Telefone:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_tel = ttk.Entry(frame_cadastro, width=40)
        self.entry_tel.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(frame_cadastro, text="✅ Cadastrar", command=self.cadastrar_cliente).grid(row=2, column=1, padx=5, pady=10)

        # Lista de clientes
        frame_lista = ttk.LabelFrame(self.aba_clientes, text="Lista de Clientes")
        frame_lista.pack(padx=10, pady=5, fill="both", expand=True)

        self.tree_clientes = ttk.Treeview(frame_lista, columns=("nome", "tel"), show="headings", height=10)
        self.tree_clientes.heading("nome", text="Nome")
        self.tree_clientes.heading("tel", text="Telefone")
        self.tree_clientes.column("nome", width=350)
        self.tree_clientes.column("tel", width=200)
        self.tree_clientes.pack(padx=5, pady=5, fill="both", expand=True)

    def cadastrar_cliente(self):
        nome = self.entry_nome.get().strip()
        tel = self.entry_tel.get().strip()
        if not nome or not tel:
            messagebox.showwarning("Atenção", "Preencha Nome e Telefone!")
            return

        clientes = carregar_dados(ARQUIVO_CLIENTES)
        clientes.append({"nome": nome, "telefone": tel})
        salvar_dados(clientes, ARQUIVO_CLIENTES)

        self.entry_nome.delete(0, tk.END)
        self.entry_tel.delete(0, tk.END)
        self.atualizar_lista_clientes()
        messagebox.showinfo("Sucesso", f"Cliente {nome} cadastrado! ✅")

    def atualizar_lista_clientes(self):
        for item in self.tree_clientes.get_children():
            self.tree_clientes.delete(item)
        clientes = carregar_dados(ARQUIVO_CLIENTES)
        for c in clientes:
            self.tree_clientes.insert("", tk.END, values=(c["nome"], c["telefone"]))

    # ===== ABA AGENDAR =====
    def criar_aba_agendar(self):
        frame = ttk.LabelFrame(self.aba_agendar, text="Novo Agendamento")
        frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Cliente
        ttk.Label(frame, text="Cliente:").grid(row=0, column=0, padx=5, pady=8, sticky="w")
        self.combo_cliente = ttk.Combobox(frame, width=38, state="readonly")
        self.combo_cliente.grid(row=0, column=1, padx=5, pady=8)
        self.combo_cliente.bind("<Button-1>", lambda e: self.atualizar_combo_clientes())

        # Serviço
        ttk.Label(frame, text="Serviço:").grid(row=1, column=0, padx=5, pady=8, sticky="w")
        self.combo_servico = ttk.Combobox(frame, width=38, values=list(SERVICOS.keys()))
        self.combo_servico.grid(row=1, column=1, padx=5, pady=8)
        self.combo_servico.bind("<<ComboboxSelected>>", self.atualizar_valor)

        # Valor
        ttk.Label(frame, text="Valor R$:").grid(row=2, column=0, padx=5, pady=8, sticky="w")
        self.label_valor = ttk.Label(frame, text="0,00", font=("", 10, "bold"))
        self.label_valor.grid(row=2, column=1, padx=5, pady=8, sticky="w")

        # Data e Hora
        ttk.Label(frame, text="Data (DD/MM/AAAA):").grid(row=3, column=0, padx=5, pady=8, sticky="w")
        self.entry_data = ttk.Entry(frame, width=38)
        self.entry_data.grid(row=3, column=1, padx=5, pady=8)

        ttk.Label(frame, text="Hora (HH:MM):").grid(row=4, column=0, padx=5, pady=8, sticky="w")
        self.entry_hora = ttk.Entry(frame, width=38)
        self.entry_hora.grid(row=4, column=1, padx=5, pady=8)

        # Botão
        ttk.Button(frame, text="✅ Confirmar Agendamento", command=self.agendar).grid(row=5, column=1, padx=5, pady=15)

    def atualizar_combo_clientes(self, event=None):
        clientes = carregar_dados(ARQUIVO_CLIENTES)
        lista = [f"{c['nome']} — {c['telefone']}" for c in clientes]
        self.combo_cliente["values"] = lista

    def atualizar_valor(self, event=None):
        servico = self.combo_servico.get()
        if servico in SERVICOS:
            self.label_valor.config(text=f"{SERVICOS[servico]:.2f}")

    def agendar(self):
        cliente_info = self.combo_cliente.get()
        servico = self.combo_servico.get()
        valor = self.label_valor.cget("text")
        data = self.entry_data.get().strip()
        hora = self.entry_hora.get().strip()

        if not cliente_info or not servico or not data or not hora:
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return

        try:
            data_hora = f"{data} {hora}"
            datetime.strptime(data_hora, "%d/%m/%Y %H:%M")
        except ValueError:
            messagebox.showerror("Erro", "Data ou Hora inválida!\nUse: DD/MM/AAAA e HH:MM")
            return

        nome_cliente = cliente_info.split(" — ")[0]
        agendamentos = carregar_dados(ARQUIVO_AGENDAMENTOS)
        agendamentos.append({
            "cliente": nome_cliente,
            "servico": servico,
            "valor": float(valor.replace(",", ".")),
            "data_hora": data_hora,
            "status": "Agendado"
        })
        salvar_dados(agendamentos, ARQUIVO_AGENDAMENTOS)

        self.combo_cliente.set("")
        self.combo_servico.set("")
        self.label_valor.config(text="0,00")
        self.entry_data.delete(0, tk.END)
        self.entry_hora.delete(0, tk.END)
        self.atualizar_lista_agendamentos()
        messagebox.showinfo("Sucesso ✅", f"Agendamento confirmado!\n{nome_cliente}\n{servico} — R$ {valor}\n{data_hora}")

    # ===== ABA LISTA DE AGENDAMENTOS =====
    def criar_aba_lista_agendamentos(self):
        frame = ttk.LabelFrame(self.aba_agendamentos, text="Todos os Agendamentos")
        frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.tree_agenda = ttk.Treeview(frame, columns=("data", "cliente", "servico", "valor", "status"), show="headings", height=12)
        self.tree_agenda.heading("data", text="Data/Hora")
        self.tree_agenda.heading("cliente", text="Cliente")
        self.tree_agenda.heading("servico", text="Serviço")
        self.tree_agenda.heading("valor", text="Valor R$")
        self.tree_agenda.heading("status", text="Status")

        self.tree_agenda.column("data", width=140)
        self.tree_agenda.column("cliente", width=180)
        self.tree_agenda.column("servico", width=160)
        self.tree_agenda.column("valor", width=90)
        self.tree_agenda.column("status", width=100)
        self.tree_agenda.pack(padx=5, pady=5, fill="both", expand=True)

    def atualizar_lista_agendamentos(self):
        for item in self.tree_agenda.get_children():
            self.tree_agenda.delete(item)
        agenda = carregar_dados(ARQUIVO_AGENDAMENTOS)
        for a in agenda:
            self.tree_agenda.insert("", tk.END, values=(
                a["data_hora"], a["cliente"], a["servico"],
                f"{a['valor']:.2f}", a["status"]
            ))

# ---------- Executar ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = AppSalao(root)
    root.mainloop()
