from utils.gpt_helper import call_llm
from datetime import datetime

def check_subscription_issues(subscriptions):
    seen = {}
    duplicates = []
    unused = []

    for sub in subscriptions:
        key = sub['name']
        if key in seen:
            duplicates.append(sub)
        else:
            seen[key] = sub

        last_used_date = datetime.strptime(sub["last_used"], "%Y-%m-%d")
        days_unused = (datetime.now() - last_used_date).days
        if days_unused > 99:
            unused.append(sub)

    return duplicates, unused

def analyze_subscriptions(user_data):
    subscriptions = user_data.get("subscriptions", [])
    duplicates, unused = check_subscription_issues(subscriptions)

    summary = f"Found {len(duplicates)} duplicates and {len(unused)} unused subscriptions.\n"

    cancel_suggestions = []

    if duplicates:
        cancel_suggestions.append(
            f"Consider canceling one of the duplicate subscriptions to {duplicates[0]['name']}."
        )

    if unused:
        for item in unused:
            cancel_suggestions.append(
                f"The subscription to {item['name']} hasn't been used since {item['last_used']}, so consider canceling it."
            )

    rules_summary = " ".join(cancel_suggestions)
    prompt = (
    f"Turn this subscription advice into one short, polite English sentence. "
    f"Use only the information shown — do not add dates, services, or assumptions:\n"
    f"{rules_summary}"
)

    advice = call_llm(prompt, model="tinyllama")

    return summary + "\n" + advice.strip()