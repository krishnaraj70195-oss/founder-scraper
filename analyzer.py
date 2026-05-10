import re

from dotenv import load_dotenv
from openai import AsyncOpenAI

from prompts import SYSTEM_PROMPT, build_user_prompt

load_dotenv()

MODEL = "gpt-4o-mini"

client = AsyncOpenAI()

ALLOWED_ROLES = [
    "Founder",
    "Co-Founder",
    "CEO",
    "Owner",
    "Co-Owner"
]


class LeadershipAnalyzer:

    def __init__(self):
        pass

    async def analyze(self, text):

        if not text.strip():
            return []

        try:

            response = await client.chat.completions.create(
                model=MODEL,
                temperature=0,
                max_tokens=80,
                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": build_user_prompt(text)
                    }
                ]
            )

            output = response.choices[0].message.content.strip()

            return self.parse_output(output)

        except Exception:
            return []

    def parse_output(self, output):

        if output.upper() == "NONE":
            return []

        results = []

        seen = set()

        lines = output.splitlines()

        for line in lines:

            if "|" not in line:
                continue

            parts = line.split("|", 1)

            if len(parts) != 2:
                continue

            role = parts[0].strip()
            name = parts[1].strip()

            if role not in ALLOWED_ROLES:
                continue

            if not self.is_valid_name(name):
                continue

            key = f"{role}-{name.lower()}"

            if key in seen:
                continue

            seen.add(key)

            results.append({
                "role": role,
                "full_name": name
            })

        return results

    def is_valid_name(self, name):

        if not name:
            return False

        lower = name.lower().strip()

        invalid_exact = [
            "none",
            "unknown",
            "n/a",
        ]

        if lower in invalid_exact:
            return False

        if len(name) > 40:
            return False

        if len(name.split()) > 5:
            return False

        if re.search(r"\d", name):
            return False

        if "@" in name:
            return False

        if ".com" in lower:
            return False

        return True
