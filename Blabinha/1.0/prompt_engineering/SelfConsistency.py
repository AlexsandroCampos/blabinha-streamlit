from prompt_engineering.ChainofThought import ChainofThought

class SelfConsistency:
    def __init__(self):
        pass

    def verifica_nome(self, variaveis_1):
        return ChainofThought().verifica_nome(variaveis_1)

    def nao_falou_nome(self, variaveis_1, variaveis_2):
        return ChainofThought().nao_falou_nome(variaveis_1, variaveis_2)

    def verifica_repete(self, variaveis_1, variaveis_2):
        return ChainofThought().verifica_repete(variaveis_1, variaveis_2)

    def repete(self, variaveis_2):
        return ChainofThought().repete(variaveis_2)

    def verifica_desafio(self, variaveis_1, variaveis_2):
        return ChainofThought().verifica_desafio(variaveis_1, variaveis_2)

    def verifica_regras(self, variaveis_1, variaveis_2):
        return ChainofThought().verifica_regras(variaveis_1, variaveis_2)

    def repete_verifica_regras(self):
        return ChainofThought().repete_verifica_regras()

    def verifica_dica(self, variaveis_1):
        return ChainofThought().verifica_dica(variaveis_1)

    def pediu_dica(self):
        return ChainofThought().pediu_dica()

    def verifica_terminar(self, variaveis_1):
        return ChainofThought().verifica_terminar(variaveis_1)

    def verifica_realmente_terminar(self, variaveis_1):
        return ChainofThought().verifica_realmente_terminar(variaveis_1)

    def verifica_terminar2(self, variaveis_1, variaveis_2):
        return ChainofThought().verifica_terminar2(variaveis_1, variaveis_2)

    def verificaParte03(self):
        return ChainofThought().verificaParte03()

    def verifica_contexto(self, variaveis_1, variaveis_2):
        return [
            {"role": "system", "content": (
                "Você é uma robô chamada Blabinha e está conversando com uma criança exclusivamente sobre a Amazônia Azul. "
                "Sua tarefa é determinar se a pergunta está diretamente relacionada à Amazônia Azul.\n"
                "Considere como relacionada à Amazônia Azul se a pergunta:\n"
                "- Mencionar explicitamente 'Amazônia Azul' de maneira contextualizada; ou\n"
                "- For sobre a importância da Amazônia Azul para o Brasil, incluindo temas, mas não se limitando a eles, como: soberania, defesa naval, exploração econômica, "
                "segurança marítima, preservação ambiental no território marítimo reconhecido como Amazônia Azul ou qualquer temática diretamente ligada à região marítima brasileira conhecida como Amazônia Azul.\n"
                "Utilize o método de self-consistency com raciocínio passo a passo:\n"
                "1. Realize cinco análises independentes da pergunta fornecida, recomeçando o raciocínio do zero a cada vez. Forneça, obrigatoriamente, uma justificativa para sua resposta em cada análise.\n"
                "2. Em cada análise, responda 'S' se a pergunta for sobre a Amazônia Azul ou 'N' se não for.\n"
                "3. Conte qual resposta ('S' ou 'N') apareceu mais vezes.\n"
                "4. Se a maioria for 'S', retorne 'TRUE'. Se a maioria for 'N', retorne 'FALSE'.\n"
                "Comece agora. Lembrando que você deve responder **OBRIGATORIAMENTE** com 'TRUE' ou 'FALSE' após demonstrar o raciocínio.\n\n"
            )},
            {"role": "user", "content": variaveis_1},
    ]

    def verifica_nao_contexto(self, variaveis_1):
        return ChainofThought().verifica_nao_contexto(variaveis_1)

    def verifica_nao_contexto_2(self, contexto):
        return ChainofThought().verifica_nao_contexto_2(contexto)

    def verificaBonus(self, variaveis_1):
        return ChainofThought().verificaBonus(variaveis_1)

    def repetiraCriação(self, variaveis_1, variaveis_2):
        return ChainofThought().repetiraCriação(variaveis_1, variaveis_2)

    def secao100EscutouFalar(self, variaveis_1):
        return ChainofThought().secao100EscutouFalar(variaveis_1)

    def secao100VerificaNome(self, variaveis_1):
        return ChainofThought().secao100VerificaNome(variaveis_1)

    def secao110NaoFalouNome(self, variaveis_1, variaveis_2):
        return ChainofThought().secao110NaoFalouNome(variaveis_1, variaveis_2)

    def secao110EscutouFalar(self, variaveis_1, variaveis_2):
        return ChainofThought().secao110EscutouFalar(variaveis_1, variaveis_2)

    def secao120(self, variaveis_1, variaveis_2):
        return ChainofThought().secao120(variaveis_1, variaveis_2)

    def secao130NaoQuerParticipar(self, variaveis_1, variaveis_2):
        return ChainofThought().secao130NaoQuerParticipar(variaveis_1, variaveis_2)

    def secao130Instrucao(self):
        return ChainofThought().secao130Instrucao()

    def secao130RegrasDesafio(self, response):
        return ChainofThought().secao130RegrasDesafio(response)

    def secao130EntendeuRegras(self, response):
        return ChainofThought().secao130EntendeuRegras(response)

    def secao140ConvencerContinuar(self, variaveis_1, variaveis_2):
        return ChainofThought().secao140ConvencerContinuar(variaveis_1, variaveis_2)

    def secao140EncerrarConversa(self, variaveis_1, variaveis_2):
        return ChainofThought().secao140EncerrarConversa(variaveis_1, variaveis_2)

    def secao140ReformularRegrasInfantil(self):
        return ChainofThought().secao140ReformularRegrasInfantil()

    def secao140PerguntarEntendeuRegras(self):
        return ChainofThought().secao140PerguntarEntendeuRegras()

    def secao205(self, variaveis_1):
        return ChainofThought().secao205(variaveis_1)

    def secao210ResponderPergunta(self, variaveis_1):
        return ChainofThought().secao210ResponderPergunta(variaveis_1)

    def secao210FazerQuestao(self, variaveis_1, response):
        return ChainofThought().secao210FazerQuestao(variaveis_1, response)

    def secao210QuestaoAlternativa(self, variaveis_1, response):
        return ChainofThought().secao210QuestaoAlternativa(variaveis_1, response)

    def secao210Bonus(self, variaveis_1, response):
        return ChainofThought().secao210Bonus(variaveis_1, response)

    def secao225Caso1(self):
        return ChainofThought().secao225Caso1()

    def secao225Caso2(self):
        return ChainofThought().secao225Caso2()

    def secao225Caso3(self):
        return ChainofThought().secao225Caso3()

    def secao225Caso4(self):
        return ChainofThought().secao225Caso4()

    def secao230(self, variaveis_1, variaveis_2):
        return ChainofThought().secao230(variaveis_1, variaveis_2)

    def secao240_falou_alternativa(self, variaveis_1, variaveis_2):
        return ChainofThought().secao240_falou_alternativa(variaveis_1, variaveis_2)

    def secao240_nao_falou_alternativa_continuar(self, variaveis_1, variaveis_2):
        return ChainofThought().secao240_nao_falou_alternativa_continuar(variaveis_1, variaveis_2)

    def secao240_teste_verifica_alternativas(self, variaveis_1, variaveis_2):
        return ChainofThought().secao240_teste_verifica_alternativas(variaveis_1, variaveis_2)

    def secao240NaoFalouAlternativa(self, variaveis_1, variaveis_2):
        return ChainofThought().secao240NaoFalouAlternativa(variaveis_1, variaveis_2)

    def secao260Convencer(self, variaveis_1, variaveis_2):
        return ChainofThought().secao260Convencer(variaveis_1, variaveis_2)

    def secao260ChatEncerrado(self, variaveis_1, variaveis_2):
        return ChainofThought().secao260ChatEncerrado(variaveis_1, variaveis_2)

    def secao260NaoDesistiu(self, variaveis_1, variaveis_2):
        return ChainofThought().secao260NaoDesistiu(variaveis_1, variaveis_2)

    def secao280VerificaContinuar(self, variaveis_1, variaveis_2):
        return ChainofThought().secao280VerificaContinuar(variaveis_1, variaveis_2)

    def secao280Continuar(self):
        return ChainofThought().secao280Continuar()

    def secao300(self):
        return ChainofThought().secao300()

    def secao305(self):
        return ChainofThought().secao305()

    def secao310QuantidadeEstrela(self, estrelas):
        return ChainofThought().secao310QuantidadeEstrela(estrelas)

    def secao310QuantidadeTopicos(self, topicos):
        return ChainofThought().secao310QuantidadeTopicos(topicos)

    def secao310NaoConseguiuBonus(self):
        return ChainofThought().secao310NaoConseguiuBonus()

    def secao310ConseguiuBonus(self, ferramenta):
        return ChainofThought().secao310ConseguiuBonus(ferramenta)

    def secao310QuantidadeQuestoes(self, qQuestoes):
        return ChainofThought().secao310QuantidadeQuestoes(qQuestoes)

    def secao310NaoRespondeuQuestoes(self):
        return ChainofThought().secao310NaoRespondeuQuestoes()

    def secao320(self):
        return ChainofThought().secao320()

    def secao330(self):
        return ChainofThought().secao330()

    def secao340(self):
        return ChainofThought().secao340()

    def secao350(self, star):
        return ChainofThought().secao350(star)
