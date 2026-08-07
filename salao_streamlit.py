import streamlit as st
import json
from datetime import datetime
import os

# Configuração da página
st.set_page_config(
    page_title="Salão Abelhinha",   # ← Nome que aparece na aba
    page_icon="🐝",                 # ← Ícone (abelhinha!)
    layout="wide"
)
)
st.image("logo.jpg", width=300)

ARQUIVO_CLIENTES = "clientes_streamlit.json"
ARQUIVO_AGENDAMENTOS = "agendamentos_streamlit.json"

SERVICOS_PADRAO = {
    "Manicure": 25.00,
    "Pedicure": 30.00,
    "Manicure + Pedicure": 50.00,
    "Hidratação Capilar": 60.00,
    "Corte Feminino": 70.00,
    "Coloração": 90.00,
    "Escova": 35.00,
    "Outros": 0.00
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
st.title("💄 Sistema de Gestão — Salão Abelhinha")
st.divider()

aba1, aba2, aba3, aba4 = st.tabs([
    "📋 Clientes",
    "📅 Agendar",
    "📖 Agendamentos",
    "📊 Relatório Financeiro"
])

# ===== ABA 1: Clientes =====
with aba1:
    st.subheader("Cadastrar Cliente")
    with st.form("form_cadastro", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome Completo")
        with col2:
            telefone = st.text_input("Telefone")
        cadastrar = st.form_submit_button("✅ Cadastrar", type="primary")
        if cadastrar:
            if nome and telefone:
                clientes = carregar_dados(ARQUIVO_CLIENTES)
                clientes.append({"nome": nome, "telefone": telefone})
                salvar_dados(clientes, ARQUIVO_CLIENTES)
                st.success(f"✅ Cliente **{nome}** cadastrado com sucesso!")
            else:
                st.warning("⚠️ Preencha Nome e Telefone!")

    st.divider()
    st.subheader("Editar / Excluir Cliente")
    clientes = carregar_dados(ARQUIVO_CLIENTES)
    if clientes:
        lista_nomes = [f"{c['nome']} — {c['telefone']}" for c in clientes]
        escolha = st.selectbox("Cliente para Editar/Excluir", [""] + lista_nomes, key="sel_editar")
        if escolha:
            indice = lista_nomes.index(escolha)
            cliente_atual = clientes[indice]
            novo_nome = st.text_input("Novo Nome", value=cliente_atual["nome"], key="edit_nome")
            novo_telefone = st.text_input("Novo Telefone", value=cliente_atual["telefone"], key="edit_tel")
            col_editar, col_excluir = st.columns(2)
            with col_editar:
                if st.button("✏️ Salvar Alterações", type="primary"):
                    clientes[indice]["nome"] = novo_nome
                    clientes[indice]["telefone"] = novo_telefone
                    salvar_dados(clientes, ARQUIVO_CLIENTES)
                    st.success("✅ Cliente atualizado!")
                    st.rerun()
            with col_excluir:
                if st.button("🗑️ Excluir Cliente", type="secondary"):
                    clientes.pop(indice)
                    salvar_dados(clientes, ARQUIVO_CLIENTES)
                    st.warning("⚠️ Cliente excluído!")
                    st.rerun()
    else:
        st.info("Nenhum cliente cadastrado.")
    st.divider()
    st.subheader("Lista de Clientes")
    st.table(clientes)

# ===== ABA 2: Agendar =====
with aba2:
    st.subheader("Novo Agendamento")
    clientes = carregar_dados(ARQUIVO_CLIENTES)
    lista_clientes = [f"{c['nome']} — {c['telefone']}" for c in clientes] if clientes else []
    with st.form("form_agendar", clear_on_submit=True):
        cliente_sel = st.selectbox("Selecione o Cliente", [""] + lista_clientes)
        servico_nome = st.selectbox("Serviço", list(SERVICOS_PADRAO.keys()))
        valor = st.number_input("Valor do Serviço (R$)", min_value=0.0, value=0.00, step=5.0, format="%.2f")
        col1, col2 = st.columns(2)
        with col1:
            data = st.date_input("Data", format="DD/MM/YYYY")
        with col2:
            hora = st.time_input("Hora")
        confirmar = st.form_submit_button("✅ Confirmar Agendamento", type="primary")
        if confirmar:
            if cliente_sel and servico_nome and valor > 0:
                nome_cliente = cliente_sel.split(" — ")[0]
                data_hora_str = data.strftime("%d/%m/%Y") + " " + hora.strftime("%H:%M")
                data_str = data.strftime("%d/%m/%Y")
                agendamentos = carregar_dados(ARQUIVO_AGENDAMENTOS)
                agendamentos.append({
                    "cliente": nome_cliente,
                    "servico": servico_nome,
                    "valor": round(valor, 2),
                    "data_hora": data_hora_str,
                    "data": data_str,
                    "status": "Agendado"
                })
                salvar_dados(agendamentos, ARQUIVO_AGENDAMENTOS)
                st.success(f"""✅ Agendamento confirmado!
👤 Cliente: {nome_cliente}
💇 Serviço: {servico_nome}
💰 Valor: R$ {valor:.2f}
📅 Data: {data_hora_str}""")
            else:
                st.warning("⚠️ Preencha todos os campos e digite o valor!")

# ===== ABA 3: Agendamentos + EXCLUIR =====
with aba3:
    st.subheader("📖 Agendamentos Realizados")
    st.divider()
    agendamentos = carregar_dados(ARQUIVO_AGENDAMENTOS)
    if agendamentos:
        lista_agendamentos = [
            f"{a['data_hora']} | {a['cliente']} | {a['servico']} | R$ {a['valor']:.2f}"
            for a in agendamentos
        ]
        escolha_ag = st.selectbox("Selecione para EXCLUIR", [""] + lista_agendamentos)
        if escolha_ag:
            indice = lista_agendamentos.index(escolha_ag)
            if st.button("🗑️ Excluir Este Agendamento", type="secondary"):
                agendamentos.pop(indice)
                salvar_dados(agendamentos, ARQUIVO_AGENDAMENTOS)
                st.warning("⚠️ Agendamento excluído!")
                st.rerun()
        st.divider()
        st.subheader("Lista Completa")
        st.table(agendamentos)
    else:
        st.info("Nenhum agendamento registrado.")

# ===== ABA 4: RELATÓRIO — BONITO NO CELULAR E COMPUTADOR =====
with aba4:
    st.subheader("💰 Relatório Financeiro")
    st.divider()

    agendamentos = carregar_dados(ARQUIVO_AGENDAMENTOS)

    if not agendamentos:
        st.info("Nenhum agendamento registrado ainda.")
    else:
        def pegar_data(agendamento):
            if "data" in agendamento:
                return agendamento["data"]
            elif "data_hora" in agendamento:
                return agendamento["data_hora"].split(" ")[0]
            return "Sem data"

        st.subheader("📅 Período do Relatório")
        col_data_ini, col_data_fim = st.columns(2)
        with col_data_ini:
            data_inicial = st.date_input("Data Inicial", format="DD/MM/YYYY")
        with col_data_fim:
            data_final = st.date_input("Data Final", format="DD/MM/YYYY")

        data_ini_str = data_inicial.strftime("%d/%m/%Y")
        data_fim_str = data_final.strftime("%d/%m/%Y")

        def data_entre(data_ag, d_ini, d_fim):
            try:
                dt_ag = datetime.strptime(data_ag, "%d/%m/%Y")
                return d_ini <= dt_ag <= d_fim
            except:
                return False

        dt_ini = datetime.strptime(data_ini_str, "%d/%m/%Y")
        dt_fim = datetime.strptime(data_fim_str, "%d/%m/%Y")

        lista_filtrada = [a for a in agendamentos if data_entre(pegar_data(a), dt_ini, dt_fim)]

        total_valor = sum([a["valor"] for a in lista_filtrada])
        qtd_servicos = len(lista_filtrada)

        st.divider()

        # ✅ CABEÇALHO DO RELATÓRIO
        st.markdown("""
        <h2 style='text-align: center; margin-bottom: 5px;'>💄 Abelhinha</h2>
        <p style='text-align: center; color: #666; margin-top: 0;'>Relatório de Movimento Financeiro</p>
        """, unsafe_allow_html=True)

        st.divider()

        st.markdown(f"**Período:** {data_ini_str} a {data_fim_str}")
        st.markdown(f"**Data de Emissão:** {datetime.now().strftime('%d/%m/%Y')}")
        st.markdown(f"**Total de Registros:** {qtd_servicos}")

        st.divider()

        # ✅ TABELA — USANDO st.table() que FUNCIONA BEM NO CELULAR!
        st.subheader("📋 Detalhamento")

        # Prepara os dados em formato de tabela
        tabela_dados = []
        for item in lista_filtrada:
            tabela_dados.append({
                "Data": pegar_data(item),
                "Cliente": item["cliente"],
                "Serviço": item["servico"],
                "Valor R$": f"{item['valor']:.2f}"
            })

        # ✅ st.table() = se adapta sozinho no celular!
        st.table(tabela_dados)

        st.divider()

        # ✅ TOTAL GERAL em destaque
        st.markdown(f"""
        <h3 style='text-align: right; padding-right: 20px;'>TOTAL GERAL: R$ {total_valor:.2f}</h3>
        """, unsafe_allow_html=True)

        st.divider()

        # ✅ Linha de assinatura
        st.markdown("&nbsp;")
        st.markdown("&nbsp;")
        st.markdown("""
        <p style='text-align: right; padding-right: 40px; margin-top: 60px;'>
        ___________________________<br>
        <strong>Responsável</strong>
        </p>
        """, unsafe_allow_html=True)

        st.info("💡 Para imprimir: aperte **Ctrl + P** ou toque em ⋮ → Imprimir no celular")
