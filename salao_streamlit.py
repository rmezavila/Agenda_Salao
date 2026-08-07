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

# Lista de serviços com "Outros" incluído
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
st.title("💄 Sistema de Gestão — Salão de Beleza")
st.divider()

aba1, aba2, aba3, aba4 = st.tabs([
    "📋 Clientes",
    "📅 Agendar",
    "📖 Agendamentos",
    "📊 Relatório Financeiro"
])

# ===== ABA 1: Clientes (Cadastrar com FORM = LIMPA AUTOMÁTICO) =====
with aba1:
    st.subheader("Cadastrar Cliente")

    # ✅ FORMULÁRIO — LIMPA TUDO APÓS SALVAR! Não duplica mais!
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

    # ✅ FORMULÁRIO — LIMPA TUDO APÓS CONFIRMAR!
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
        # Lista para selecionar e excluir
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

# ===== ABA 4: RELATÓRIO FINANCEIRO — FORMATO CONTÁBIL =====
with aba4:
    st.subheader("💰 Relatório Financeiro")
    st.divider()

    agendamentos = carregar_dados(ARQUIVO_AGENDAMENTOS)

    if not agendamentos:
        st.info("Nenhum agendamento registrado ainda.")
    else:
        # Função auxiliar para extrair data
        def pegar_data(agendamento):
            if "data" in agendamento:
                return agendamento["data"]
            elif "data_hora" in agendamento:
                return agendamento["data_hora"].split(" ")[0]
            return "Sem data"

        # FILTRO POR PERÍODO
        st.subheader("📅 Período do Relatório")
        col_data_ini, col_data_fim = st.columns(2)
        with col_data_ini:
            data_inicial = st.date_input("Data Inicial", format="DD/MM/YYYY")
        with col_data_fim:
            data_final = st.date_input("Data Final", format="DD/MM/YYYY")

        data_ini_str = data_inicial.strftime("%d/%m/%Y")
        data_fim_str = data_final.strftime("%d/%m/%Y")

        # Filtrar agendamentos dentro do período
        def data_entre(data_ag, d_ini, d_fim):
            try:
                dt_ag = datetime.strptime(data_ag, "%d/%m/%Y")
                return d_ini <= dt_ag <= d_fim
            except:
                return False

        dt_ini = datetime.strptime(data_ini_str, "%d/%m/%Y")
        dt_fim = datetime.strptime(data_fim_str, "%d/%m/%Y")

        lista_filtrada = [a for a in agendamentos if data_entre(pegar_data(a), dt_ini, dt_fim)]

        # Calcular totais
        total_valor = sum([a["valor"] for a in lista_filtrada])
        qtd_servicos = len(lista_filtrada)

        st.divider()

        # ✅ RELATÓRIO NO FORMATO CONTÁBIL
        st.markdown("""
        <style>
        .relatorio {
            font-family: 'Courier New', monospace;
            background: #fff;
            color: #000;
            padding: 2rem;
            border: 1px solid #ccc;
        }
        </style>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="relatorio">

        <h3 style="text-align: center; margin-bottom: 0;">RELATÓRIO FINANCEIRO</h3>
        <p style="text-align: center; margin-top: 0; font-size: 0.9em;">Salão de Beleza</p>
        <hr>

        <p><strong>Período:</strong> {data_ini_str} a {data_fim_str}</p>
        <p><strong>Data de Emissão:</strong> {datetime.now().strftime("%d/%m/%Y")}</p>

        <hr>

        <table style="width:100%; border-collapse: collapse;">
        <tr>
            <th style="text-align:left; border-bottom: 1px solid #000; padding: 8px;">Data</th>
            <th style="text-align:left; border-bottom: 1px solid #000; padding: 8px;">Cliente</th>
            <th style="text-align:left; border-bottom: 1px solid #000; padding: 8px;">Serviço</th>
            <th style="text-align:right; border-bottom: 1px solid #000; padding: 8px;">Valor R$</th>
        </tr>
        """, unsafe_allow_html=True)

        for item in lista_filtrada:
            st.markdown(f"""
        <tr>
            <td style="padding: 6px 0; border-bottom: 1px solid #ddd;">{pegar_data(item)}</td>
            <td style="padding: 6px 0; border-bottom: 1px solid #ddd;">{item['cliente']}</td>
            <td style="padding: 6px 0; border-bottom: 1px solid #ddd;">{item['servico']}</td>
            <td style="padding: 6px 0; border-bottom: 1px solid #ddd; text-align:right;">{item['valor']:.2f}</td>
        </tr>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <tr>
            <td colspan="3" style="text-align:right; padding: 12px 0 4px 0; font-weight: bold; font-size: 1.1em;">TOTAL GERAL .................</td>
            <td style="text-align:right; padding: 12px 0 4px 0; font-weight: bold; font-size: 1.1em;">R$ {total_valor:.2f}</td>
        </tr>
        </table>

        <hr>

        <p style="text-align: right; margin-top: 40px;">_______________________________<br>Responsável</p>

        </div>
        """, unsafe_allow_html=True)

        st.info("💡 Para imprimir: aperte **Ctrl + P** → o relatório sai formatado em página branca!")
