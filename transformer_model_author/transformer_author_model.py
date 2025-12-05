# Mounting Google Drive
# from google.colab import drive
# drive.mount('/content/drive')

import gc
import tensorflow as tf
gc.collect()
tf.keras.backend.clear_session()

# prompts = [
#     "The caretaker knew the creatures weren’t bound by the treaties anymore.",
#     "The artifact glowed only when touched by someone who’d sworn to protect magical beings.",
#     "She fed the shadows without realizing she’d been feeding memories.",
#     "The sanctuary gates opened for the first time in over a century — and not from the inside.",
#     "The dragons once guarded balance. Now, they hungered for it.",

#     "In the fifth realm, creation wasn’t magic — it was rebellion.",
#     "He shaped illusions as armor, but the real battle was remembering who he was.",
#     "They entered the kingdom through a thought, not a door.",
#     "Each realm had rules. She was born to break all of them.",
#     "His talent wasn’t rare here. It was forbidden everywhere else.",

#     "A word spoken backwards unraveled the spell holding time in place.",
#     "They thought the oracle was a myth until it answered a question they hadn’t asked.",
#     "Crossing realms was easy. Coming back was what hurt.",
#     "The truth wasn’t hidden in riddles — it was the riddle.",
#     "He wasn’t summoned — he was forgotten. That’s why it worked.",

#     "The book didn’t need to be read — it read you.",
#     "She made the mistake of telling the creature her name.",
#     "Not all doors are meant to be opened — some are meant to open themselves.",
#     "The magic wasn’t in the spell. It was in who dared to cast it.",
#     "Rules were written in invisible ink — and he was starting to see them."
# ]

prompts = [
    "<|stormlight|> Kaladin reached for the Stormlight, letting it surge through his veins as the highstorm howled above.",
    "<|stormlight|> Shallan's illusions flickered as the truth she feared most whispered through the chasm darkness.",
    "<|stormlight|> Dalinar stood before the shattered plains, Oathbringer in hand, preparing to speak the Words once more.",

    "<|reckoners|> Steelheart's shadow loomed over the city, but David raised his weapon with defiant resolve.",
    "<|reckoners|> The explosion rocked the hideout, and Megan vanished before anyone could ask how.",
    "<|reckoners|> Prof’s eyes glowed with Epic power as he stepped into the ruins, silence hanging thick.",

    "<|mistborn|> Vin launched into the mists, coins flaring beneath her as she soared over Luthadel's rooftops.",
    "<|mistborn|> Waxillium holstered his pistol, scanning the ballroom for signs of Allomantic disturbances.",
    "<|mistborn|> The ash fell steadily as Kelsier smiled — a rebellion always begins with one spark.",

    "<|skyward|> Spensa's cockpit shuddered as M-Bot spiraled into the debris field, enemy ships closing fast.",
    "<|skyward|> The Krell formation shifted on her radar — and she grinned. \"Time to be a little bit insane.\"",
    "<|skyward|> Jorgen’s grav-cap flickered, but he kept flying. Leadership wasn't just about being in control.",

    "<|standalone|> Raoden traced a glowing glyph on the wall, hope stirring as the Aon finally shimmered with power.",
    "<|standalone|> Lightsong rolled his eyes, lounging on his throne of color, while outside, war whispered through the petals.",
    "<|standalone|> Hoid cleared his throat. \"Now, where were we? Ah yes — the part where everything goes wrong.\""
]

# Globals
# BASE_PATH = "/content/drive/My Drive/Language Model"
BASE_PATH = "Language Model"
MODEL_CHOICE = 3
MODEL_OPTION = 1
AUTHOR = 1
BATCH_SIZE = 16 # 256 for character
BUFFER_SIZE = 10000
EPOCHS = 50
embedding_dim = 512
rnn_units = 1024
seq_length = 100
SEQ_LEN = 256
STRIDE = 256

# Imports
import os
import time
import random
import re
import numpy as np
import spacy

nlp = spacy.load("en_core_web_sm")

from tokenizers import Tokenizer, models, pre_tokenizers, trainers
from transformers import PreTrainedTokenizerFast
from transformers import DataCollatorForLanguageModeling
from transformers import TrainingArguments
from transformers import Trainer, EarlyStoppingCallback
from transformers import GPT2LMHeadModel

# Tokenizer
if MODEL_CHOICE == 2:
    tokenizer = PreTrainedTokenizerFast(
        tokenizer_file=os.path.join(BASE_PATH, f'tokenizer{AUTHOR}'),
        pad_token="<pad>",
        bos_token="<s>",
        eos_token="</s>",
        additional_special_tokens=[
            "<|series|>", "<|book|>", "<|book_start|>", "<|book_end|>",
            "<|sentence_start|>", "<|sentence_end|>"
        ]
    )

    special_series_tokens = [
        "<|stormlight|>",
        "<|reckoners|>",
        "<|mistborn|>",
        "<|skyward|>",
        "<|standalone|>"
    ]

    tokenizer.add_special_tokens({
        "additional_special_tokens": special_series_tokens
    })

    series_token_ids = {
        "stormlight": tokenizer.convert_tokens_to_ids("<|stormlight|>"),
        "reckoners": tokenizer.convert_tokens_to_ids("<|reckoners|>"),
        "mistborn": tokenizer.convert_tokens_to_ids("<|mistborn|>"),
        "skyward": tokenizer.convert_tokens_to_ids("<|skyward|>"),
        "standalone": tokenizer.convert_tokens_to_ids("<|standalone|>"),
    }

    book_to_series = {
        0: "skyward",       # Skyward
        1: "skyward",       # Starsight
        2: "mistborn",      # Arcanum Unbounded: The Cosmere Collection
        3: "mistborn",      # Mistborn Era 1 - The Final Empire
        4: "mistborn",      # The Well of Ascension
        5: "mistborn",      # The Hero of Ages
        6: "mistborn",      # The Alloy of Law
        7: "mistborn",      # Shadows of Self
        8: "mistborn",      # The Bands of Mourning
        9: "mistborn",      # Mistborn Secret History
        10: "standalone",   # Elantris
        11: "standalone",   # Warbreaker
        12: "stormlight",   # The Way of Kings
        13: "stormlight",   # Words of Radiance
        14: "stormlight",   # Edgedancer
        15: "stormlight",   # Oathbringer
        16: "stormlight",   # Dawnshard
        17: "stormlight",   # Rhythm of War
        18: "reckoners",    # Steelheart
        19: "reckoners",    # Firefight
        20: "reckoners",    # Calamity
    }

# Prepare Data
if MODEL_CHOICE == 2:
    import torch
    from torch.utils.data import Dataset, DataLoader
    from torch.nn.utils.rnn import pad_sequence

    def chunk_sequence(token_ids, chunk_size=SEQ_LEN, stride=STRIDE):
        return [
            token_ids[i:i + chunk_size]
            for i in range(0, len(token_ids) - chunk_size + 1, stride)
        ]

    class TextDataset(Dataset):
        def __init__(self, chunks):
            self.examples = []
            for chunk in chunks:
                input_ids = torch.tensor(chunk[:-1], dtype=torch.long)
                labels = torch.tensor(chunk[1:], dtype=torch.long)
                self.examples.append({
                    "input_ids": input_ids,
                    "labels": labels
                })

        def __len__(self):
            return len(self.examples)

        def __getitem__(self, idx):
            return self.examples[idx]

    # === Read the file ===
    with open(os.path.join(BASE_PATH, f'corpus{AUTHOR}_cleaned.txt'), encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    # === Parse and tokenize book blocks ===
    current_book_index = -1
    book_lines = []
    tokenized_chunks = []

    def process_book(book_lines, book_index):
        if book_index not in book_to_series:
            return []

        # Prepend series token
        series = book_to_series[book_index]
        series_token = f"<|{series}|>"
        full_text = f"{series_token} " + " ".join(book_lines)
        tokens = tokenizer.encode(full_text)
        print(f"Encoded {len(tokens)} tokens for book {book_index} (series: {series})")
        chunks = chunk_sequence(tokens)
        print(f"Produced {len(chunks)} chunks")
        return chunks

    for line in lines:
        if line.startswith("<|book|>"):
            print(f"Found <|book|> token, current_book_index={current_book_index}")
            # Process previous book
            if book_lines:
                tokenized_chunks.extend(process_book(book_lines, current_book_index))
            current_book_index += 1
            book_lines = []
        else:
            book_lines.append(line)

    # Final book
    if book_lines:
        tokenized_chunks.extend(process_book(book_lines, current_book_index))

    # === Shuffle and split ===
    np.random.shuffle(tokenized_chunks)
    split = int(0.9 * len(tokenized_chunks))
    train_dataset = TextDataset(tokenized_chunks[:split])
    val_dataset = TextDataset(tokenized_chunks[split:])

    print()
    print(f"Train size: {len(train_dataset)}")
    print(f"Val size: {len(val_dataset)}")

# Build Model
if MODEL_CHOICE == 2:
    model = GPT2LMHeadModel.from_pretrained("gpt2")
    model.resize_token_embeddings(len(tokenizer))

    training_args = TrainingArguments(
        output_dir=BASE_PATH + "/transfer_model_test",
        per_device_train_batch_size=16,
        gradient_accumulation_steps=1,
        num_train_epochs=6,
        eval_strategy="epoch",
        save_strategy="epoch",
        # save_steps=1000,
        logging_steps=1000,
        logging_strategy="steps",
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        greater_is_better=False,
        report_to="none",
        fp16=True,
        dataloader_num_workers=8
    )

    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        data_collator=data_collator,
        processing_class=tokenizer,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=2)]
    )

    trainer.train()

# Save off model
if MODEL_CHOICE == 2:
    model.save_pretrained(BASE_PATH + "/transfer_model")
    tokenizer.save_pretrained(BASE_PATH + "/transfer_model")

# Generate Text Function
def generate_text(prompt, model, tokenizer, max_length=100, temperature=1.0, top_k=50, top_p=0.95):
    # Set device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.eval()
    if next(model.parameters()).device != device:
        model.to(device)

    # Tokenize input
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(device)

    with torch.no_grad():
        output_ids = model.generate(
            input_ids=input_ids,
            max_new_tokens=max_length,
            do_sample=True,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id
        )

    # Decode and return result
    return tokenizer.decode(output_ids[0], skip_special_tokens=True)

# Prompts
if MODEL_CHOICE == 2:
  for prompt in prompts:
      temperature = round(random.uniform(0.8, 1.2), 2)
      print(f"\n{'='*60}")
      print(f"🧠 Temperature: {temperature}")
      print(f"💬 Prompt: {repr(prompt)}\n")

      generated = generate_text(prompt, model, tokenizer, temperature=temperature)
      print(f"📝 Generated Text:\n{generated}")