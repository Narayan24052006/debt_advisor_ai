from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import LoraConfig, get_peft_model
from datasets import load_dataset
import torch

# 1. Load dataset
dataset = load_dataset("json", data_files="/Users/kcsn/Downloads/projects/debt_advisor_ai/data/financial_advisor_dataset.jsonl")
dataset = dataset["train"].train_test_split(test_size=0.1)
dataset = dataset.map(lambda x: {"text": "### Instruction: " + x["instruction"] + "\n### Response: " + x["response"]})

# 2. Load tokenizer and model (no quantization)
model_id = "TinyLLaMA/TinyLLaMA-1.1B-Chat-v1.0"
tokenizer = AutoTokenizer.from_pretrained(model_id, use_fast=True)
tokenizer.padding_side = "right"
model = AutoModelForCausalLM.from_pretrained(model_id)

# 3. Apply LoRA
lora_config = LoraConfig(
    r=16, lora_alpha=32, target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05, bias="none", task_type="CAUSAL_LM"
)
model = get_peft_model(model, lora_config)

# 4. Tokenization
def tokenize_fn(ex):
    result = tokenizer(ex["text"], truncation=True, max_length=512)
    result["labels"] = result["input_ids"]
    return result

tokenized = dataset.map(tokenize_fn, batched=True, remove_columns=["instruction", "response", "text"])
tokenized.set_format("torch")

# 5. Training
from transformers import Trainer, TrainingArguments
training_args = TrainingArguments(
    output_dir="lora_out",
    num_train_epochs=3,
    per_device_train_batch_size=1,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    logging_steps=50,
    save_steps=200,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized["train"],
    eval_dataset=tokenized["test"],
)
trainer.train()

# 6. Save the model
model.save_pretrained("lora_out")
tokenizer.save_pretrained("lora_out")
