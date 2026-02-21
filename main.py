import os
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

load_dotenv()

# Toggle this later with Stripe
PREMIUM_ENABLED = False

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# -----------------------------
# ANALYSIS ENGINE
# -----------------------------

def calculate_leverage_score(bill_amount, facility_type, insurance_status):
    score = 50

    if bill_amount > 2000:
        score += 15
    if bill_amount > 5000:
        score += 10

    if facility_type == "Hospital":
        score += 10

    if insurance_status == "Uninsured":
        score += 15
    elif insurance_status == "High Deductible":
        score += 8

    return min(score, 95)


def leverage_verdict(score):
    if score >= 75:
        return "STRONG NEGOTIATION OPPORTUNITY", "🟢"
    elif score >= 60:
        return "MODERATE LEVERAGE", "🟡"
    else:
        return "LOW NEGOTIATION LIKELIHOOD", "🔴"


def red_flags(bill_amount, facility_type):
    flags = []
    if facility_type == "Hospital":
        flags.append("Facility fees may be billed separately.")
    if bill_amount > 3000:
        flags.append("High totals often include miscoded or unbundled charges.")
    if bill_amount > 7000:
        flags.append("Large balances frequently qualify for hardship review.")
    return flags


# -----------------------------
# ROUTES
# -----------------------------

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "prefill": {
            "procedure": "",
            "location": "",
            "facility_type": "Hospital",
            "bill_amount": "",
            "insurance_status": "Insured",
        },
        "weekly_hint": 1126
    })


@app.post("/analyze", response_class=HTMLResponse)
async def analyze(
    request: Request,
    procedure: str = Form(...),
    location: str = Form(...),
    facility_type: str = Form(...),
    bill_amount: float = Form(...),
    insurance_status: str = Form(...)
):

    leverage_score = calculate_leverage_score(
        bill_amount, facility_type, insurance_status
    )

    verdict, emoji = leverage_verdict(leverage_score)
    potential_savings = round(bill_amount * (leverage_score / 100) * 0.35)
    flags = red_flags(bill_amount, facility_type)

    call_script = f"""Hi, I’m reviewing my recent bill for {procedure}.
Before making payment, I’d like to request an itemized statement and confirm coding accuracy.
Are there any discounts, prompt-pay reductions, or financial assistance options available?"""

    phase2 = {
        "coding_review": f"I would like a formal coding review for my {procedure}. Can you verify that all CPT and ICD codes accurately reflect services provided?",
        "prompt_pay": "If I can make payment today, are there prompt-pay or administrative discounts available?",
        "self_pay": "If treated as self-pay, what discount structure could apply?"
    }

    phase3 = {
        "supervisor": "I would like to escalate this account to a supervisor for detailed review.",
        "hardship": "I am requesting evaluation for financial assistance or hardship review.",
        "formal_dispute": "Please document this account as under formal billing dispute until review is complete."
    }

    return templates.TemplateResponse("result.html", {
        "request": request,
        "procedure": procedure,
        "potential_savings": potential_savings,
        "verdict": verdict,
        "emoji": emoji,
        "leverage_score": leverage_score,
        "flags": flags,
        "call_script": call_script,
        "phase2": phase2,
        "phase3": phase3,
        "premium": PREMIUM_ENABLED
    })