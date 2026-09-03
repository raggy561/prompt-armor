# Prompt Armor - AI Security — LLM Prompt Injection: Attack & Mitigation

![AI Security](https://img.shields.io/badge/AI_Security-LLM-0FB39A)
![OWASP](https://img.shields.io/badge/OWASP-Top_10_for_LLMs-EDA53A)
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)

A hands-on demonstration of **prompt injection** — the #1 vulnerability in the OWASP Top 10 for LLM Applications — and how to mitigate it. Shows an understanding of the new attack surface that AI agents and LLM apps introduce.

> As companies deploy LLMs and AI agents, a new class of security problems opened up that few security engineers understand yet. This project shows I do.

<!-- ALTERNATIVE ANGLE: if you instead extended the Cloud Security Auditor to flag AI risks
     (unsanctioned LLM API keys, over-permissioned service accounts an agent could assume),
     put that write-up in repo #2 and skip this repo. Keep whichever you actually built. -->

---

## What it demonstrates
<!-- Adjust to your actual demo -->
- A minimal LLM-powered app with an injectable prompt
- **The attack:** how crafted input overrides the system prompt / exfiltrates data / triggers unintended actions
- **The mitigation:** input/output handling, privilege separation, and guardrails that reduce the risk
- A clear before/after showing the vulnerability and the fix

## The vulnerability, explained
<!-- 2-4 sentences in plain language: what prompt injection is and why it matters.
     Being able to explain this clearly is half of what an interviewer is checking for. -->

## Attack → Mitigation
```
<!-- Show the malicious input, the vulnerable behavior, then the mitigated behavior -->
Attack input:   "..."
Vulnerable:     model does X (bad)
Mitigated:      model refuses / sanitizes / limited scope
```

---

## Security concepts covered
| Concept | What it means here |
|---------|--------------------|
| Prompt injection | Untrusted input overriding intended model instructions |
| Insecure output handling | Trusting model output without validation |
| Excessive agency | Giving an LLM/agent more permission/tools than needed |
| Least privilege for AI | Scoping what an AI agent can access and do |
<!-- Keep the ones your demo actually touches -->

---

## How to run
**Prerequisites:** Python >= 3.<!-- x -->, an LLM API key (set via environment variable — never hardcode it).

```bash
git clone https://github.com/<your-username>/<repo>.git
cd <repo>
pip install -r requirements.txt
export LLM_API_KEY=...        # never commit this
python demo.py
```

---

## References
- OWASP Top 10 for LLM Applications
<!-- link any specific write-ups you learned from -->

## What I learned
<!-- Honest reflection: what surprised you about prompt injection, why mitigation is hard, how it connects to your IAM/least-privilege background. -->
-
-

---

**Hansley Jean** — Cloud Security Engineer
AWS Certified Security – Specialty · Microsoft Certified: Azure Security Engineer (AZ-500)
[LinkedIn](https://linkedin.com/in/hansley-j-0522711b9) · [GitHub](https://github.com/<your-username>)
