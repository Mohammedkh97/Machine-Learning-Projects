

### 🌟 What is a Prompt Template?

A **Prompt Template** is a way to define a reusable *text instruction* to the LLM — with **placeholders** (variables) you can fill dynamically.

* It’s like a “mail merge” for AI prompts.
* You write the base prompt once, and at **runtime** you ***insert the specific variables***.

---

### ✅ Why use Prompt Templates?

1️⃣ You **avoid *copy/pasting* prompt** text in code
2️⃣ You can update your prompt in one place
3️⃣ You can pass variables (document text, user query, doc type, etc.)
4️⃣ You can switch between **LLM** and **ChatModel** easily
5️⃣ You can test prompts faster

---

### 🚀 Example 1: String PromptTemplate

```python
from langchain_core.prompts import PromptTemplate

# Define prompt template
prompt_template = PromptTemplate.from_template(
    "Tell me a joke about {topic}"
)

# Fill variable
final_prompt = prompt_template.invoke({"topic": "cats"})

print(final_prompt)
# Output: "Tell me a joke about cats"
```

→ This produces a single **string prompt**
→ Used with simple LLMs (ChatGroq, OpenAI, Claude...)

---

### 🚀 Example 2: ChatPromptTemplate (multi-message)

```python
from langchain_core.prompts import ChatPromptTemplate

prompt_template = ChatPromptTemplate([
    ("system", "You are a helpful assistant"),
    ("user", "Tell me a joke about {topic}")
])

# Fill variable
final_prompt = prompt_template.invoke({"topic": "cats"})
```

This produces a list of **two messages**:

1. System message
2. User message with filled `{topic}`

**Why use ChatPromptTemplate?**

* Many LLMs (like GPT-4o, Groq) work better with multi-message chat
* You can separate **system instructions** from **user queries**

---

### 🚀 Example 3: MessagesPlaceholder (for dynamic conversation)

```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage

prompt_template = ChatPromptTemplate([
    ("system", "You are a helpful assistant"),
    MessagesPlaceholder("msgs")
])

final_prompt = prompt_template.invoke({
    "msgs": [HumanMessage(content="hi!")]
})
```

**MessagesPlaceholder** lets you insert a *list of messages* (ex: chat history, memory).
This is great for **chatbots** and **multi-turn conversation**.

---

### 💡 In your case (Document Extraction)

Here’s the PromptTemplate I'm using:

```python
template = """
You are an expert document parser.

Document types you know:
- Passport
- Visa - [Tourism or Employment]
- Change Status
- Employment Contract
- Residence
- Healthcare

Based on this document content, first decide the document type, then extract fields as structured JSON using the correct schema.

Return only the final JSON. Do not explain.

Document content:
-------------------
{document_text}
-------------------
"""
```

---

When you do:

```python
prompt = PromptTemplate.from_template(template)
final_prompt = prompt.format(document_text=document_text)
```

You’re building a **specific prompt per PDF**, by injecting the `document_text`.
So the LLM sees:

```txt
You are an expert document parser.
...
Document content:
-------------------
{actual PDF text here}
-------------------
```

---

### ⚠️ Important Notes

1️⃣ **PromptTemplates help organize your prompt logic**
2️⃣ They support variables → you can dynamically insert text
3️⃣ You can switch between **PromptTemplate** (string) and **ChatPromptTemplate** (messages) easily
4️⃣ **PromptValue** object helps you pass the result directly to LLM or ChatModel without reformatting

---

### 🎁 Summary:

| Type                  | Used for                                       |
| --------------------- | ---------------------------------------------- |
| `PromptTemplate`      | Simple string prompts                          |
| `ChatPromptTemplate`  | Multi-message prompts (system + user + others) |
| `MessagesPlaceholder` | Inserting history of messages                  |
| Output: `PromptValue` | You can pass this to LLM or ChatModel          |

---

### 🚀 In my current project:

The recommended approach is using **ChatPromptTemplate**, because:

✅ You can define a clear system message → "You are an expert document parser"
✅ You can insert `document_text` as user message
✅ The LLM will perform better (most chat LLMs prefer multi-message chat)
