# 💸 Debt Advisor AI

An AI-powered offline assistant that suggests optimal debt payoff strategies and reviews active subscriptions using a local TinyLLaMA model combined with rule-based logic. Built for privacy and portability — no API or internet required.

---

## 🔍 Features

* 📊 Recommends Avalanche or Snowball payoff method
* 🔍 Detects duplicate and unused subscriptions
* 💬 Natural language advice using local LLM (TinyLLaMA)
* 🔐 Fully offline and private
* 💾 Save/load user sessions as JSON

---

## 🧠 Powered By

* **TinyLLaMA** via [Ollama](https://ollama.com)
* Fine-tuning with **LoRA** and **Transformers**
* Optional self-training with custom financial dataset

---

## 📁 Project Structure

```bash
debt_advisor_ai/
├── main.py                    # Interactive CLI tool
├── train_lora.py              # Fine-tune TinyLLaMA with custom data
├── merge_model.py            # Merge LoRA with base model
├── requirements.txt
├── run_guide.md              # Step-by-step instructions
├── data/
│   └── financial_advisor_dataset.jsonl
├── lora_out/                 # LoRA training output
├── merged_tinyllama/         # Final usable model after merge
├── modules/
│   ├── debt_analyzer.py      # Strategy logic + LLM prompt
│   └── subscription_checker.py  # Checks duplicates/inactivity + LLM
├── utils/
│   └── gpt_helper.py         # LLM wrapper (Ollama/local)
```

---

## 🚀 How to Run

1. ✅ Install dependencies

```bash
pip install -r requirements.txt
```

2. 🔁 Start Ollama and load the model

```bash
ollama run tinyllama
```

3. ▶️ Run the application

```bash
python main.py
```

---

## 🧪 Optional: Train Your Own Model

Customize your own LLM for domain-specific responses:

1. Add training samples to `data/financial_advisor_dataset.jsonl`
2. Run training

```bash
python train_lora.py
```

3. Merge the model

```bash
python merge_model.py
```

The final model will be saved in `merged_tinyllama/`.

---

## 📦 Example Output

```text
----- DEBT STRATEGY -----
Top interest debt is credit card a at 20%. Using avalanche method.
Focus on paying down high-interest debt first to reduce overall interest.

----- SUBSCRIPTION REVIEW -----
Found 0 duplicates and 1 unused subscriptions.
Consider cancelling your Netflix subscription to reduce unnecessary spending.
```

---

## 🛡 License

MIT License — free for personal or commercial use.

---

## 🙋 Need Help?

Use `run_guide.md` for full execution steps. Pull requests and contributions welcome!

---

Built with ❤️ by Narayan using open-source LLMs and logic rules.
