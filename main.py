"""
File: main.py
Description:
Interactive CLI for the AI Debate Arena.
"""

from dotenv import load_dotenv

load_dotenv()

from src.sdk.sdk import DebateSDK


def print_menu():
    """
    Print system menu.
    """

    print("\n" + "=" * 60)

    print("🤖 AI DEBATE ARENA 🤖")

    print("=" * 60)

    print("1️⃣  Set Debate Topic")
    print("2️⃣  Run Debate")
    print("3️⃣  View Final Verdict")
    print("4️⃣  Exit")

    print("=" * 60)


def main():
    """
    Main CLI loop.
    """

    sdk = DebateSDK()

    while True:

        print_menu()

        choice = input(
            "\nSelect an option (1-4): "
        )

        if choice == "1":

            topic = input(
                "\nEnter debate topic: "
            )

            sdk.configure_debate(topic)

            print("\nTopic saved.")

        elif choice == "2":

            print("\nStarting debate...\n")

            sdk.run_debate()

        elif choice == "3":

            print("\nFinal verdict:\n")

            print(
                sdk.get_final_verdict()
            )

        elif choice == "4":

            print("\nExiting system.")

            break

        else:

            print("\nInvalid option.")


if __name__ == "__main__":

    main()