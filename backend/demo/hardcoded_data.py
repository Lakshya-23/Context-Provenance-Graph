"""Hardcoded deterministic extraction results for demo Revenue Recognition Policy.

These replace the LLM extraction pipeline entirely. All evidence text is verbatim
from the actual PDF content (sourced from demo/generate_pdfs.py sections).

v1.2 → 9 glossary terms, 17 claims
v1.3 → same 9 terms with updated refund rules, 17 claims
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# V1.2 — CLAIMS  (17 claims)
# ---------------------------------------------------------------------------

HARDCODED_CLAIMS_V1_2: list[dict] = [
    {
        "id": "claim_1",
        "text": "Revenue is recognized when an order has been fulfilled.",
        "claim_type": "business_rule",
        "source_page": 1,
        "related_terms": ["Revenue", "Fulfilled Order"],
    },
    {
        "id": "claim_2",
        "text": "A fulfilled order is an order for which the customer has received the purchased product or service.",
        "claim_type": "definition",
        "source_page": 1,
        "related_terms": ["Fulfilled Order"],
    },
    {
        "id": "claim_3",
        "text": "Cancelled orders that have not been fulfilled do not generate recognized revenue.",
        "claim_type": "business_rule",
        "source_page": 1,
        "related_terms": ["Revenue", "Fulfilled Order"],
    },
    {
        "id": "claim_4",
        "text": "Refunds are amounts returned to customers after a completed transaction.",
        "claim_type": "definition",
        "source_page": 1,
        "related_terms": ["Refund"],
    },
    {
        "id": "claim_5",
        "text": "Refunds processed before settlement are excluded from recognized revenue.",
        "claim_type": "business_rule",
        "source_page": 1,
        "related_terms": ["Refund", "Settlement", "Revenue"],
    },
    {
        "id": "claim_6",
        "text": "Refunds processed after settlement are recorded separately and do not change the original fulfillment event.",
        "claim_type": "business_rule",
        "source_page": 1,
        "related_terms": ["Refund", "Settlement"],
    },
    {
        "id": "claim_7",
        "text": "A chargeback is a disputed card transaction initiated by a customer through their payment provider.",
        "claim_type": "definition",
        "source_page": 1,
        "related_terms": ["Chargeback"],
    },
    {
        "id": "claim_8",
        "text": "Chargebacks are treated as a financial loss associated with the original transaction.",
        "claim_type": "business_rule",
        "source_page": 1,
        "related_terms": ["Chargeback"],
    },
    {
        "id": "claim_9",
        "text": "Chargebacks are tracked separately from recognized revenue.",
        "claim_type": "business_rule",
        "source_page": 1,
        "related_terms": ["Chargeback", "Revenue"],
    },
    {
        "id": "claim_10",
        "text": "Gross Revenue represents the value of fulfilled orders before refund adjustments.",
        "claim_type": "definition",
        "source_page": 1,
        "related_terms": ["Gross Revenue", "Fulfilled Order", "Refund"],
    },
    {
        "id": "claim_11",
        "text": "Net Revenue represents Gross Revenue less applicable refunds and chargeback losses used for management reporting.",
        "claim_type": "definition",
        "source_page": 1,
        "related_terms": ["Net Revenue", "Gross Revenue", "Refund", "Chargeback"],
    },
    {
        "id": "claim_12",
        "text": "Realized Revenue represents recognized revenue after applicable refund adjustments.",
        "claim_type": "definition",
        "source_page": 1,
        "related_terms": ["Realized Revenue", "Revenue", "Refund"],
    },
    {
        "id": "claim_13",
        "text": "Revenue reporting uses fulfilled orders as the recognition event.",
        "claim_type": "business_rule",
        "source_page": 1,
        "related_terms": ["Revenue", "Fulfilled Order"],
    },
    {
        "id": "claim_14",
        "text": "Refunds and chargebacks must be distinguished because they have different accounting and reporting implications.",
        "claim_type": "semantic_statement",
        "source_page": 1,
        "related_terms": ["Refund", "Chargeback"],
    },
    {
        "id": "claim_15",
        "text": "Settlement is the process by which a payment transaction is finalized between the merchant and the payment processor.",
        "claim_type": "definition",
        "source_page": 1,
        "related_terms": ["Settlement"],
    },
    {
        "id": "claim_16",
        "text": "Recognized revenue is the portion of revenue that meets the criteria for formal accounting recognition.",
        "claim_type": "definition",
        "source_page": 1,
        "related_terms": ["Revenue"],
    },
    {
        "id": "claim_17",
        "text": "The recognition event for revenue is the fulfillment of a customer order, not the payment receipt.",
        "claim_type": "business_rule",
        "source_page": 1,
        "related_terms": ["Revenue", "Fulfilled Order"],
    },
]


# ---------------------------------------------------------------------------
# V1.3 — CLAIMS  (17 claims, refund rule updated)
# ---------------------------------------------------------------------------

HARDCODED_CLAIMS_V1_3: list[dict] = [
    {
        "id": "claim_1",
        "text": "Revenue is recognized when an order has been fulfilled.",
        "claim_type": "business_rule",
        "source_page": 1,
        "related_terms": ["Revenue", "Fulfilled Order"],
    },
    {
        "id": "claim_2",
        "text": "A fulfilled order is an order for which the customer has received the purchased product or service.",
        "claim_type": "definition",
        "source_page": 1,
        "related_terms": ["Fulfilled Order"],
    },
    {
        "id": "claim_3",
        "text": "Cancelled orders that have not been fulfilled do not generate recognized revenue.",
        "claim_type": "business_rule",
        "source_page": 1,
        "related_terms": ["Revenue", "Fulfilled Order"],
    },
    {
        "id": "claim_4",
        "text": "Refunds are amounts returned to customers after a completed transaction.",
        "claim_type": "definition",
        "source_page": 1,
        "related_terms": ["Refund"],
    },
    {
        "id": "claim_5",
        "text": "Refunds processed within 30 days of fulfillment are excluded from recognized revenue.",
        "claim_type": "business_rule",
        "source_page": 1,
        "related_terms": ["Refund", "Revenue", "Fulfilled Order"],
    },
    {
        "id": "claim_6",
        "text": "Refunds processed after 30 days are recorded separately and do not reduce reported revenue.",
        "claim_type": "business_rule",
        "source_page": 1,
        "related_terms": ["Refund", "Revenue"],
    },
    {
        "id": "claim_7",
        "text": "Refunds processed after settlement are recorded separately and do not change the original fulfillment event.",
        "claim_type": "business_rule",
        "source_page": 1,
        "related_terms": ["Refund", "Settlement"],
    },
    {
        "id": "claim_8",
        "text": "A chargeback is a disputed card transaction initiated by a customer through their payment provider.",
        "claim_type": "definition",
        "source_page": 1,
        "related_terms": ["Chargeback"],
    },
    {
        "id": "claim_9",
        "text": "Chargebacks are treated as a financial loss associated with the original transaction.",
        "claim_type": "business_rule",
        "source_page": 1,
        "related_terms": ["Chargeback"],
    },
    {
        "id": "claim_10",
        "text": "Chargebacks are tracked separately from recognized revenue.",
        "claim_type": "business_rule",
        "source_page": 1,
        "related_terms": ["Chargeback", "Revenue"],
    },
    {
        "id": "claim_11",
        "text": "Gross Revenue represents the value of fulfilled orders before refund adjustments.",
        "claim_type": "definition",
        "source_page": 1,
        "related_terms": ["Gross Revenue", "Fulfilled Order", "Refund"],
    },
    {
        "id": "claim_12",
        "text": "Net Revenue represents Gross Revenue less applicable refunds and chargeback losses used for management reporting.",
        "claim_type": "definition",
        "source_page": 1,
        "related_terms": ["Net Revenue", "Gross Revenue", "Refund", "Chargeback"],
    },
    {
        "id": "claim_13",
        "text": "Realized Revenue represents recognized revenue after applicable refund adjustments.",
        "claim_type": "definition",
        "source_page": 1,
        "related_terms": ["Realized Revenue", "Revenue", "Refund"],
    },
    {
        "id": "claim_14",
        "text": "Revenue reporting uses fulfilled orders as the recognition event.",
        "claim_type": "business_rule",
        "source_page": 1,
        "related_terms": ["Revenue", "Fulfilled Order"],
    },
    {
        "id": "claim_15",
        "text": "Refunds and chargebacks must be distinguished because they have different accounting and reporting implications.",
        "claim_type": "semantic_statement",
        "source_page": 1,
        "related_terms": ["Refund", "Chargeback"],
    },
    {
        "id": "claim_16",
        "text": "Settlement is the process by which a payment transaction is finalized between the merchant and the payment processor.",
        "claim_type": "definition",
        "source_page": 1,
        "related_terms": ["Settlement"],
    },
    {
        "id": "claim_17",
        "text": "The recognition event for revenue is the fulfillment of a customer order, not the payment receipt.",
        "claim_type": "business_rule",
        "source_page": 1,
        "related_terms": ["Revenue", "Fulfilled Order"],
    },
]


# ---------------------------------------------------------------------------
# V1.2 — GLOSSARY TERMS  (9 terms)
# Evidence text is verbatim from the v1.2 PDF sections.
# ---------------------------------------------------------------------------

_SRC_V1_2 = "doc_revenue_policy_v1_2"

HARDCODED_GLOSSARY_V1_2: list[dict] = [
    {
        "id": "term_revenue",
        "name": "Revenue",
        "definition": "The value recognized from fulfilled customer orders, recorded at the point of order fulfillment.",
        "aliases": ["Recognized Revenue", "Reported Revenue"],
        "business_rules": [
            "Revenue is recognized when an order has been fulfilled.",
            "Cancelled orders that have not been fulfilled do not generate recognized revenue.",
            "The recognition event is the fulfillment of a customer order, not the payment receipt.",
        ],
        "evidence": [
            {
                "source_id": _SRC_V1_2,
                "page": 1,
                "text": "Revenue is recognized when an order has been fulfilled.",
            },
            {
                "source_id": _SRC_V1_2,
                "page": 1,
                "text": "Cancelled orders that have not been fulfilled do not generate recognized revenue.",
            },
        ],
        "confidence": 0.98,
    },
    {
        "id": "term_fulfilled_order",
        "name": "Fulfilled Order",
        "definition": "An order for which the customer has received the purchased product or service; the trigger event for revenue recognition.",
        "aliases": ["Completed Order", "Delivered Order"],
        "business_rules": [
            "A fulfilled order is an order for which the customer has received the purchased product or service.",
            "Revenue reporting uses fulfilled orders as the recognition event.",
        ],
        "evidence": [
            {
                "source_id": _SRC_V1_2,
                "page": 1,
                "text": "A fulfilled order is an order for which the customer has received the purchased product or service.",
            },
            {
                "source_id": _SRC_V1_2,
                "page": 1,
                "text": "Revenue reporting uses fulfilled orders as the recognition event.",
            },
        ],
        "confidence": 0.97,
    },
    {
        "id": "term_refund",
        "name": "Refund",
        "definition": "An amount returned to a customer after a completed transaction, with accounting treatment depending on whether it occurs before or after settlement.",
        "aliases": ["Return", "Customer Refund"],
        "business_rules": [
            "Refunds processed before settlement are excluded from recognized revenue.",
            "Refunds processed after settlement are recorded separately and do not change the original fulfillment event.",
        ],
        "evidence": [
            {
                "source_id": _SRC_V1_2,
                "page": 1,
                "text": "Refunds are amounts returned to customers after a completed transaction.",
            },
            {
                "source_id": _SRC_V1_2,
                "page": 1,
                "text": "Refunds processed before settlement are excluded from recognized revenue.",
            },
        ],
        "confidence": 0.96,
    },
    {
        "id": "term_chargeback",
        "name": "Chargeback",
        "definition": "A disputed card transaction initiated by a customer through their payment provider, treated as a financial loss and tracked separately from recognized revenue.",
        "aliases": ["Dispute", "Card Dispute"],
        "business_rules": [
            "Chargebacks are treated as a financial loss associated with the original transaction.",
            "Chargebacks are tracked separately from recognized revenue.",
            "Refunds and chargebacks must be distinguished because they have different accounting and reporting implications.",
        ],
        "evidence": [
            {
                "source_id": _SRC_V1_2,
                "page": 1,
                "text": "A chargeback is a disputed card transaction initiated by a customer through their payment provider.",
            },
            {
                "source_id": _SRC_V1_2,
                "page": 1,
                "text": "Chargebacks are treated as a financial loss associated with the original transaction.",
            },
        ],
        "confidence": 0.95,
    },
    {
        "id": "term_settlement",
        "name": "Settlement",
        "definition": "The finalization of a payment transaction between the merchant and the payment processor; determines the accounting boundary for refund classification.",
        "aliases": ["Payment Settlement", "Transaction Settlement"],
        "business_rules": [
            "Refunds processed before settlement are excluded from recognized revenue.",
            "Refunds processed after settlement are recorded separately and do not change the original fulfillment event.",
        ],
        "evidence": [
            {
                "source_id": _SRC_V1_2,
                "page": 1,
                "text": "Refunds processed before settlement are excluded from recognized revenue.",
            },
            {
                "source_id": _SRC_V1_2,
                "page": 1,
                "text": "Refunds processed after settlement are recorded separately and do not change the original fulfillment event.",
            },
        ],
        "confidence": 0.93,
    },
    {
        "id": "term_gross_revenue",
        "name": "Gross Revenue",
        "definition": "The total value of fulfilled orders before any refund adjustments are applied.",
        "aliases": ["Total Revenue", "Pre-Refund Revenue"],
        "business_rules": [
            "Gross Revenue represents the value of fulfilled orders before refund adjustments.",
            "Net Revenue is derived from Gross Revenue by deducting refunds and chargeback losses.",
        ],
        "evidence": [
            {
                "source_id": _SRC_V1_2,
                "page": 1,
                "text": "Gross Revenue represents the value of fulfilled orders before refund adjustments.",
            },
        ],
        "confidence": 0.97,
    },
    {
        "id": "term_net_revenue",
        "name": "Net Revenue",
        "definition": "Gross Revenue less applicable refunds and chargeback losses, used for management reporting purposes.",
        "aliases": ["Adjusted Revenue", "Management Revenue"],
        "business_rules": [
            "Net Revenue represents Gross Revenue less applicable refunds and chargeback losses used for management reporting.",
            "Net Revenue is the primary metric used for management and executive reporting.",
        ],
        "evidence": [
            {
                "source_id": _SRC_V1_2,
                "page": 1,
                "text": "Net Revenue represents Gross Revenue less applicable refunds and chargeback losses used for management reporting.",
            },
        ],
        "confidence": 0.96,
    },
    {
        "id": "term_realized_revenue",
        "name": "Realized Revenue",
        "definition": "Recognized revenue after all applicable refund adjustments have been applied; the final cash-basis revenue figure.",
        "aliases": ["Adjusted Recognized Revenue", "Cash Revenue"],
        "business_rules": [
            "Realized Revenue represents recognized revenue after applicable refund adjustments.",
            "Realized Revenue reflects the net amount after all pre-settlement refunds have been deducted.",
        ],
        "evidence": [
            {
                "source_id": _SRC_V1_2,
                "page": 1,
                "text": "Realized Revenue represents recognized revenue after applicable refund adjustments.",
            },
        ],
        "confidence": 0.95,
    },
    {
        "id": "term_recognition_event",
        "name": "Recognition Event",
        "definition": "The specific business milestone that triggers formal revenue recognition; for this policy, this is the fulfillment of a customer order.",
        "aliases": ["Trigger Event", "Revenue Trigger"],
        "business_rules": [
            "Revenue reporting uses fulfilled orders as the recognition event.",
            "The recognition event is the fulfillment of a customer order, not the payment receipt.",
        ],
        "evidence": [
            {
                "source_id": _SRC_V1_2,
                "page": 1,
                "text": "Revenue reporting uses fulfilled orders as the recognition event.",
            },
        ],
        "confidence": 0.91,
    },
]


# ---------------------------------------------------------------------------
# V1.3 — GLOSSARY TERMS  (9 terms, refund rules updated)
# ---------------------------------------------------------------------------

_SRC_V1_3 = "doc_revenue_policy_v1_3"

HARDCODED_GLOSSARY_V1_3: list[dict] = [
    {
        "id": "term_revenue",
        "name": "Revenue",
        "definition": "The value recognized from fulfilled customer orders, recorded at the point of order fulfillment.",
        "aliases": ["Recognized Revenue", "Reported Revenue"],
        "business_rules": [
            "Revenue is recognized when an order has been fulfilled.",
            "Cancelled orders that have not been fulfilled do not generate recognized revenue.",
            "The recognition event is the fulfillment of a customer order, not the payment receipt.",
        ],
        "evidence": [
            {
                "source_id": _SRC_V1_3,
                "page": 1,
                "text": "Revenue is recognized when an order has been fulfilled.",
            },
            {
                "source_id": _SRC_V1_3,
                "page": 1,
                "text": "Cancelled orders that have not been fulfilled do not generate recognized revenue.",
            },
        ],
        "confidence": 0.98,
    },
    {
        "id": "term_fulfilled_order",
        "name": "Fulfilled Order",
        "definition": "An order for which the customer has received the purchased product or service; the trigger event for revenue recognition.",
        "aliases": ["Completed Order", "Delivered Order"],
        "business_rules": [
            "A fulfilled order is an order for which the customer has received the purchased product or service.",
            "Revenue reporting uses fulfilled orders as the recognition event.",
        ],
        "evidence": [
            {
                "source_id": _SRC_V1_3,
                "page": 1,
                "text": "A fulfilled order is an order for which the customer has received the purchased product or service.",
            },
            {
                "source_id": _SRC_V1_3,
                "page": 1,
                "text": "Revenue reporting uses fulfilled orders as the recognition event.",
            },
        ],
        "confidence": 0.97,
    },
    {
        "id": "term_refund",
        "name": "Refund",
        "definition": "An amount returned to a customer after a completed transaction, with accounting treatment now determined by whether the refund occurs within or after 30 days of fulfillment.",
        "aliases": ["Return", "Customer Refund"],
        "business_rules": [
            "Refunds processed within 30 days of fulfillment are excluded from recognized revenue.",
            "Refunds processed after 30 days are recorded separately and do not reduce reported revenue.",
            "Refunds processed after settlement are recorded separately and do not change the original fulfillment event.",
        ],
        "evidence": [
            {
                "source_id": _SRC_V1_3,
                "page": 1,
                "text": "Refunds are amounts returned to customers after a completed transaction.",
            },
            {
                "source_id": _SRC_V1_3,
                "page": 1,
                "text": "Refunds processed within 30 days of fulfillment are excluded from recognized revenue.",
            },
        ],
        "confidence": 0.96,
    },
    {
        "id": "term_chargeback",
        "name": "Chargeback",
        "definition": "A disputed card transaction initiated by a customer through their payment provider, treated as a financial loss and tracked separately from recognized revenue.",
        "aliases": ["Dispute", "Card Dispute"],
        "business_rules": [
            "Chargebacks are treated as a financial loss associated with the original transaction.",
            "Chargebacks are tracked separately from recognized revenue.",
            "Refunds and chargebacks must be distinguished because they have different accounting and reporting implications.",
        ],
        "evidence": [
            {
                "source_id": _SRC_V1_3,
                "page": 1,
                "text": "A chargeback is a disputed card transaction initiated by a customer through their payment provider.",
            },
            {
                "source_id": _SRC_V1_3,
                "page": 1,
                "text": "Chargebacks are treated as a financial loss associated with the original transaction.",
            },
        ],
        "confidence": 0.95,
    },
    {
        "id": "term_settlement",
        "name": "Settlement",
        "definition": "The finalization of a payment transaction between the merchant and the payment processor; still referenced as a secondary accounting boundary for post-30-day refunds.",
        "aliases": ["Payment Settlement", "Transaction Settlement"],
        "business_rules": [
            "Refunds processed after settlement are recorded separately and do not change the original fulfillment event.",
            "In v1.3, the primary refund boundary is 30 days post-fulfillment, not the settlement event.",
        ],
        "evidence": [
            {
                "source_id": _SRC_V1_3,
                "page": 1,
                "text": "Refunds processed after settlement are recorded separately and do not change the original fulfillment event.",
            },
        ],
        "confidence": 0.91,
    },
    {
        "id": "term_gross_revenue",
        "name": "Gross Revenue",
        "definition": "The total value of fulfilled orders before any refund adjustments are applied.",
        "aliases": ["Total Revenue", "Pre-Refund Revenue"],
        "business_rules": [
            "Gross Revenue represents the value of fulfilled orders before refund adjustments.",
            "Net Revenue is derived from Gross Revenue by deducting refunds and chargeback losses.",
        ],
        "evidence": [
            {
                "source_id": _SRC_V1_3,
                "page": 1,
                "text": "Gross Revenue represents the value of fulfilled orders before refund adjustments.",
            },
        ],
        "confidence": 0.97,
    },
    {
        "id": "term_net_revenue",
        "name": "Net Revenue",
        "definition": "Gross Revenue less applicable refunds and chargeback losses, used for management reporting purposes.",
        "aliases": ["Adjusted Revenue", "Management Revenue"],
        "business_rules": [
            "Net Revenue represents Gross Revenue less applicable refunds and chargeback losses used for management reporting.",
            "Net Revenue is the primary metric used for management and executive reporting.",
        ],
        "evidence": [
            {
                "source_id": _SRC_V1_3,
                "page": 1,
                "text": "Net Revenue represents Gross Revenue less applicable refunds and chargeback losses used for management reporting.",
            },
        ],
        "confidence": 0.96,
    },
    {
        "id": "term_realized_revenue",
        "name": "Realized Revenue",
        "definition": "Recognized revenue after all applicable refund adjustments have been applied; under v1.3 this reflects the 30-day refund window.",
        "aliases": ["Adjusted Recognized Revenue", "Cash Revenue"],
        "business_rules": [
            "Realized Revenue represents recognized revenue after applicable refund adjustments.",
            "Under v1.3, only refunds within 30 days of fulfillment reduce Realized Revenue.",
        ],
        "evidence": [
            {
                "source_id": _SRC_V1_3,
                "page": 1,
                "text": "Realized Revenue represents recognized revenue after applicable refund adjustments.",
            },
        ],
        "confidence": 0.95,
    },
    {
        "id": "term_recognition_event",
        "name": "Recognition Event",
        "definition": "The specific business milestone that triggers formal revenue recognition; for this policy, this is the fulfillment of a customer order.",
        "aliases": ["Trigger Event", "Revenue Trigger"],
        "business_rules": [
            "Revenue reporting uses fulfilled orders as the recognition event.",
            "The recognition event is the fulfillment of a customer order, not the payment receipt.",
        ],
        "evidence": [
            {
                "source_id": _SRC_V1_3,
                "page": 1,
                "text": "Revenue reporting uses fulfilled orders as the recognition event.",
            },
        ],
        "confidence": 0.91,
    },
]


# ---------------------------------------------------------------------------
# SEMANTIC DIFF — v1.2 → v1.3
# ---------------------------------------------------------------------------

HARDCODED_DIFF_V1_2_TO_V1_3: dict = {
    "changes": [
        {
            "change_type": "modified",
            "old_text": "Refunds processed before settlement are excluded from recognized revenue.",
            "new_text": "Refunds processed within 30 days of fulfillment are excluded from recognized revenue.",
            "affected_terms": ["Refund", "Settlement", "Revenue"],
            "semantic_explanation": (
                "The refund exclusion criterion has shifted from a payment-processing milestone "
                "(settlement) to a time-based window (30 days from fulfillment). This is a significant "
                "semantic change: previously, only pre-settlement refunds reduced recognized revenue. "
                "Under v1.3, any refund issued within 30 days of fulfillment — regardless of settlement "
                "status — is excluded. This widens the refund deduction window and will directly reduce "
                "Realized Revenue and Net Revenue figures for merchants with active post-settlement, "
                "within-30-day return programmes."
            ),
        },
        {
            "change_type": "modified",
            "old_text": "Refunds processed after settlement are recorded separately and do not change the original fulfillment event.",
            "new_text": "Refunds processed after 30 days are recorded separately and do not reduce reported revenue.",
            "affected_terms": ["Refund", "Revenue"],
            "semantic_explanation": (
                "The secondary refund clause now uses a 30-day time boundary instead of the settlement "
                "event as the demarcation point. Under v1.2, any post-settlement refund was merely "
                "recorded separately. Under v1.3, refunds after 30 days explicitly do not reduce reported "
                "revenue, providing a clearer accounting boundary. Downstream SQL models and metrics "
                "that calculate Net Revenue or Realized Revenue must be updated to use a 30-day lookback "
                "filter rather than a settlement-date filter."
            ),
        },
        {
            "change_type": "added",
            "old_text": "",
            "new_text": "Refunds processed after settlement are recorded separately and do not change the original fulfillment event.",
            "affected_terms": ["Refund", "Settlement"],
            "semantic_explanation": (
                "V1.3 retains the original settlement-based clause as a third condition alongside the "
                "new 30-day rule, providing an additional accounting safeguard for edge cases where "
                "settlement occurs more than 30 days after fulfillment. This clause was not present as "
                "a distinct rule in v1.2 in conjunction with the 30-day window."
            ),
        },
    ],
    "affected_terms": [
        "term_refund",
        "term_settlement",
        "term_revenue",
        "term_realized_revenue",
        "term_net_revenue",
    ],
}
