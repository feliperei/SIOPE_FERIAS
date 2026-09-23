import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import io
import os
import re

# 1. Configuração da Página
st.set_page_config(
    page_title="Portal Integrado de Carga & Gestão",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicialização do Módulo Ativo
if 'modulo_ativo' not in st.session_state:
    st.session_state['modulo_ativo'] = 'home'

# 2. CSS Personalizado Dark Glassmorphism Premium
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    /* Reset e Fundo Gradiente */
    html, body, [class*="css"], .stApp {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background: radial-gradient(circle at top right, #131E35, #080D1A 85%) !important;
        color: #F8FAFC !important;
    }

    #MainMenu, footer { visibility: hidden; }

    .main .block-container {
        padding-top: 1.2rem !important;
        padding-bottom: 2.5rem !important;
        max-width: 1350px;
    }

    /* Sidebar Glassmorphism */
    [data-testid="stSidebar"] {
        background-color: rgba(13, 21, 38, 0.85) !important;
        backdrop-filter: blur(16px);
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }
    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }

    /* Inputs e Uploaders */
    .stTextInput input, [data-testid="stFileUploader"] section {
        background-color: #141E33 !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 10px !important;
        color: #FFFFFF !important;
    }

    /* Header Cards */
    .header-card {
        background: linear-gradient(135deg, rgba(23, 37, 66, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 24px 32px;
        margin-bottom: 24px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
        display: flex;
        align-items: center;
        gap: 20px;
    }

    .header-logo {
        max-height: 60px;
        max-width: 140px;
        object-fit: contain;
    }

    .header-text-container {
        flex: 1;
    }

    .header-title {
        font-size: 1.8rem;
        font-weight: 800;
        color: #FFFFFF !important;
        letter-spacing: -0.02em;
        margin-bottom: 4px;
    }

    .header-subtitle {
        font-size: 0.92rem;
        color: #94A3B8 !important;
        margin: 0;
        line-height: 1.4;
    }

    /* Cards de Navegação (Home) */
    .nav-card-container {
        background: linear-gradient(145deg, rgba(23, 37, 66, 0.6) 0%, rgba(13, 21, 38, 0.8) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        padding: 26px;
        min-height: 160px;
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        margin-bottom: 12px;
    }
    .nav-card-container:hover {
        border-color: #3B82F6;
        transform: translateY(-4px);
        box-shadow: 0 12px 30px rgba(37, 99, 235, 0.2);
    }
    .nav-card-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #FFFFFF !important;
        margin-bottom: 8px;
    }
    .nav-card-desc {
        font-size: 0.88rem;
        color: #94A3B8 !important;
        line-height: 1.5;
    }

    /* Metric Cards */
    .metric-card {
        background: linear-gradient(145deg, rgba(23, 37, 66, 0.5) 0%, rgba(15, 23, 42, 0.7) 100%);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 18px;
        min-height: 135px;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-sizing: border-box;
        transition: all 0.2s ease;
    }
    .metric-card:hover {
        border-color: rgba(255, 255, 255, 0.2);
        transform: translateY(-2px);
    }

    .border-blue   { border-left: 4px solid #3B82F6; }
    .border-purple { border-left: 4px solid #8B5CF6; }
    .border-red    { border-left: 4px solid #EF4444; }
    .border-green  { border-left: 4px solid #10B981; }
    .border-tag    { border-left: 4px solid #06B6D4; }

    .card-label {
        font-size: 0.72rem;
        font-weight: 700;
        color: #94A3B8 !important;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }
    .card-value {
        font-size: clamp(1.1rem, 1.3vw, 1.45rem);
        font-weight: 800;
        color: #FFFFFF !important;
        margin: 6px 0;
    }
    .card-subtext {
        font-size: 0.78rem;
        color: #CBD5E1 !important;
        font-weight: 500;
    }

    /* Títulos de Seções */
    .section-header {
        font-size: 1.2rem;
        font-weight: 700;
        color: #FFFFFF !important;
        margin: 28px 0 16px 0;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Botões Principais */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        padding: 12px 20px !important;
        border: none !important;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35) !important;
    }

    /* Botões de Download */
    div[data-testid="stDownloadButton"] > button {
        width: 100% !important;
        border-radius: 10px !important;
        padding: 12px 16px !important;
        font-weight: 700 !important;
        color: #FFFFFF !important;
    }
    .btn-download-verde div[data-testid="stDownloadButton"] > button {
        background-color: #059669 !important;
        border: 1px solid #10B981 !important;
    }
    .btn-download-verde div[data-testid="stDownloadButton"] > button:hover {
        background-color: #10B981 !important;
    }
    .btn-download-vermelho div[data-testid="stDownloadButton"] > button {
        background-color: #DC2626 !important;
        border: 1px solid #EF4444 !important;
    }
    .btn-download-vermelho div[data-testid="stDownloadButton"] > button:hover {
        background-color: #EF4444 !important;
    }

    /* Dataframe */
    [data-testid="stDataFrame"] {
        background-color: #111A2E !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# Helper para Renderizar o Cabeçalho com Suporte a Logo
def render_header(titulo, subtitulo, icone_padrao="⚡"):
    logo_path = "logo.png"
    if os.path.exists(logo_path):
        import base64
        with open(logo_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        img_html = f'<img src="data:image/png;base64,{encoded_string}" class="header-logo" alt="Logo">'
    else:
        img_html = f'<div style="font-size: 2.2rem;">{icone_padrao}</div>'

    st.markdown(f"""
    <div class="header-card">
        {img_html}
        <div class="header-text-container">
            <div class="header-title">{titulo}</div>
            <div class="header-subtitle">{subtitulo}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- FUNÇÕES UTILITÁRIAS ---
def string_para_float(texto):
    if not texto: return 0.0
    limpo = re.sub(r'[^\d,. ]', '', str(texto)).strip()
    if not limpo: return 0.0
    if ',' in limpo:
        limpo = limpo.replace('.', '').replace(',', '.')
    return float(limpo)

def fmt_brl(val):
    return f"R$ {val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def separar_datas_rapido(df, coluna_origem, col_ini, col_fim):
    if coluna_origem in df.columns:
        serie = df[coluna_origem].astype(str).replace(['nan', 'None', '<NA>', ''], np.nan)
        split_df = serie.str.strip().str.split(' ', n=1, expand=True)
        df[col_ini] = split_df[0] if 0 in split_df.columns else np.nan
        df[col_fim] = split_df[1] if 1 in split_df.columns else np.nan
        df[col_ini] = df[col_ini].replace(['nan', 'None', ''], np.nan)
        df[col_fim] = df[col_fim].replace(['nan', 'None', ''], np.nan)
    return df

def calcular_prescricao_2_anos(data_serie):
    datas_dt = pd.to_datetime(data_serie, format='%d/%m/%Y', errors='coerce', dayfirst=True)
    datas_prescricao = datas_dt + pd.DateOffset(years=2)
    return datas_prescricao.dt.strftime('%d/%m/%Y').replace(['NaT', 'nan'], np.nan)

def aplicar_layout(df, colunas_layout):
    for col in colunas_layout:
        if col not in df.columns:
            df[col] = np.nan
    return df[colunas_layout]


# ==============================================================================
# TELA 1: HOME (MENU INICIAL)
# ==============================================================================
if st.session_state['modulo_ativo'] == 'home':
    render_header(
        "Portal Integrado de Gestão DBA",
        "Selecione um dos módulos operacionais abaixo para processar e exportar seus dados.",
        "🗂️"
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="nav-card-container">
            <div>
                <div class="nav-card-title">⚡ Otimizador de Massa Financeira - SIOPE</div>
                <div class="nav-card-desc">
                    Ajuste algorítmico na coluna <b>VLR_BRUTO_70</b> com proteção automática 
                    de servidores em <b>PUBLICO_ALVO</b> para atendimento de metas contábeis.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Acessar Módulo SIOPE ➔", key="btn_ir_siope", type="primary", use_container_width=True):
            st.session_state['modulo_ativo'] = 'siope'
            st.rerun()

    with col2:
        st.markdown("""
        <div class="nav-card-container">
            <div>
                <div class="nav-card-title">🏖️ Processador de Carga - FÉRIAS & SIOPE</div>
                <div class="nav-card-desc">
                    Tratamento de períodos, validação de portarias do DOE, cálculo de prescrição bienal 
                    e exportação de arquivos <b>CSV formatados para carga em banco</b>.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Acessar Módulo Férias ➔", key="btn_ir_ferias", type="primary", use_container_width=True):
            st.session_state['modulo_ativo'] = 'ferias'
            st.rerun()


# ==============================================================================
# TELA 2: MÓDULO SIOPE
# ==============================================================================
elif st.session_state['modulo_ativo'] == 'siope':
    if st.button("⬅️ Voltar ao Menu Principal", key="btn_voltar_siope"):
        st.session_state['modulo_ativo'] = 'home'
        st.rerun()

    render_header(
        "⚡ Otimizador de Massa Financeira - SIOPE",
        "Ajuste da coluna <b>VLR_BRUTO_70</b> preservando registros com <b>PUBLICO_ALVO</b> preenchido."
    )

    st.sidebar.header("⚙️ Configurações - SIOPE")
    uploaded_file_siope = st.sidebar.file_uploader("📂 Enviar Planilha (.xlsx)", type=["xlsx"], key="upl_siope")
    valor_texto = st.sidebar.text_input(
        "💰 Meta do Financeiro (R$):",
        value="204.321.373,60",
        help="Digite o valor repassado pelo financeiro"
    )
    valor_alvo = string_para_float(valor_texto)

    st.sidebar.markdown(f"""
    <div style="margin-top: 10px; margin-bottom: 14px;">
        <span style="color: #94A3B8; font-size: 0.72rem; font-weight: 700; text-transform: uppercase;">META FORMATADA</span><br>
        <span style="color: #10B981; font-size: 1.25rem; font-weight: 800;">{fmt_brl(valor_alvo)}</span>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.divider()
    btn_processar_siope = st.sidebar.button("🚀 Processar Ajuste", type="primary", use_container_width=True, key="btn_proc_siope")

    if uploaded_file_siope is not None and valor_alvo > 0 and btn_processar_siope:
        prog_siope = st.progress(0)
        status_siope = st.empty()
        
        status_siope.markdown("⌛ **Lendo dados da planilha...**")
        prog_siope.progress(20)
        
        df = pd.read_excel(uploaded_file_siope)
        
        if 'VLR_BRUTO_70' not in df.columns or 'PUBLICO_ALVO' not in df.columns:
            status_siope.empty()
            prog_siope.empty()
            st.error("❌ A planilha precisa conter as colunas 'VLR_BRUTO_70' e 'PUBLICO_ALVO'.")
            st.stop()

        status_siope.markdown("🔍 **Filtrando registros elegíveis...**")
        prog_siope.progress(40)
        
        df['VLR_BRUTO_70'] = pd.to_numeric(df['VLR_BRUTO_70'], errors='coerce').fillna(0)
        df_base = df[df['CPF'].notna()].copy() if 'CPF' in df.columns else df.copy()

        mask_vazio = (
            df_base['PUBLICO_ALVO'].isna() | 
            (df_base['PUBLICO_ALVO'].astype(str).str.strip() == '') | 
            (df_base['PUBLICO_ALVO'].astype(str).str.strip().str.lower() == 'nan')
        )
        
        df_candidatos = df_base[mask_vazio].copy()
        df_protegidos = df_base[~mask_vazio].copy()
        
        categorias_mapeamento = {
            'C': 'EDUCAÇÃO DO CAMPO',
            'I': 'EDUCAÇÃO INDÍGENA',
            'P': 'PRIVADOS DE LIBERDADE',
            'Q': 'EDUCAÇÃO QUILOMBOLA',
            'TI': 'TEMPO INTEGRAL'
        }
        
        resumo_tags = {}
        for tag, nome_extenso in categorias_mapeamento.items():
            mask_tag = df_protegidos['PUBLICO_ALVO'].astype(str).str.strip().str.upper() == tag
            df_tag = df_protegidos[mask_tag]
            resumo_tags[tag] = {
                'nome': nome_extenso,
                'qtd': len(df_tag),
                'soma': df_tag['VLR_BRUTO_70'].sum()
            }

        soma_total = df_base['VLR_BRUTO_70'].sum()
        diferenca_para_remover = soma_total - valor_alvo
        
        status_siope.markdown("⚡ **Calculando otimização gulosa...**")
        prog_siope.progress(70)

        if diferenca_para_remover <= 0:
            status_siope.empty()
            prog_siope.empty()
            st.warning("⚠️ O valor total da planilha já é menor ou igual à meta do financeiro.")
        else:
            df_candidatos_sorted = df_candidatos.sort_values(by='VLR_BRUTO_70', ascending=False)
            indices_removidos = []
            acumulado_removido = 0.0
            
            for idx, row in df_candidatos_sorted.iterrows():
                val = row['VLR_BRUTO_70']
                if acumulado_removido + val <= diferenca_para_remover:
                    acumulado_removido += val
                    indices_removidos.append(idx)
            
            df_removidos = df_base.loc[indices_removidos].copy()
            df_ajustado = df_base.drop(index=indices_removidos).copy()
            
            soma_final = df_ajustado['VLR_BRUTO_70'].sum()
            total_retirado = df_removidos['VLR_BRUTO_70'].sum()
            diferenca_final = abs(soma_final - valor_alvo)
            
            status_siope.markdown("📁 **Gerando arquivos consolidados...**")
            prog_siope.progress(90)
            
            st.session_state['siope_processado'] = True
            st.session_state['soma_total'] = soma_total
            st.session_state['valor_alvo'] = valor_alvo
            st.session_state['soma_final'] = soma_final
            st.session_state['total_retirado'] = total_retirado
            st.session_state['diferenca_final'] = diferenca_final
            st.session_state['total_removidos_qtd'] = len(df_removidos)
            st.session_state['total_mantidos_qtd'] = len(df_ajustado)
            st.session_state['resumo_tags'] = resumo_tags
            st.session_state['df_ajustado_siope'] = df_ajustado
            st.session_state['df_removidos_siope'] = df_removidos
            
            out_ajustado = io.BytesIO()
            with pd.ExcelWriter(out_ajustado, engine='openpyxl') as writer:
                df_ajustado.to_excel(writer, index=False)
            st.session_state['excel_ajustado'] = out_ajustado.getvalue()
            
            out_removidos = io.BytesIO()
            with pd.ExcelWriter(out_removidos, engine='openpyxl') as writer:
                df_removidos.to_excel(writer, index=False)
            st.session_state['excel_removidos'] = out_removidos.getvalue()
            
            prog_siope.progress(100)
            status_siope.empty()
            prog_siope.empty()

    if st.session_state.get('siope_processado'):
        st.markdown('<div class="section-header">📌 Resumo Geral do Ajuste</div>', unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"""
            <div class="metric-card border-blue">
                <div class="card-label">Soma Total Inicial</div>
                <div class="card-value">{fmt_brl(st.session_state['soma_total'])}</div>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class="metric-card border-purple">
                <div class="card-label">Meta Financeiro</div>
                <div class="card-value">{fmt_brl(st.session_state['valor_alvo'])}</div>
            </div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""
            <div class="metric-card border-red">
                <div class="card-label">Total Retirado</div>
                <div class="card-value">{fmt_brl(st.session_state['total_retirado'])}</div>
                <div class="card-subtext">👥 {st.session_state['total_removidos_qtd']:,} servidores desconsiderados</div>
            </div>""", unsafe_allow_html=True)
        with c4:
            st.markdown(f"""
            <div class="metric-card border-green">
                <div class="card-label">Meta Alcançada (Diferença)</div>
                <div class="card-value">{fmt_brl(st.session_state['diferenca_final'])}</div>
                <div class="card-subtext">Diferença apurada</div>
            </div>""", unsafe_allow_html=True)

        st.markdown('<div class="section-header">🏷️ Detalhamento por PÚBLICO ALVO</div>', unsafe_allow_html=True)
        tags = st.session_state['resumo_tags']
        t1, t2, t3, t4, t5 = st.columns(5)
        for col, k in zip([t1, t2, t3, t4, t5], ['C', 'I', 'P', 'Q', 'TI']):
            item = tags[k]
            with col:
                st.markdown(f"""
                <div class="metric-card border-tag">
                    <div class="card-label">[{k}] {item['nome']}</div>
                    <div class="card-value">{fmt_brl(item['soma'])}</div>
                    <div class="card-subtext">👥 {item['qtd']:,} servidores</div>
                </div>""", unsafe_allow_html=True)

        st.markdown('<div class="section-header">📊 Indicadores Visuais</div>', unsafe_allow_html=True)
        g1, g2 = st.columns(2)
        with g1:
            fig_donut = go.Figure(data=[go.Pie(
                labels=['Valor Mantido', 'Valor Retirado'],
                values=[st.session_state['soma_final'], st.session_state['total_retirado']],
                hole=.6,
                marker_colors=['#10B981', '#EF4444']
            )])
            fig_donut.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#FFFFFF'), margin=dict(t=20, b=20, l=20, r=20))
            st.plotly_chart(fig_donut, use_container_width=True)
        with g2:
            fig_bar = go.Figure(data=[go.Bar(
                x=['Carga Inicial', 'Meta Financeiro', 'Resultado Final'],
                y=[st.session_state['soma_total'], st.session_state['valor_alvo'], st.session_state['soma_final']],
                marker_color=['#3B82F6', '#8B5CF6', '#10B981'],
                text=[fmt_brl(st.session_state['soma_total']), fmt_brl(st.session_state['valor_alvo']), fmt_brl(st.session_state['soma_final'])],
                textposition='auto'
            )])
            fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#FFFFFF'), margin=dict(t=20, b=20, l=20, r=20), yaxis=dict(showgrid=False))
            st.plotly_chart(fig_bar, use_container_width=True)

        st.divider()
        st.markdown('<div class="section-header">📥 Exportar Planilhas Formatadas</div>', unsafe_allow_html=True)
        dl1, dl2 = st.columns(2)
        with dl1:
            st.markdown('<div class="btn-download-verde">', unsafe_allow_html=True)
            st.download_button(
                label=f"🟢 Baixar Planilha Ajustada ({st.session_state['total_mantidos_qtd']:,} registros)",
                data=st.session_state['excel_ajustado'],
                file_name="SIOPE_AJUSTADO.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
            st.markdown('</div>', unsafe_allow_html=True)
        with dl2:
            st.markdown('<div class="btn-download-vermelho">', unsafe_allow_html=True)
            st.download_button(
                label=f"🔴 Baixar Registros Retirados ({st.session_state['total_removidos_qtd']:,} registros)",
                data=st.session_state['excel_removidos'],
                file_name="SIOPE_RETIRADOS.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
        st.divider()
        st.markdown('<div class="section-header">🔍 Pré-visualização dos Dados</div>', unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["Servidores Mantidos (Preview)", "Servidores Retirados (Preview)"])
        with tab1:
            col_preview = [c for c in ['NOME', 'CPF', 'VLR_BRUTO_70', 'PUBLICO_ALVO'] if c in st.session_state['df_ajustado_siope'].columns]
            st.dataframe(st.session_state['df_ajustado_siope'][col_preview].head(100), use_container_width=True)
        with tab2:
            col_preview = [c for c in ['NOME', 'CPF', 'VLR_BRUTO_70', 'PUBLICO_ALVO'] if c in st.session_state['df_removidos_siope'].columns]
            st.dataframe(st.session_state['df_removidos_siope'][col_preview].head(100), use_container_width=True)
    else:
        st.info("👈 Utilize o painel lateral para anexar a planilha e processar o ajuste.")


# ==============================================================================
# TELA 3: MÓDULO CARGA DE FÉRIAS
# ==============================================================================
elif st.session_state['modulo_ativo'] == 'ferias':
    if st.button("⬅️ Voltar ao Menu Principal", key="btn_voltar_ferias"):
        st.session_state['modulo_ativo'] = 'home'
        st.rerun()

    render_header(
        "🏖️ Processador de Carga - Férias & DBA",
        "Padronização de regras de negócio, prescrição bienal e geração de arquivos <b>CSV</b> para carga em banco de dados."
    )

    st.sidebar.header("⚙️ Configurações - Férias")
    uploaded_file_ferias = st.sidebar.file_uploader("📂 Anexe a planilha de férias (.xlsx)", type=["xlsx"], key="upl_ferias")
    
    st.sidebar.divider()
    btn_processar_ferias = st.sidebar.button("🚀 Processar Carga", type="primary", use_container_width=True, key="btn_proc_ferias")

    if uploaded_file_ferias is not None and btn_processar_ferias:
        prog_f = st.progress(0)
        status_f = st.empty()
        
        try:
            status_f.markdown("⌛ **Lendo abas da planilha na memória...**")
            xls = pd.ExcelFile(uploaded_file_ferias)
            prog_f.progress(20)

            # 1. TELA DE REGISTRO
            status_f.markdown("🔄 **Processando regras: Tela de Registro...**")
            df_registro = pd.read_excel(xls, sheet_name='TELA DE REGISTRO')
            
            col_matvinc = 'MAT+VINC' if 'MAT+VINC' in df_registro.columns else 'MATVINC'
            if col_matvinc in df_registro.columns:
                mat_str = df_registro[col_matvinc].astype(str)
                df_registro['MATVINC'] = mat_str.str.replace('-', '', regex=False)
                split_matvinc = mat_str.str.split('-', n=1, expand=True)
                df_registro['MATRICULA'] = split_matvinc[0] if 0 in split_matvinc.columns else np.nan
                df_registro['VINCULO'] = split_matvinc[1] if 1 in split_matvinc.columns else np.nan

            if 'NOME DO SERVIDOR' in df_registro.columns:
                df_registro['NOME'] = df_registro['NOME DO SERVIDOR']
            if 'EXERCÍCIO' in df_registro.columns:
                df_registro['EXERCICIO'] = df_registro['EXERCÍCIO']
            if 'TOTAL DIAS DE FÉRIAS' in df_registro.columns:
                df_registro['QTD_DIAS'] = df_registro['TOTAL DIAS DE FÉRIAS']

            df_registro = separar_datas_rapido(df_registro, 'PERÍODO AQUISITIVO', 'DT_INI_PERIODO_AQ', 'DT_FIM_PERIODO_AQ')
            df_registro = separar_datas_rapido(df_registro, '1º PERÍODO FÉRIAS', 'DT_INI_P1', 'DT_FIM_P1')
            df_registro = separar_datas_rapido(df_registro, '2º PERÍODO FÉRIAS', 'DT_INI_P2', 'DT_FIM_P2')

            if 'DT_FIM_PERIODO_AQ' in df_registro.columns:
                df_registro['DT_PRESCRICAO'] = calcular_prescricao_2_anos(df_registro['DT_FIM_PERIODO_AQ'])

            layout_registro = [
                'PONTPUBL', 'CHAVE', 'SEQ', 'MATVINC', 'NOME', 'MATRICULA', 'VINCULO', 
                'DT_INI_PERIODO_AQ', 'DT_FIM_PERIODO_AQ', 'DT_INI_P1', 'DT_FIM_P1', 
                'DT_INI_P2', 'DT_FIM_P2', 'QTD_DIAS', 'EXERCICIO', 'DT_PRESCRICAO', 'PONTPUBL_P2'
            ]
            df_registro = aplicar_layout(df_registro, layout_registro)
            prog_f.progress(55)

            # 2. DADOS DE PUBLICAÇÃO
            status_f.markdown("🔄 **Processando regras: Dados de Publicação...**")
            df_publicacao = pd.read_excel(xls, sheet_name='DADOS DE PUBLICAÇÃO')
            
            col_matvinc_pub = 'MAT+VINC' if 'MAT+VINC' in df_publicacao.columns else 'MATVINC'
            if col_matvinc_pub in df_publicacao.columns:
                mat_str_pub = df_publicacao[col_matvinc_pub].astype(str)
                split_matvinc = mat_str_pub.str.split('-', n=1, expand=True)
                df_publicacao['MATRICULA'] = split_matvinc[0] if 0 in split_matvinc.columns else np.nan
                df_publicacao['VINCULO'] = split_matvinc[1] if 1 in split_matvinc.columns else np.nan

            if 'PORTARIA' in df_publicacao.columns:
                df_publicacao['NUMERO'] = df_publicacao['PORTARIA']
            if 'DATA PORTARIA' in df_publicacao.columns:
                df_publicacao['DATA'] = df_publicacao['DATA PORTARIA']
            if 'Nº DOE' in df_publicacao.columns:
                df_publicacao['NUM_D_O_FLEX01'] = (
                    df_publicacao['Nº DOE'].astype(str).str.replace(r'\.0$', '', regex=True).str.replace(r'[.,]', '', regex=True)
                )
            if 'DATA DOE' in df_publicacao.columns:
                df_publicacao['DATA_D_O'] = df_publicacao['DATA DOE']
            if 'Nº PROC. PORTARIA' in df_publicacao.columns:
                df_publicacao['NUMERO_PROCESSO'] = df_publicacao['Nº PROC. PORTARIA']
                
            df_publicacao['TIPO_D_O'] = 'DOE'
            df_publicacao['AUTORIDADE'] = 'SECRETARIO ADJUNTO'
            df_publicacao['USUARIO'] = '57213288'

            layout_publicacao = [
                'MATRICULA', 'VINCULO', 'VERSAO', 'NUMERO', 'DATA', 'TIPO', 
                'NUM_D_O_FLEX01', 'DATA_D_O', 'TIPO_D_O', 'AUTORIDADE', 
                'NUMERO_PROCESSO', 'MOTIVO', 'OBSERVACAO', 'SITUACAO', 'USUARIO', 'PONTPUBL'
            ]
            df_publicacao = aplicar_layout(df_publicacao, layout_publicacao)
            prog_f.progress(80)

            # 3. GERAÇÃO CSV
            status_f.markdown("📁 **Gerando arquivos CSV...**")
            csv_registro = df_registro.to_csv(index=False, sep=';', encoding='utf-8-sig').encode('utf-8-sig')
            csv_publicacao = df_publicacao.to_csv(index=False, sep=';', encoding='utf-8-sig').encode('utf-8-sig')
            
            st.session_state['ferias_processado'] = True
            st.session_state['csv_registro'] = csv_registro
            st.session_state['csv_publicacao'] = csv_publicacao
            st.session_state['total_registro'] = len(df_registro)
            st.session_state['total_publicacao'] = len(df_publicacao)
            st.session_state['df_registro_preview'] = df_registro.head(100)
            st.session_state['df_publicacao_preview'] = df_publicacao.head(100)
            
            prog_f.progress(100)
            status_f.empty()
            prog_f.empty()
            
        except Exception as e:
            prog_f.empty()
            status_f.empty()
            st.error(f"❌ Erro ao processar o arquivo de férias: {e}")

    if st.session_state.get('ferias_processado'):
        st.markdown('<div class="section-header">📌 Resumo da Carga de Férias</div>', unsafe_allow_html=True)
        f1, f2 = st.columns(2)
        with f1:
            st.markdown(f"""
            <div class="metric-card border-blue">
                <div class="card-label">Registros (Tela de Registro)</div>
                <div class="card-value">{st.session_state['total_registro']:,}</div>
                <div class="card-subtext">Linhas estruturadas com prescrição bienal</div>
            </div>""", unsafe_allow_html=True)
        with f2:
            st.markdown(f"""
            <div class="metric-card border-purple">
                <div class="card-label">Registros (Dados de Publicação)</div>
                <div class="card-value">{st.session_state['total_publicacao']:,}</div>
                <div class="card-subtext">Portarias e dados de DOE padronizados</div>
            </div>""", unsafe_allow_html=True)

        st.divider()
        st.markdown('<div class="section-header">📥 Baixar Arquivos CSV (Prontos para Banco de Dados)</div>', unsafe_allow_html=True)
        dl1, dl2 = st.columns(2)
        with dl1:
            st.markdown('<div class="btn-download-verde">', unsafe_allow_html=True)
            st.download_button(
                label=f"⬇️ Baixar TELA_REGISTRO.csv ({st.session_state['total_registro']:,} linhas)",
                data=st.session_state['csv_registro'],
                file_name="TELA_REGISTRO.csv",
                mime="text/csv",
                use_container_width=True
            )
            st.markdown('</div>', unsafe_allow_html=True)
        with dl2:
            st.markdown('<div class="btn-download-verde">', unsafe_allow_html=True)
            st.download_button(
                label=f"⬇️ Baixar DADOS_PUBLICACAO.csv ({st.session_state['total_publicacao']:,} linhas)",
                data=st.session_state['csv_publicacao'],
                file_name="DADOS_PUBLICACAO.csv",
                mime="text/csv",
                use_container_width=True
            )
            st.markdown('</div>', unsafe_allow_html=True)

        st.divider()
        st.markdown('<div class="section-header">🔍 Pré-visualização dos Dados Formatados</div>', unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["📋 Tela de Registro", "📰 Dados de Publicação"])
        with tab1:
            st.dataframe(st.session_state['df_registro_preview'], use_container_width=True)
        with tab2:
            st.dataframe(st.session_state['df_publicacao_preview'], use_container_width=True)
    else:
        st.info("👈 Utilize o painel lateral para anexar a planilha de férias e clicar em **Processar Carga DBA**.")