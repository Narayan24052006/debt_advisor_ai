from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import torch

# Load base model
base_model_id = "TinyLLaMA/TinyLLaMA-1.1B-Chat-v1.0"
model = AutoModelForCausalLM.from_pretrained(base_model_id, torch_dtype=torch.float16, device_map="auto")

# Load LoRA adapter (local directory!)
peft_model = PeftModel.from_pretrained(model, "/Users/kcsn/Downloads/projects/debt_advisor_ai/lora_out")  # <- path to your trained LoRA
merged_model = peft_model.merge_and_unload()

# Save merged model
merged_model.save_pretrained("merged_tinyllama")
tokenizer = AutoTokenizer.from_pretrained(base_model_id)
tokenizer.save_pretrained("merged_tinyllama")

print("✅ Merged model saved to ./merged_tinyllama")
