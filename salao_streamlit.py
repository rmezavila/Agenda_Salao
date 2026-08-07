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

# Lista padrão de serviços com valores SUGERIDOS (pode alterar ao agendar)
SERVICOS_PADRAO = {
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

# ---------- Interface Principal ----------
st.title("💄 Sistema de Gestão — Salão de Beleza")
st.divider()

aba1, aba2, aba3, aba4 = st.tabs([
    "📋 Clientes",
    "📅 Agendar",
    "📖 Agendamentos",
    "📊 Financeiro"
])

# ===== ABA 1: Clientes (Cadastrar, Editar, Excluir) =====
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
    st.subheader("Editar / Excluir Cliente")

    clientes = carregar_dados(ARQUIVO_CLIENTES)
    if clientes:
        lista_nomes = [f"{c['nome']} — {c['telefone']}" for c in clientes]
        escolha = st.selectbox("Selecione o Cliente", [""] + lista_nomes)

        if escolha:
            indice = lista_nomes.index(escolha)
            cliente_atual = clientes[indice]

            novo_nome = st.text_input("Novo Nome", value=cliente_atual["nome"])
            novo_telefone = st.text_input("Novo Telefone", value=cliente_atual["telefone"])

            col_editar, col_excluir = st.columns(2)

            with col_editar:
                if st.button("✏️ Salvar Alterações", type="primary"):
                    clientes[indice]["nome"] = novo_nome
                    clientes[indice]["telefone"] = novo_telefone
                    salvar_dados(clientes, ARQUIVO_CLIENTES)
                    st.success("Cliente atualizado! ✅")
                    st.rerun()

            with col_excluir:
                if st.button("🗑️ Excluir Cliente", type="secondary"):
                    clientes.pop(indice)
                    salvar_dados(clientes, ARQUIVO_CLIENTES)
                    st.warning("Cliente excluído! ⚠️")
                    st.rerun()
    else:
        st.info("Nenhum cliente cadastrado.")

    st.divider()
    st.subheader("Lista de Clientes")
    st.table(clientes)

# ===== ABA 2: Agendar (com valor editável) =====
with aba2:
    st.subheader("Novo Agendamento")

    clientes = carregar_dados(ARQUIVO_CLIENTES)
    lista_clientes = [f"{c['nome']} — {c['telefone']}" for c in clientes] if clientes else []

    cliente_sel = st.selectbox("Selecione o Cliente", [""] + lista_clientes)

    servico_nome = st.selectbox("Serviço", list(SERVICOS_PADRAO.keys()))

    if servico_nome:
        valor_padrao = SERVICOS_PADRAO[servico_nome]
        valor = st.number_input("Valor do Serviço (R$)",
                                  min_value=0.0,
                                  value=float(valor_padrao),
                                  step=5.0,
                                  format="%.2f")
        st.info(f"Valor padrão: R$ {valor_padrao:.2f} — ajuste acima se precisar")

    col1, col2 = st.columns(2)
    with col1:
        data = st.date_input("Data")
    with col2:
        hora = st.time_input("Hora")

    data_hora_str = data.strftime("%d/%m/%Y") + " " + hora.strftime("%H:%M")

    if st.button("✅ Confirmar Agendamento", type="primary"):
        if cliente_sel and servico_nome and valor > 0:
            nome_cliente = cliente_sel.split(" — ")[0]
            agendamentos = carregar_dados(ARQUIVO_AGENDAMENTOS)
            agendamentos.append({
                "cliente": nome_cliente,
                "servico": servico_nome,
                "valor": round(valor, 2),
                "data_hora": data_hora_str,
                "data": data.strftime("%d/%m/%Y"),
                "status": "Agendado"
            })
            salvar_dados(agendamentos, ARQUIVO_AGENDAMENTOS)
            st.success(f"""✅ Agendamento confirmado!
👤 Cliente: {nome_cliente}
💇 Serviço: {servico_nome}
💰 Valor: R$ {valor:.2f}
📅 Data: {data_hora_str}""")
            st.rerun()
        else:
            st.warning("Preencha todos os campos!")

# ===== ABA 3: Agendamentos =====
with aba3:
    st.subheader("Todos os Agendamentos")
    agendamentos = carregar_dados(ARQUIVO_AGENDAMENTOS)

    if agendamentos:
        st.table(agendamentos)
    else:
        st.info("Nenhum agendamento registrado.")

# ===== ABA 4: RELATÓRIO FINANCEIRO =====
with aba4:
    st.subheader("💰 Relatório Financeiro")
    st.divider()

    agendamentos = carregar_dados(ARQUIVO_AGENDAMENTOS)

    if not agendamentos:
        st.info("Nenhum agendamento registrado ainda.")
    else:
        # Pegar datas únicas para filtro
        datas_disponiveis = sorted(list(set([a["data"] for a in agendamentos])), reverse=True)

        filtro_data = st.selectbox("Filtrar por Data", ["Todas"] + datas_disponiveis)

        # Aplicar filtro
        if filtro_data == "Todas":
            lista_filtrada = agendamentos
            st.info(f"Período: TODAS as datas ({len(agendamentos)} agendamentos)")
        else:
            lista_filtrada = [a for a in agendamentos if a["data"] == filtro_data]
            st.info(f"Data: {filtro_data} ({len(lista_filtrada)} agendamentos)")

        # Calcular totais
        total_valor = sum([a["valor"] for a in lista_filtrada])
        qtd_servicos = len(lista_filtrada)

        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.metric(label="🔢 Serviços Realizados", value=f"{qtd_servicos}")
        with col_res2:
            st.metric(label="💵 Valor Total", value=f"R$ {total_valor:.2f}")

        st.divider()
        st.subheader("📋 Detalhamento")
        st.table(lista_filtrada)
