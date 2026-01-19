
# from backend.rag import rag_response

# ROLE = "finance"

# print("\n🤖 Infosys Internal Chatbot (Terminal)")
# print("Type 'exit' to quit\n")

# while True:
#     query = input("You: ")

#     if query.lower() == "exit":
#         print("Bot: Goodbye 👋")
#         break

#     response = rag_response(query, ROLE)

#     print("\nBot:", response["answer"])

#     if response["sources"]:
#         print("Sources:")
#         for s in response["sources"]:
#             print("-", s)

#     print()


from backend.rag import rag_response

ROLE = "finance"   # change to: hr | finance | engineering | c_level
USER = "terminal"

print("\n🤖 Infosys Internal Chatbot (Terminal)")
print("Type 'exit' to quit\n")

while True:
    query = input("You: ").strip()

    if query.lower() in {"exit", "quit"}:
        print("\nBot: Goodbye! 👋")
        break

    try:
        result = rag_response(query, ROLE, USER)

        print("\nBot:", result["answer"])

        if result["sources"]:
            print("📄 Sources:", ", ".join(result["sources"]))

        print("🔎 Confidence:", result["confidence"])
        print("-" * 50)

    except Exception as e:
        print("❌ Error:", str(e))
        print("-" * 50)
