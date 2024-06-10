from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from chatbot_Vitoria import enviar_mensagem
import datetime

app = Flask(__name__)

@app.route('/bot_vitoria', methods=['POST'])

def bot_vitoria():
    
    print(request.values)

    # Pega a mensagem do usuário
    msg_usuario = request.values.get('Body', '')

    #Pegando o nome do usuário
    usuario = request.values.get('ProfileName')

    #Pegando o telefone do usuário
    num_telefone = request.values.get('Waid')

    #Pegando a data da mensagem
    dtMensagem = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Gera a resposta do chatbot
    bot_response = enviar_mensagem(msg_usuario, num_telefone, usuario, dtMensagem)

    # Cria uma resposta do Twilio
    resp = MessagingResponse()

    # Adiciona a mensagem à resposta
    resp.message(bot_response)

    

    return str(resp)

@app.route('/')
def index():
    return "Tá funcionando o flask"

if __name__ == '__main__':
    app.run()