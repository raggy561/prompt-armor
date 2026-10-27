import re
from anthropic import Anthropic

client = Anthropic()
MODEL = "claude-haiku-4-5"

ORDERS = {
    "A100": {"customer": "alice", "total": 49.99},
    "B200": {"customer": "bob",   "total": 19.95},
    "C300": {"customer": "alice", "total": 500.00},
}
REFUNDS_ISSUED = []
MANUAL_REVIEW_CAP = 100.00     # refunds above this need a human

SYSTEM = """You are RefundBot for Acme. A customer describes a refund request.
Respond with ONE line only:
ACTION: refund <order_id> <amount>"""

def _model_proposes(customer_msg: str) -> str:
    resp = client.messages.create(model=MODEL, max_tokens=100, system=SYSTEM,
        messages=[{"role": "user", "content": customer_msg}])
    return resp.content[0].text

def authorize_refund(auth_customer: str, order_id: str, amount: float):
    """The real security control. Deterministic policy gate that runs on the
    PROPOSED action — independent of how the model was prompted or tricked.
    Authorization keys off the AUTHENTICATED customer, never the request text."""
    order = ORDERS.get(order_id)
    if not order:
        return False, f"DENY: order {order_id} does not exist"
    if order["customer"] != auth_customer:                      # ownership
        return False, f"DENY: {auth_customer} does not own {order_id}"
    if amount <= 0:
        return False, "DENY: non-positive amount"
    if amount > order["total"]:                                 # ground truth
        return False, f"DENY: ${amount:.2f} exceeds order total ${order['total']:.2f}"
    if amount > MANUAL_REVIEW_CAP:                              # human-in-the-loop
        return False, f"HOLD: ${amount:.2f} over ${MANUAL_REVIEW_CAP:.0f} cap — needs human approval"
    return True, "ALLOW"

def secure_agent(auth_customer: str, customer_msg: str) -> str:
    text = _model_proposes(customer_msg)

    # ✅ Insecure-output-handling fix: the model output must match a strict
    # schema exactly. Anything else is rejected, never executed.
    m = re.fullmatch(r"\s*ACTION:\s*refund\s+(\S+)\s+\$?([\d.]+)\s*", text)
    if not m:
        return f"DENY: model output rejected (did not match allowed schema): {text!r}"

    order_id, amount = m.group(1), float(m.group(2))
    ok, reason = authorize_refund(auth_customer, order_id, amount)
    if not ok:
        return f"🛡️  BLOCKED — {reason}"

    REFUNDS_ISSUED.append((order_id, amount))
    return f"✅ Approved refund of ${amount:.2f} on {order_id}"