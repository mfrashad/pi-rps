import os
import time
import telebot
import random
import tensorflow as tf

API_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']

bot = telebot.TeleBot(API_TOKEN)
rps_list = ['Rock', 'Paper', 'Scissors']


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, I am EchoBot.
I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
""")


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(commands=['play'])
def play(message):
    bot.send_message(message.chat.id, "Show your hand to the camera in 5 seconds")
    os.system('fswebcam -D 4 image.jpg')
    time.sleep(5);
    photo = open('image.jpg', 'rb')
    bot.send_photo(message.chat.id, photo)
    user_choice = predict('image.jpg')
    bot.send_message(message.chat.id, f'You choose {user_choice}')
    bot_choice = random.choice(rps_list)
    bot.send_message(message.chat.id, f'Bot choose {bot_choice}')
    result = check_win(user_choice, bot_choice)
    if(result == 0):
        bot.send_message(message.chat.id, 'You lose!')
    elif(result == 1):
        bot.send_message(message.chat.id, 'You win!')
    elif(result == 2):
        bot.send_message(message.chat.id, "It's a draw!")
        

def check_win(c1, c2):
    if(c1 == c2):
        return 2
    elif(c1 == 'Rock' and c2 == 'Paper'):
        return 0
    elif(c1 == 'Rock' and c2 == 'Scissors'):
        return 1
    elif(c1 == 'Paper' and c2 == 'Rock'):
        return 1
    elif(c1 == 'Paper' and c2 == 'Scisscors'):
        return 0
    elif(c1 == 'Scissors' and c2 == 'Rock'):
        return 0
    elif(c2 == 'Scissors' and c2 == 'Paper'):
        return 1

        
    

def predict(filepath):
    interpreter = tf.lite.Interpreter(model_path="model.tflite") # path to the model file
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    image = tf.io.read_file(filepath) #path to saved image
    image = tf.image.decode_image(image,channels=3)
    image = tf.cast(image,dtype=tf.float32) /255.
    image = tf.image.resize(image,(224,224))
    image = image *2 -1
    # plt.imshow(image) # can comment out to not show the image
    interpreter.set_tensor(input_details[0]['index'], tf.expand_dims(image,axis=0))
    interpreter.invoke()
    prediction = interpreter.get_tensor(output_details[0]['index'])
    prediction = tf.squeeze(prediction)
    prediction = tf.nn.softmax(prediction,axis=-1)
    prediction = int(tf.argmax(prediction,axis=-1))
    print('Prediction:')
    if prediction == 0:
        print("Paper")
        return "Paper"
    elif prediction ==1:
        print("Rock")
        return "Rock"
    else:
        print("Scissors")
        return "Scissors"




bot.polling()
