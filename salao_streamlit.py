import streamlit as st
import json
from datetime import datetime
import os

# Configuração da página
st.set_page_config(
    page_title="💄 Salão de Beleza",
    page_icon="💅",
    layout="wide"
)

ARQUIVO_CLIENTES = "clientes_streamlit.json"
ARQUIVO_AGENDAMENTOS = "agendamentos_streamlit.json"

SERVICOS = {
    "Manicure": 25.00,
    "Pedicure": 30.00,
    "Manicure + Pedicure": 50.00,
    "Hidratação Capilar": 60.00,
    "Corte Feminino": 70.00,
    "Coloração": 90.00,
    "Escova": 35.00
}

# ---------- Funções de Dados ----------
def carregar_dados(arquivo):
    if not os.path.exists(arquivo):
        return []
    with open(arquivo, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_dados(dados, arquivo):
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

# ---------- Interface ----------
st.title("💄 Sistema de Gestão — Salão de Beleza")
st.divider()

aba1, aba2, aba3 = st.tabs(["📋 Clientes", "📅 Agendar", "📖 Agendamentos"])

# ===== ABA 1: Clientes =====
with aba1:
    st.subheader("Cadastrar Cliente")
    col1, col2 = st.columns(2)
    with col1:
        nome = st.text_input("Nome Completo")
    with col2:
        telefone = st.text_input("Telefone")

    if st.button("✅ Cadastrar", type="primary"):
        if nome and telefone:
            clientes = carregar_dados(ARQUIVO_CLIENTES)
            clientes.append({"nome": nome, "telefone": telefone})
            salvar_dados(clientes, ARQUIVO_CLIENTES)
            st.success(f"Cliente {nome} cadastrado com sucesso!")
            st.rerun()
        else:
            st.warning("Preencha Nome e Telefone!")

    st.divider()
    st.subheader("Lista de Clientes")
    clientes = carregar_dados(ARQUIVO_CLIENTES)
    if clientes:
        st.table(clientes)
    else:
        st.info("Nenhum cliente cadastrado.")

# ===== ABA 2: Agendar =====
with aba2:
    st.subheader("Novo Agendamento")

    clientes = carregar_dados(ARQUIVO_CLIENTES)
    lista_clientes = [f"{c['nome']} — {c['telefone']}" for c in clientes] if clientes else []

    cliente_sel = st.selectbox("Selecione o Cliente", [""] + lista_clientes)
    servico_nome = st.selectbox("Serviço", list(SERVICOS.keys()))

    if servico_nome:
        valor = SERVICOS[servico_nome]
        st.info(f"Valor: R$ {valor:.2f}")

    col1, col2 = st.columns(2)
    with col1:
        data = st.date_input("Data")
    with col2:
        hora = st.time_input("Hora")

    data_hora_str = data.strftime("%d/%m/%Y") + " " + hora.strftime("%H:%M")

    if st.button("✅ Confirmar Agendamento", type="primary"):
        if cliente_sel and servico_nome:
            nome_cliente = cliente_sel.split(" — ")[0]
            agendamentos = carregar_dados(ARQUIVO_AGENDAMENTOS)
            agendamentos.append({
                "cliente": nome_cliente,
                "servico": servico_nome,
                "valor": valor,
                "data_hora": data_hora_str,
                "status": "Agendado"
            })
            salvar_dados(agendamentos, ARQUIVO_AGENDAMENTOS)
            st.success(f"Agendamento confirmado!\n{nome_cliente}\n{servico_nome} — R$ {valor:.2f}\n{data_hora_str}")
            st.rerun()
        else:
            st.warning("Selecione o cliente e o serviço!")

# ===== ABA 3: Agendamentos =====
with aba3:
    st.subheader("Todos os Agendamentos")
    agendamentos = carregar_dados(ARQUIVO_AGENDAMENTOS)

    if agendamentos:
        st.table(agendamentos)
    else:
        st.info("Nenhum agendamento registrado.")