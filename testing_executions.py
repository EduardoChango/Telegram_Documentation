import telebot
import os
from dotenv import load_dotenv
from libs.chatgpt_simpler import GPT
import json
import logging

gpt = GPT()

bot = telebot.TeleBot(os.environ.get('TELEGRAM_READ_BOT_TOKEN'))




def get_quiz(book_parameters):
    page = book_parameters[0]['documents']['actual_page']
    page_counter = book_parameters[0]['documents']['page_quiz_reminded']
    book = book_parameters[0]['documents']['filename']
    document = {
        "file_id":book_parameters[0]['documents']['document_id'],
        "files_info.filename":book
    }
    response = mongo_manager.retrieve_doc(document)

    offset = response['files_info']['page_summary'][0]['page']
    reference = page+page_counter-offset-1

    return gpt.quiz_options(response['files_info']['page_summary'][reference]['text'],response['files_info']['page_summary'][reference]['page'],book)






def create_poll(message):
    #Define message
    chat_id =  message['chat']['id']

    #print(quiz_questions_str)
    quiz_questions =  {
        "question": "¿Cual es el planeta mas cercano al sol?",
        "option_0": "Marte",
        "option_1": "Venus",
        "option_2": "Mercurio",
        "correct_answer": 2
    }

    answer_options = ['a','b','c']
    correct_answer = 0
    question = 'Error'

    try:
        answer_options = [quiz_questions['option_0'],quiz_questions['option_1'],quiz_questions['option_2']]
        correct_answer = int(quiz_questions['correct_answer'])
        question = [quiz_questions['question']]

        bot.send_poll(
        chat_id=chat_id,
        question=question,
        options=answer_options,
        type="quiz",
        correct_option_id=correct_answer,
        is_anonymous=False,
    )

    except Exception as e:
        message_text = e
        bot.send_message(chat_id, message_text)






def manage_poll_answer(poll):
    chat_id = poll['user']['id']#poll.user.id
    poll_id = poll['poll_id']#poll.poll_id
    option_ids = poll['option_ids']#poll.option_ids
    message_text = f"La opcion escogida para la encuesta # {poll_id} fue: {option_ids[0]}"
    bot.send_message(chat_id, message_text)







def lambda_handler(event, context):
    try:
        
        if 'message' in list(json.loads(event['body']).keys()):
            message = json.loads(event['body'])['message']
            chat_id =  message['chat']['id']
            print(list(message.keys()))
            if 'entities' in list(message.keys()):
                print(message['entities'][0]['type'])
                if message['text'] == '/quiz':
                    create_poll(message)
            else:
                print(message)
                message_text = gpt.interaction(message['text'])
                print(message_text)
                bot.send_message(chat_id, message_text)   
                print('message send')
        if 'poll_answer' in list(json.loads(event['body']).keys()):
            #function to move forward on pages
            poll = json.loads(event['body'])['poll_answer']
            manage_poll_answer(poll)

            
    except Exception as e:
        logging.error(str(e))
        print(e)