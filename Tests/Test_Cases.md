# Test Cases

The classifier was evaluated using customer email scenarios designed to test category selection, urgency detection, summaries, suggested actions, and handling of multiple issues.

## Test A — Damaged Shipment

### Scenario

Customer received a damaged package and requested a refund.

### Expected Behavior

The system should identify the shipping problem as the primary issue and treat the refund as a requested resolution rather than automatically creating a separate refund category.

### Observed Output

```json
{
  "primary_category": "shipping",
  "secondary_categories": [],
  "summary": "Customer received a damaged package and requests a full refund.",
  "suggested_action": "Verify the damaged shipment and check refund eligibility under the company's refund policy.",
  "urgency": "medium"
}
```

## Test B — Multi-Issue Customer Request

### Scenario

Customer email containing more than one actionable customer-service issue.

### Expected Behavior

The system should identify the most important customer problem as the primary category and assign a secondary category only when there is a genuinely distinct second actionable issue.

## Classification Rules Tested

* Primary category represents the customer's main problem or request.
* Secondary categories represent only distinct actionable issues.
* Context alone should not create a secondary category.
* The same category should not appear as both primary and secondary.
* Refund is treated as a requested resolution rather than an independent category.
* Urgency should reflect the importance of the customer's situation.