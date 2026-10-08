"""Static downstream context registry.

This represents the existing AI/data environment that consumes
the glossary terms. These are NOT extracted by the LLM — they
are static demo data representing downstream systems.
"""

from __future__ import annotations

# --- Metrics ---

METRICS = {
    "metric_gross_revenue": {
        "id": "metric_gross_revenue",
        "name": "Gross Revenue",
        "definition": "The total value of fulfilled orders before refund adjustments.",
        "uses_terms": ["term_revenue"],
    },
    "metric_net_revenue": {
        "id": "metric_net_revenue",
        "name": "Net Revenue",
        "definition": "Gross Revenue less applicable refunds and chargeback losses used for management reporting.",
        "uses_terms": ["term_revenue", "term_refund", "term_chargeback"],
    },
}

# --- Context Repositories ---

CONTEXT_REPOSITORIES = {
    "repo_finance_analytics": {
        "id": "repo_finance_analytics",
        "name": "Finance Analytics Context Repository",
        "definition": "Central context repository for financial analytics and reporting.",
        "depends_on": [
            "term_revenue",
            "term_refund",
            "term_chargeback",
            "metric_gross_revenue",
            "metric_net_revenue",
            "term_realized_revenue",
        ],
    },
}

# --- Skills ---

SKILLS = {
    "skill_revenue_analyst": {
        "id": "skill_revenue_analyst",
        "name": "Revenue Analyst",
        "definition": "Skill for analyzing revenue data and trends.",
        "depends_on": ["repo_finance_analytics"],
    },
}

# --- Agents ---

AGENTS = {
    "agent_finance_copilot": {
        "id": "agent_finance_copilot",
        "name": "Finance Copilot",
        "definition": "AI copilot for finance team members.",
        "depends_on": ["skill_revenue_analyst", "repo_finance_analytics"],
    },
    "agent_executive_analyst": {
        "id": "agent_executive_analyst",
        "name": "Executive Analyst",
        "definition": "AI analyst for executive-level financial reporting.",
        "depends_on": ["repo_finance_analytics"],
    },
}

# --- Evaluation Nodes ---

EVALUATIONS = {
    "eval_q1": {
        "id": "eval_q1",
        "name": "Evaluation Q1",
        "question": "When is revenue recognized?",
        "depends_on": ["term_revenue"],
    },
    "eval_q2": {
        "id": "eval_q2",
        "name": "Evaluation Q2",
        "question": "What is the definition of a refund?",
        "depends_on": ["term_refund"],
    },
    "eval_q3": {
        "id": "eval_q3",
        "name": "Evaluation Q3",
        "question": "How are chargebacks treated in reporting?",
        "depends_on": ["term_chargeback", "term_revenue"],
    },
}


def get_all_downstream():
    """Return all downstream registry items."""
    return {
        "metrics": METRICS,
        "context_repositories": CONTEXT_REPOSITORIES,
        "skills": SKILLS,
        "agents": AGENTS,
        "evaluations": EVALUATIONS,
    }
