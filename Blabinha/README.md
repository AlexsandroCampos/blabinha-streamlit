# Blabinha 2.0 (EN)

Its second version (Blabinha 2.0) was implemented as an instance of a goal-oriented chat-like system. In this case, with interaction via chat (text), it uses OpenAI models and prompt engineering as the core of its reasoning. Since it is a goal-oriented system, it has some objectives to achieve during the conversation: introduction and contextualization of the dialogue; persuasion and engagement; scope restriction of interaction; use of appropriate language (for conversing with children); formulation of multiple-choice questions; and topic analysis. To learn more about Blabinha 2.0, you can access the conversation logs, the evaluation form used to evaluate it, and the results of this evaluation, all available in this directory.

# Blabinha 2.0 (PT-BR)

Blabinha 2.0 é a segunda versão de um sistema de diálogo orientado a objetivos, desenvolvido para interações por chat com crianças sobre a **Amazônia Azul**. Essa versão usa modelos da OpenAI, Gemini e engenharia de prompts para orientar a conversa e atingir objetivos como:

- Introdução e contextualização
- Persuasão e engajamento
- Restrição de escopo da interação
- Linguagem apropriada para crianças
- Formulação de perguntas de múltipla escolha
- Análise de tópicos

Além disso, você pode acessar os registros de conversa, o formulário de avaliação e os resultados da avaliação diretamente neste repositório.

---

## 🚀 Como Rodar o Projeto


### 1. Crie o arquivo `.env`
Crie um arquivo `.env` no diretório raiz com sua chave da OpenAI: (caso não queira ficar fornecendo a chave da API pelo terminal)

```env
OPENAI_API_KEY="sua-chave-aqui" (independentemente de usar ou não modelos da OpenAI, é necessário fornecer uma API_KEY para a criação da imagem de um super-herói ao final do diálogo)
GOOGLE_API_KEY="sua-chave-aqui" (caso vá usar o Gemini)
```

---

### 2. Crie e ative um ambiente virtual

**Windows:**

```powershell
python -m venv venv
.\\venv\Scripts\Activate.ps1
```

**Linux/macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Instale os requisitos

#### Requisitos gerais:
```bash
pip install -r requirements.txt
```

#### Requisitos específicos da pasta `models`:
```bash
pip install -r models/requerimentos.txt
```

#### ⚠️ Instalação do PyTorch

> **Observação:** O PyTorch **não** está incluído no `requirements.txt`, pois a instalação depende da sua GPU/CPU e da versão do CUDA que você possui.
```bash
# 1. Verifique se o PyTorch já está instalado:
python -c "import torch; print(torch.__version__)"

# 2. Caso esteja instalado, desinstale todas as instâncias atuais:
pip uninstall -y torch torchvision torchaudio

# 3. Identifique a versão do CUDA suportada pela sua GPU:
nvcc --version
# (ou consulte o site do fabricante da sua placa)

Instale a versão correta de acordo com seu sistema diretamente do [site oficial do PyTorch](https://pytorch.org/get-started/locally/) ou com um dos comandos abaixo:

**CPU-only (mais seguro para evitar problemas):**

```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

**Com suporte a GPU (CUDA 11.8, por exemplo):**

```bash
pip install torch --index-url https://download.pytorch.org/whl/cu118
```

---

### 4. Execute o aplicativo com Streamlit

**Windows**
```bash
py -m streamlit run .\FrontPage.py
```

**Linux / macOSs**
```bash
python -m streamlit run FrontPage.py 
```

Por padrão, a versão azul do Blabinha será exibida.

#### Alternativas:
- Para a versão vermelha (Komodo), acesse diretamente:

```
http://localhost:8501/FrontPageKomodo
```

---

## 📂 Visualizando Logs: DiaLOGS

Blabinha possui uma interface para análise de conversas na pasta `/Camaleon`.

Para acessá-la:

1. Execute novamente o Streamlit (caso já não esteja rodando)
2. No navegador, acesse:

```
http://localhost:8501/Camaleon
```

> ⚠️ Importante: selecione **apenas arquivos `.json`** com logs de conversa para análise.

---

## ✅ Checklist Rápido

- [x] `.env` criado com a chave da OpenAI
- [x] Ambiente virtual ativado
- [x] Requisitos instalados
- [x] PyTorch instalado
- [x] App rodando via `streamlit run FrontPage.py`

---

## 🧠 Sobre o Projeto

Blabinha 2.0 é parte de uma pesquisa voltada ao uso de sistemas de IA na educação, especialmente com públicos infantis. A estrutura modular e baseada em objetivos permite analisar o impacto das interações em diferentes contextos.
