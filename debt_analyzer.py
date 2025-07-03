from utils.gpt_helper import call_llm

def analyze_debt_strategy(user_data):
    debts = user_data["debts"]

    # Choose strategy based on debt structure:
    # If the interest difference is significant, use avalanche; else use snowball
    avg_interest = sum(d["interest"] for d in debts) / len(debts)
    max_interest = max(d["interest"] for d in debts)
    min_interest = min(d["interest"] for d in debts)

    max_amount = max(d["amount"] for d in debts)
    min_amount = min(d["amount"] for d in debts)

    if max_interest - min_interest > 5:  # Interest rate gap is big
        strategy = "avalanche"
        debts = sorted(debts, key=lambda x: x["interest"], reverse=True)
    else:  # Smaller interest differences → psychological wins
        strategy = "snowball"
        debts = sorted(debts, key=lambda x: x["amount"])  # smallest debt first

    top_debt = debts[0]

    strategy_explanation = {
        "avalanche": "Pay off debts starting with the highest interest rate. This reduces the total interest paid.",
        "snowball": "Pay off the smallest debt first to gain motivation, then move to larger ones."
    }[strategy]

    prompt = (
        f"Paraphrase this debt payoff strategy in one sentence. "
        f"Keep it simple, use plain English, and do not add or assume anything:\n"
        f"{strategy_explanation}"
    )

    explanation = call_llm(prompt, model="tinyllama")

    return (
        f"Top priority debt is {top_debt['name']} at "
        f"{top_debt['interest']}% interest and ${top_debt['amount']:.2f} amount. "
        f"Using {strategy.upper()} method.\n\n{explanation.strip()}"
    )
