import json
import os
from modules.debt_analyzer import analyze_debt_strategy
from modules.subscription_checker import analyze_subscriptions

SESSION_FILE = "user_session.json"

def get_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a valid number.")

def get_user_input():
    debts = []
    print("\nEnter debt details:")
    while True:
        name = input("Debt Name (or press Enter to stop): ")
        if not name:
            break
        amount = get_float("Amount: ")
        interest = get_float("Interest Rate (%): ")
        debts.append({"name": name, "amount": amount, "interest": interest})

    subscriptions = []
    print("\nEnter subscription details:")
    while True:
        name = input("Subscription Name (or press Enter to stop): ")
        if not name:
            break
        price = get_float("Price: ")
        last_used = input("Last Used (YYYY-MM-DD): ").strip()
        subscriptions.append({"name": name, "price": price, "last_used": last_used})

    return {"debts": debts, "subscriptions": subscriptions}

def save_session(user_data):
    try:
        with open(SESSION_FILE, "w") as f:
            json.dump(user_data, f, indent=2)
        print(f"\n✅ Session saved to {SESSION_FILE}")
    except Exception as e:
        print(f"❌ Failed to save session: {e}")

def load_session():
    if os.path.exists(SESSION_FILE):
        try:
            with open(SESSION_FILE, "r") as f:
                user_data = json.load(f)
            print(f"\n📂 Loaded session from {SESSION_FILE}")
            return user_data
        except Exception as e:
            print(f"❌ Failed to load session: {e}")
    return None

def main():
    print("📊 Welcome to Debt Advisor AI")
    choice = input("\nDo you want to load previous session? (y/n): ").lower()
    
    if choice == 'y':
        user_data = load_session()
        if not user_data:
            print("⚠️ No valid session found. Starting new input.")
            user_data = get_user_input()
    else:
        user_data = get_user_input()

    print("\n----- DEBT STRATEGY -----")
    print(analyze_debt_strategy(user_data))

    print("\n----- SUBSCRIPTION REVIEW -----")
    print(analyze_subscriptions(user_data))

    save_choice = input("\nDo you want to save this session? (y/n): ").lower()
    if save_choice == 'y':
        save_session(user_data)

if __name__ == "__main__":
    main()
