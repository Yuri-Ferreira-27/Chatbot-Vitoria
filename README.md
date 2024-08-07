# Chatbot-Vitoria
## Descrição
Este projeto tem como objetivo desenvolver um sistema onde um usuário pode conversar através do WhatsApp utilizando a API da Twilio. O sistema integra um chatbot que interage com o usuário, registra os dados em um banco de dados, e responde às mensagens utilizando a API da OpenAI para geração de texto. Após as interações, as mensagens são enviadas para um modelo de Machine Learning que analisa e classifica se o uusuário está depressivo ou não, a partir da acurácia do modelo de Machine Learning treinado.

## Funcionalidades
Interação via WhatsApp: Usuários podem enviar mensagens através do WhatsApp, utilizando a API da Twilio.
Chatbot Inteligente: As mensagens são processadas por um chatbot que utiliza a API da OpenAI para gerar respostas inteligentes.
Registro de Dados: Os dados dos usuários e as mensagens trocadas são registrados em um banco de dados.
Análise de Sintomas de Depressão: Um modelo de Machine Learning analisa as mensagens para determinar e classificar um possível sintoma de depressão.

## Tecnologias Utilizadas
Twilio API: Para integração com o WhatsApp.
OpenAI API: Para geração de respostas do chatbot. Neste projeto, foi utilizado o modelo "gpt-3.5-turbo"
Banco de Dados PostgreSQL: Para armazenamento de dados dos usuários e mensagens.
Machine Learning: Para análise e determinação do nível e tipo de depressão.

## Versões utilizadas
Python: 3.9.2 (3.10 / 3.11 pode ser utilizado)
Tensorflow: 2.15.0 
Keras: 2.15.0
Observação: Para que as libs do keras e tensorflow funcionem corretamente, o ideal é utilizar as versões citadas anteriormente e as versões do python mencionadas
OpenAI: 0.28.0
Pandas: 2.2.2
NumPy: 1.26.4

## Licença
Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para mais detalhes.

Autores: Yuri Carvalho Ferreira / Bianca Daniella Salino de Carvalho
Orientador: Raphael Silva de Abreu 
Contatos: yuri.ferreira2781@gmail.com / yuri.ferreira@soulasalle.com.br / bianca.carvalho@soulasalle.com.br

Nota: Este projeto foi desenvolvido como parte do Trabalho de Conclusão de Curso e destina-se a fins educacionais e de pesquisa.