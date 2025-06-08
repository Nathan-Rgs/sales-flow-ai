# SalesFlow 🚀  
Chatbot RAG para apoio à conversão de potenciais clientes  
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)  
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

SalesFlow é um assistente conversacional que combina **Large-Language Models (LLMs)** com **Retrieval-Augmented Generation (RAG)** para responder, qualificar e encaminhar leads de forma automatizada em canais digitais (chat web, WhatsApp, etc.).

---

## ✨ Principais recursos

| Recurso | Descrição rápida |
|---------|------------------|
| **Classificador de intenção** | Roteia cada mensagem entre módulos *Info*, *Preço* ou *Diálogo*. |
| **Recuperação vetorial**      | Busca dinâmica em base de conhecimento (FAISS + embeddings OpenAI). |
| **Prompts contextuais**       | Histórico da sessão e trechos recuperados são injetados no prompt. |
| **Logs e métricas**           | Latência, erros de inferência e satisfação do usuário são registrados. |
| **Arquitetura modular**       | Fácil adição de novos domínios ou integração com ERPs/CRMs. |

---

## 🏗️ Arquitetura (alto nível)

```
Usuário ⇄ Aplicação Orquestradora
           ├─► Classificador  (LLM temperatura 0)
           ├─► Módulo Info    (LLM + VetorStore)
           ├─► Módulo Preço   (LLM + VetorStore)
           └─► Módulo Diálogo (LLM)
                          ╰────── VetorStore (FAISS)
```

*Diagrama detalhado disponível em* `docs/arquitetura.png`.

---

## ⚙️ Stack Tecnológico

| Camada             | Ferramentas                                            |
|--------------------|--------------------------------------------------------|
| Linguagem          | Python 3.12                                            |
| Framework IA       | [LangChain 0.3](https://www.langchain.com/)            |
| VetorStore/Search  | FAISS                                                  |
| Embeddings         | `text-embedding-3-small` (OpenAI)                      |
| Modelo de geração  | `gpt-4o-mini` (ou compatível)                          |
| API / Backend      | FastAPI                                                |
| Orquestração       | Docker Compose                                         |

---

## 🖥️ Pré-requisitos

* Python ≥ 3.12  
* Conta OpenAI (ou provedor compatível)  
* Docker (opcional para execução containerizada)

---

## 🚀 Instalação rápida

```bash
# clone
git clone https://github.com/seu-usuario/salesflow.git
cd salesflow

# crie o ambiente
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# dependências
pip install -r requirements.txt
```

### Variáveis de ambiente

Crie um arquivo `.env` na raiz:

```
OPENAI_API_KEY=seu_token_aqui
VECTORSTORE_PATH=.vectorstore
```

## 📄 Licença

Distribuído sob a licença MIT. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.
