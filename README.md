# 🤖 Legal Chatbot for Social Assistance

This is a hybrid legal chatbot designed to assist individuals in vulnerable situations by providing access to legal information and guidance. It combines rule-based logic with AI-powered responses using LLMs.

## 🚀 Features

* ✅ Support for legal FAQs (family law, housing, labor, etc.)
* 🧠 Hybrid logic: Deterministic + LLM for natural language understanding
* 💬 Integrated with WhatsApp using Twilio
* 🗣️ Dialogflow CX for managing conversation flows
* ⚙️ FastAPI backend for webhook processing and logic control
* ☁️ Hosted on Google Cloud Platform

## 🛠️ Technologies Used

* [Dialogflow CX](https://cloud.google.com/dialogflow/cx) – Conversation flow management
* [FastAPI](https://fastapi.tiangolo.com/) – Backend API for handling webhooks and custom logic
* [Twilio](https://www.twilio.com/whatsapp) – WhatsApp messaging integration
* [Python](https://www.python.org/) – Backend language
* [Docker](https://www.docker.com/) – Containerization
* [Google Cloud Platform (GCP)](https://cloud.google.com/) – Deployment & hosting

## 📦 Project Structure

```
legal-chatbot/
├── app/                    # FastAPI application
│   ├── main.py             # Entry point
│   ├── webhook_handler.py  # Dialogflow CX webhook logic
│   └── db.py               # (Optional) Database integration
├── Dockerfile              # Docker configuration
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

## ⚙️ How to Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/legal-chatbot.git
cd legal-chatbot
```

### 2. Create a virtual environment and install dependencies

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 3. Run the FastAPI server

```bash
uvicorn app.main:app --reload
```

## 🧪 Testing the Webhook

Use the Dialogflow CX console to test the conversation. Make sure the webhook URL is correctly pointing to your FastAPI server (locally or on GCP).

## ☁️ Deployment (GCP)

To deploy the FastAPI app to Google Cloud Run:

```bash
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/legal-chatbot
gcloud run deploy legal-chatbot \
  --image gcr.io/YOUR_PROJECT_ID/legal-chatbot \
  --platform managed \
  --allow-unauthenticated \
  --region YOUR_REGION
```

Update the webhook URL in Dialogflow CX to the Cloud Run endpoint.

## 🙌 Contributing

Contributions are welcome! Open an issue or submit a pull request.

## 🤝 Acknowledgements

* OpenAI for LLM inspiration
* Twilio for WhatsApp integration
* Google Cloud for Dialogflow and hosting

## 📬 Contact

For questions or support, reach out via DM.




# 🤖 Chatbot Jurídico para Assistência Social

Este é um chatbot jurídico híbrido projetado para auxiliar indivíduos em situações de vulnerabilidade, oferecendo acesso a informações e orientações legais. Ele combina lógica determinística com respostas baseadas em IA utilizando LLMs.

## 🚀 Funcionalidades

* ✅ Suporte a perguntas frequentes jurídicas (direito de família, habitação, trabalho, etc.)
* 🧠 Lógica híbrida: determinística + LLM para compreensão de linguagem natural
* 💬 Integração com WhatsApp via Twilio
* 🗣️ Dialogflow CX para gerenciamento dos fluxos de conversação
* ⚙️ Backend em FastAPI para processamento de webhooks e controle de lógica
* ☁️ Hospedado no Google Cloud Platform

## 🛠️ Tecnologias Utilizadas

* [Dialogflow CX](https://cloud.google.com/dialogflow/cx) – Gerenciamento de fluxos de conversação
* [FastAPI](https://fastapi.tiangolo.com/) – API backend para tratamento de webhooks e lógica personalizada
* [Twilio](https://www.twilio.com/whatsapp) – Integração de mensagens no WhatsApp
* [Python](https://www.python.org/) – Linguagem do backend
* [Docker](https://www.docker.com/) – Contêinerização
* [Google Cloud Platform (GCP)](https://cloud.google.com/) – Hospedagem e deployment

## 📦 Estrutura do Projeto

```
legal-chatbot/
├── app/                         # Aplicação FastAPI
│   ├── main.py                  # Ponto de entrada
│   ├── webhook_handler.py       # Lógica de webhook do Dialogflow CX
│   └── db.py                    # (Opcional) Integração com banco de dados
├── Dockerfile                   # Configuração do Docker
├── requirements.txt             # Dependências Python
└── README.MG                    # Documentação do projeto
```

## ⚙️ Como Executar Localmente

### 1. Clone o repositório

```bash
git clone https://github.com/seuusuario/legal-chatbot.git
cd legal-chatbot
```

### 2. Crie um ambiente virtual e instale as dependências

```bash
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
pip install -r requirements.txt
```

### 3. Execute o servidor FastAPI

```bash
uvicorn app.main:app --reload
```

## 🧪 Testando o Webhook

Use o console do Dialogflow CX para testar a conversa. Certifique-se de que a URL do webhook esteja apontando corretamente para seu servidor FastAPI (local ou no GCP).

## ☁️ Deploy (GCP)

Para fazer o deploy da aplicação FastAPI no Google Cloud Run:

```bash
gcloud builds submit --tag gcr.io/SEU_PROJECT_ID/legal-chatbot
gcloud run deploy legal-chatbot \
  --image gcr.io/SEU_PROJECT_ID/legal-chatbot \
  --platform managed \
  --allow-unauthenticated \
  --region SUA_REGIAO
```

Atualize a URL do webhook no Dialogflow CX para o endpoint do Cloud Run.


## 🙌 Contribuições

Contribuições são bem-vindas! Abra uma issue ou envie um pull request.

## 🤝 Agradecimentos

* OpenAI pela inspiração nos LLMs
* Twilio pela integração com WhatsApp
* Google Cloud pelo Dialogflow e hospedagem

## 📬 Contato

Para dúvidas ou suporte, entre em contato via DM.


