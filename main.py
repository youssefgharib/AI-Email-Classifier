import os
import json
import openai
from openai import OpenAI

# --- API key ---------------------------------------------------------------

api_key = os.getenv("GROQ_API_KEY")

# The email we want to classify (hardcoded for now)

customer_email = (
    "My subscription was charged twice this month, and I was also charged an extra $15 for the same subscription. Please check both charges and refund anything that was duplicated."
)

# The exact shape we want the model to reply in.

schema = {
    "name": "email_classification",
    "schema": {
        "type": "object",
        "properties": {
            "primary_category": {
                "type": "string",
                "enum": [
                    "billing",
                    "technical_support",
                    "account",
                    "shipping",
                    "other",
                ],
            },
            "secondary_categories": {
                "type": "array",
                "items": {
                    "type": "string",
                    "enum": [
                        "billing",
                        "technical_support",
                        "account",
                        "shipping",
                        "other",
                    ],
                },
            },
            "urgency": {
                "type": "string",
                "enum": ["low", "medium", "high"],
            },
            "summary": {"type": "string"},
            "suggested_action": {"type": "string"},
        },
        "required": [
            "primary_category",
            "secondary_categories",
            "urgency",
            "summary",
            "suggested_action",
        ],
        "additionalProperties": False,
    },
    "strict": True,
}

client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)

try:
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": (
                    "Classify the customer email using the given format.\n\n"

                    "Step 1 — identify every independent problem or request "
                    "in the email. Do not stop after finding only the first "
                    "or second one.\n\n"

                    "Step 2 — from that full list, select the most important "
                    "one as primary_category. It is NOT necessarily the first "
                    "one mentioned. Choose the category that should determine "
                    "the first business workflow used to handle the case, "
                    "based on the customer's actual needs and priorities.\n\n"

                    "Step 3 — put every other independent problem or request "
                    "into secondary_categories. Test for each one: would this "
                    "require a separate business workflow? If yes, include it. "
                    "If no, leave it out.\n\n"

                    "refund is NOT a category. A refund is a requested "
                    "resolution, not a separate problem — reflect it in "
                    "summary and suggested_action instead, never as a category.\n\n"

                    "Do not add a category just because it is mentioned as "
                    "context.\n"

                    "Do not add a category for a conditional fallback "
                    "(for example, 'if you cannot do X, I will want Y').\n"

                    "Never repeat primary_category inside secondary_categories.\n"
                    "Never repeat the same category twice inside "
                    "secondary_categories.\n"

                    "If there are no secondary categories, return an empty "
                    "array.\n\n"

                    "summary: briefly and accurately describe the customer's "
                    "actual problems and requests, including important details "
                    "from the email. Do not invent facts or add information "
                    "the customer did not provide. If there are multiple "
                    "independent problems, mention all of them.\n\n"

                    "suggested_action: "
                    "State the specific and concrete next operational step for the support team. "
                    "Base the action only on facts explicitly stated in the customer email "
                    "and procedures or policies explicitly provided to the model. "
                    "Do not assume that the company allows a requested action unless the "
                    "relevant policy or procedure is provided. "
                    "When a customer requests an action that depends on eligibility, permission, "
                    "approval, or company policy, first recommend verifying the relevant "
                    "condition and then following the applicable company procedure. "
                    "For example, if the customer requests a refund, do not automatically say "
                    "to issue the refund. Recommend verifying the charge or problem and checking "
                    "refund eligibility under the company's refund policy. "
                    "If the customer requests a replacement, do not assume replacement is "
                    "available. Recommend verifying the order or problem and checking "
                    "replacement eligibility under the company's policy. "
                    "If the customer requests an account unlock, do not assume the support team "
                    "can unlock it. Recommend verifying the account status and following the "
                    "approved account-recovery or unlock procedure. "
                    "If the customer reports a technical problem, recommend a concrete "
                    "diagnostic or troubleshooting step supported by the information provided. "
                    "Do not claim that a fix has been deployed or that a technical issue has "
                    "been resolved. "
                    "Do not invent company policies, eligibility rules, permissions, refunds, "
                    "compensation, replacement availability, deadlines, internal systems, or "
                    "actions that have already been performed. "
                    "If the email contains multiple independent problems, provide a specific "
                    "action for each problem. "
                    "Do not use vague phrases such as 'look into the issue', "
                    "'assist the customer', 'handle appropriately', or 'investigate further'. "
                    "The action should tell the support team what to verify or do next without "
                    "assuming facts that are not known.\n\n"
                    

                    "Examples:\n"

                    "Email: 'My package arrived damaged. I want a refund.'\n"
                    "-> primary_category: 'shipping', "
                    "secondary_categories: []\n"
                    "suggested_action: 'Verify the damaged shipment and check "
                    "refund eligibility under the company's refund policy.'\n\n"

                    "Email: 'My package hasn't arrived. Also, please change "
                    "the email address on my account.'\n"
                    "-> primary_category: 'shipping', "
                    "secondary_categories: ['account']\n"
                    "(two independent requests, each needing its own workflow)\n\n"

                    "Email: 'My password reset email isn't arriving, so I "
                    "can't access my account.'\n"
                    "-> primary_category: 'technical_support', "
                    "secondary_categories: []\n"
                    "(the account is context for the technical problem, "
                    "not a separate request)\n\n"

                    "Email: 'If you can't deliver my package by Friday, "
                    "I'll want a refund.'\n"
                    "-> primary_category: 'shipping', "
                    "secondary_categories: []\n"
                    "(the refund is a conditional fallback, not a current "
                    "independent problem)\n\n"

                    "Email: 'My package arrived damaged and I also can't "
                    "log into the mobile app.'\n"
                    "-> summary: 'Customer received a damaged package and "
                    "cannot access the mobile app.'\n"
                    "-> suggested_action: 'Verify the damaged shipment and "
                    "check refund/replacement eligibility under company "
                    "policy; separately, investigate the mobile app login "
                    "issue and provide the customer with the appropriate "
                    "account-recovery or troubleshooting steps.'"
                ),
            },
            {"role": "user", "content": customer_email},
        ],
        response_format={
            "type": "json_schema",
            "json_schema": schema,
        },
    )

    result = json.loads(response.choices[0].message.content)
    print(json.dumps(result, indent=2))

except openai.AuthenticationError as e:
    print(
        f"Error: authentication failed — check that your API key is valid. ({e})"
    )

except openai.RateLimitError as e:
    print(
        f"Error: rate limit hit — you're sending requests too fast "
        f"or have exceeded your quota. ({e})"
    )

except openai.BadRequestError as e:
    print(
        f"Error: the request was invalid — check the schema, "
        f"model name, or message content. ({e})"
    )

except openai.InternalServerError as e:
    print(
        f"Error: the LLM provider had a server-side problem — "
        f"try again shortly. ({e})"
    )

except openai.APIConnectionError as e:
    print(
        f"Error: could not connect to the LLM provider — "
        f"check your network connection. ({e})"
    )

except openai.APITimeoutError as e:
    print(
        f"Error: the request to the LLM provider timed out. ({e})"
    )

except openai.APIStatusError as e:
    print(
        f"Error: the LLM provider returned an unexpected error "
        f"(status {e.status_code}). ({e})"
    )