# Imports and Parameters

restart = True
epoch_to_pickup = 0

# Import libraries

from tensorflow.keras.layers import StringLookup
import numpy as np
import os
import time
import random
import contextlib
import io
import re
import string
import gc  # Import the garbage collector module
import requests
import urllib.request
import pickle

import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Embedding, GlobalAveragePooling1D
from tensorflow.keras.layers import TextVectorization

import matplotlib.pyplot as plt
from collections import defaultdict
from collections import Counter

print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))

path = ''

# from google.colab import drive
# drive.mount('/content/drive')
# path = '/content/drive/My Drive/M6_Fall2023e/'

vocab_size = 8192
sequence_length = 128
embedding_dim = 128
rnn_units = 512
BATCH_SIZE = 64
BUFFER_SIZE = 10000
num_epochs_total = 12
initial_learning_rate = 0.005  # Increased from 0.002 for better convergence with reduced vocab

author_metrics = defaultdict(lambda: {
    'vocab_size': 0,
    'final_loss': 0,
    'epoch_losses': [],
    'repetition_metrics': {}
})

# Sources

authors = {
    "burroughs": [
        "https://www.gutenberg.org/files/62/62-0.txt",
        "https://www.gutenberg.org/files/64/64-0.txt",
        "https://www.gutenberg.org/files/68/68-0.txt",
        "https://www.gutenberg.org/files/72/72-0.txt",
        "https://www.gutenberg.org/files/78/78-0.txt",
        "https://www.gutenberg.org/files/81/81-0.txt",
        "https://www.gutenberg.org/files/85/85-0.txt",
        "https://www.gutenberg.org/files/90/90-0.txt",
        "https://www.gutenberg.org/files/92/92-0.txt",
        "https://www.gutenberg.org/files/96/96-0.txt",
        "https://www.gutenberg.org/files/123/123-0.txt",
        "https://www.gutenberg.org/files/149/149-0.txt",
        "https://www.gutenberg.org/files/331/331-0.txt",
        "https://www.gutenberg.org/files/364/364-0.txt",
        "https://www.gutenberg.org/files/551/551-0.txt",
        "https://www.gutenberg.org/files/552/552-0.txt",
        "https://www.gutenberg.org/files/553/553-0.txt",
        "https://www.gutenberg.org/files/605/605-0.txt",
        "https://www.gutenberg.org/files/1153/1153-0.txt",
        "https://www.gutenberg.org/files/1401/1401-0.txt",
        "https://www.gutenberg.org/files/2020/2020-0.txt",
        "https://www.gutenberg.org/files/3475/3475-0.txt",
        "https://www.gutenberg.org/files/8748/8748-0.txt",
        "https://www.gutenberg.org/files/8751/8751-0.txt",
        "https://www.gutenberg.org/files/8752/8752-0.txt",
        "https://www.gutenberg.org/files/8753/8753-0.txt",
        "https://www.gutenberg.org/files/8754/8754-0.txt",
        "https://www.gutenberg.org/files/8755/8755-0.txt",
        "https://www.gutenberg.org/files/8756/8756-0.txt",
        "https://www.gutenberg.org/files/8757/8757-0.txt",
        "https://www.gutenberg.org/files/8758/8758-0.txt",
        "https://www.gutenberg.org/files/8760/8760-0.txt",
        "https://www.gutenberg.org/files/8762/8762-0.txt",
        "https://www.gutenberg.org/files/8763/8763-0.txt",
        "https://www.gutenberg.org/files/8766/8766-0.txt",
        "https://www.gutenberg.org/files/8767/8767-0.txt",
        "https://www.gutenberg.org/files/8768/8768-0.txt",
        "https://www.gutenberg.org/files/8769/8769-0.txt",
        "https://www.gutenberg.org/files/58874/58874-0.txt",
        "https://www.gutenberg.org/files/61837/61837-0.txt",
        "https://www.gutenberg.org/files/62409/62409-0.txt",
        "https://www.gutenberg.org/files/69191/69191-0.txt",
        "https://www.gutenberg.org/files/69703/69703-0.txt",
        "https://www.gutenberg.org/files/70002/70002-0.txt",
        "https://www.gutenberg.org/files/70101/70101-0.txt",
        "https://www.gutenberg.org/files/70124/70124-0.txt",
        "https://www.gutenberg.org/files/70195/70195-0.txt",
        "https://www.gutenberg.org/files/70536/70536-0.txt",
        "https://www.gutenberg.org/files/70589/70589-0.txt",
        "https://www.gutenberg.org/files/70815/70815-0.txt",
        "https://www.gutenberg.org/files/71316/71316-0.txt",
        "https://www.gutenberg.org/files/72938/72938-0.txt",
    ],
    "baum": [
        "https://www.gutenberg.org/files/4357/4357-0.txt",
        "https://www.gutenberg.org/files/53196/53196-0.txt",
        "https://www.gutenberg.org/files/16566/16566-0.txt",
        "https://www.gutenberg.org/files/10432/10432-0.txt",
        "https://www.gutenberg.org/files/10124/10124-0.txt",
        "https://www.gutenberg.org/files/10359/10359-0.txt",
        "https://www.gutenberg.org/files/13110/13110-0.txt",
        "https://www.gutenberg.org/files/10468/10468-0.txt",
        "https://www.gutenberg.org/files/16567/16567-0.txt",
        "https://www.gutenberg.org/files/10123/10123-0.txt",
        "https://www.gutenberg.org/files/35859/35859-0.txt",
        "https://www.gutenberg.org/files/53965/53965-0.txt",
        "https://www.gutenberg.org/files/53735/53735-0.txt",
        "https://www.gutenberg.org/files/54540/54540-0.txt",
        "https://www.gutenberg.org/files/22566/22566-0.txt",
        "https://www.gutenberg.org/files/37976/37976-0.txt",
        "https://www.gutenberg.org/files/41667/41667-0.txt",
        "https://www.gutenberg.org/files/518/518-0.txt",
        "https://www.gutenberg.org/files/53566/53566-0.txt",
        "https://www.gutenberg.org/files/53386/53386-0.txt",
        "https://www.gutenberg.org/files/53692/53692-0.txt",
        "https://www.gutenberg.org/files/39868/39868-0.txt",
        "https://www.gutenberg.org/files/47166/47166-0.txt",
        "https://www.gutenberg.org/files/519/519-0.txt",
        "https://www.gutenberg.org/files/41361/41361-0.txt",
        "https://www.gutenberg.org/files/53844/53844-0.txt",
        "https://www.gutenberg.org/files/55020/55020-0.txt",
        "https://www.gutenberg.org/files/520/520-0.txt",
        "https://www.gutenberg.org/files/25519/25519-0.txt",
        "https://www.gutenberg.org/files/24459/24459-0.txt",
        "https://www.gutenberg.org/files/50194/50194-0.txt",
        "https://www.gutenberg.org/files/54/54-0.txt",
        "https://www.gutenberg.org/files/5660/5660-0.txt",
        "https://www.gutenberg.org/files/24578/24578-0.txt",
        "https://www.gutenberg.org/files/21876/21876-0.txt",
        "https://www.gutenberg.org/files/22225/22225-0.txt",
        "https://www.gutenberg.org/files/436/436-0.txt",
        "https://www.gutenberg.org/files/21150/21150-0.txt",
        "https://www.gutenberg.org/files/33361/33361-0.txt",
        "https://www.gutenberg.org/files/32094/32094-0.txt",
        "https://www.gutenberg.org/files/55461/55461-0.txt",
        "https://www.gutenberg.org/files/30852/30852-0.txt",
        "https://www.gutenberg.org/files/23076/23076-0.txt",
        "https://www.gutenberg.org/files/26624/26624-0.txt",
        "https://www.gutenberg.org/files/21159/21159-0.txt",
        "https://www.gutenberg.org/files/30883/30883-0.txt",
        "https://www.gutenberg.org/files/55/55-0.txt",
        "https://www.gutenberg.org/files/958/958-0.txt",
        "https://www.gutenberg.org/files/521/521-0.txt",
        "https://www.gutenberg.org/files/21979/21979-0.txt",
        "https://www.gutenberg.org/files/30658/30658-0.txt",
    ],
    "wells": [
        "https://www.gutenberg.org/cache/epub/35/pg35.txt",
        "https://www.gutenberg.org/cache/epub/36/pg36.txt",
        "https://www.gutenberg.org/cache/epub/159/pg159.txt",
        "https://www.gutenberg.org/cache/epub/5230/pg5230.txt",
        "https://www.gutenberg.org/cache/epub/1013/pg1013.txt",
        "https://www.gutenberg.org/cache/epub/105/pg105.txt",
        "https://www.gutenberg.org/cache/epub/780/pg780.txt",
        "https://www.gutenberg.org/cache/epub/456/pg456.txt",
        "https://www.gutenberg.org/cache/epub/2701/pg2701.txt",
        "https://www.gutenberg.org/cache/epub/12163/pg12163.txt",
        "https://www.gutenberg.org/cache/epub/724/pg724.txt",
        "https://www.gutenberg.org/cache/epub/6593/pg6593.txt",
        "https://www.gutenberg.org/cache/epub/747/pg747.txt",
        "https://www.gutenberg.org/cache/epub/4398/pg4398.txt",
        "https://www.gutenberg.org/cache/epub/22067/pg22067.txt",
        "https://www.gutenberg.org/cache/epub/104/pg104.txt",
        "https://www.gutenberg.org/cache/epub/1044/pg1044.txt",
        "https://www.gutenberg.org/cache/epub/10376/pg10376.txt",
        "https://www.gutenberg.org/cache/epub/23254/pg23254.txt",
        "https://www.gutenberg.org/cache/epub/4225/pg4225.txt",
        "https://www.gutenberg.org/cache/epub/1368/pg1368.txt",
        "https://www.gutenberg.org/cache/epub/4397/pg4397.txt",
        "https://www.gutenberg.org/cache/epub/4000/pg4000.txt",
        "https://www.gutenberg.org/cache/epub/4599/pg4599.txt",
        "https://www.gutenberg.org/cache/epub/1254/pg1254.txt",
        "https://www.gutenberg.org/cache/epub/23255/pg23255.txt",
        "https://www.gutenberg.org/cache/epub/23256/pg23256.txt",
        "https://www.gutenberg.org/cache/epub/23257/pg23257.txt",
        "https://www.gutenberg.org/cache/epub/4595/pg4595.txt",
        "https://www.gutenberg.org/cache/epub/4597/pg4597.txt",
        "https://www.gutenberg.org/cache/epub/171/pg171.txt",
        "https://www.gutenberg.org/cache/epub/4598/pg4598.txt",
        "https://www.gutenberg.org/cache/epub/3223/pg3223.txt",
        "https://www.gutenberg.org/cache/epub/23258/pg23258.txt",
        "https://www.gutenberg.org/cache/epub/23259/pg23259.txt",
        "https://www.gutenberg.org/cache/epub/23260/pg23260.txt",
        "https://www.gutenberg.org/cache/epub/23261/pg23261.txt",
        "https://www.gutenberg.org/cache/epub/23262/pg23262.txt",
        "https://www.gutenberg.org/cache/epub/23263/pg23263.txt",
        "https://www.gutenberg.org/cache/epub/23264/pg23264.txt",
        "https://www.gutenberg.org/cache/epub/23265/pg23265.txt",
        "https://www.gutenberg.org/cache/epub/23266/pg23266.txt",
        "https://www.gutenberg.org/cache/epub/23267/pg23267.txt",
        "https://www.gutenberg.org/cache/epub/23268/pg23268.txt",
        "https://www.gutenberg.org/cache/epub/23269/pg23269.txt",
        "https://www.gutenberg.org/cache/epub/23270/pg23270.txt",
        "https://www.gutenberg.org/cache/epub/23271/pg23271.txt",
        "https://www.gutenberg.org/cache/epub/23272/pg23272.txt",
        "https://www.gutenberg.org/cache/epub/23273/pg23273.txt",
        "https://www.gutenberg.org/cache/epub/23274/pg23274.txt",
        "https://www.gutenberg.org/cache/epub/23275/pg23275.txt",
    ]
}

# Functions

### Text Functions


def preprocess_text(text):
    text = text.replace("Project Gutenberg", "")
    text = text.replace("Gutenberg", "")

    # Remove carriage returns
    text = text.replace("\r", "")

    # fix quotes
    text = text.replace(""", "\"")
    text = text.replace(""", "\"")

    # Convert to lowercase
    text = text.lower()

    # Remove duplicate whitespace
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\n+", "\n", text)
    text = re.sub(r"\t+", "\t", text)

    # Replace newlines and tabs with spaces (preserve continuity)
    text = text.replace("\n", " ")
    text = text.replace("\t", " ")

    # Collapse multiple spaces
    text = re.sub(r" +", " ", text)

    # Add spaces around common punctuation (keep words intact, limit to essential punctuation)
    # This helps the model learn sentence structure without exploding vocabulary
    for punct in ",.!?;:\"'()-":
        text = text.replace(punct, f" {punct} ")

    # Remove spaces around quotes and apostrophes for contractions
    text = re.sub(r" ' ", "'", text)


    # Clean up any duplicate spaces created by punctuation replacement
    text = re.sub(r" +", " ", text)

    return text

def postprocess_text(text):
    # Remove spaces around punctuation for cleaner output
    text = re.sub(r' ([,.!?;:"\')(\-])', r'\1', text)
    # Fix spacing around quotes
    text = re.sub(r'(" |" )', '"', text)

    return text

# def getMyText():
#   path_to_file = tf.keras.utils.get_file('austen.txt', 'https://raw.githubusercontent.com/byui-cse/cse450-course/master/data/austen/austen.txt')

#   text = open(path_to_file, 'rb').read().decode(encoding='utf-8')

#   # path_to_file = tf.keras.utils.get_file('903-0.txt', 'https://www.gutenberg.org/files/903/903-0.txt')
#   # author_text += open(path_to_file, 'rb').read().decode(encoding='utf-8')[2999:-19194]
#   # tf.io.gfile.remove(path_to_file)

#   return preprocess_text(text)

import os
import tensorflow as tf

def getMyText(urls_list=None):
    if urls_list is None:
        urls_list = []

    combined_texts = []

    for i, url in enumerate(urls_list):
        try:
            print(f"Downloading [{i+1}/{len(urls_list)}]: {url}")
            response = urllib.request.urlopen(url, timeout=10)
            text = response.read().decode(encoding='utf-8', errors='ignore')

            if len(text) > 1000:
                combined_texts.append(text)
            else:
                print(f"Text too short, skipping")
        except Exception as e:
            print(f"Failed to download: {e}")

    full_text = '\n\n'.join(combined_texts)
    print(f"Combined {len(combined_texts)} texts: {len(full_text):,} characters\n")

    return preprocess_text(full_text)

def getRandomText(numbooks=1, verbose=False):
    download_log = io.StringIO()
    text_random = ''
    for b in range(numbooks):
        foundbook = False
        while(foundbook == False):
            booknum = random.randint(100, 60000)
            if verbose:
                print('Trying Book #: ', booknum)
            if random.random() > 0.5:
                url = 'https://www.gutenberg.org/files/' + str(booknum) + '/' + str(booknum) + '-0.txt'
                filename_temp = str(booknum) + '-0.txt'
            else:
                url = 'https://www.gutenberg.org/cache/epub/' + str(booknum) + '/pg' + str(booknum) + '.txt'
                filename_temp = 'pg' + str(booknum) + '.txt'
            if verbose:
                print('Trying: ', url)
            try:
                if verbose:
                    path_to_file_temp = tf.keras.utils.get_file(filename_temp, url)
                else:
                    with contextlib.redirect_stdout(download_log):
                        path_to_file_temp = tf.keras.utils.get_file(filename_temp, url)
                temptext = open(path_to_file_temp, 'rb').read().decode(encoding='utf-8')
                tf.io.gfile.remove(path_to_file_temp)
                if (temptext.find('Language: English') >= 0):
                    offset = random.randint(-20, 20)
                    header = 2000
                    total_length = 200000
                    chopoffend = 10000
                    if len(temptext) > (header+total_length+offset+chopoffend):
                        foundbook = True
                        text_random += temptext[header+offset:header+total_length+offset]
                        if verbose:
                            print('New size of dataset: ', len(text_random))
                    elif len(temptext) > (header+12000):
                        foundbook = True
                        text_random += temptext[header:-chopoffend]
                        if verbose:
                            print('New size of dataset: ', len(text_random))
                    else:
                        if verbose:
                            print('Not long enough. Trying again...')
                else:
                    if verbose:
                        print('Not English. Trying again...')
                del temptext
            except:
                if verbose:
                    print('Not valid file. Trying again...')
                foundbook = False
        if verbose:
            print("Found " + str(b+1) + " books so far...")
    del download_log
    return preprocess_text(text_random)

### Vocabulary Functions



def create_vectorize_layer(text):
    vectorize_layer = TextVectorization(
        standardize='lower',
        split='whitespace',
        max_tokens=vocab_size,
        output_mode='int',
    )

    vectorize_layer.adapt([text])
    return vectorize_layer

Save Vocabulary

def save_vocabulary(vectorize_layer, author_name):
    author_dir = os.path.join(path, "models", author_name)
    os.makedirs(author_dir, exist_ok=True)

    vocabulary = vectorize_layer.get_vocabulary()
    vocab_file = os.path.join(author_dir, "vocabulary.txt")

    with open(vocab_file, "w") as file:
        for word in vocabulary:
            file.write(word + "\n")

    print(f"Vocabulary saved: {vocab_file}")
    return vocabulary

Load Saved Vocabulary

def load_vocabulary(author_name):
    author_dir = os.path.join(path, "models", author_name)
    vocab_file = os.path.join(author_dir, "vocabulary.txt")

    if os.path.exists(vocab_file):
        with open(vocab_file, "r") as file:
            vocabulary = [word.strip() for word in file.readlines()]
        print(f"Vocabulary loaded: {vocab_file}")
        return vocabulary

    return None

Turn text into a dataset

# This function will generate our sequence pairs:
def split_input_target(sequence):
    input_ids = sequence[:-1]
    target_ids = sequence[1:]
    return input_ids, target_ids

# This function will create the dataset
def text_to_dataset(text):
    all_ids = vectorize_layer(text)
    ids_dataset = tf.data.Dataset.from_tensor_slices(all_ids)
    del all_ids
    sequences = ids_dataset.batch(sequence_length+1, drop_remainder=True)
    del ids_dataset

    dataset = sequences.map(split_input_target)
    del sequences

    return dataset

Test on vocab text

def setup_dataset(dataset):
    dataset = (
        dataset
        .shuffle(BUFFER_SIZE)
        .batch(BATCH_SIZE, drop_remainder=True)
        .prefetch(tf.data.experimental.AUTOTUNE))
    return dataset

### Model Functions


# Create our custom model. Given a sequence of characters, this
# model's job is to predict what character should come next.
class AuthorTextModel(tf.keras.Model):

    def __init__(self, vocab_size, embedding_dim, rnn_units):
        super().__init__()

        # 1. Embedding layer
        self.embedding = tf.keras.layers.Embedding(vocab_size, embedding_dim)

        # 2. LSTM layers for capturing long-range dependencies
        self.lstm1 = tf.keras.layers.LSTM(rnn_units, return_sequences=True, return_state=True)
        self.lstm2 = tf.keras.layers.LSTM(rnn_units, return_sequences=True, return_state=True)
        self.lstm3 = tf.keras.layers.LSTM(rnn_units, return_sequences=True, return_state=True)

        # 3. Dense hidden layers
        self.hidden1 = tf.keras.layers.Dense(embedding_dim*64, activation='relu')
        self.hidden2 = tf.keras.layers.Dense(embedding_dim*16, activation='relu')

        # 4. Output layer - logits for each vocabulary token
        self.dense = tf.keras.layers.Dense(vocab_size)

    def call(self, inputs, states=None, return_state=False, training=False):
        x = inputs

        # 1. Embedding
        x = self.embedding(x, training=training)

        # 2. Initialize states if needed
        batch_size = tf.shape(inputs)[0]

        if states is None:
            states1 = [tf.zeros([batch_size, self.lstm1.units]), tf.zeros([batch_size, self.lstm1.units])]
            states2 = [tf.zeros([batch_size, self.lstm2.units]), tf.zeros([batch_size, self.lstm2.units])]
            states3 = [tf.zeros([batch_size, self.lstm3.units]), tf.zeros([batch_size, self.lstm3.units])]
        else:
            states1 = states[0]
            states2 = states[1]
            states3 = states[2]

        # 3. LSTM layers with state tracking
        x, state_h_1, state_c_1 = self.lstm1(x, initial_state=states1, training=training)
        states_out_1 = [state_h_1, state_c_1]

        x, state_h_2, state_c_2 = self.lstm2(x, initial_state=states2, training=training)
        states_out_2 = [state_h_2, state_c_2]

        x, state_h_3, state_c_3 = self.lstm3(x, initial_state=states3, training=training)
        states_out_3 = [state_h_3, state_c_3]

        states_out = [states_out_1, states_out_2, states_out_3]

        # 4. Dense hidden layers
        x = self.hidden1(x, training=training)
        x = self.hidden2(x, training=training)

        # 5. Output layer
        x = self.dense(x, training=training)

        # 6. Return results
        if return_state:
            return x, states_out
        else:
            return x

# Here's the code we'll use to sample for us. It has some extra steps to apply
# the temperature to the distribution, and to make sure we don't get empty
# characters in our text. Most importantly, it will keep track of our model
# state for us.

class OneStep(tf.keras.Model):

    def __init__(self, model, vectorize_layer, vocabulary, temperature=1):
        super().__init__()
        self.temperature = temperature
        self.model = model
        self.vectorize_layer = vectorize_layer
        self.vocabulary = vocabulary

        # Create a mask to prevent "" or "[UNK]" from being generated.
        skip_ids = StringLookup(vocabulary=list(vocabulary))(['', '[UNK]'])[:, None]
        sparse_mask = tf.SparseTensor(
            values=[-float('inf')]*len(skip_ids),
            indices=skip_ids,
            dense_shape=[len(vocabulary)])
        self.prediction_mask = tf.sparse.to_dense(sparse_mask, validate_indices=False)

    @tf.function
    def generate_one_step(self, inputs, states=None):
        # Convert strings to token IDs.
        input_ids = self.vectorize_layer(inputs)

        # Run the model.
        predicted_logits, states = self.model(inputs=input_ids, states=states,
                                              return_state=True)
        del input_ids

        # Only use the last prediction.
        predicted_logits = predicted_logits[:, -1, :]
        predicted_logits = predicted_logits / self.temperature

        # Apply the prediction mask
        predicted_logits = predicted_logits + self.prediction_mask

        # Sample the output logits to generate token IDs.
        predicted_ids = tf.random.categorical(predicted_logits, num_samples=1)
        del predicted_logits
        predicted_ids = tf.squeeze(predicted_ids, axis=-1)

        # Return the words and model state.
        vocabulary_adjusted = list(vocabulary)
        vocabulary_adjusted[0] = '[UNK]'
        vocabulary_adjusted[1] = ''
        words_from_ids = tf.keras.layers.StringLookup(vocabulary=vocabulary_adjusted, invert=True)

        predicted_words = words_from_ids(predicted_ids)

        return predicted_words, states

def produce_sample(model, vectorize_layer, vocabulary, temp, epoch, prompt, author_name):
    one_step_model = OneStep(model, vectorize_layer, vocabulary, temp)

    states = None
    next_char = tf.constant([preprocess_text(prompt)])
    result = [prompt]  # Store as strings directly, not TF tensors

    for n in range(200):
        next_char, states = one_step_model.generate_one_step(next_char, states=states)
        # Extract the generated word as a string
        generated_word = next_char.numpy()[0].decode('utf-8', errors='ignore')
        result.append(generated_word)
        next_char = tf.constant([generated_word])

    # Join all words and postprocess
    generated_text = ' '.join(result)
    generated_text = postprocess_text(generated_text)

    # Print and save results
    print(generated_text)

    author_dir = os.path.join(path, "models", author_name)
    os.makedirs(author_dir, exist_ok=True)
    output_file = os.path.join(author_dir, "generated_samples.txt")

    print(f'Epoch: {epoch}\n', file=open(output_file, 'a'))
    print(f'Temp: {temp}\n', file=open(output_file, 'a'))
    print(generated_text, file=open(output_file, 'a'))
    print('\n\n', file=open(output_file, 'a'))

    # Calculate repetition metrics
    words = generated_text.split()
    unique_words = len(set(words))
    total_words = len(words)
    repetition_ratio = unique_words / total_words if total_words > 0 else 0

    # Track most repeated word
    word_counts = Counter(words)
    most_common_word, most_common_count = word_counts.most_common(1)[0] if word_counts else ('', 0)

    # Store metrics
    if temp not in author_metrics[author_name]['repetition_metrics']:
        author_metrics[author_name]['repetition_metrics'][temp] = []

    author_metrics[author_name]['repetition_metrics'][temp].append({
        'unique_ratio': repetition_ratio,
        'most_common_word': most_common_word,
        'most_common_count': most_common_count
    })

    del states
    del next_char

### Generate Single Submission Text After Training

def generate_author_submission(model, vectorize_layer, vocabulary, selected_author):
    """Generate a single 1000+ character submission right after training"""
    print("\n" + "="*80)
    print(f"GENERATING SUBMISSION TEXT FOR {selected_author.upper()}")
    print("="*80 + "\n")

    prompt = "The world seemed like such a peaceful place until the magic tree was discovered in London."

    # Generate text using trained model (no reloading needed!)
    print(f"Generating 1000+ character submission...")
    submission_text = generate_long_text(
        model, vectorize_layer, vocabulary,
        temperature=0.7,
        prompt=prompt,
        min_length=1000
    )

    print(f"Generated {len(submission_text)} characters\n")

    # Write individual author submission file
    author_dir = os.path.join(path, "models", selected_author)
    submission_file = os.path.join(author_dir, f"{selected_author}_submission.txt")

    with open(submission_file, 'w') as f:
        f.write(f"{'='*80}\n")
        f.write(f"RNN LANGUAGE MODEL - {AUTHOR_INFO[selected_author].upper()} SUBMISSION\n")
        f.write(f"{'='*80}\n\n")

        f.write(f"This text is based on words from {AUTHOR_INFO[selected_author]}.\n\n")

        f.write("--- GENERATED TEXT ---\n\n")
        f.write(submission_text)
        f.write("\n\n")

        f.write(f"--- METADATA ---\n")
        f.write(f"Generated characters: {len(submission_text)}\n")
        f.write(f"Minimum required: 1000\n")
        f.write(f"Status: {'PASS' if len(submission_text) >= 1000 else 'FAIL'}\n")
        f.write(f"Prompt: {prompt}\n")

    print(f"Submission file created: {submission_file}\n")
    status = "PASS" if len(submission_text) >= 1000 else "FAIL"
    print(f"Result: {status} ({len(submission_text)} characters)\n")

# Model

### Select Author

# Select which author to train on (change this to switch authors)
selected_author = "wells"  # Options: "burroughs", "baum", "wells"

author_urls = authors[selected_author]
author_dir = os.path.join(path, "models", selected_author)
os.makedirs(author_dir, exist_ok=True)

print(f"\n{'='*70}")
print(f"TRAINING MODEL FOR: {selected_author.upper()}")
print(f"{'='*70}\n")

### Step 1: Fetch Text and Build Vocabulary

print("STEP 1: Fetching text and building vocabulary...")
training_text = getMyText(author_urls)
training_text_preprocessed = preprocess_text(training_text)

vectorize_layer = create_vectorize_layer(training_text_preprocessed)
vocabulary = save_vocabulary(vectorize_layer, selected_author)

print(f"Vocabulary size: {len(vocabulary)}")
print(f"First 20 tokens: {vocabulary[:20]}")
print(f"Last 20 tokens: {vocabulary[-20:]}\n")

### Step 2: Create Dataset

print("STEP 2: Creating dataset...")
vocab_ds = text_to_dataset(training_text_preprocessed)

# Display sample data
def text_from_ids(ids):
    text = ''.join([vocabulary[index] for index in ids])
    return postprocess_text(text)

vocabulary_adjusted = list(vocabulary)
vocabulary_adjusted[0] = '[UNK]'
vocabulary_adjusted[1] = ''

words_from_ids = tf.keras.layers.StringLookup(vocabulary=vocabulary_adjusted, invert=True)

# Test on vocab text
for input_example, target_example in vocab_ds.take(1):
    print("Input: ")
    print(input_example)
    print(text_from_ids(input_example))
    print(words_from_ids(input_example))
    print("Target: ")
    print(target_example)
    print(text_from_ids(target_example))

print()

# Setup batched dataset
dataset = setup_dataset(vocab_ds)
print(f"Dataset created\n")

### Step 3: Build Author Specific Model

print("STEP 3: Building model...")
model = AuthorTextModel(vocab_size, embedding_dim, rnn_units)

# Verify the output of our model is correct by running one sample through
# This will also compile the model for us. This step will take a bit.
for input_example_batch, target_example_batch in dataset.take(1):
    example_batch_predictions = model(input_example_batch)
    print(example_batch_predictions.shape, "# (batch_size, sequence_length, vocab_size)")

print()

# Now let's view the model summary
model.summary()
print()

### Step 4: Compile

print("STEP 4: Compiling model...")
loss = tf.losses.SparseCategoricalCrossentropy(from_logits=True)
opt = tf.keras.optimizers.Adam(learning_rate=initial_learning_rate)
model.compile(optimizer=opt, loss=loss)
print("Model compiled\n")

### Step 5: Train Model

print("STEP 5: Training model...")

start_epoch = 0
for e in range(start_epoch, num_epochs_total):
    success = False
    while success == False:
        try:
            print(f"epoch: {e}")

            # Create dataset from same text with different shuffles
            dataset = text_to_dataset(training_text_preprocessed)
            dataset = setup_dataset(dataset)

            model.optimizer.learning_rate.assign(initial_learning_rate * (0.99**e))

            # Train and track loss
            history = model.fit(dataset, epochs=1, verbose=1)
            epoch_loss = history.history['loss'][0]
            author_metrics[selected_author]['epoch_losses'].append(epoch_loss)

            print("finished training...")
            print(f"Epoch {e} loss: {epoch_loss:.4f}")
            del dataset

            # Generate samples
            print("Generating samples...")
            for temp in [0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
                produce_sample(model, vectorize_layer, vocabulary, temp, e,
                             'The world seemed like such a peaceful place until the magic tree was discovered in London.',
                             selected_author)
            print("samples produced...\n")

            # Cleanup
            gc.collect()
            print("garbage collected...")
            tf.keras.backend.clear_session()
            print("session cleared (to save memory)...\n")

            success = True

        except Exception as ex:
            print(f"Error during training: {ex}")
            gc.collect()
            tf.keras.backend.clear_session()
            try:
                del dataset
            except:
                print("dataset already deleted")
            print(f"retrying epoch: {e}\n")

### Step 6: Save Model Weights and Metrics

print("STEP 6: Saving model weights and metrics...")
model_path = os.path.join(author_dir, f"{selected_author}_model_weights.weights.h5")
model.save_weights(model_path)
print(f"Model weights saved: {model_path}\n")

# Store author metrics for graphics
author_metrics[selected_author]['vocab_size'] = len(vocabulary)
author_metrics[selected_author]['final_loss'] = author_metrics[selected_author]['epoch_losses'][-1] if author_metrics[selected_author]['epoch_losses'] else 0

# Save metrics to file
metrics_file = os.path.join(author_dir, f"{selected_author}_metrics.txt")
with open(metrics_file, 'w') as f:
    f.write(f"Author: {selected_author.upper()}\n")
    f.write(f"Vocabulary Size: {author_metrics[selected_author]['vocab_size']}\n")
    f.write(f"Final Loss: {author_metrics[selected_author]['final_loss']:.4f}\n")
    f.write(f"Epoch Losses: {author_metrics[selected_author]['epoch_losses']}\n")
print(f"Metrics saved: {metrics_file}\n")

### Step 6.5: Generate Submission Text (Immediately After Training)

generate_author_submission(model, vectorize_layer, vocabulary, selected_author)

### Step 7: Generate Graphics

print("STEP 7: Generating individual author graphics...\n")

# Graphics function 1: Training Loss Over Epochs
def plot_training_loss(author_name, epoch_losses):
    if not epoch_losses:
        print(f"No epoch losses to plot for {author_name}")
        return

    plt.figure(figsize=(10, 6))
    epochs = list(range(len(epoch_losses)))
    plt.plot(epochs, epoch_losses, marker='o', linewidth=2, markersize=8, color='#2E86AB')
    plt.xlabel('Epoch', fontsize=12, fontweight='bold')
    plt.ylabel('Training Loss', fontsize=12, fontweight='bold')
    plt.title(f'{author_name.upper()} - Training Loss Over Epochs', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    graphics_dir = os.path.join(path, "models", author_name, "graphics")
    os.makedirs(graphics_dir, exist_ok=True)
    plot_path = os.path.join(graphics_dir, f"{author_name}_training_loss.png")
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    print(f"Training loss plot saved: {plot_path}")
    plt.close()

# Graphics function 2: Repetition Metrics by Temperature
def plot_repetition_metrics(author_name, repetition_metrics):
    if not repetition_metrics:
        print(f"No repetition metrics to plot for {author_name}")
        return

    temperatures = sorted(repetition_metrics.keys())
    avg_unique_ratios = []

    for temp in temperatures:
        metrics_list = repetition_metrics[temp]
        avg_ratio = np.mean([m['unique_ratio'] for m in metrics_list])
        avg_unique_ratios.append(avg_ratio)

    plt.figure(figsize=(10, 6))
    bars = plt.bar([str(t) for t in temperatures], avg_unique_ratios, color='#A23B72', alpha=0.8, edgecolor='black', linewidth=1.5)
    plt.xlabel('Temperature', fontsize=12, fontweight='bold')
    plt.ylabel('Unique Words Ratio (Higher = Less Repetitive)', fontsize=12, fontweight='bold')
    plt.title(f'{author_name.upper()} - Text Repetition by Temperature', fontsize=14, fontweight='bold')
    plt.ylim(0, 1)
    plt.grid(True, alpha=0.3, axis='y')

    # Add value labels on bars
    for bar, ratio in zip(bars, avg_unique_ratios):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{ratio:.2f}', ha='center', va='bottom', fontweight='bold')

    plt.tight_layout()

    graphics_dir = os.path.join(path, "models", author_name, "graphics")
    os.makedirs(graphics_dir, exist_ok=True)
    plot_path = os.path.join(graphics_dir, f"{author_name}_repetition_metrics.png")
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    print(f"Repetition metrics plot saved: {plot_path}")
    plt.close()

# Generate plots for current author
plot_training_loss(selected_author, author_metrics[selected_author]['epoch_losses'])
plot_repetition_metrics(selected_author, author_metrics[selected_author]['repetition_metrics'])

print()

# Load Saved Model and Generate Text

### Generate Per Author Samples

model.load_weights(model_path)
print(f"Model weights loaded: {model_path}\n")

print("Generating new text samples...\n")
for temp in [0.5, 0.7, 0.9]:
    produce_sample(model, vectorize_layer, vocabulary, temp, "final",
        'The world seemed like such a peaceful place until the magic tree was discovered in London.',
        selected_author)

print("\n" + "="*70)
print("TRAINING COMPLETE")
print("="*70)

### Generate Author Comparison Graphics

print("\n" + "="*70)
print("MULTI-AUTHOR COMPARISON GRAPHICS")
print("="*70)

def plot_multi_author_comparison():

    # Collect data from all author directories
    authors_data = {}

    for author_name in authors.keys():
        author_model_dir = os.path.join(path, "models", author_name)
        metrics_file = os.path.join(author_model_dir, f"{author_name}_metrics.txt")

        if os.path.exists(metrics_file):
            with open(metrics_file, 'r') as f:
                content = f.read()
                # Parse metrics
                vocab_line = [line for line in content.split('\n') if 'Vocabulary Size' in line][0]
                loss_line = [line for line in content.split('\n') if 'Final Loss' in line][0]

                vocab_size = int(vocab_line.split(': ')[1])
                final_loss = float(loss_line.split(': ')[1])

                authors_data[author_name] = {
                    'vocab_size': vocab_size,
                    'final_loss': final_loss
                }

    if len(authors_data) == 0:
        print("No trained authors found. Train at least one author first.")
        return

    # Create comparison plot
    fig, ax = plt.subplots(figsize=(12, 7))

    author_names = list(authors_data.keys())
    vocab_sizes = [authors_data[a]['vocab_size'] for a in author_names]
    final_losses = [authors_data[a]['final_loss'] for a in author_names]

    # Create scatter plot
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    for i, (author, vocab, loss) in enumerate(zip(author_names, vocab_sizes, final_losses)):
        ax.scatter(vocab, loss, s=500, alpha=0.7, color=colors[i % len(colors)], edgecolors='black', linewidth=2)
        ax.annotate(author.upper(), (vocab, loss), fontsize=12, fontweight='bold', ha='center', va='center')

    ax.set_xlabel('Vocabulary Size', fontsize=13, fontweight='bold')
    ax.set_ylabel('Final Training Loss', fontsize=13, fontweight='bold')
    ax.set_title('Multi-Author Model Comparison: Vocabulary Size vs Final Loss', fontsize=15, fontweight='bold')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    graphics_dir = os.path.join(path, "models", "graphics")
    os.makedirs(graphics_dir, exist_ok=True)
    plot_path = os.path.join(graphics_dir, "multi_author_comparison.png")
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    print(f"Multi-author comparison plot saved: {plot_path}")
    plt.close()

def plot_vocab_richness_comparison():
    #Plot vocabulary uniqueness across authors - what % of each author's vocab
    #is EXCLUSIVE to them (not found in other authors' vocabularies).
    #Shows linguistic distinctiveness and writing style differences.

    print("\n" + "="*80)
    print("GENERATING VOCABULARY UNIQUENESS COMPARISON")
    print("="*80 + "\n")

    authors_data = {}
    all_vocabularies = {}

    # Load all vocabularies first
    for author_name in authors.keys():
        author_model_dir = os.path.join(path, "models", author_name)
        vocab_file = os.path.join(author_model_dir, "vocabulary.txt")

        if os.path.exists(vocab_file):
            with open(vocab_file, "r") as f:
                vocabulary = set([word.strip() for word in f.readlines()])
            # Filter out empty strings and special tokens
            vocabulary = set([w for w in vocabulary if w and w not in ['', '[UNK]']])
            all_vocabularies[author_name] = vocabulary

    # Calculate uniqueness metrics
    for author_name in all_vocabularies.keys():
        author_model_dir = os.path.join(path, "models", author_name)
        metrics_file = os.path.join(author_model_dir, f"{author_name}_metrics.txt")

        if os.path.exists(metrics_file):
            # Load metrics
            with open(metrics_file, 'r') as f:
                content = f.read()
                vocab_line = [line for line in content.split('\n') if 'Vocabulary Size' in line][0]
                loss_line = [line for line in content.split('\n') if 'Final Loss' in line][0]

                vocab_size = int(vocab_line.split(': ')[1])
                final_loss = float(loss_line.split(': ')[1])

            # Get this author's vocabulary
            author_vocab = all_vocabularies[author_name]

            # Find other authors' combined vocabulary
            other_vocab = set()
            for other_author, other_vocab_set in all_vocabularies.items():
                if other_author != author_name:
                    other_vocab.update(other_vocab_set)

            # Calculate exclusive vocabulary (words ONLY in this author, not in others)
            exclusive_vocab = author_vocab - other_vocab
            exclusive_percentage = (len(exclusive_vocab) / len(author_vocab)) * 100 if len(author_vocab) > 0 else 0

            # Calculate shared vocabulary (words that appear in other authors)
            shared_vocab = author_vocab & other_vocab
            shared_percentage = (len(shared_vocab) / len(author_vocab)) * 100 if len(author_vocab) > 0 else 0

            authors_data[author_name] = {
                'vocab_size': vocab_size,
                'total_unique_words': len(author_vocab),
                'exclusive_words': len(exclusive_vocab),
                'shared_words': len(shared_vocab),
                'exclusive_percentage': exclusive_percentage,
                'shared_percentage': shared_percentage,
                'final_loss': final_loss
            }

            print(f"{author_name.upper()}:")
            print(f"  Total unique words: {len(author_vocab)}")
            print(f"  Exclusive words (not in other authors): {len(exclusive_vocab)}")
            print(f"  Shared words (found in other authors): {len(shared_vocab)}")
            print(f"  Exclusivity: {exclusive_percentage:.1f}%")
            print(f"  Final loss: {final_loss:.4f}\n")

    if len(authors_data) < 2:
        print("Need at least 2 trained authors for comparison.")
        return

    # Create single panel: Vocabulary Exclusivity vs Final Loss (Scatter)
    fig, ax = plt.subplots(figsize=(12, 7))

    author_names = sorted(authors_data.keys())
    exclusive_percentages = [authors_data[a]['exclusive_percentage'] for a in author_names]
    final_losses = [authors_data[a]['final_loss'] for a in author_names]
    exclusive_counts = [authors_data[a]['exclusive_words'] for a in author_names]

    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']

    # Scatter plot: Vocabulary Exclusivity vs Final Loss
    for i, (author, exclusivity, loss, count) in enumerate(zip(author_names, exclusive_percentages, final_losses, exclusive_counts)):
        ax.scatter(exclusivity, loss, s=800, alpha=0.8, color=colors[i % len(colors)],
                   edgecolors='black', linewidth=2.5, label=author.upper())
        # Annotate with author name and exclusive word count
        ax.annotate(f"{author.upper()}\n({count} exclusive)", (exclusivity, loss), fontsize=11, fontweight='bold',
                    ha='center', va='center')

    ax.set_xlabel('Vocabulary Exclusivity (%)', fontsize=13, fontweight='bold')
    ax.set_ylabel('Final Training Loss', fontsize=13, fontweight='bold')
    ax.set_title('Author Linguistic Distinctiveness vs Model Performance', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='best', fontsize=11)

    plt.tight_layout()

    graphics_dir = os.path.join(path, "models", "graphics")
    os.makedirs(graphics_dir, exist_ok=True)
    plot_path = os.path.join(graphics_dir, "vocab_uniqueness_comparison.png")
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    print(f"Vocabulary uniqueness comparison plot saved: {plot_path}\n")
    plt.close()

plot_multi_author_comparison()
plot_vocab_richness_comparison()


### Function for 1000 Word Text

print("\nSTEP 9: Generating submission text for all authors...\n")

def generate_long_text(model, vectorize_layer, vocabulary, temperature, prompt, min_length=1000):
    """Generate long text using the OneStep model, similar to produce_sample but returns a string"""
    one_step_model = OneStep(model, vectorize_layer, vocabulary, temperature)

    states = None
    next_char = tf.constant([preprocess_text(prompt)])
    result = [prompt]  # Store as strings directly, not TF tensors

    # Generate until we have enough characters
    max_iterations = 2000
    iterations = 0

    while len(postprocess_text(' '.join(result))) < min_length and iterations < max_iterations:
        next_char, states = one_step_model.generate_one_step(next_char, states=states)
        # Extract the generated word as a string
        generated_word = next_char.numpy()[0].decode('utf-8', errors='ignore')
        result.append(generated_word)
        next_char = tf.constant([generated_word])
        iterations += 1

    # Join all words with spaces and postprocess
    generated_text = ' '.join(result)
    final_text = postprocess_text(generated_text)
    return final_text

# Author information for attribution
AUTHOR_INFO = {
    "burroughs": "Edgar Rice Burroughs",
    "baum": "L. Frank Baum",
    "wells": "H.G. Wells"
}