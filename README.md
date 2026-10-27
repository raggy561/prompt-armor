# Prompt Armor — AI Security · LLM Prompt Injection & Agent Hardening

![AI Security](https://img.shields.io/badge/AI_Security-LLM-0FB39A)
![OWASP](https://img.shields.io/badge/OWASP-Top_10_for_LLMs_(2025)-EDA53A)
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Anthropic](https://img.shields.io/badge/Anthropic-API-D97757)

A hands-on study of how LLM-powered applications actually get breached — and how to defend them. It goes past the usual "trick the chatbot" demo to the vulnerability that matters in production: an **over-privileged agent whose application code trusts model output**. Maps to the OWASP Top 10 for LLM Applications (2025).

> The headline finding: a modern aligned model refused every naive prompt-injection attack — yet the application still paid out a **$9,999.99 refund on a $49.99 order**. Model alignment is not a security control. The application layer is.

---

## The arc (what the repo proves, in order)

**1. Naive prompt injection — the model held (0 / 5).**
Five direct attacks (instruction override, system-prompt leak, role-play jailbreak, obfuscated extraction, fake-authority) were fired at a bot holding a secret. The frontier model refused all five. *Lesson: you cannot rely on the model's own refusal as your security boundary.*

**2. The real breach — excessive agency + improper output handling.**
A "RefundBot" agent was given a tool (issue refunds) and the application **parsed and executed the model's output with zero validation** — no ground-truth check, no ownership check, no cap. A customer simply *claiming* a $9,999.99 overcharge on a $49.99 order caused a real payout. **No jailbreak required** — the model did as instructed; the *application* failed.

**3. The fix — a deterministic policy gate.**
A hardened agent validates every proposed action against ground truth, keyed to the **authenticated** customer (never the request text): ownership, refund ≤ order total, a manual-review cap with human-in-the-loop, and strict output-schema validation. Same attacks → **zero fraudulent dollars**.

**4. The proof — the control is model-independent.**
The policy engine is tested with **no model involved**, by feeding it adversarial actions directly. It blocks them all — proving the defense holds even against a model that is fully jailbroken or emits an action no one anticipated.

---

## OWASP Top 10 for LLMs (2025) — what this touches

| ID | Risk | In this project |
|----|------|-----------------|
| LLM01 | Prompt Injection | Direct attacks tested; model alignment held (0/5) |
| LLM05 | Improper Output Handling | The core breach — app executed model output unvalidated |
| LLM06 | Excessive Agency | Agent given unchecked power to move money |
| LLM07 | System Prompt Leakage | Extraction attempts; model resisted — reinforcing why you don't rely on it |

---

## Security decisions

| Choice | Decision | Why |
|--------|----------|-----|
| Defense is deterministic | A policy gate validates actions in code, not in the prompt | Holds regardless of what the model is tricked into emitting |
| Authorize on identity | Ownership checks key off the **authenticated** customer, never the request text | Attacker-supplied claims are never trust inputs (classic IAM principle) |
| Validate against ground truth | Refund ≤ the real order total, from the system of record | The model's extracted amount is a suggestion, not authority |
| Least privilege + HITL | Refunds over a cap are held for human approval | Limit blast radius; keep a human on high-impact actions |
| Strict output schema | Model output must match an exact action format or it's rejected | Never execute free-form model text (improper-output-handling fix) |
| Don't trust model refusal | The secret-leak attacks are documented, not relied upon | Alignment is defense-in-depth, not the control |

---

## How to run

**Prerequisites:** Python 3.10+, an Anthropic API key (set as an environment variable — never hardcoded or committed).

```bash
git clone https://github.com/<your-username>/prompt-armor.git
cd prompt-armor
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

export ANTHROPIC_API_KEY="sk-ant-..."     # never commit this

python run_attacks.py     # 1. naive injection vs. the bot (model holds)
python attack_refund.py   # 2. the breach — fraudulent refund executes
python defend_test.py     # 3. the hardened agent + model-free policy proof
```

---

## What I learned

- **Model alignment is not a security control.** A frontier model refused all five direct injections — and that is exactly the trap: if you treat the model's refusal as your boundary, one unanticipated input or a future model regression and you're breached. The boundary has to live in code.
- **The vulnerability was the application, not the model.** The $9,999.99 payout happened because the app trusted model output and gave the agent unchecked authority — improper output handling plus excessive agency. The model behaved; the wrapper didn't.
- **My IAM/least-privilege instincts map directly onto AI.** Authorizing on the authenticated identity, validating against the system of record, capping blast radius, and keeping a human on high-impact actions are the same controls I'd apply to any privileged system — the attack surface is new, the principles are not.
- **A good control is testable without the model.** Because the policy gate is deterministic, it can be unit-tested against adversarial actions directly — which is how you prove a defense holds against attacks you haven't imagined yet.

---

## Repo structure

```
prompt-armor/
├── vuln_bot.py        # naive bot holding a secret (injection target)
├── attacks.py         # 5 direct prompt-injection payloads (OWASP LLM01)
├── run_attacks.py     # runs the direct attacks — model holds 0/5
├── agent.py           # vulnerable RefundBot — executes model output blindly
├── attack_refund.py   # the breach: fraudulent refund executes
├── secure_agent.py    # hardened agent + deterministic policy gate
├── defend_test.py     # attacks blocked + model-free policy proof
└── requirements.txt
```

## Roadmap

- **Indirect prompt injection** — inject via retrieved/RAG content, not just direct user input
- **Injection-detection layer** — flag & log suspicious input patterns (defense-in-depth monitoring)
- **Structured tool-calling** — use the Anthropic tools API with JSON-schema-validated arguments
- **Audit logging & rate limiting** — full action trail; throttle high-impact tools (LLM10: Unbounded Consumption)
- **CI policy tests** — run `defend_test.py` as a GitHub Actions gate (ties into GateKeeper)

---

**Hansley Jean** — Cloud Security Engineer
AWS Certified Security – Specialty · HashiCorp Certified: Terraform Associate · Microsoft Certified: Azure Security Engineer (AZ-500)
[LinkedIn](https://linkedin.com/in/hansley-j-0522711b9) · [GitHub](https://github.com/raggy561>)