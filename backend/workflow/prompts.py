"""Prompt templates for the extraction workflow.

Prompts are separated from business logic for maintainability.
"""

SYSTEM_EXTRACTOR = """You are a precise business-document analyst. You extract structured information from policy documents.
You NEVER fabricate information. Every piece of output must be grounded in the source text.
You return valid JSON only — no markdown fences, no commentary outside the JSON."""


EXTRACT_CLAIMS_PROMPT = """Analyze the following business policy document and extract all meaningful claims.

A claim is any statement that:
- Defines a business term
- States a business rule
- Describes a relationship between concepts
- Makes a semantic assertion about how something works

For each claim, provide:
- id: a short unique identifier like "claim_1", "claim_2", etc.
- text: the exact or near-exact statement from the source
- claim_type: one of "definition", "business_rule", "relationship", "semantic_statement"
- source_page: the page number where this claim appears
- related_terms: list of business terms this claim references

IMPORTANT:
- Do NOT invent claims not present in the document
- Preserve the original meaning
- Include the page number exactly as shown in the [Page N] markers

Return JSON in this exact format:
{{
  "claims": [
    {{
      "id": "claim_1",
      "text": "...",
      "claim_type": "definition",
      "source_page": 1,
      "related_terms": ["Revenue"]
    }}
  ]
}}

DOCUMENT:
{document_text}"""


EXTRACT_GLOSSARY_PROMPT = """Based on the following business policy document and extracted claims, create a structured glossary of important business terms.

IMPORTANT GUIDELINES:
- Extract terms that have BUSINESS SIGNIFICANCE — domain-specific concepts with specific meanings
- Do NOT extract generic/common words like "customer", "order", "amount", "process", "report"
- DO extract terms like: Revenue, Refund, Chargeback, Settlement, Gross Revenue, Net Revenue, Realized Revenue, Fulfilled Order
- Each term must have a definition grounded in the source document
- Include aliases if a term is referred to by different names
- Include business rules that apply to each term
- Provide evidence: exact quotes from the document that support the term's definition
- Include the page number where each piece of evidence appears
- Assign a confidence score (0.0 to 1.0) based on how clearly the term is defined in the source
- NEVER fabricate evidence — only include text actually present in the document

For each term, return:
- id: a snake_case identifier like "term_revenue", "term_refund"
- name: the canonical name (e.g., "Revenue", "Net Revenue")
- definition: a concise definition derived from the source
- aliases: list of alternative names (can be empty)
- business_rules: list of rules that apply to this term
- evidence: list of supporting quotes with source_id and page number
- confidence: float between 0.0 and 1.0

Return JSON in this exact format:
{{
  "terms": [
    {{
      "id": "term_revenue",
      "name": "Revenue",
      "definition": "The value recognized from fulfilled customer orders.",
      "aliases": [],
      "business_rules": ["Revenue is recognized when an order has been fulfilled."],
      "evidence": [
        {{
          "source_id": "{source_id}",
          "page": 1,
          "text": "Revenue is recognized when an order has been fulfilled."
        }}
      ],
      "confidence": 0.95
    }}
  ]
}}

CLAIMS:
{claims_json}

DOCUMENT:
{document_text}"""


SEMANTIC_DIFF_PROMPT = """Compare these two versions of a business policy document and identify semantic changes.

Do NOT just compare strings. Identify changes in MEANING:
- Changed business rules
- Modified definitions
- Altered thresholds or conditions
- New requirements or removed requirements

For each semantic change, explain:
1. What changed (old rule vs new rule)
2. Which business terms are affected
3. Why this change matters for downstream systems

VERSION 1 ({old_version}):
{old_text}

VERSION 2 ({new_version}):
{new_text}

Return JSON:
{{
  "changes": [
    {{
      "change_type": "modified",
      "old_text": "exact old text",
      "new_text": "exact new text",
      "affected_terms": ["Revenue", "Refund"],
      "semantic_explanation": "The refund eligibility window changed from..."
    }}
  ]
}}"""
