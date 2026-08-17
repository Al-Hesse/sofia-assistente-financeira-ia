import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from agente import SofiaAgente
import os

# Configuração de Página Premium
st.set_page_config(
    page_title="Sofia | Sua Consultora de Economia Diária",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo CSS Customizado para uma Estética Premium (Glassmorphism e Cores Harmoniosas)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Outfit', sans-serif;
        background-color: #0E1117;
        color: #E2E8F0;
    }
    
    /* Customizando os Títulos com Gradientes */
    .premium-title {
        background: linear-gradient(135deg, #38BDF8 0%, #818CF8 50%, #C084FC 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 3rem;
        margin-bottom: 5px;
    }
    
    .premium-subtitle {
        color: #94A3B8;
        font-size: 1.15rem;
        margin-bottom: 30px;
        font-weight: 300;
    }
    
    /* Card Glassmorphism */
    .glass-card {
        background: rgba(30, 41, 59, 0.45);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    
    /* KPI Cards */
    .metric-container {
        display: flex;
        justify-content: space-between;
        gap: 15px;
        margin-bottom: 25px;
    }
    
    .metric-card {
        flex: 1;
        background: linear-gradient(145deg, #1E293B, #0F172A);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 16px 20px;
        text-align: left;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: rgba(56, 189, 248, 0.3);
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 4px;
    }
    
    .metric-value {
        font-size: 1.6rem;
        font-weight: 700;
        color: #F1F5F9;
    }
    
    /* Chat Bubbles customizadas */
    .chat-bubble {
        padding: 14px 18px;
        border-radius: 16px;
        margin-bottom: 12px;
        max-width: 85%;
        line-height: 1.5;
        font-size: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    }
    
    .chat-user {
        background-color: #312E81;
        color: #F8FAFC;
        margin-left: auto;
        border-top-right-radius: 2px;
        border: 1px solid rgba(99, 102, 241, 0.3);
    }
    
    .chat-sofia {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        color: #E2E8F0;
        margin-right: auto;
        border-top-left-radius: 2px;
        border: 1px solid rgba(56, 189, 248, 0.2);
    }
    
    .chip-button {
        display: inline-block;
        background-color: #1E293B;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 6px 14px;
        margin: 5px;
        cursor: pointer;
        font-size: 0.9rem;
        color: #38BDF8;
        transition: all 0.2s ease;
    }
    
    .chip-button:hover {
        background-color: #38BDF8;
        color: #0E1117;
        border-color: #38BDF8;
    }
</style>
""", unsafe_allow_html=True)

# Instancia o Agente da Sofia
@st.cache_resource
def get_agente():
    # Define caminhos baseados na pasta atual
    return SofiaAgente(data_dir="data")

sofia = get_agente()

# --- SIDEBAR LATERAL PREMIUM ---
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; margin-bottom: 15px;'>
        <h1 style='color: #38BDF8; font-weight: 700; margin-bottom: 5px; font-size: 2rem;'>🤖 Sofia</h1>
        <p style='color: #94A3B8; font-size: 0.9rem; font-weight: 300;'>Sua Consultora de Economia Diária</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Seção para chave de API do Gemini (Permite rodar local e de graça, sem travar se não tiver)
    st.markdown("### 🧠 Inteligência Artificial (Opcional)")
    gemini_key = st.text_input(
        "Chave de API do Google Gemini:",
        type="password",
        help="Obtenha sua chave gratuita em: https://aistudio.google.com/. Caso prefira testar de graça sem chave, Sofia rodará em modo Simulador Inteligente Local!",
        value=os.environ.get("GEMINI_API_KEY", "")
    )
    
    if gemini_key:
        st.success("Chave Gemini Ativa! Modo Inteligente habilitado. 🤖✨")
    else:
        st.info("Rodando em modo Simulador Local (offline). Insira sua chave Gemini ao lado para habilitar IA Generativa em tempo real!")
        
    st.markdown("---")
    
    # Exibe Perfil do Cliente
    st.markdown("### 👤 Usuário do Perfil")
    st.markdown(f"""
    **Nome:** {sofia.perfil['nome']}  
    **Profissão:** {sofia.perfil['profissao']}  
    **Idade:** {sofia.perfil['idade']} anos  
    **Renda Mensal:** R$ {sofia.perfil['renda_mensal']:.2f}  
    **Perfil de Investimento:** <span style="background-color: #1E3A8A; color: #38BDF8; padding: 2px 8px; border-radius: 4px; font-weight: bold; font-size: 0.85rem;">{sofia.perfil['perfil_investidor'].upper()}</span>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Exibe Metas com Lindas Barras de Progresso
    st.markdown("### 🎯 Metas Ativas")
    for m in sofia.perfil.get("metas", []):
        meta_nome = m['meta']
        valor_alvo = m['valor_necessario']
        
        # Mapeamento do progresso atual conforme dados
        atual = 0.0
        if "reserva" in meta_nome.lower():
            atual = sofia.perfil['reserva_emergencia_atual']
        else:
            # Entrada do apê (Soma do patrimônio extra que sobrou do fundo)
            atual = max(0.0, sofia.perfil['patrimonio_total'] - sofia.perfil['reserva_emergencia_atual'])
            
        porcentagem = min(1.0, atual / valor_alvo)
        
        st.markdown(f"**{meta_nome}**")
        st.progress(porcentagem)
        st.markdown(f"<div style='display:flex; justify-content:space-between; font-size:0.85rem; color:#94A3B8; margin-top:-10px; margin-bottom:12px;'><span>R$ {atual:,.2f}</span><span>R$ {valor_alvo:,.2f} ({int(porcentagem*100)}%)</span></div>", unsafe_allow_html=True)


# --- MAIN VIEW ---
st.markdown("<h1 class='premium-title'>Sofia: Finanças Humanizadas</h1>", unsafe_allow_html=True)
st.markdown("<p class='premium-subtitle'>Seu agente inteligente para encontrar ralos financeiros e alcançar seus sonhos mais rápido 🚀</p>", unsafe_allow_html=True)

# KPI Dashboard no Topo
st.markdown("""
<div class='metric-container'>
    <div class='metric-card'>
        <div class='metric-label'>Renda Mensal (Salário)</div>
        <div class='metric-value' style='color: #34D399;'>R$ 5.000,00</div>
    </div>
    <div class='metric-card'>
        <div class='metric-label'>Despesas do Mês</div>
        <div class='metric-value' style='color: #F87171;'>R$ {:.2f}</div>
    </div>
    <div class='metric-card'>
        <div class='metric-label'>Saldo Líquido Disponível</div>
        <div class='metric-value' style='color: #60A5FA;'>R$ {:.2f}</div>
    </div>
    <div class='metric-card'>
        <div class='metric-label'>Reserva de Emergência Atual</div>
        <div class='metric-value' style='color: #FBBF24;'>R$ {:.2f}</div>
    </div>
</div>
""".format(sofia.total_despesa, sofia.saldo_liquido, sofia.perfil['reserva_emergencia_atual']), unsafe_allow_html=True)

# Tabs Interativas
tab_chat, tab_dashboard, tab_docs = st.tabs([
    "💬 Conversar com a Sofia", 
    "📊 Painel de Despesas & Projeções", 
    "📄 Documentação do Desafio"
])

# TAB 1: INTERFACE DE CHAT
with tab_chat:
    st.markdown("""
    <div class='glass-card'>
        <p style='margin: 0; color: #38BDF8; font-weight: 500;'>💡 Dica da Sofia:</p>
        <p style='margin: 0 0 10px 0; color: #94A3B8; font-size: 0.95rem;'>Tente me perguntar sobre quais são seus maiores ralos de gastos, quanto falta para atingir sua reserva, ou onde aplicar o que sobra para sua reserva render!</p>
    </div>
    """, unsafe_allow_html=True)

    # Estado da conversa
    if "messages" not in st.session_state:
        st.session_state.messages = [
            ("sofia", "Oi, João! Sofia aqui. 😍 Prontinho para darmos uma olhada esperta nos gastos deste mês e planejar como alcançar as chaves do seu novo apê muito mais rápido?")
        ]

    # Exibe histórico de mensagens
    for role, text in st.session_state.messages:
        if role == "user":
            st.markdown(f"<div class='chat-bubble chat-user'>👤 <b>Você:</b><br>{text}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-bubble chat-sofia'>🤖 <b>Sofia:</b><br>{text}</div>", unsafe_allow_html=True)

    # Chips de Sugestões de Cliques Rápidos
    st.write(" ")
    st.caption("Perguntas Rápidas Sugeridas:")
    col_chip1, col_chip2, col_chip3 = st.columns(3)
    
    click_prompt = None
    if col_chip1.button("📈 Quais são meus maiores gastos?", use_container_width=True):
        click_prompt = "Quais são meus maiores gastos esse mês?"
    if col_chip2.button("🛡️ Quanto falta para minha reserva de emergência?", use_container_width=True):
        click_prompt = "Quanto falta para mim completar minha reserva de emergência?"
    if col_chip3.button("🏦 Onde devo investir minhas economias de forma segura?", use_container_width=True):
        click_prompt = "Quais são as melhores opções de investimento seguras para o meu perfil moderado?"

    # Entrada do chat
    user_input = st.chat_input("Digite sua mensagem para a Sofia aqui...")
    
    # Se clicou em um chip, sobrescreve o input
    if click_prompt:
        user_input = click_prompt

    if user_input:
        # Exibe mensagem do usuário imediatamente
        st.session_state.messages.append(("user", user_input))
        st.rerun()

    # Processa resposta se a última mensagem for do usuário
    if st.session_state.messages[-1][0] == "user":
        ultimo_input = st.session_state.messages[-1][1]
        
        # Gera a resposta do agente (passando a chave se houver)
        with st.spinner("Sofia está analisando suas contas e digitando... 💬✍️"):
            resposta_sofia = sofia.responder(
                input_usuario=ultimo_input, 
                chat_history=st.session_state.messages[:-1], 
                api_key=gemini_key if gemini_key else None
            )
            
        st.session_state.messages.append(("sofia", resposta_sofia))
        st.rerun()


# TAB 2: PAINEL DE DESPESAS E GRÁFICOS
with tab_dashboard:
    col_graph1, col_graph2 = st.columns(2)
    
    with col_graph1:
        st.markdown("<h3 style='color: #F1F5F9; font-size:1.25rem;'>Distribuição Percentual de Gastos</h3>", unsafe_allow_html=True)
        # Montar gráfico de pizza das despesas por categoria
        despesas_df = sofia.transacoes_df[sofia.transacoes_df["tipo"] == "saida"]
        if not despesas_df.empty:
            fig_pizza = px.pie(
                despesas_df, 
                names="categoria", 
                values="valor", 
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig_pizza.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#E2E8F0"),
                legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
            )
            st.plotly_chart(fig_pizza, use_container_width=True)
        else:
            st.info("Nenhuma despesa registrada para gerar o gráfico.")

    with col_graph2:
        st.markdown("<h3 style='color: #F1F5F9; font-size:1.25rem;'>Simulador de Meta: Completar Reserva (R$ 15k)</h3>", unsafe_allow_html=True)
        # Gráfico de projeção do acúmulo da reserva
        reserva_atual = sofia.perfil['reserva_emergencia_atual']
        falta_reserva = 15000.00 - reserva_atual
        
        # Simular acúmulo mensal guardando R$ 500 por mês
        meses = ["Atual", "Mês 1", "Mês 2", "Mês 3", "Mês 4", "Mês 5"]
        valores_reserva = [reserva_atual]
        
        economia_mensal_sugerida = 1000.00 # Guardando R$ 1.000 do saldo livre de R$ 2.511
        for i in range(1, 6):
            valores_reserva.append(min(15000.00, reserva_atual + (economia_mensal_sugerida * i)))
            
        fig_linha = go.Figure()
        fig_linha.add_trace(go.Scatter(
            x=meses, 
            y=valores_reserva, 
            mode='lines+markers',
            line=dict(color='#FBBF24', width=3),
            marker=dict(size=8),
            name="Projeção com Economia de R$ 1.000/mês"
        ))
        
        # Linha do Objetivo de R$ 15.000
        fig_linha.add_trace(go.Scatter(
            x=meses,
            y=[15000.00]*len(meses),
            mode='lines',
            line=dict(color='#F87171', dash='dash'),
            name="Meta Alvo (R$ 15.000,00)"
        ))
        
        fig_linha.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#E2E8F0"),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)"),
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_linha, use_container_width=True)

    # Listagem das tabelas de dados em expanders organizados
    st.markdown("<h3 style='color: #F1F5F9; font-size:1.25rem; margin-top:20px;'>Dados de Base Consultados</h3>", unsafe_allow_html=True)
    exp_trans = st.expander("📁 Visualizar Tabela de Transações Recentes (`transacoes.csv`)")
    with exp_trans:
        st.dataframe(sofia.transacoes_df, use_container_width=True)

    exp_prod = st.expander("📁 Visualizar Tabela de Produtos de Investimento Recomendados (`produtos_financeiros.json`)")
    with exp_prod:
        st.dataframe(pd.DataFrame(sofia.produtos), use_container_width=True)


# TAB 3: DOCUMENTAÇÃO DO DESAFIO DIO
with tab_docs:
    st.markdown("""
    <div class='glass-card'>
        <h2 style='color:#38BDF8; font-size:1.5rem; font-weight:700;'>Entregáveis do Desafio DIO</h2>
        <p style='color:#94A3B8; font-size:0.95rem; margin-bottom:15px;'>Para o seu projeto receber nota máxima na avaliação da DIO, toda a documentação de apoio foi gerada detalhadamente na pasta <code>docs/</code>:</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_doc1, col_doc2 = st.columns(2)
    with col_doc1:
        st.markdown("""
        - 📄 **1. Documentação do Agente:**  
          Definição detalhada do caso de uso da Sofia, persona, tom de voz, arquitetura Mermaid e limites seguros contra alucinações.  
          *Arquivo:* `docs/01-documentacao-agente.md`
          
        - 📄 **2. Base de Conhecimento:**  
          Explicação sobre a estratégia de dados locais e a técnica de RAG estruturado para compilar os resumos matemáticos em Python.  
          *Arquivo:* `docs/02-base-conhecimento.md`
          
        - 📄 **3. Prompts do Agente:**  
          Demonstração do System Prompt principal da Sofia e engenharia de Few-shot prompts com tratamento contra indução ao erro.  
          *Arquivo:* `docs/03-prompts.md`
        """)
    with col_doc2:
        st.markdown("""
        - 📄 **4. Avaliação e Métricas:**  
          Tabela de métricas de qualidade como acurácia aritmética e proteção de riscos, acompanhada de roteiros e resultados de testes estruturados.  
          *Arquivo:* `docs/04-metricas.md`
          
        - 📄 **5. Roteiro de Pitch (3 min):**  
          Roteiro cronometrado estilo elevador dividindo a dor do João Silva, o diferencial tecnológico da Sofia e o impacto social da solução.  
          *Arquivo:* `docs/05-pitch.md`
        """)
