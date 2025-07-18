from django.shortcuts import render
# from .rag import run_rag  # We'll create this next


def chat_view(request):
    answer = ""
    question = ""

    # if request.method == "POST":
    #     question = request.POST.get("question")
    #     if question:
    #         answer = run_rag(question)

    return render(
        request,
        "chatbot/chat.html",
        {
            "question": question,
            "answer": answer,
        },
    )
