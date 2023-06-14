# Import the necessary libraries
import tensorflow as tf
from tensorflow.keras.applications.inception_v3 import InceptionV3
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.applications.inception_v3 import preprocess_input
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, Embedding, LSTM

# Load the pre-trained InceptionV3 model
image_model = InceptionV3(include_top=True)
image_model = Model(image_model.input, image_model.layers[-2].output)

# Load the pre-trained captioning model
caption_model = tf.keras.models.load_model('caption_model.h5')

# Function to preprocess the image
def preprocess_image(image_path):
    img = load_img(image_path, target_size=(299, 299))
    img = img_to_array(img)
    img = preprocess_input(img)
    img = img.reshape(1, 299, 299, 3)
    return img

# Function to generate captions for images
def generate_caption(image_path):
    img = preprocess_image(image_path)
    feature_vector = image_model.predict(img)
    start = caption_model.tokenizer.word_index['<start>']
    end = caption_model.tokenizer.word_index['<end>']
    caption_input = [start]
    caption = []
    while True:
        sequence = pad_sequences([caption_input], maxlen=caption_model.max_length)
        prediction = caption_model.predict([feature_vector, sequence], verbose=0)
        predicted_id = tf.argmax(prediction, axis=2)
        caption_word = caption_model.tokenizer.index_word[predicted_id.numpy()[0][0]]
        if caption_word == '<end>' or len(caption) >= caption_model.max_length:
            break
        caption.append(caption_word)
        caption_input.append(predicted_id.numpy()[0][0])
    return ' '.join(caption)

# Example usage
image_path = 'example_image.jpg'
caption = generate_caption(image_path)
print(caption)
