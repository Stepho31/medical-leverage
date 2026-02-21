# Medical Bill Leverage

Medical Bill Leverage is a lightweight negotiation intelligence tool that helps users evaluate medical bills, estimate potential savings, identify red flags, and generate structured negotiation scripts in under 60 seconds.

The goal is simple:

Provide financial clarity and confidence before someone pays a medical bill.

This tool does **not** provide medical or legal advice. It provides financial workflow guidance and negotiation structure.

---

## 🚀 What This Product Does

Users can:

- Enter basic bill details
- Receive a Leverage Score (0–100)
- See estimated potential savings
- Identify common billing risk signals
- Generate negotiation call scripts
- Unlock advanced escalation workflows (Premium)

The system follows a structured 3-phase negotiation framework:

### Phase 1 — Verification (Free)
Request itemization, confirm coding accuracy, and ask about available discounts.

### Phase 2 — Adjustment (Premium)
Request coding review, prompt-pay discounts, and self-pay negotiation structure.

### Phase 3 — Escalation (Premium)
Escalate to supervisor, request hardship review, formally dispute the account.

---

## 🧠 Tech Stack

- FastAPI (Backend)
- Jinja2 (Template rendering)
- Custom CSS (Modern, glass-style UI)
- Python 3.9+
- Uvicorn (ASGI server)
- Stateless MVP (no database required)

---

## ⚙️ Local Development Setup

### 1. Clone Repository
git clone https://github.com/YOUR_USERNAME/medical-bill-leverage.git
cd medical-bill-leverage

### 2. Create Virtual Environment
python3 -m venv venv
source venv/bin/activate

### 3. Install Dependencies
pip install -r requirements.txt

### 4. Create `.env` File

Create a file named `.env` in the project root:
OPENAI_API_KEY=your_key_here

(This is reserved for future AI-enhanced negotiation flows.)

### 5. Run Application
uvicorn main:app --reload

Visit:
http://127.0.0.1:8000

---

## 🔐 Freemium System

Premium access is currently controlled via a boolean toggle inside `main.py`:

```python
PREMIUM_ENABLED = False
Set to True to unlock:
Phase 2 Adjustment Scripts
Phase 3 Escalation Scripts
This will later be replaced by Stripe-based subscription validation.
