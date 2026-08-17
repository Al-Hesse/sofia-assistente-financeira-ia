# 🤖 Sofia: Consultora Inteligente de Economia Diária e Finanças

Bem-vindo ao repositório do projeto **Sofia**, um Assistente Virtual de Finanças Pessoais desenvolvido como entrega para o laboratório prático **"Construa Seu Assistente Virtual Com Inteligência Artificial"** da **DIO (Digital Innovation One)**.

A Sofia foi projetada para ir muito além de uma planilha passiva ou de um assistente de jargões complexos. Ela é uma mentora empática, motivadora e inteligente, projetada especificamente para ajudar o usuário **João Silva** (e profissionais em posições similares) a desmascarar os "ralos financeiros" de seu orçamento diário, acelerar a construção de sua reserva de emergência e conquistar o sonho da casa própria.

---

## 🚀 Como Rodar o Projeto Localmente

Siga o passo a passo simplificado para ver a Sofia funcionando em uma interface interativa premium construída com **Streamlit** e **Plotly**:

### 1. Pré-requisitos
Certifique-se de ter o Python 3.9+ instalado em sua máquina.

### 2. Clonar o Repositório e Navegar até a pasta
```bash
git clone <url-do-seu-repositorio>
cd dio
```

### 3. Criar e Ativar um Ambiente Virtual (Opcional, mas recomendado)
No Linux/macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```
No Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### 4. Instalar as Dependências
```bash
pip install -r src/requirements.txt
```

### 5. Executar o Servidor de Desenvolvimento
```bash
streamlit run src/app.py
```

*Pronto! Uma aba no seu navegador se abrirá automaticamente apontando para `http://localhost:8501/` com o painel premium da Sofia rodando.*

---

## 🗂️ Estrutura do Repositório e Entregáveis da DIO

Este repositório está organizado de acordo com as exigências máximas do laboratório em 6 etapas:

```text
📁 dio/
│
├── 📄 README.md                      # Este arquivo (Apresentação geral)
├── 📄 projeto.md                     # Instruções originais da DIO
│
├── 📁 data/                          # Base de Conhecimento (Dados locais seguros)
│   ├── transacoes.csv                # Extrato fictício do cliente João Silva
│   ├── perfil_investidor.json        # Perfil e metas estruturadas do cliente
│   ├── produtos_financeiros.json     # Produtos de investimento regulamentados
│   └── historico_atendimento.csv     # Atendimentos de suporte anteriores
│
├── 📁 docs/                          # Documentação detalhada em 5 Etapas
│   ├── 01-documentacao-agente.md     # Definição de Persona, Tom de voz, Caso de Uso e Diagrama de Fluxo
│   ├── 02-base-conhecimento.md       # Estratégia de dados e engenharia de RAG estruturado em Python
│   ├── 03-prompts.md                 # System Prompt completo da Sofia e exemplos Few-Shot contra alucinação
│   ├── 04-metricas.md                # Resultados de testes, métricas de acurácia e prevenção de riscos
│   └── 05-pitch.md                   # Roteiro do Pitch de elevador de 3 minutos
│
├── 📁 src/                           # Código-fonte da aplicação funcional
│   ├── app.py                        # Interface de usuário interativa em Streamlit
│   ├── agente.py                     # Motor lógico do agente (Pandas + Google Gemini)
│   └── requirements.txt              # Declaração exata das dependências do sistema
│
└── 📁 assets/                        # Imagens e diagramas
```

---

## 💡 Destaques Tecnológicos da Sofia

- **Cálculos Matemáticos Programáticos (Zero Alucinação):** Em vez de deixar a IA somar e subtrair valores financeiros do usuário (o que frequentemente causa erros aritméticos em modelos de linguagem), toda a análise estatística de receitas, gastos por categoria e progressos de metas é processada de forma exata e rápida via código Python tradicional (usando Pandas).
- **RAG Estruturado:** O orquestrador compila as análises calculadas e injeta um sumário analítico perfeitamente formatado no contexto do prompt, permitindo que a Sofia saiba exatamente com quem está conversando.
- **Prevenção Ética de Risco:** Respeitando o perfil de investidor do João, a Sofia é explicitamente proibida de indicar ativos voláteis ou de alto risco, priorizando soluções de liquidez diária garantidas pelo FGC (como o Tesouro Selic).
- **Simulador Offline de Segurança (Mock fallback):** Caso o avaliador da DIO não possua ou não queira inserir uma Chave de API do Google Gemini, a aplicação conta com um motor heurístico local que responde em tempo real com diálogos inteligentes e contextuais focados no cliente João Silva, bastando ligar a chave se desejar ativar a inteligência generativa plena!

---

## 👩‍💻 Autoria do Projeto

- **Estudante:** [Seu Nome Aqui]
- **Bootcamp:** DIO / Inteligência Artificial Generativa e Agentes Inteligentes
- **Instrutor de Referência:** Pierre Falvo (`falvojr`)
