import random
import os
import getpass
from dotenv import load_dotenv
from openai import OpenAI
import prompt_engineering
import FileManipulator as manip
import Parte3Azul as parte3
import prompt_engineering
import importlib
import brain as br
import sys

load_dotenv()

stat = 0

#******** OBSERVAÇÂO ***********
# A lista chat['varial'] é utilizada para trocar informações entre a interface e o GPT
# Presta atenção o que cada posição representa
# [0] -> Status | [1] -> Fala Usuario Atual | [2] -> Fala GPT Atual  | [3] -> Quantidade de Bônus rodados | [4] -> Nome da pessoa | [5] -> Nome da Pasta Log
# Uso via CLI para teste rápido
if len(sys.argv) >= 2:
    choice = sys.argv[1]
else:
    # choice = input("Escolha o modelo (GPT, Llama, Qwen, Gemini): ")
    choice = "gpt"

br.select_model(choice)
print(f"Modelo '{choice}' selecionado.\n")
modeloLLM = choice

# Inicializa a API key se não definida
if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")

client = OpenAI(
    # api_key defaults to os.environ.get("openai_API_KEY")  
    api_key=os.getenv("OPENAI_API_KEY"),
)

class PromptStrategy:
    def __init__(self, original_strategy):
        self.strategy = original_strategy
        print("Estratégia selecionada: ", self.strategy)

    def get_strategy(self):
        try:
            module_name = f"prompt_engineering.{self.strategy.replace('-', '')}"
            strategy_module = importlib.import_module(module_name)
            strategy_class = getattr(strategy_module, self.strategy.replace('-', ''))
            return strategy_class()
        
        except ModuleNotFoundError:
            raise ValueError(f"Estratégia '{self.strategy}' não encontrada.")
        
        except AttributeError:
            raise ValueError(f"A classe correspondente à estratégia '{self.strategy}' não foi encontrada no módulo.") #mandar para o streamlit?

class Variaveis:
    def __init__(self):
        self.estrelas = 0
        self.limite = 0
        self.hero = []
        self.path = ""

    def setPath(self,variaveis):
        '''
        seta o path da conversa atual
        '''
        self.estrelas = 0
        self.heto = []
        self.path = manip.return_dialog_folder(variaveis[4],variaveis[5])

    def pathTeste(self):
         '''
         seta um path para testar a parte03
         '''
         path_Vivan = "DiaLOGS\\vivian\\Chat_0_tempo3M_27D_16H_"
         path_Bibi = "DiaLOGS\\bibi\\2024_04_24_20_03_15Chat_0"
         self.path = path_Bibi

    def getPath(self):
        '''
        :return: Retorna o path setado anteriormente
        :rtype: string
        '''
        return self.path
    
    def addStar(self, quantidade: int):
        '''
        :param int quantidade: Adiciona a quantidade de estrelas no total
        '''
        self.estrelas = self.estrelas + quantidade


    def addHeroFeature(self, feature: str):
        '''
        :param str feature: String com a feature do herói
        '''
        self.hero.append(feature)

    def getHeroFeature(self):
        '''
        :return: texto formato com todas as features do herói
        :rtype: string
        '''
        tamanho = len(self.hero)
        frase_final = ""
        if tamanho >= 5:
            frase_final = "O herói tem uma casa: " + self.hero[4]
        if tamanho >= 4:
            frase_final =  frase_final + ". O herói tem como companheiro um :" + self.hero[3]
        if tamanho >= 3:
            frase_final =  frase_final + ". O herói tem uma capa com as seguintes características:" + self.hero[2]
        if tamanho >=2:
            frase_final = frase_final + ". A roupa do herói tem as seguintes características :" + self.hero[1]
        return (frase_final + ". O herói tem como ferramenta :" + self.hero[0])

    def addLimite(self):
        '''
        Adiciona em um o valor de limite para mesma interação
        '''
        self.limite = self.limite + 1

    def resetLimite(self):
        '''
        Reseta o limite para 0
        '''
        self.limite = 0

    def getLimite(self):
        '''
        :return: retorna o valor que está limitando a interação
        :rtype: int
        '''
        print()
        print("O valor do limite é de:" + str(self.limite))
        print()

        return self.limite
    
    def getStar(self):
        '''
        :return: retorna a qauntidade de estrelas
        :rtype: int
        '''
        return self.estrelas
    
var = Variaveis()

class BlabGPTAzul:
    def __init__(self, strategy_name):
        
        self.strategy_instance = PromptStrategy(strategy_name)
        self.strategy = self.strategy_instance.get_strategy()
        
        if not self.strategy_instance:
            raise ValueError(f"Estratégia '{strategy_name}' não encontrada!")
 

    def printVerificador(self, tipoVerificador, caso):
        print("\n-------- Verificador: " + tipoVerificador + " -------- ")
        print("\n ##### \n" + caso + " \n #####")

    def printSecao(self, variaveis):
        print("\n-------- " + str(variaveis[0]) + " -------- ")

    #Formata a resposta do gpt, envia para criação de logs e retorna a resposta formatada
    def enviaResultados(self, respostas, variaveis):
        '''
        Formata as respostas geradas para um padrão e gera chama a função de log
        :param list variaveis: lista de responses geradas pelo GPT
        :retur: Fala do gpt formata
        :rtype: string
        '''
        #Inicio as duas variaveis
        falaGPT_total = ""
        tokens = 0

        #Recebo as respostas do GPT e formato os valores
        for r in respostas:
            falaGPT = r.choices[0].message.content
            falaGPT = falaGPT.replace(".", ".\n")
            falaGPT_total = falaGPT_total + "||" + falaGPT
            tokens = tokens + r.usage.total_tokens

        manip.completaLog(variaveis[0], falaGPT_total, variaveis[1], tokens,variaveis[4],variaveis[5],modeloLLM)

        #Retorno a resposta do GPT formatada
        return falaGPT_total

    #Escolhe qual sequencia de prompt vai ser usada para responder
    def escolheParte(self, variaveis):
        #strategy  = PromptStrategy(strategy_name)
        #print("Estratégia selecionada 2: ", strategy.getStrategy())

        '''
        Escolhe qual função chamar conforme o que está na variavel[0] -> seção
        '''
        secao = variaveis[0]

        if 100 <= secao < 200:
            if secao == 100:
                resposta = self.secao100(variaveis)
            elif secao == 110:
                resposta =  self.secao110(variaveis)
            elif secao == 120:
                resposta = self.secao120(variaveis)
            elif secao == 130:
                resposta = self.secao130(variaveis)
            elif  140 <=secao <= 141:
                resposta = self.secao140(variaveis)
            elif secao == 142:
                variaveis[2] = "Este chat está encerrado pois você informou que não gostaria de continuar."
                resposta = variaveis
            else:
                variaveis[2] = "Este chat está encerrado pois ocorreu um erro. Erro de seção tipo 01"
                resposta = variaveis

        elif 200 <= secao < 300:
            if secao == 205:
                resposta = self.secao205(variaveis)
            elif 210 <= secao < 218:
                resposta = self.secao210(variaveis)
            elif secao == 218:
                resposta = self.secao305(variaveis)
            elif 230 <= secao <= 240:
                resposta = self.secao230(variaveis)
            elif 240 <= secao <= 250:
                resposta = self.secao240(variaveis)
            elif 260 <= secao < 280:
                resposta = self.secao260(variaveis)
            elif 280 <= secao <= 288:
                resposta = self.secao280(variaveis)
            elif 290 <= secao < 300:
                variaveis[2] = "Este chat está encerrado pois você informou que não gostaria de continuar."
                resposta = variaveis
            else:
                variaveis[2] = "Este chat está encerrado pois ocorreu um erro. Erro de seção tipo 02"
                resposta = variaveis
        elif 300 <= secao < 400:
            if 300 <= secao < 310:
                resposta = self.secao300(variaveis)
            elif 310 <= secao < 320:
                resposta = self.secao310(variaveis)
            elif 320 <= secao < 330:
                resposta = self.secao320(variaveis)
            elif 330 <= secao < 340:
                resposta = self.secao330(variaveis)
            elif 340 <= secao < 350:
                resposta = self.secao340(variaveis)
            elif 350 <= secao < 360:
                resposta = self.secao350(variaveis)
            elif 370 <= secao < 380:
                variaveis[2] = "Este chat está encerrado."
                resposta = variaveis
            else: 
                variaveis[2] = "Este chat está encerrado pois ocorreu um erro. Erro de seção tipo 03"
                resposta = variaveis
        else:
            variaveis[2] = "Este chat está encerrado pois ocorreu um erro. Erro de seção tipo 04"
            resposta = variaveis
        return resposta

    #-------------------------------------------------------------------------------------------------
    #Verificadores da PARTE 1

    #Verifica se o nome da pessoa foi dito
    def verificaNome(self, variaveis):
        prompt = self.strategy.verifica_nome(variaveis[1])

        messages=prompt
        response = br.call(messages)
        print(response)
        print("resposta", response.choices[0].message.content.upper())

        if (response.choices[0].message.content.upper().__contains__("FALSE")):
            self.printVerificador("Falou nome", " A pessoa NÃO falou o nome!")
            if (variaveis[0] != 100):
                prompt = self.strategy.nao_falou_nome(variaveis[1], variaveis[2])
                messages=prompt
                response = br.call(messages=prompt)
                print(response)
                variaveis[2] = self.enviaResultados([response], variaveis)
                return False

        else:
            self.printVerificador("Falou nome", "A pessoa falou o nome!")
            return True

    #Verifica se a pessoa pediu para repetir
    def verificaRepete(self, variaveis):   
        prompt = self.strategy.verifica_repete(variaveis[1], variaveis[2])
        messages=prompt
        response = br.call(messages)
        print("a resposta do verifica repete é: ", response.choices[0].message.content)
        if (response.choices[0].message.content.upper().__contains__("TRUE")):
            self.printVerificador("Repete Fala", "A pessoa pediu para repetir ou não entendeu o que foi dito!")

            prompt = self.strategy.repete(variaveis[2])
            messages=prompt
            response = br.call(messages)

            falaGPT = self.enviaResultados([response], variaveis)
            variaveis[2] = falaGPT
            return True

        else:
            self.printVerificador("Repete Fala", "A pessoa não pediu para repetir e entendeu o que foi dito!")
            return False

    #Verifica se a pessoa terminou o desafio
    def verificaDesafio(self, variaveis):   
        prompt = self.strategy.verifica_desafio(variaveis[1], variaveis[2])
        messages=prompt
        response = br.call(messages)

        falaGPT = response.choices[0].message.content

        print("verifica desafio: ", falaGPT)
        self.printVerificador("Verifica Desafio", "verifica Desafio saida :" + str(falaGPT))

        if (response.choices[0].message.content.upper().__contains__("TRUE")):
            return True
        return False
        
    #Verifica se a pessoa entendeu as regras
    def verificaRegras(self, variaveis):   
        prompt = self.strategy.verifica_regras(variaveis[1], variaveis[2])
        messages=prompt
        response = br.call(messages)

        if (response.choices[0].message.content.upper().__contains__("FALSE")):
            self.printVerificador("Verifica Regras", "A pessoa não entendeu as regras!")

            prompt = self.strategy.repete_verifica_regras()
            messages=prompt
            response = br.call(messages)
            variaveis[2] = self.enviaResultados([response], variaveis)
            return False
        else :
            self.printVerificador("Verifica Regras", "A pessoa disse que entendeu as regras!")
            return True

    def casoTeste(self, variaveis):
        '''
        Caso criado para teste
        Vai para função de teste se escrito "jaguatirica"
        '''
        if(variaveis[1] == "jaguatirica"):
            variaveis[0] == 300
            return True
        return False
    #-------------------------------------------------------------------------------------------------
    #Verificadores da PARTE 2    

    #Verifica se a pessoa pediu dica ou não
    def verificaDica(self, variaveis):
        prompt = self.strategy.verifica_dica(variaveis[1])
        messages=prompt  # Responda, Sim, se a pessoa tiver
        response = br.call(messages)

        if (response.choices[0].message.content.upper().__contains__("TRUE")):
            self.printVerificador("Verifica Dica", "A pessoa pediu alguma dica!")
            prompt = self.strategy.pediu_dica()
            messages=prompt
            response = br.call(messages)
            falaGPT  = self.enviaResultados([response], variaveis)
            variaveis[2] = falaGPT       
            return True

        else:
            self.printVerificador("Verifica Dica", "A pessoa não pediu nenhuma dica")
            return False

    #Verifica se a pessoa pediu para terminar
    def verificaTerminar(self, variaveis):
        prompt = self.strategy.verifica_terminar(variaveis[1])
        messages=prompt
        response = br.call(messages)

        if (response.choices[0].message.content.upper().__contains__("TRUE")):
            self.printVerificador("Verifica Termino", "A pessoa pediu para terminar!")

            prompt = self.strategy.verifica_realmente_terminar(variaveis[1])
            messages=prompt
            response = br.call(messages)
            falaGPT  = self.enviaResultados([response], variaveis)
            variaveis[2] = falaGPT
            variaveis[0] = variaveis[0] + 50
            return True

        else:
            self.printVerificador("Verifica Termino", "A pessoa não pediu para terminar")
            return False

    def verifica_terminar2(self, variaveis):
        prompt = self.strategy.verifica_terminar2(variaveis[1], variaveis[2])
        messages=prompt
        response = br.call(messages)

        if (response.choices[0].message.content.upper().__contains__("TRUE")):
            self.printVerificador("Verifica Termino2", "A pessoa pediu para terminar! 2")

            prompt = self.strategy.verifica_realmente_terminar(variaveis[1])
            messages=prompt
            response = br.call(messages)
            falaGPT  = self.enviaResultados([response], variaveis)
            variaveis[2] = falaGPT
            variaveis[0] = variaveis[0] + 10
            return True

        else:
            self.printVerificador("Verifica Termino", "A pessoa não pediu para terminar")
            return False

    def verificaParte03(self, variaveis):
        frase = str.lower(variaveis[1])
        possibilidades = ["criar heroi","criar héroi","parte 3","parte 03"]

        prompt = self.strategy.verificaParte03()
        if frase in possibilidades:
            messages=prompt
            response1 = br.call(messages)
            falaGPT  = self.enviaResultados([response1], variaveis)
            variaveis[2] = falaGPT
            variaveis[0] = variaveis[0] + 70
            return True

        else:
            self.printVerificador("Verifica Termino", "A pessoa não pediu para terminar")
            return False

    #Verifica se a pessoa falou sobre o contexto da amazônia Azul
    def verificaContexto(self, variaveis):

        prompt = self.strategy.verifica_contexto(variaveis[1], variaveis[2])

        contexto = (
            "Amazônia Azul é a região que compreende a superfície do mar, águas sobrejacentes ao leito do mar, solo e subsolo marinhos contidos na extensão atlântica que se projeta a partir do litoral até o limite exterior da Plataforma Continental brasileira."
            "Podemos resumir como tudo que envolve o Mar Brasileiro como animais, locais, navios,etc")
        
        messages=prompt
        response = br.call(messages)

        print("Resposta do verifica contexto: \n", response.choices[0].message.content.upper())

        if (response.choices[0].message.content.upper().__contains__("TRUE")):
            self.printVerificador("Verifica Contexto", "Falou sobre Amazônia Azul")
            print("caiu aqui no verifica contexto**")
            return True

        else:
            self.printVerificador("Verifica Contexto", "NÃO está dentro do contexto")

            prompt = self.strategy.verifica_nao_contexto(variaveis[1])
            messages=prompt
            response = br.call(messages)

            prompt = self.strategy.verifica_nao_contexto_2(contexto)
            messages=prompt
            response1 = br.call(messages)

            respostas = [response,response1]
            falaGPT = self.enviaResultados(respostas, variaveis)    
            falaRotativa = self.secao225(variaveis)
            variaveis[2] = falaGPT + falaRotativa  

            return False


    #Verifica se a pessoa falou alguma das palavras chaves
    def verificaBonus(self, variaveis):
        prompt = self.strategy.verificaBonus(variaveis[1])
        messages=prompt
        response = br.call(messages)

        
        falaGPT = response.choices[0].message.content
        print("fala do gpt", falaGPT)

        if "FALSE" in falaGPT.upper():
            self.printVerificador("Verifica Bonus", "Não caiu no caso Bonus")
            return False

        elif "TRUE" in falaGPT.upper():
            self.printVerificador("Verifica Bonus", "Caiu no caso Bonus")
            return True
        
    def repetiraCriação(self, variaveis):
        print("chamou a criação do heroi")
        prompt = self.strategy.repetiraCriação(variaveis[1], variaveis[2])

        messages=prompt
        response = br.call(messages)
        
        falaGPT = response.choices[0].message.content

        if "FALSE" in falaGPT.upper():
            self.printVerificador("Verifica Bonus - Heroi", "Não caiu no caso Bonus")
            return False

        else:
            self.printVerificador("Verifica Bonus - Heroi", "Caiu no caso Bonus")
            return True

    def secao100(self, variaveis):
        prompt = self.strategy.secao100EscutouFalar(variaveis[1])

        if self.casoTeste(variaveis) is True:
            return self.secaoTeste(variaveis)

        if (self.verificaNome(variaveis) is True):
            print("caiu aqui")
            messages=prompt
            response = br.call(messages)

            respostas = [response]    
            variaveis[2] = self.enviaResultados(respostas, variaveis)    
            variaveis[0] = 120
            return variaveis

        
        prompt = self.strategy.secao100VerificaNome(variaveis[1])
        response = br.call(messages=prompt)
        respostas = [response]    
        variaveis[2] = self.enviaResultados(respostas, variaveis)    
        variaveis[0] = 110
        return variaveis

    def secao110(self, variaveis):
        prompt = self.strategy.secao110NaoFalouNome(variaveis[1], variaveis[2])
        if var.getLimite() < 2:
            if (self.verificaNome(variaveis) is False):
                var.addLimite()
                return variaveis
        else:
            messages=prompt
            response = br.call(messages)
            respostas = [response]    
            variaveis[2] = self.enviaResultados(respostas, variaveis)    
            variaveis[0] = 120
            var.resetLimite()
            return variaveis

        prompt = self.strategy.secao110EscutouFalar(variaveis[1], variaveis[2])      
        messages=prompt
        response = br.call(messages)
        respostas = [response]    
        variaveis[2] = self.enviaResultados(respostas, variaveis)    
        variaveis[0] = 120
        var.resetLimite()
        return variaveis

    def secao120(self, variaveis):
        prompt = self.strategy.secao120(variaveis[1], variaveis[2])
        if self.verificaRepete(variaveis) is True:
                return variaveis

        messages=prompt
        response = br.call(messages)
        respostas = [response]    
        variaveis[2] = self.enviaResultados(respostas, variaveis)    
        variaveis[0] = 130
        var.resetLimite()
        return variaveis

    def secao130(self, variaveis):

        if self.verificaRepete(variaveis) is True:
            return variaveis

        if self.verificaDesafio(variaveis) is False:

            prompt = self.strategy.secao130NaoQuerParticipar(variaveis[1], variaveis[2])
            messages=prompt
            response = br.call(messages)

            respostas = [response]    
            variaveis[2] = self.enviaResultados(respostas, variaveis)    
            variaveis[0] = 140
            var.resetLimite()
            return variaveis
        
        else:
            prompt = self.strategy.secao130Instrucao()
            messages=prompt
            response0 = br.call(messages)
            prompt = self.strategy.secao130RegrasDesafio(response0.choices[0].message.content)
            messages=prompt
            response1 = br.call(messages)

            prompt = self.strategy.secao130EntendeuRegras(response1.choices[0].message.content)
            messages=prompt
            response2 = br.call(messages)


            respostas = [response1,response2]    
            variaveis[2] = self.enviaResultados(respostas, variaveis)    
            variaveis[0] = 205
            var.resetLimite()
            return variaveis

    def secao140(self, variaveis):        

            prompt = self.strategy.secao140ConvencerContinuar(variaveis[1], variaveis[2])
            result = self.verificaDesafio(variaveis)

            if(result is False and variaveis[0] < 141):
                messages=prompt
                response2 = br.call(messages)
                respostas = [response2]
                variaveis[2] = self.enviaResultados(respostas, variaveis)    
                variaveis[0] = variaveis[0] + 1
                return variaveis

            
            if(result is False and variaveis[0] == 141):
                prompt = self.strategy.secao140EncerrarConversa(variaveis[1], variaveis[2])
                messages=prompt
                response2 = br.call(messages)
                respostas = [response2]
                variaveis[2] = self.enviaResultados(respostas, variaveis)    
                variaveis[0] = variaveis[0] + 1
                return variaveis

            
            prompt = self.strategy.secao140ReformularRegrasInfantil()
            messages=prompt
            response1 = br.call(messages)

            prompt = self.strategy.secao140PerguntarEntendeuRegras()
            messages=prompt
            response2 = br.call(messages)

            respostas = [response1,response2]    
            variaveis[2] = self.enviaResultados(respostas, variaveis)    
            variaveis[0] = 205
            return variaveis

    def secao205(self, variaveis):
        prompt = self.strategy.secao205(variaveis[1])

        if self.verificaRegras(variaveis) is False:
            return variaveis

        messages=prompt
        response = br.call(messages)

        variaveis[2] = self.enviaResultados([response] , variaveis)
        variaveis[0] = 210    
        return variaveis

    def secao210(self, variaveis):
        print("variavel 0 antes", variaveis[0])
        print("variavel 3 antes", variaveis[3])
        quests = [212,214,216]

        if self.verificaParte03(variaveis) is True:
            return variaveis 
        
        if self.verificaTerminar(variaveis) is True:
            return variaveis    
        
        if self.verificaDica(variaveis) is True:
            return variaveis
        
        if self.verificaContexto(variaveis) is False:
            return variaveis
        
        prompt = self.strategy.secao210ResponderPergunta(variaveis[1])
        messages=prompt
        response = br.call(messages)

        prompt = self.strategy.secao210FazerQuestao(variaveis[1], response.choices[0].message.content)

        if variaveis[0] in quests:
            messages=prompt
            response1 = br.call(messages)

            prompt = self.strategy.secao210QuestaoAlternativa(variaveis[1], response.choices[0].message.content)
            messages=prompt
            response2 = br.call(messages)
            resposta = [response,response1,response2]
            variaveis[2] = self.enviaResultados(resposta, variaveis)
            variaveis[0] = variaveis[0] + 21
            print("variavel 0 (21)", variaveis[0])
            return variaveis
        
        if (self.verificaBonus(variaveis)):
            print("caiu no bonus")
            
            prompt = self.strategy.secao210Bonus(variaveis[1], response.choices[0].message.content)
            if(variaveis[3] < 1):
                print("caiu aquiaa1")
                messages=prompt
                response2 = br.call(messages)

                resposta = [response,response2]
                variaveis[0] = variaveis[0] + 31
                variaveis[2] = self.enviaResultados(resposta, variaveis)
                variaveis[3] = variaveis[3] + 1
                print("variavel 0 (31)", variaveis[0])
                print("variavel 3", variaveis[3])
                return variaveis
            
        resposta = [response]

        falaGPT = self.enviaResultados(resposta, variaveis)
        falaRotativa = self.secao225(variaveis)


        variaveis[0] = variaveis[0] + 1
        print("variavel 0 fora", variaveis[0])
        variaveis[2]  = falaGPT + falaRotativa

        return variaveis

    def secao225(self, variaveis):
        print("\n--------  225  -------- ")
        alea = random.randint(1,4)
        if alea == 1:
            print("\n--------  caso1  -------- ")
            prompt = self.strategy.secao225Caso1()
            messages=prompt
            response = br.call(messages)
        elif alea == 2:
            print("\n--------  caso2  -------- ")
            prompt = self.strategy.secao225Caso2()
            messages=prompt
            response = br.call(messages)
        elif alea == 3:
            print("\n--------  caso3  -------- ")
            prompt = self.strategy.secao225Caso3()
            messages=prompt
            response = br.call(messages)
        else:
            print("\n--------  caso4  -------- ")
            prompt = self.strategy.secao225Caso4()
            messages=prompt
            response = br.call(messages)
            
        resposta = [response]

        falaGPT = self.enviaResultados(resposta, variaveis)

        return falaGPT

    def secao230(self, variaveis):
        print("entrou aqui no 230")
        print("variaveis[0] antes de atualizada no 230", variaveis[0])
        prompt = self.strategy.secao230(variaveis[1], variaveis[2])
        messages=prompt
        response = br.call(messages)
        resposta = [response]
        variaveis[0] = variaveis[0] - 20
        print("variaveis[0] depois de atualizada no 230", variaveis[0])
        falaGPT = self.enviaResultados(resposta, variaveis)
        falaRotativa = self.secao225(variaveis)
        variaveis[2]  = falaGPT + falaRotativa
        return variaveis

    def secao240(self, variaveis):
        self.printSecao(variaveis)
        print("limite está em", var.getLimite())
        
        value = self.verificaAlternativa(variaveis) 
        if var.getLimite() < 2 and value is False:
                return variaveis
        else:
            if value is True:
                    print("entrou aqui?")
                    #já que nao quer falar uma resposta valida, vamos seguir...
                    print(f"variavel 1: {variaveis[1]}\n")
                    print(f"variavel 2: {variaveis[2]}\n")
                    prompt = self.strategy.secao240_falou_alternativa(variaveis[1], variaveis[2])
            else:
                print("entrou no else")
                prompt = self.strategy.secao240_nao_falou_alternativa_continuar(variaveis[1], variaveis[2])
            messages=prompt
            response = br.call(messages)

            resposta = [response]
            falaGPT = self.enviaResultados(resposta, variaveis)
            variaveis[0] = variaveis[0] - 30
            falaRotativa = self.secao225(variaveis)
            variaveis[2] = falaGPT + falaRotativa
            var.resetLimite()
            return variaveis


    def verificaAlternativa(self, variaveis):
        prompt = self.strategy.secao240_teste_verifica_alternativas(variaveis[1], variaveis[2])
        contexto = variaveis[2]
        print(f"variavel 1 (verificaAlternativa): {variaveis[1]}\n")
        print(f"variavel 2 (verificaAlternativa): {variaveis[2]}\n")
        print("dentro de verifica Alternativa")
        print("**limite está em", var.getLimite())
        messages=prompt
        response = br.call(messages)
        if (response.choices[0].message.content.upper().__contains__("FALSE")):
            var.addLimite()
            prompt = self.strategy.secao240NaoFalouAlternativa(variaveis[1], contexto)
            messages=prompt
            response = br.call(messages)
            variaveis[2] = self.enviaResultados([response], variaveis)
            return False
        else:
            # se falou a alternativa correta
            return True
        
    def secao260(self, variaveis):  
        def retornaValor(status):

            if status >= 260:
                estado = status - 260  
            if status >= 270:
                estado = status - 270  
            if status >= 280:
                estado = status - 280

            estado = estado + 210
            return estado
        
        result = self.verifica_terminar2(variaveis)

        if (result is True and variaveis[0] < 270):

            prompt = self.strategy.secao260Convencer(variaveis[1], variaveis[2])
            messages=prompt
            response2 = br.call(messages)
            respostas = [response2]
            variaveis[2] = self.enviaResultados(respostas, variaveis)    
            variaveis[0] = variaveis[0] + 10
            return variaveis
        
        elif ( result is True and variaveis[0] >= 270):
            prompt = self.strategy.secao260ChatEncerrado(variaveis[1], variaveis[2])
            messages=prompt
            response2 = br.call(messages)
            respostas = [response2]
            variaveis[2] = self.enviaResultados(respostas, variaveis)    
            variaveis[0] = 295
            return variaveis
        else:
            prompt = self.strategy.secao260NaoDesistiu(variaveis[1], variaveis[2])        
            messages=prompt
            response1 = br.call(messages)

            respostas = [response1]    
            falaGPT = self.enviaResultados(respostas, variaveis)
            falaRotativa = self.secao225(variaveis)
            variaveis[2]  = falaGPT + falaRotativa          
            variaveis[0] = retornaValor(variaveis[0])
            return variaveis   

    def secao280(self, variaveis):
        prompt = self.strategy.secao280VerificaContinuar(variaveis[1], variaveis[2])
        messages=prompt
        response = br.call(messages)

        if (response.choices[0].message.content.upper().__contains__("TRUE")):
            return self.secao300(variaveis)
        
        print("caiu aqui")
        print("caiu aqui")
        print("caiu aqui")
        print("caiu aqui")

        prompt = self.strategy.secao280Continuar()
        messages=prompt
        response1 = br.call(messages)

        respostas = [response1]    
        falaGPT = self.enviaResultados(respostas, variaveis)
        falaRotativa = self.secao225(variaveis)
        variaveis[2]  = falaGPT + falaRotativa          
        variaveis[0] = variaveis[0] - 70
        print(variaveis[0])
        return variaveis   

    def secao300(self, variaveis):
        var.setPath(variaveis)

        prompt = self.strategy.secao300()
        messages=prompt
        response1 = br.call(messages)
        falaGPT = self.enviaResultados([response1], variaveis)
        variaveis[2]  = falaGPT         
        variaveis[0] = 310
        return variaveis

    def secao305(self, variaveis):
        var.setPath(variaveis)

        prompt = self.strategy.secao305()
        messages=prompt
        response1 = br.call(messages)
        falaGPT = self.enviaResultados([response1], variaveis)
        variaveis[2]  = falaGPT         
        variaveis[0] = 310
        return variaveis

    def secao310(self, variaveis):
        '''
        :Verifica o quanto a pessoa interagiu e da estrelas
        :Verifica a quantidade de topicos e da estrelas
        :Verifica se ela caiu em bônus
        :Verifica a quantidade de questões que foi achada
        :Escolher as caracteristicas
        '''

        file_path = var.getPath()

        topicos = parte3.geraTopicos(file_path)

        var.addStar(int(topicos[3]))

        estrelas = parte3.estrelasCompletude(file_path)

        var.addStar(int(estrelas))

        qQuestoes = parte3.analisaRespostas(file_path)

        bonus = manip.returnBonus(var.getPath())

        prompt = self.strategy.secao310QuantidadeEstrela(estrelas)
        messages=prompt
        response1 = br.call(messages)

        prompt = self.strategy.secao310QuantidadeTopicos(topicos)
        messages=prompt
        response2 = br.call(messages)


        if(bonus == False):
            prompt = self.strategy.secao310NaoConseguiuBonus()
            messages=prompt
            response3 = br.call(messages)
            var.addHeroFeature("nada")
        else:
            ferramenta = parte3.verificaBonus(bonus)
            prompt = self.strategy.secao310ConseguiuBonus(ferramenta)
            messages=prompt
            response3 = br.call(messages)
            var.addStar(2)
            var.addHeroFeature(ferramenta)

        if qQuestoes >= 1:
            prompt = self.strategy.secao310QuantidadeQuestoes(qQuestoes)
            messages=prompt
            response4 = br.call(messages)
            resposta = [response1,response2,response3,response4]
            variaveis[2] = self.enviaResultados(resposta,variaveis)
            variaveis[0] = parte3.escolheQuestões(qQuestoes)
        else:
            prompt = self.strategy.secao310NaoRespondeuQuestoes()
            messages=prompt
            response4 = br.call(messages)
            resposta = [response1,response2,response3,response4]
            variaveis[2] = self.enviaResultados(resposta,variaveis)
            variaveis[0] = 352
        return variaveis

    def secao320(self, variaveis):
        prompt = self.strategy.secao320()
        var.addHeroFeature(variaveis[1])
        messages=prompt
        response1 = br.call(messages)
        resposta = [response1]
        variaveis[2] = self.enviaResultados(resposta,variaveis)
        if(variaveis[0] > 322):
            variaveis[0] = variaveis[0] + 10
        else:
            variaveis[0] = 350
        return variaveis

    def secao330(self, variaveis):
        prompt = self.strategy.secao330()
        var.addHeroFeature(variaveis[1])
        messages=prompt
        response1 = br.call(messages)
        resposta = [response1]
        variaveis[2] = self.enviaResultados(resposta,variaveis)
        if(variaveis[0] > 333):
            variaveis[0] = variaveis[0] + 10
        else:
            variaveis[0] = 350
        return variaveis
        
    def secao340(self, variaveis):
        prompt = self.strategy.secao340()
        var.addHeroFeature(variaveis[1])
        messages=prompt
        response1 = br.call(messages)
        resposta = [response1]
        variaveis[2] = self.enviaResultados(resposta,variaveis)
        variaveis[0] = 350
        return variaveis

    def secao350(self, variaveis):
        prompt = self.strategy.secao350(str(var.getStar()))
        var.addHeroFeature(variaveis[1])

        messages=prompt
        response1 = br.call(messages)
        prompt = var.getHeroFeature()
        print(prompt)
        frase =  "Gere um heroi que vai proteger o oceano do Brasil. Ele tem as seguintes caracteristicas:" + prompt + "A sua força está ligada com a quantidade de pontos. Ele tem" + str(var.getStar()) + "pontos de um total de 10."
        imagem = client.images.generate(
            model="dall-e-3",
            prompt=frase,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        resposta = [response1]
        variaveis[2] = self.enviaResultados(resposta,variaveis)
        variaveis[2] = variaveis[2] + "\nlink para a imagem gerada:  " + imagem.data[0].url
        variaveis[0] = 371
        manip.saveImages(variaveis[4],variaveis[5],imagem.data[0].url)
        return variaveis

    def secaoTeste(self, variaveis):
        var.pathTeste()
        return self.secao300(variaveis)
        