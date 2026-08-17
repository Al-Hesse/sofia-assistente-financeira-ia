# Sofia: Consultora Inteligente de Economia Diaria e Financas

Bem-vindo ao repositorio do projeto Sofia, um Assistente Virtual de Financas Pessoais desenvolvido como entrega para o laboratorio pratico "Construa Seu Assistente Virtual Com Inteligencia Artificial" da DIO (Digital Innovation One).

A Sofia foi projetada para ir muito alem de uma planilha passiva ou de um assistente de jargoes complexos. Ela e uma mentora empatica, motivadora e inteligente, projetada especificamente para ajudar o usuario Joao Silva (e profissionais em posicoes similares) a desmascarar os "ralos financeiros" de seu orcamento diario, acelerar a construcao de sua reserva de emergencia e conquistar o sonho da casa propria.

---

## Como Rodar o Projeto Localmente

Siga o passo a passo simplificado para ver a Sofia funcionando em uma interface interativa premium construida com Streamlit e Plotly:

### 1. Pre-requisitos
Certifique-se de ter o Python 3.9+ instalado em sua maquina.

### 2. Clonar o Repositorio e Navegar ate a pasta
```bash
git clone https://github.com/Al-Hesse/sofia-assistente-financeira-ia.git
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

### 4. Instalar as Dependencias
```bash
pip install -r src/requirements.txt
```

### 5. Executar o Servidor de Desenvolvimento
```bash
streamlit run src/app.py
```

Pronto! Uma aba no seu navegador se abrira automaticamente apontando para http://localhost:8501/ com o painel premium da Sofia rodando.

---

## Estrutura do Repositorio e Entregaveis da DIO

Este repositorio esta organizado de acordo com as exigencias maximas do laboratorio em 6 etapas:

```text
dio/
│
├── README.md                      # Este arquivo (Apresentacao geral)
├── projeto.md                     # Instrucoes originais da DIO
│
├── data/                          # Base de Conhecimento (Dados locais seguros)
│   ├── transacoes.csv                # Extrato ficticio do cliente Joao Silva
│   ├── perfil_investidor.json        # Perfil e metas estruturadas do cliente
│   ├── produtos_financeiros.json     # Produtos de investimento regulamentados
│   └── historico_atendimento.csv     # Atendimentos de suporte anteriores
│
├── docs/                          # Documentacao detalhada em 5 Etapas
│   ├── 01-documentacao-agente.md     # Definicao de Persona, Tom de voz, Caso de Uso e Diagrama de Fluxo
│   ├── 02-base-conhecimento.md       # Estrategia de dados e engenharia de RAG estruturado em Python
│   ├── 03-prompts.md                 # System Prompt completo da Sofia e exemplos Few-Shot contra alucinacao
│   ├── 04-metricas.md                # Resultados de testes, metricas de acuracia e prevencao de riscos
│   └── 05-pitch.md                   # Roteiro do Pitch de elevador de 3 minutos
│
├── src/                           # Codigo-fonte da aplicacao funcional
│   ├── app.py                        # Interface de usuario interativa em Streamlit
│   ├── agente.py                     # Motor logico do agente (Pandas + Google Gemini)
│   └── requirements.txt              # Declaracao exata das dependencias do sistema
│
└── assets/                        # Imagens e diagramas
```

---

## Destaques Tecnologicos da Sofia

- **Calculos Matematicos Programaticos (Zero Alucinacao):** Em vez de deixar a IA somar e subtrair valores financeiros do usuário (o que frequentemente causa erros aritmeticos em modelos de linguagem), toda a analise estatistica de receitas, gastos por categoria e progressos de metas e processada de forma exata e rapida via codigo Python tradicional (usando Pandas).
- **RAG Estruturado:** O orquestrador compila as analises calculadas e injeta um sumario analitico perfeitamente formatado no contexto do prompt, permitindo que a Sofia saiba exatamente com quem esta conversando.
- **Prevencao Etica de Risco:** Respeitando o perfil de investidor do Joao, a Sofia e explicitamente proibida de indicar ativos volateis ou de alto risco, priorizando solucoes de liquidez diaria garantidas pelo FGC (como o Tesouro Selic).
- **Simulador Offline de Seguranca (Mock fallback):** Caso o avaliador da DIO nao possua ou nao queira inserir uma Chave de API do Google Gemini, a aplicacao conta com um motor heuristico local que responde em tempo real com dialogos inteligentes e contextuais focados no cliente Joao Silva, bastando ligar a chave se desejar ativar a inteligencia generativa plena!

---

## Autoria do Projeto

- **Estudante:** Al-Hesse
- **Bootcamp:** DIO / Inteligencia Artificial Generativa e Agentes Inteligentes
- **Instrutor de Referencia:** Pierre Falvo (falvojr)
