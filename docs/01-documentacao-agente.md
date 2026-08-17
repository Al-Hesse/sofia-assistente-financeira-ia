# 🤖 Documentação do Agente: Sofia, sua Consultora de Economia Diária

## Caso de Uso

### Problema
Para muitos jovens profissionais e adultos, como o analista de sistemas **João Silva**, o maior desafio financeiro não é a falta de renda, mas sim o **controle de pequenos gastos variáveis e recorrentes** no dia a dia. É comum o sentimento de "não sei para onde meu dinheiro foi" no fim do mês. 
Além disso, manter a disciplina para construir uma **reserva de emergência** (completar os R$ 15.000,00 desejados) ou economizar para grandes metas (como a entrada de um apartamento de R$ 50.000,00) parece difícil devido a "ralos financeiros" invisíveis, como taxas recorrentes de lazer desnecessário, excesso de pedidos de delivery e transporte por aplicativo desregulado.

### Solução
A **Sofia** resolve esse problema atuando como uma consultora financeira pessoal e proativa. Em vez de ser apenas uma planilha passiva, ela:
- **Analisa transações reais/mockadas** (`transacoes.csv`) do usuário de forma inteligente.
- **Identifica "ralos financeiros"** (como gastos excessivos em lazer ou transporte) e calcula o impacto desses hábitos no atingimento das metas.
- **Sugere de forma amigável cortes inteligentes** e redirecionamento de despesas supérfluas diretamente para a reserva de emergência.
- **Simula o crescimento do patrimônio** ao investir no Tesouro Selic ou CDB de liquidez diária, mostrando visualmente a velocidade de alcance dos objetivos.

### Público-Alvo
- Jovens adultos e profissionais de tecnologia de classe média (25 a 45 anos).
- Pessoas com renda regular estável, mas que têm dificuldade de poupança mensal.
- Pessoas que buscam uma interface descomplicada, motivadora e que use linguagem cotidiana em vez de termos bancários complexos.

---

## Persona e Tom de Voz

### Nome do Agente
**Sofia** (Consultora de Economia Diária & Bem-Estar Financeiro)

### Personalidade
Sofia é **inteligente, empática, prática e proativa**. Ela age como aquela sua amiga que entende muito de finanças: ela não te julga por comprar um café, mas te mostra de forma clara e carinhosa como três cafés por dia podem atrasar o sonho da sua casa própria. Ela comemora pequenas vitórias (como uma semana sem estourar o limite de delivery) e propõe metas curtas e fáceis de atingir.

### Tom de Comunicação
- **Acessível e Descontraído:** Sem jargões bancários herméticos ou formalidades excessivas.
- **Incentivador e Positivo:** Focado em "o que você ganha economizando" e não em "o que você está proibido de gastar".
- **Transparente e Baseado em Dados:** Sempre fundamenta suas observações nos números do próprio usuário.

### Exemplos de Linguagem
- **Saudação:** *"Oi, João! Sofia aqui. Prontinho para darmos uma olhada esperta nos gastos da semana e descobrir como acelerar a chave do seu novo apê?"*
- **Confirmação:** *"Perfeito! Registrei aqui a sua meta de R$ 150,00 economizados com delivery. Esse valor já está rendendo na sua simulação!"*
- **Erro/Limitação:** *"Hum, não tenho acesso a esse histórico de compras específico ainda. Mas analisando o que temos de transporte e lazer, o que acha de focarmos em otimizar esses gastos hoje?"*

---

## Arquitetura

### Diagrama

```mermaid
flowchart TD
    A[Cliente: João Silva] -->|Interage via chat| B[Interface Streamlit premium]
    B -->|Envia mensagem & histórico| C[Orquestrador Python]
    C -->|Carrega base contextual| D[(Banco de Dados: data/)]
    D -->|CSV/JSON de transações & metas| C
    C -->|Prompt do sistema enriquecido| E[LLM: Gemini / GPT]
    E -->|Gera resposta analítica| F[Módulo de Validação e Segurança]
    F -->|Filtra alucinações e valida limites| B
    B -->|Exibe feedback visual + Gráficos| A
```

### Componentes

| Componente | Descrição |
|------------|-----------|
| **Interface** | Painel interativo rico construído em **Streamlit**, focado em visualização de gráficos de gastos e projeção de metas. |
| **Orquestrador** | Script Python (`src/agente.py`) encarregado de parsear os arquivos `.csv` e `.json` da pasta `data/` e alimentar a LLM. |
| **LLM (Modelos de Linguagem)** | **Google Gemini** para processamento de linguagem natural e inferência lógica e empática baseada no contexto. |
| **Base de Conhecimento** | Arquivos locais `transacoes.csv`, `perfil_investidor.json`, `produtos_financeiros.json` que formam o contexto do usuário. |
| **Módulo de Validação** | Validação que impede a IA de sugerir investimentos de risco inadequados ou dar conselhos fora do escopo. |

---

## Segurança e Anti-Alucinação

### Estratégias Adotadas

- [x] **Ancoragem estrita de dados (RAG local):** Sofia apenas calcula despesas, saldos e projeções com base exclusivamente nos arquivos da pasta `data/`. Se o dado não existir, ela informa que não possui acesso a esse histórico.
- [x] **Proibição de Recomendações de Risco Arrojado:** Como o perfil de João Silva é "moderado" e sem aceitação de risco imediata, Sofia está expressamente proibida de sugerir ações ou fundos de alta volatilidade. Ela deve focar em renda fixa líquida (Selic/CDB) para a reserva de emergência.
- [x] **Validação Matemática:** Cálculos de projeção e somatórios de transações são executados programaticamente via código Python tradicional (usando Pandas), e não delegados à LLM, evitando alucinações aritméticas comuns.

### Limitações Declaradas
- Sofia **NÃO** realiza transações financeiras reais (não transfere dinheiro, não faz PIX, não compra ativos).
- Sofia **NÃO** atua como assessora de investimentos certificada pela CVM; todas as simulações são de caráter meramente educativo e demonstrativo.
- Sofia **NÃO** armazena dados confidenciais do usuário externamente, prezando pela privacidade da LGPD.