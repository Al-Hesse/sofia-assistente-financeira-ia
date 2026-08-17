import os
import json
import pandas as pd
import google.generativeai as genai

class SofiaAgente:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.load_data()
        self.calcular_resumos()

    def load_data(self):
        """Carrega todos os dados mockados da pasta data"""
        try:
            self.transacoes_df = pd.read_csv(os.path.join(self.data_dir, "transacoes.csv"))
        except Exception:
            self.transacoes_df = pd.DataFrame(columns=["data", "descricao", "categoria", "valor", "tipo"])

        try:
            with open(os.path.join(self.data_dir, "perfil_investidor.json"), "r", encoding="utf-8") as f:
                self.perfil = json.load(f)
        except Exception:
            self.perfil = {
                "nome": "João Silva",
                "idade": 32,
                "profissao": "Analista de Sistemas",
                "renda_mensal": 5000.00,
                "perfil_investidor": "moderado",
                "objetivo_principal": "Construir reserva de emergência",
                "patrimonio_total": 15000.00,
                "reserva_emergencia_atual": 10000.00,
                "aceita_risco": False,
                "metas": []
            }

        try:
            with open(os.path.join(self.data_dir, "produtos_financeiros.json"), "r", encoding="utf-8") as f:
                self.produtos = json.load(f)
        except Exception:
            self.produtos = []

        try:
            self.atendimento_df = pd.read_csv(os.path.join(self.data_dir, "historico_atendimento.csv"))
        except Exception:
            self.atendimento_df = pd.DataFrame(columns=["data", "canal", "tema", "resumo", "resolvido"])

    def calcular_resumos(self):
        """Calcula agregações financeiras exatas usando Pandas (evitando alucinações matemáticas da LLM)"""
        if self.transacoes_df.empty:
            self.total_receita = 0.0
            self.total_despesa = 0.0
            self.saldo_liquido = 0.0
            self.gastos_por_categoria = {}
            return

        # Filtrar receitas e saídas
        receitas = self.transacoes_df[self.transacoes_df["tipo"] == "entrada"]
        despesas = self.transacoes_df[self.transacoes_df["tipo"] == "saida"]

        self.total_receita = receitas["valor"].sum()
        self.total_despesa = despesas["valor"].sum()
        self.saldo_liquido = self.total_receita - self.total_despesa

        # Agrupar gastos por categoria
        categoria_df = despesas.groupby("categoria")["valor"].sum().reset_index()
        self.gastos_por_categoria = dict(zip(categoria_df["categoria"], categoria_df["valor"]))

    def obter_contexto_string(self):
        """Monta uma string estruturada para injetar como base de conhecimento no prompt da LLM"""
        perfil_str = (
            f"Nome: {self.perfil['nome']}\n"
            f"Idade: {self.perfil['idade']} anos\n"
            f"Profissão: {self.perfil['profissao']}\n"
            f"Renda Mensal Declarada: R$ {self.perfil['renda_mensal']:.2f}\n"
            f"Perfil de Investimento: {self.perfil['perfil_investidor'].upper()}\n"
            f"Patrimônio Total: R$ {self.perfil['patrimonio_total']:.2f}\n"
            f"Reserva de Emergência Atual: R$ {self.perfil['reserva_emergencia_atual']:.2f}\n"
            f"Objetivo Principal: {self.perfil['objetivo_principal']}\n"
        )

        metas_str = ""
        for m in self.perfil.get("metas", []):
            metas_str += f"- {m['meta']}: Necessário R$ {m['valor_necessario']:.2f} (Prazo: {m['prazo']})\n"

        gastos_str = ""
        for cat, val in self.gastos_por_categoria.items():
            gastos_str += f"- {cat.capitalize()}: R$ {val:.2f}\n"

        produtos_str = ""
        for p in self.produtos:
            produtos_str += f"- {p['nome']} ({p['categoria'].replace('_', ' ').capitalize()}): Rendimento {p['rentabilidade']}, Risco: {p['risco']}, Aporte Mínimo: R$ {p['aporte_minimo']:.2f} (Indicado: {p['indicado_para']})\n"

        historico_str = ""
        if not self.atendimento_df.empty:
            for idx, row in self.atendimento_df.tail(3).iterrows():
                historico_str += f"- {row['data']} ({row['canal']}): {row['tema']} - {row['resumo']} (Resolvido: {row['resolvido']})\n"

        contexto = (
            "==================================================\n"
            "DADOS DO CLIENTE (DADOS REAIS DA BASE DE CONHECIMENTO):\n"
            f"{perfil_str}\n"
            "METAS ATUAIS:\n"
            f"{metas_str}\n"
            "BALANÇO FINANCEIRO DO MÊS (CALCULADO VIA PANDAS):\n"
            f"- Receitas Totais: R$ {self.total_receita:.2f}\n"
            f"- Despesas Totais: R$ {self.total_despesa:.2f}\n"
            f"- Saldo Líquido Restante: R$ {self.saldo_liquido:.2f}\n\n"
            "DISTRIBUIÇÃO DE GASTOS DO MÊS:\n"
            f"{gastos_str}\n"
            "PRODUTOS FINANCEIROS DISPONÍVEIS:\n"
            f"{produtos_str}\n"
            "HISTÓRICO RECENTE DE INTERAÇÕES:\n"
            f"{historico_str if historico_str else 'Nenhum contato anterior.'}\n"
            "=================================================="
        )
        return contexto

    def responder(self, input_usuario, chat_history=[], api_key=None):
        """Gera resposta da Sofia usando a API do Google Gemini ou fallback simulado se não houver chave"""
        contexto_financas = self.obter_contexto_string()

        system_prompt = (
            "Você é a Sofia, consultora financeira de economia diária inteligente, empática e divertida.\n"
            "Seu objetivo principal é ajudar o cliente João Silva a encontrar ralos financeiros e economizar.\n\n"
            "DIRETRIZES DE PERSONA:\n"
            "1. Seja calorosa, motivadora e use tópicos legíveis.\n"
            "2. NUNCA julgue João pelos gastos. Ensine e proponha pequenos desafios de economia.\n"
            "3. Use emojis estratégicos para criar conexão.\n\n"
            "SEGURANÇA E ANTI-ALUCINAÇÃO:\n"
            "1. Baseie suas respostas estritamente no CONTEXTO FINANCEIRO fornecido abaixo.\n"
            "2. Não invente transações adicionais ou produtos financeiros fora da lista.\n"
            "3. O perfil do João é MODERADO. Nunca recomende produtos de alto risco como fundos de ações ou criptomoedas.\n"
            "4. Deixe claro que você é um agente consultivo e não executa transações reais de dinheiro."
        )

        prompt_completo = (
            f"{system_prompt}\n\n"
            f"BASE DE CONHECIMENTO DO CLIENTE:\n{contexto_financas}\n\n"
            "HISTÓRICO DE MENSAGENS DO CHAT:\n"
        )

        for autor, txt in chat_history[-6:]:
            prompt_completo += f"{'Usuário' if autor == 'user' else 'Sofia'}: {txt}\n"

        prompt_completo += f"\nUsuário (João Silva): {input_usuario}\nSofia: "

        # Se houver API key configurada, usa o Gemini de verdade!
        if api_key:
            try:
                genai.configure(api_key=api_key)
                # Utiliza o modelo estável mais recente do Gemini 1.5 Flash para responder rápido
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(prompt_completo)
                return response.text
            except Exception as e:
                return (
                    f"Ops! Tive um probleminha para me conectar ao cérebro de IA do Gemini. 🧠💔\n"
                    f"Erro técnico: {str(e)}\n\n"
                    "Por favor, verifique se a chave de API fornecida na barra lateral está ativa e correta!"
                )

        # Fallback de IA Simulada inteligente e contextual se não houver chave de API
        return self._gerar_resposta_simulada(input_usuario)

    def _gerar_resposta_simulada(self, input_usuario):
        """Gera respostas interativas e amigáveis baseadas em heurísticas locais de forma offline (mock mode)"""
        input_lower = input_usuario.lower()

        if "olá" in input_lower or "oi" in input_lower or "bom dia" in input_lower or "boa tarde" in input_lower:
            return (
                "Oi, João! 😍 Sofia aqui. Que bom falar com você! Estava justamente dando uma olhada "
                "no seu balanço de outubro. Temos algumas conquistas bem legais para comemorar e alguns "
                "pontos de atenção para batermos um papo. Como você quer começar hoje? Podemos olhar seu resumo de gastos "
                "ou traçar um plano de economia para a sua reserva de emergência!"
            )
        
        if "gasto" in input_lower or "extrato" in input_lower or "categoria" in input_lower or "transaç" in input_lower or "transac" in input_lower:
            gastos_resumo = ""
            for cat, val in self.gastos_por_categoria.items():
                gastos_resumo += f"- **{cat.capitalize()}**: R$ {val:.2f}\n"

            return (
                f"João, fiz um consolidado de gastos do seu mês atual usando a nossa base de dados. Olha só onde seu dinheiro foi:\n\n"
                f"{gastos_resumo}\n"
                f"O seu maior gasto de consumo variável está concentrado em **Alimentação (R$ 570,00)** e **Transporte (R$ 295,00)**. 🚗🍔\n\n"
                f"Se conseguirmos poupar só 10% de alimentação e transporte este mês, são **R$ 86,50** livres para irem direto para "
                f"o seu fundo de emergência! O que acha de começarmos por aí?"
            )

        if "reserva" in input_lower or "meta" in input_lower or "emergencia" in input_lower or "poupar" in input_lower or "economizar" in input_lower:
            falta_reserva = 15000.00 - self.perfil["reserva_emergencia_atual"]
            return (
                f"João, sua meta atual de **Reserva de Emergência** é de R$ 15.000,00, e você já tem R$ {self.perfil['reserva_emergencia_atual']:.2f} poupados! "
                f"Falta bem pouquinho: apenas **R$ {falta_reserva:.2f}**! 🎯\n\n"
                f"Como o seu saldo líquido livre esse mês após pagar as contas obrigatórias é de **R$ {self.saldo_liquido:.2f}**, você conseguiria fechar essa meta "
                f"em apenas **2 meses** se direcionar as economias do mês para lá!\n\n"
                f"Minha recomendação é investir esse valor no **Tesouro Selic** ou no **CDB Liquidez Diária** da nossa lista de produtos. Ambas opções rendem "
                f"excelente taxa diária de baixo risco. Quer que eu te explique o rendimento de um deles?"
            )

        if "selic" in input_lower or "cdb" in input_lower or "investir" in input_lower or "produto" in input_lower:
            return (
                "Excelente escolha! Como o seu perfil é **moderado** e seu foco atual é a liquidez para emergências, vamos analisar "
                "as duas melhores opções de renda fixa que temos disponíveis:\n\n"
                "1. **Tesouro Selic (Baixo Risco):** Rende 100% da Taxa Selic oficial. O investimento mínimo é de aproximadamente R$ 30,00, "
                "o que é fantástico para começar pequeno! É o ativo mais seguro do país.\n"
                "2. **CDB Liquidez Diária (Baixo Risco):** Rende 102% do CDI. O investimento inicial é a partir de R$ 100,00, com rendimento que você pode resgatar a qualquer dia útil.\n\n"
                "Se você investir os R$ 300,00 economizados este mês no **CDB Liquidez Diária**, ele já começará a render juros compostos imediatamente, acelerando sua reserva. "
                "Prefere o Tesouro ou o CDB?"
            )

        if "ajuda" in input_lower or "funciona" in input_lower or "o que fazer" in input_lower:
            return (
                "Eu posso te ajudar com várias coisas legais! Digite por exemplo:\n"
                "- *'Quais são os meus maiores gastos?'*\n"
                "- *'Quanto falta para a minha reserva de emergência?'*\n"
                "- *'Onde devo investir minhas economias?'*\n"
                "- *'Como alcançar a entrada do meu apartamento?'*\n\n"
                "Estou aqui para deixar sua jornada financeira mais leve e divertida! 😊"
            )

        # Resposta genérica conectando ao contexto de João Silva
        return (
            f"João, gostei muito da sua pergunta! Analisando sua renda mensal de R$ {self.perfil['renda_mensal']:.2f} "
            f"e o seu saldo líquido disponível de R$ {self.saldo_liquido:.2f}, vejo que você tem uma margem incrível para alcançar a "
            f"sua meta de **{self.perfil['objetivo_principal'].lower()}** sem precisar cortar o lazer que você tanto gosta. ☕✨\n\n"
            f"Para te responder com precisão cirúrgica de IA e simular cenários futuros, insira uma **chave de API do Google Gemini** "
            f"no painel à esquerda, ou diga-me: o que acha de traçarmos uma meta de economia diária para esta semana?"
        )
