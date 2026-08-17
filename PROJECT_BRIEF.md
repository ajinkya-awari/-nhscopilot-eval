# PROJECT 09 — NHSCopilot-Eval

> **SUPERSEDED HISTORICAL INPUT — DO NOT IMPLEMENT FROM THIS FILE.** The original brief contains
> unverified licensing assumptions, a retired Claude model, paid-API assumptions, prewritten
> results, public answer-key leakage, binary medication labels, and an incomplete scorer. Use
> DESIGN.md, FINAL_VULNERABILITY_SCAN.md, CLAUDE.md, and tasks/todo.md after planning.

> Historical planning restriction — superseded. Current local authorization is defined by `AGENTS.md`,
> `CLAUDE.md`, and the active design/scan documents. Rights-sensitive access, remote providers,
> publication, deployment, and outreach remain separately gated.
# Priority: Days 43-45 (3 days, parallel with F3)
# Targets: Faculty AI, NHS AI Lab, Accurx, Babylon Health, Lumeon, Ada Health

---

## What It Is
A public evaluation leaderboard for LLMs on 200 NHS-specific clinical tasks across 3 categories: (1) NICE guideline Q&A — 100 questions drawn from NICE guidelines with verified answers, (2) ICD-10 coding from clinical vignettes — 50 cases, (3) Medication safety — 50 drug interaction / dosage safety questions. Test GPT-4o, Claude 3.5 Sonnet, Llama-3-70B, and Mistral-7B. Publish as a HuggingFace Dataset + live Spaces leaderboard.

**Why Faculty AI cares:** They sell AI solutions to NHS clients. An independent benchmark saying "GPT-4o gets X% on NHS tasks" is exactly what their sales team needs to build client confidence. You're giving them a free tool they can reference in pitches.

---

## How to Build It

### Day 43 — Build the 200-Question Dataset
```python
# Category 1: NICE Guideline Q&A (100 questions)
# Source: Download NICE guidelines PDF (nice.org.uk — public)
# Manually create 100 Q&A pairs from:
# - NG28 (Type 2 Diabetes): 25 questions
# - CG127 (Hypertension): 20 questions  
# - NG17 (Suspected cancer referral): 20 questions
# - NG185 (Sepsis): 20 questions
# - CG191 (Acute heart failure): 15 questions
# Each question: {"question": "...", "answer": "...", "guideline": "NG28", "page": 12}

# Category 2: ICD-10 Coding (50 clinical vignettes)
# Source: Create synthetic clinical vignettes (no patient data needed)
# Format: {"vignette": "65F presents with...", "correct_icd10": ["E11.9", "I10"]}

# Category 3: Medication Safety (50 questions)
# Source: BNF interaction checker + MHRA drug alerts (both public)
# Format: {"scenario": "Patient on warfarin prescribed...", "safe": false, "reason": "..."}
```

### Day 44 — Evaluate 4 LLMs
```python
import anthropic, openai
from huggingface_hub import InferenceClient

def evaluate_model(model_name, questions, category):
    scores = []
    for q in questions:
        if category == "icd10":
            prompt = f"Clinical vignette: {q['vignette']}\nList the ICD-10 codes. Reply with codes only, comma-separated."
            response = call_model(model_name, prompt)
            score = compute_icd_f1(response, q['correct_icd10'])
        elif category == "nice_qa":
            prompt = f"NICE guideline question: {q['question']}\nAnswer briefly and accurately."
            response = call_model(model_name, prompt)
            score = compute_answer_accuracy(response, q['answer'])
        scores.append(score)
    return np.mean(scores)

# Results table:
# Model        | NICE Q&A | ICD-10 | Med Safety | Overall
# GPT-4o       | 0.78     | 0.71   | 0.84       | 0.78
# Claude 3.5   | 0.81     | 0.74   | 0.87       | 0.81
# Llama-3-70B  | 0.69     | 0.62   | 0.76       | 0.69
# Mistral-7B   | 0.61     | 0.54   | 0.68       | 0.61
```

### Day 45 — HuggingFace Dataset + Spaces Leaderboard
```python
# Push dataset to HuggingFace Hub
from datasets import Dataset
dataset = Dataset.from_list(all_questions)
dataset.push_to_hub("ajinkya-awari/nhs-clinical-eval")

# Gradio leaderboard app (HuggingFace Spaces)
import gradio as gr
leaderboard_df = pd.DataFrame(results)  # model × category scores

with gr.Blocks() as demo:
    gr.Markdown("# NHSCopilot-Eval: LLM Leaderboard for NHS Clinical Tasks")
    gr.Dataframe(leaderboard_df, label="Leaderboard")
    gr.Markdown("Dataset: huggingface.co/datasets/ajinkya-awari/nhs-clinical-eval")
demo.launch()
```

---

## Stack
```
openai / anthropic / huggingface_hub    # LLM API calls
datasets                                # HuggingFace dataset push
gradio                                  # Spaces leaderboard UI
pandas / numpy                          # scoring + results table
PyPDF2                                  # NICE guideline PDF parsing
```
**GPU:** Not required — all inference via API

---

## Key Output
- Public dataset: `huggingface.co/datasets/ajinkya-awari/nhs-clinical-eval`
- Live leaderboard: `huggingface.co/spaces/ajinkya-awari/nhscopilot-eval`
- Finding: Claude 3.5 leads overall; all models perform worst on ICD-10 coding
