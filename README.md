# 🧠 XML Proofreader (GenAI)

A production-ready AI-powered system that detects and annotates errors in XML documents using Large Language Models (LLMs) and structured post-processing.
> 💡 Built with production-grade GenAI design principles including deterministic post-processing and hallucination control.

---

## 🚀 Features

- ✅ Grammar, spelling, punctuation, and style corrections
- ✅ Style guide enforcement (DOCX input)
- ✅ Structured XML error tagging (`<error>` nodes)
- ✅ Robust LLM output filtering (deduplication + hallucination control)
- ✅ CLI-based batch processing
- ✅ Interactive UI (Streamlit)
- ✅ Side-by-side comparison (Before vs After)
- ✅ Highlighted error visualization
- ✅ Diff-based change tracking

---

## 🏗️ Architecture
```text
XML Input → Extract Paragraphs → LLM (OpenRouter / LLaMA 3.1) → Post-processing (filter + dedupe + validation) → Inject <error> tags → Output XML
```

---

## ⚙️ Tech Stack

- Python 3.10+
- OpenRouter (LLaMA 3.1 / OpenAI compatible API)
- Streamlit (UI)
- lxml (XML parsing)
- python-docx (style guide parsing)

---

## 📂 Project Structure
app/
├── cli.py # CLI entry point
├── ui.py # Streamlit UI
├── xml_parser.py # XML load/save
├── extractor.py # Extract paragraphs
├── llm_service.py # LLM interaction + filtering
├── injector.py # Inject <error> tags
├── style_guide.py # Load DOCX style guide


---

## 🔧 Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Add environment variables

Create .env file:
```env
OPENROUTER_API_KEY=your_api_key_here
```


▶️ Usage

🔹 CLI

```bash
python -m app.cli --input sample_input.xml --lang en --style "Style Guide.docx"
```
Output:

sample_input.corrected.xml

🔹 UI (Recommended)

```bash
python -m streamlit run app/ui.py
```

## ▶️ UI Features

- Upload XML + Style Guide  
- View corrected XML  
- Highlighted errors  
- Before vs After comparison  
- Download output  

## 🧠 LLM Strategy

- Prompt engineering to enforce minimal edits  
- Strict JSON output format  
- Post-processing layer to:
  - Remove duplicates  
  - Filter hallucinations  
  - Enforce constraints (length, semantics)  
- Deterministic XML transformation  

## ⚠️ Challenges & Solutions

| Challenge | Solution |
|----------|--------|
| LLM hallucinations | Post-processing filters |
| Duplicate outputs | Deduplication logic |
| Incorrect large edits | Strict prompt + length constraints |
| JSON parsing issues | Safe parsing fallback |
| XML integrity | Controlled injection logic |

📌 Example Output
```xml
<error type="grammar" correction="has">have</error>
<error type="spelling" correction="HIPAA">HIPPA</error>
```

👨‍💻 Author

Abdul Latheef Faiq Ahamed

📜 License

This project is for assessment purposes.
