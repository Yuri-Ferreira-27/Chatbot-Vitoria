import openai
from conexao_Postgres import get_connection
from modeloML import *

chave_api = "minha-chave" #Informe a sua chave da API 

openai.api_key = chave_api

conexao = get_connection()
respostas = []

conexao = get_connection()

def verifica_usuario(user):
      #Função para verificar se usuário existe
      connect = conexao.cursor() 
      
      connect.execute("SELECT EXISTS(SELECT usuario FROM USUARIO WHERE telefone = %s)", (user, ))
   
      resultado = connect.fetchone()[0]
      connect.close()
      return resultado
    
def selecionar_mensagens(telefone):
      #Função para selecionar as mensagens gravadas no campo mensagem da tabela mensagens
      connect = conexao.cursor()
      
      connect.execute("SELECT CONCAT ('chatbot:',message_chatbot),CONCAT ('resposta da pessoa:',message_user) FROM MENSAGEM WHERE usuario = %s", (telefone, ))
    
      respostas = connect.fetchall()
      
      connect.close()
      return respostas

def selecionar_mensagens_usuario(telefone):
      connect = conexao.cursor()
      connect.execute("SELECT CONCAT (message_user) FROM MENSAGEM WHERE usuario = %s", (telefone,))
      respostas_usuario = connect.fetchall()
      connect.close()
      return respostas_usuario

def formatar_mensagens(mensagens):
  #Converte uma lista de tuplas de mensagens em uma lista plana de strings.
  mensagens_formatadas = []
  for mensagem in mensagens:
    mensagens_formatadas.append(mensagem[0])
  return mensagens_formatadas[1:]

def inserir_usuario(telefone,usuario):
      connect = conexao.cursor()
      connect.execute("INSERT INTO usuario (telefone, nome) VALUES (%s, %s)", (telefone,usuario))
      conexao.commit()
      connect.close()

def contar_linhas_usuario(telefone):
      connect = conexao.cursor()
      connect.execute("SELECT COUNT(*) FROM MENSAGEM WHERE usuario = %s", (telefone,))
      resultado = connect.fetchone()  # Recupera o resultado da consulta (uma tupla)
      num_linhas = resultado[0]
      connect.close()

      if num_linhas > 0:
        num_linhas -= 1
      return num_linhas
      
def registrar_diagnostico(diagnostico,telefone):
      connect = conexao.cursor()
      connect.execute("INSERT INTO diagnostico (diagnostico,usuario) VALUES (%s, %s)", (diagnostico, telefone,))
      conexao.commit()
      connect.close()

def enviar_mensagem(mensagem, telefone, usuario, dtMensagem):

    cursor = conexao.cursor()
    # Verifica se o usuário existe
    user_exist = verifica_usuario(telefone)

    if user_exist == False:
        inserir_usuario(telefone, usuario)
        print("Usuário inserido")
    else:
        print("Usuário já existe")
        #Seleciona todas as mensagens do usuário e do chatbot 
        msgSalva = selecionar_mensagens(telefone)
        
        #Seleciona todas as mensagens do usuário
        msgUser = selecionar_mensagens_usuario(telefone)
        msgFormatada = formatar_mensagens(msgUser)
        
        qtd_msg = contar_linhas_usuario(telefone)
        print("Qtd mensagens: ",qtd_msg)
        if(qtd_msg == 10):
            res = predict(msgFormatada)
            result_final = calcular_media(res)
            if(result_final == 1):
                  diagnostico = "Positivo"
                  resp_chat = f"{usuario}, pelos sintomas mencionados na conversa, existe a possiibilidade de você estar com sintomas de depressão. Por isso, recomendo que você procure um profissional de saúde mental para uma avaliação mais detalhada. Cuidar da sua saúde mental é muito importante."
            else:
                  diagnostico = "Negativo"
                  resp_chat = f"{usuario}, não identifiquei sintomas de depressão em suas respostas. No entanto, é sempre bom estar atento à sua saúde mental e procurar ajuda se sentir necessidade. "
            registrar_diagnostico(diagnostico,telefone)
            print("Mensagens do usuário: ",msgFormatada)
            return resp_chat
            
        # Adicione o prompt ao início da mensagem do usuário
        messages = [
        {"role": "system", "content": "Você é uma psicóloga chamada Vitória. Seu objetivo é tentar identificar se a pessoa está com depressão. Para isso, você deve fazer perguntas baseadas nos questionários PHQ-8 e PHQ-9, que são ferramentas de triagem para a depressão. As perguntas devem ser feitas uma de cada vez e devem abordar sintomas fisiológicos, comportamentais e psíquicos da depressão. No entanto, para tornar a conversa mais natural e menos direta, você também deve intercalar suas perguntas com outras que não sejam diretamente sobre a depressão. Essas perguntas podem ser sobre o dia do usuário, seus hobbies, ou qualquer outro tópico que possa ajudar o usuário a se sentir mais à vontade para responder. Pergunte ao usuário como ele se sente com relação ao que ele respondeu. Evite perguntas que façam julgamentos. Lembre-se, o objetivo é identificar possíveis sinais de depressão, mas também criar um ambiente de conversa confortável e acolhedor. Importante: Não faça duas perguntas de uma vez. Cada pergunta deve ser feita e respondida antes de passar para a próxima. Gere respostas de até 200 caracteres"},
        {"role": "user", "content": f"O paciente {usuario} já conversou com você antes. Todas as mensagens anteriores são essas: {msgSalva}. Agora ele diz{mensagem}"}
    ]
        
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages, temperature=0.3, max_tokens=200)
        print("Mensagens do usuário: ",msgFormatada)

        #respostas.append((message, response.choices[0]['message']['content'].strip()))
        #print("Respostas:\n")
        #print(respostas)
        resp_chat = response.choices[0]['message']['content'].strip()
        
        cursor.execute("INSERT INTO MENSAGEM(message_user, message_chatbot, dt_mensagem, usuario) VALUES (%s, %s, %s, %s)", (mensagem, resp_chat,dtMensagem, telefone))
        print("Mensagem inserida para o usuário:", usuario)
        
        conexao.commit()
        cursor.close()
        return resp_chat