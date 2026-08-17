# 🗄️ Estratégia de Base de Conhecimento: Sofia

Este documento descreve detalhadamente como a Sofia lê, organiza e contextualiza as informações locais da pasta `data/` para gerar conselhos financeiros personalizados, seguros e de altíssimo valor.

---

## Dados Utilizados

Utilizamos a base de dados padrão fornecida no laboratório para contextualizar o cliente **João Silva**:

| Arquivo | Formato | Utilização no Agente Sofia |
|---------|---------|---------------------|
| `transacoes.csv` | CSV | **Análise de Gastos e Ralos Financeiros:** Permite a Sofia consolidar despesas em categorias (moradia, lazer, alimentação, transporte, saúde) e encontrar as categorias que mais pesam no orçamento diário. |
| `perfil_investidor.json` | JSON | **Personalização e Metas:** Fornece o norte estratégico (Completar reserva de emergência e entrada do apê) e dita que Sofia deve agir com foco em perfis moderados, sem induzir João a assumir riscos desnecessários. |
| `produtos_financeiros.json` | JSON | **Recomendações Seguras:** Uma lista de produtos de renda fixa e fundos. Sofia usará estes dados para projetar onde guardar a economia sugerida (como o Tesouro Selic ou CDB Liquidez Diária para reserva). |
| `historico_atendimento.csv` | CSV | **Histórico e Relacionamento:** Dá a Sofia o histórico de dúvidas anteriores de João, permitindo criar saudações e comentários do tipo: *"Que bom te ver de novo, João! Vi que recentemente conversamos sobre o Tesouro Selic, quer dar uma olhada em como as economias deste mês podem render lá?"* |

---

## Adaptações nos Dados

Para tornar a experiência de João Silva ainda mais rica, as seguintes adaptações dinâmicas são calculadas em memória via Python (com Pandas) antes de serem inseridas no contexto da LLM:
1. **Cálculo de Receita vs. Despesas:** Soma de receitas (Salário) e dedução de todas as despesas listadas em `transacoes.csv` para encontrar o saldo líquido disponível no mês corrente.
2. **Classificação por Categoria:** Agrupamento de gastos (Ex: Moradia: R$ 1380.00, Alimentação: R$ 570.00, Transporte: R$ 295.00, Saúde: R$ 188.00, Lazer: R$ 55.90) para que a IA tenha uma visão analítica consolidada em vez de ler apenas transações brutas e soltas.
3. **Cálculo de Projeção de Metas:** Um motor em Python calcula matematicamente em quantos meses a meta de João (ex: completar R$ 15.000,00 da reserva de emergência, faltando R$ 5.000,00) será alcançada com base na economia mensal simulada de forma exata, evitando que a IA alucine no cálculo de juros compostos ou meses restantes.

---

## Estratégia de Integração

### Como os dados são carregados?
Os dados são parseados e carregados no início da sessão do Streamlit usando a biblioteca `pandas` (para os CSVs) e `json` (para os arquivos JSON). Eles residem em memória de forma segura no estado da sessão do usuário (`st.session_state`).

### Como os dados são usados no prompt?
Sofia utiliza uma estratégia híbrida de **RAG estruturado**. Em vez de injetar o conteúdo bruto e gigante de arquivos no prompt, o orquestrador Python compila um resumo analítico e limpo das finanças de João Silva.

A estrutura do contexto formatado enviado à LLM no prompt do sistema se parece com isso:

```text
==================================================
CONTEXTO ATUAL DO CLIENTE (JOÃO SILVA):
- Renda Mensal: R$ 5.000,00
- Despesas Totais Calculadas: R$ 2.488,90
- Saldo Líquido do Mês: R$ 2.511,10

CONSOLIDADO DE GASTOS POR CATEGORIA:
- Moradia: R$ 1.380,00 (Aluguel, Luz)
- Alimentação: R$ 570,00 (Supermercado, Restaurantes)
- Transporte: R$ 295,00 (Uber, Combustível)
- Saúde: R$ 188,00 (Farmácia, Academia)
- Lazer: R$ 55,90 (Netflix)

METAS DO CLIENTE:
1. Completar reserva de emergência (Faltam R$ 5.000,00 para atingir R$ 15.000,00)
2. Entrada do apartamento (Precisa de R$ 50.000,00 até Dezembro/2027)

HISTÓRICO RECENTE DE ATENDIMENTO:
- Conversou recentemente sobre Tesouro Selic e progresso de metas.

PRODUTOS FINANCEIROS DISPONÍVEIS (SEGUROS):
- Tesouro Selic (Rendimento: 100% Selic, indicado para Reserva)
- CDB Liquidez Diária (Rendimento: 102% CDI, indicado para Reserva)
==================================================
```

Isso garante que Sofia saiba exatamente com quem está conversando, quanto ele gasta, no que ele gasta e quais produtos são seguros e adequados para as suas metas!
