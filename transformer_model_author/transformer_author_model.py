# Mounting Google Drive
# from google.colab import drive
# drive.mount('/content/drive')

import gc
gc.collect()

# Test prompt
TEST_PROMPT = "The world seemed like such a peaceful place until the magic tree was discovered in London."

# Sources

AUTHORS = {
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

# Globals & Imports

# Globals
BASE_PATH = "Language Model"
BATCH_SIZE = 16
BUFFER_SIZE = 10000
EPOCHS = 20
SEQ_LEN = 256
STRIDE = 256
MAX_GENERATION_LENGTH = 1000

# Import libraries

import os
import time
import random
import re
import numpy as np
import requests
import urllib.request

from tokenizers import Tokenizer, models, pre_tokenizers, trainers
from transformers import PreTrainedTokenizerFast, GPT2Tokenizer
from transformers import DataCollatorForLanguageModeling
from transformers import TrainingArguments
from transformers import Trainer, EarlyStoppingCallback
from transformers import GPT2LMHeadModel

## Functions for downloading text


def download_gutenberg_text(url, output_path):
    """Download text from Project Gutenberg URL."""
    try:
        print(f"Downloading from {url}...")
        urllib.request.urlretrieve(url, output_path)
        print(f"✓ Downloaded to {output_path}")
        return True
    except Exception as e:
        print(f"✗ Failed to download {url}: {e}")
        return False

def clean_gutenberg_text(text):
    """Clean Project Gutenberg header/footer and normalize text."""
    # Remove Project Gutenberg header/footer
    lines = text.split('\n')
    
    # Find start of actual content (after header)
    start_idx = 0
    for i, line in enumerate(lines):
        if '***START' in line.upper() or 'START OF' in line.upper():
            start_idx = i + 1
            break
    
    # Find end of content (before footer)
    end_idx = len(lines)
    for i in range(len(lines) - 1, -1, -1):
        if '***END' in lines[i].upper() or 'END OF' in lines[i].upper():
            end_idx = i
            break
    
    text = '\n'.join(lines[start_idx:end_idx])
    
    # Basic cleaning
    text = re.sub(r'\n\s*\n+', '\n', text)  # Remove extra blank lines
    text = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]', '', text)  # Remove control chars
    
    return text.strip()

def fetch_and_prepare_corpus(author_name, urls):
    """Download and prepare corpus for an author."""
    corpus_dir = os.path.join(BASE_PATH, "corpora")
    os.makedirs(corpus_dir, exist_ok=True)
    
    combined_text = []
    
    for i, url in enumerate(urls):
        file_path = os.path.join(corpus_dir, f"{author_name}_book_{i}.txt")
        
        # Download if not exists
        if not os.path.exists(file_path):
            if not download_gutenberg_text(url, file_path):
                continue
        
        # Read and clean
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
                cleaned = clean_gutenberg_text(text)
                combined_text.append(cleaned)
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    # Save combined corpus
    corpus_path = os.path.join(corpus_dir, f"{author_name}_combined_corpus.txt")
    with open(corpus_path, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(combined_text))
    
    print(f"✓ Combined corpus saved for {author_name}: {corpus_path}")
    return corpus_path

# Tokenizer

def create_tokenizer(author_name, corpus_path):
    """Create or load tokenizer for an author."""
    # Use GPT-2's tokenizer directly (pre-trained and compatible with the model)
    # This avoids tokenization mismatches that cause garbled output
    print(f"Loading GPT-2 tokenizer for {author_name}...")
    
    from transformers import GPT2Tokenizer
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    
    # Set special tokens to match model expectations
    tokenizer.pad_token = tokenizer.eos_token  # Use EOS as PAD
    
    print(f"✓ GPT-2 tokenizer ready for {author_name}")
    return tokenizer

# Data Prep

import torch
from torch.utils.data import Dataset, DataLoader
from torch.nn.utils.rnn import pad_sequence

def chunk_sequence(token_ids, chunk_size=SEQ_LEN, stride=STRIDE):
    """Create overlapping chunks from token sequence."""
    return [
        token_ids[i:i + chunk_size]
        for i in range(0, len(token_ids) - chunk_size + 1, stride)
    ]

class TextDataset(Dataset):
    """PyTorch dataset for text generation."""
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

def prepare_dataset_for_author(author_name, tokenizer, corpus_path):
    """Prepare train/val datasets for an author."""
    print(f"\n{'='*60}")
    print(f"Preparing dataset for {author_name.upper()}")
    print('='*60)
    
    # Read and tokenize corpus
    with open(corpus_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    tokens = tokenizer.encode(text)
    print(f"Total tokens: {len(tokens)}")
    
    # Create chunks
    chunks = chunk_sequence(tokens)
    print(f"Created {len(chunks)} chunks")
    
    # Shuffle and split
    np.random.shuffle(chunks)
    split = int(0.9 * len(chunks))
    train_chunks = chunks[:split]
    val_chunks = chunks[split:]
    
    train_dataset = TextDataset(train_chunks)
    val_dataset = TextDataset(val_chunks)
    
    print(f"Train size: {len(train_dataset)}")
    print(f"Val size: {len(val_dataset)}")
    
    return train_dataset, val_dataset

# Train Model

def train_author_model(author_name, train_dataset, val_dataset, tokenizer):
    """Train a model for a specific author."""
    print(f"\n{'='*60}")
    print(f"Training model for {author_name.upper()}")
    print('='*60)
    
    model_dir = os.path.join(BASE_PATH, "models", author_name)
    os.makedirs(model_dir, exist_ok=True)
    
    model = GPT2LMHeadModel.from_pretrained("gpt2")
    model.resize_token_embeddings(len(tokenizer))

    training_args = TrainingArguments(
        output_dir=model_dir,
        per_device_train_batch_size=BATCH_SIZE,
        gradient_accumulation_steps=1,
        num_train_epochs=EPOCHS,
        eval_strategy="epoch",
        save_strategy="epoch",
        logging_steps=100,
        logging_strategy="steps",
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        greater_is_better=False,
        report_to="none",
        fp16=True,
        dataloader_num_workers=0,  # Set to 0 for Windows compatibility
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
    
    # Save model
    model_save_path = os.path.join(model_dir, "final_model")
    model.save_pretrained(model_save_path)
    tokenizer.save_pretrained(model_save_path)
    print(f"✓ Model saved to {model_save_path}")
    
    return model, tokenizer

# Model


def generate_text(prompt, model, tokenizer, max_length=MAX_GENERATION_LENGTH, temperature=1.0, top_k=50, top_p=0.95):
    """Generate text based on a prompt using a trained model."""
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

# Main Execution

def main():
    """Main training and generation pipeline."""
    os.makedirs(BASE_PATH, exist_ok=True)
    
    results = {}
    
    # Process each author
    for author_name, urls in AUTHORS.items():
        print(f"\n{'#'*60}")
        print(f"# PROCESSING AUTHOR: {author_name.upper()}")
        print(f"{'#'*60}")
        
        # 1. Fetch and prepare corpus
        corpus_path = fetch_and_prepare_corpus(author_name, urls)
        
        # 2. Create/load tokenizer
        tokenizer = create_tokenizer(author_name, corpus_path)
        
        # 3. Prepare datasets
        train_dataset, val_dataset = prepare_dataset_for_author(author_name, tokenizer, corpus_path)
        
        # 4. Train model
        model, tokenizer = train_author_model(author_name, train_dataset, val_dataset, tokenizer)
        
        # 5. Generate text with test prompt
        print(f"\n{'='*60}")
        print(f"Generating text for {author_name.upper()}")
        print('='*60)
        temperature = 0.9
        print(f"Temperature: {temperature}")
        print(f"Prompt: {TEST_PROMPT}\n")
        
        generated = generate_text(TEST_PROMPT, model, tokenizer, temperature=temperature)
        results[author_name] = generated
        
        print(f"Generated Text:\n{generated}\n")
    
    # Save results to file
    output_path = os.path.join(BASE_PATH, "generated_outputs.txt")
    with open(output_path, 'w', encoding='utf-8') as f:
        for author_name, text in results.items():
            f.write(f"\n{'='*60}\n")
            f.write(f"AUTHOR: {author_name.upper()}\n")
            f.write(f"{'='*60}\n")
            f.write(f"Prompt: {TEST_PROMPT}\n\n")
            f.write(f"Generated Text:\n{text}\n")
    
    print(f"\n✓ All results saved to {output_path}")

# Visualization & Graphics

def create_training_visualizations():
    """Create and save visualization graphics for the trained models."""
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    
    # Training metrics data from Colab execution
    training_data = {
        "burroughs": {
            "epochs": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            "train_loss": [3.2146, 3.0619, 2.9678, 2.8901, 2.8191, 2.7671, 2.7115, 2.683, 2.6529, 2.6077, 2.575, 2.539],
            "val_loss": [3.0605, 2.9811, 2.9422, 2.9169, 2.8992, 2.8876, 2.8834, 2.8781, 2.8789, 2.8768, 2.8815, 2.8805],
            "color": "#1f77b4"  # Blue
        },
        "baum": {
            "epochs": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
            "train_loss": [3.3697, 3.1595, 3.0377, 2.9467, 2.8504, 2.7846, 2.7481, 2.7041, 2.654, 2.6196, 2.5822, 2.5413, 2.5282, 2.4958, 2.4753, 2.4655],
            "val_loss": [3.198, 3.0777, 3.014, 2.9758, 2.9487, 2.929, 2.9157, 2.9073, 2.9023, 2.8966, 2.8929, 2.8925, 2.8923, 2.8919, 2.8943, 2.8938],
            "color": "#ff7f0e"  # Orange
        },
        "wells": {
            "epochs": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
            "train_loss": [3.3699, 3.2175, 3.1542, 3.0923, 3.0366, 2.9961, 2.961, 2.9163, 2.8798, 2.8623, 2.838, 2.8085, 2.773],
            "val_loss": [3.2295, 3.1743, 3.1419, 3.1234, 3.1076, 3.098, 3.0948, 3.0916, 3.0889, 3.0885, 3.0856, 3.0879, 3.0912],
            "color": "#2ca02c"  # Green
        }
    }
    
    # Create graphics directory
    graphics_dir = os.path.join(BASE_PATH, "graphics")
    os.makedirs(graphics_dir, exist_ok=True)
    
    # Graphic 1: Individual author training curves
    print("\n📊 Creating Graphic 1: Individual Author Training Curves...")
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    fig.suptitle('Training Progress by Author', fontsize=16, fontweight='bold')
    
    for idx, (author, data) in enumerate(training_data.items()):
        ax = axes[idx]
        ax.plot(data["epochs"], data["train_loss"], marker='o', label='Training Loss', 
                linewidth=2, markersize=6, color=data["color"], alpha=0.7)
        ax.plot(data["epochs"], data["val_loss"], marker='s', label='Validation Loss', 
                linewidth=2, markersize=6, color=data["color"], alpha=1.0, linestyle='--')
        
        ax.set_xlabel('Epoch', fontsize=11)
        ax.set_ylabel('Loss', fontsize=11)
        ax.set_title(f'{author.upper()} ({len(data["epochs"])} epochs)', fontsize=12, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)
        ax.set_ylim(2.4, 3.4)
    
    plt.tight_layout()
    graphic1_path = os.path.join(graphics_dir, "01_training_curves_by_author.png")
    plt.savefig(graphic1_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {graphic1_path}")
    plt.close()
    
    # Graphic 2: Comparison of all authors on same plot
    print("\n📊 Creating Graphic 2: All Authors Validation Loss Comparison...")
    fig, ax = plt.subplots(figsize=(12, 7))
    
    for author, data in training_data.items():
        ax.plot(data["epochs"], data["val_loss"], marker='o', label=author.upper(), 
                linewidth=2.5, markersize=7, color=data["color"])
    
    ax.set_xlabel('Epoch', fontsize=12, fontweight='bold')
    ax.set_ylabel('Validation Loss', fontsize=12, fontweight='bold')
    ax.set_title('Validation Loss Comparison - All Authors', fontsize=14, fontweight='bold')
    ax.legend(fontsize=11, loc='best')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    graphic2_path = os.path.join(graphics_dir, "02_validation_loss_comparison.png")
    plt.savefig(graphic2_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {graphic2_path}")
    plt.close()
    
    # Graphic 3: Loss improvement over training
    print("\n📊 Creating Graphic 3: Loss Improvement Statistics...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('Training Efficiency Analysis', fontsize=14, fontweight='bold')
    
    # Subplot 1: Loss reduction per author
    authors_list = list(training_data.keys())
    initial_losses = [training_data[a]["val_loss"][0] for a in authors_list]
    final_losses = [training_data[a]["val_loss"][-1] for a in authors_list]
    loss_reductions = [initial - final for initial, final in zip(initial_losses, final_losses)]
    
    colors = [training_data[a]["color"] for a in authors_list]
    bars1 = ax1.bar(authors_list, loss_reductions, color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)
    ax1.set_ylabel('Loss Reduction', fontsize=11, fontweight='bold')
    ax1.set_title('Validation Loss Improvement per Author', fontsize=12, fontweight='bold')
    ax1.set_ylim(0, max(loss_reductions) * 1.2)
    
    # Add value labels on bars
    for bar, reduction in zip(bars1, loss_reductions):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{reduction:.3f}', ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # Subplot 2: Epochs completed per author
    epochs_completed = [len(training_data[a]["epochs"]) for a in authors_list]
    bars2 = ax2.bar(authors_list, epochs_completed, color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)
    ax2.set_ylabel('Epochs', fontsize=11, fontweight='bold')
    ax2.set_title('Training Duration (Epochs)', fontsize=12, fontweight='bold')
    ax2.set_ylim(0, 20)
    ax2.axhline(y=20, color='red', linestyle='--', linewidth=2, label='Max Requested (20)')
    ax2.legend(fontsize=10)
    
    # Add value labels on bars
    for bar, epochs in zip(bars2, epochs_completed):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{epochs}', ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    graphic3_path = os.path.join(graphics_dir, "03_loss_improvement_and_epochs.png")
    plt.savefig(graphic3_path, dpi=300, bbox_inches='tight')
    print(f"Saved: {graphic3_path}")
    plt.close()
    
    print("\n" + "="*70)
    print("ALL GRAPHICS CREATED SUCCESSFULLY")
    print("="*70)
    print(f"Graphics saved to: {graphics_dir}")
    print("\nFiles created:")
    print("  1. 01_training_curves_by_author.png")
    print("  2. 02_validation_loss_comparison.png")
    print("  3. 03_loss_improvement_and_epochs.png")
    print("\nUse these for your executive summary!")

if __name__ == "__main__":
    main()