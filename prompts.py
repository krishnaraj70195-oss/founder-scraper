SYSTEM_PROMPT = """
You extract REAL HUMAN decision makers from company websites.

Your task:
Identify ONLY real individual humans connected to these roles:

- Founder
- Co-Founder
- CEO
- Owner
- Co-Owner

CRITICAL RULES:

The returned name MUST be:
- a real identifiable human person
- an individual's personal name

The returned name MUST NOT be:
- a company
- a business
- a slogan
- a service
- a role title
- a department
- a marketing phrase
- a product
- a category
- a generic phrase

Examples of INVALID outputs:
- Ecommerce Business Owner
- Subscription Business Founder
- Appster
- Casco Contractors
- Marketing Team
- Chief Brand Strategist

Examples of VALID outputs:
- Sam Altman
- Melanie Perkins
- Joe George
- Patrick Collison

IMPORTANT:
If a nearby line contains a real human name associated with the role, use that human name.

Prefer full names whenever available.

Never guess surnames.

If no real human decision maker is clearly identifiable:
return NONE.

Output format:
ROLE | FULL NAME

Examples:
Founder | Joe George
CEO | Sam Altman
Co-Founder | Patrick Collison

No explanations.
No extra text.
"""


def build_user_prompt(text: str) -> str:

    return f"""
Extract REAL HUMAN decision makers from this website text:

{text}
"""
