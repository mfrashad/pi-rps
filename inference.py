import tensorflow as tf
import sys
# import matplotlib.pyplot as plt

interpreter = tf.lite.Interpreter(model_path="model.tflite") # path to the model file
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
image = tf.io.read_file(sys.argv[1]) #path to saved image
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
elif prediction ==1:
    print("Rock")
else:
    print("Scissors")
