# Presence Suite Background Task

Serviço para comunicação com o Presence Suite para comunicação com operador do Google Chat Bot.

Este serviço que roda com Python 3.7 e FastAPI tem como objetivo realizar a comunicação com o sistema de chat do Presence suite para comunicação com operador através do Bot no Google Chat.

### Uso do código
Para implantação e teste do código é preciso ter instalado o [Cloud SDK](https://cloud.google.com/sdk/docs/install-sdk#installing_the_latest_version) no computador para realização dos seguintes processos.

#### Rodando Localmente
Para realização de testes locais é preciso ter instalado o [Python](https://www.python.org/downloads/) e no seu computador pelo menos na versão 3.7. (Para realização do testes de desenvolvimento deste código é recomendável o uso de um ambiente virtual do python)

Para criação do ambiente virtual do python é preciso ter instalado o [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html) no seu pacote de instalação do python e utilizar o comando `virtualenv -p python3.7 venv` para criar o ambiente.

Após isso você pode usar o comando `source venv/bin/activate` para ativar o ambiente virtual e executar o código no *Linux* ou `.\venv\Scripts\activate` no *Windows*.

Antes de executar é necessário que seja instalado os pacotes necessário para a execução do código com o seguinte comando:
```bash
pip install -r requirements.txt
```

Com tudo instalado, para executar o código basta rodar o seguinte comando:

```bash
uvicorn main:app --port 8080 --reload
```
#### Implantação do serviço

Para implantação do código é preciso ter configurado o projeto desejado no terminal, você pode validar as informações do Cloud SDK utilizando o seguinte comando:
```bash
gcloud config list
```

Com o ambiente configurado corretamente você pode implantar o código no Cloud Run utilizando o Cloud Build, para enviar o código para o Cloud Build basta usar o seguinte comando:
```bash
gcloud builds submit --config=cloudbuild.yaml --gcs-source-staging-dir=gs://artifacts.sas-enduser-chat-ti.appspot.com/images
```
