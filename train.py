import pandas as pd
from transliterate import translit
from datasets import Dataset
from transformers import (
    T5ForConditionalGeneration,
    T5TokenizerFast,
    DataCollatorForSeq2Seq,
    Seq2SeqTrainingArguments,
    Seq2SeqTrainer
)

# 1. Read your OCR output
df = pd.read_csv("ocr_output.csv")  # columns: cutout_path, cyrillic_text

# 2. Ensure there's no NaN in 'cyrillic_text'
df['cyrillic_text'] = df['cyrillic_text'].fillna("")  # replace NaN with empty string

# 3. Build source/target pairs
def make_pair(row):
    src = str(row["cyrillic_text"])
    # transliterate to Latin ('' → '')
    tgt = translit(src, "ru", reversed=True)
    return {"source": src, "target": tgt}

pairs = [make_pair(r) for _, r in df.iterrows()]
ds = Dataset.from_list(pairs)

# 4. Load T5 tokenizer & model
model_name = "t5-small"
tokenizer = T5TokenizerFast.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

# 5. Tokenization function
max_len = 128
def tokenize_batch(batch):
    inputs = tokenizer(
        ["transliterate: " + s for s in batch["source"]],
        max_length=max_len,
        truncation=True,
        padding="max_length"
    )
    targets = tokenizer(
        batch["target"],
        max_length=max_len,
        truncation=True,
        padding="max_length"
    )
    batch["input_ids"] = inputs.input_ids
    batch["attention_mask"] = inputs.attention_mask
    batch["labels"] = targets.input_ids
    return batch

# Map & drop the two columns you do have
tokenized = ds.map(
    tokenize_batch,
    batched=True,
    remove_columns=["source", "target"]
)

# 6. Prepare Trainer
data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)
training_args = Seq2SeqTrainingArguments(
    output_dir="t5_translit_finetuned",
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    predict_with_generate=True,
    logging_steps=50,
    eval_steps=200,
    save_steps=500,
    num_train_epochs=3,
    learning_rate=3e-4,
    weight_decay=0.01,
    evaluation_strategy="steps",
    save_total_limit=2,
)

# split off 10% for eval
split = tokenized.train_test_split(test_size=0.1)

trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=split["train"],
    eval_dataset=split["test"],
    tokenizer=tokenizer,
    data_collator=data_collator,
)

# 7. Train!
trainer.train()
