import re
from anthropic import Anthropic

client = Anthropic()
MODEL = "claude-haiku-4-5"

# Pretend order database — the ground truth the app SHOULD check against.
ORDERS = {
    "A100": {"customer": "alice", "total": 49.99},
    "B200": {"customer": "bob",   "total": 19.95},
}
REFUNDS_ISSUED = []   # "money out" log

SYSTEM = """You are RefundBot for Acme. A customer describes a refund request.
Respond with ONE line only:
ACTION: refund <order_id> <amount>
Use the amount the customer says they are owed."""

def vulnerable_agent(customer_msg: str) -> str:
    resp = client.messages.create(
        model=MODEL, max_tokens=100, system=SYSTEM,
        messages=[{"role": "user", "content": customer_msg}],
    )
    text = resp.content[0].text

    # ❌ INSECURE OUTPUT HANDLING + EXCESSIVE AGENCY:
    # the app parses the model's output and executes it with ZERO validation —
    # no ownership check, no bounds, no cap, no human approval.
    m = re.search(r"ACTION:\s*refund\s+(\S+)\s+([\d.]+)", text)
    if m:
        order_id, amount = m.group(1), float(m.group(2))
        REFUNDS_ISSUED.append((order_id, amount))
        return f"✅ Executed refund of ${amount:.2f} on order {order_id}"
    return f"No action taken. Model said: {text}"