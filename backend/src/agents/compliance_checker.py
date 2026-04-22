"""
Phase 16: Compliance Checker Agent.

Validates each post against content_rules.yaml BEFORE human review.
Checks: hotline inclusion, language rules, source citation, survivor anonymity.
Can auto-fix simple violations.
"""
import os
import re
import logging
import yaml
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langsmith import traceable
from src.state import AgentState, CampaignPost

logger = logging.getLogger("redm.compliance")


class ComplianceResult(BaseModel):
    passed: bool = Field(description="True if no critical violations found")
    violations: list[str] = Field(default_factory=list, description="List of violation descriptions")
    auto_fixable: bool = Field(description="True if the checker can fix all violations automatically")
    fixed_caption: str = Field(default="", description="If auto_fixable, the corrected caption. Empty otherwise.")


class ComplianceChecker:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0).with_structured_output(ComplianceResult)
        self._rules = self._load_rules()

    @staticmethod
    def _load_rules() -> dict:
        path = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "config", "content_rules.yaml"))
        try:
            with open(path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.warning("Content rules not found")
            return {}

    def _build_rules_prompt(self) -> str:
        """Convert YAML rules into a plain-text checklist for the LLM."""
        lines = ["CHECK THE FOLLOWING RULES:\n"]

        # Language rules
        for rule in self._rules.get("language_rules", []):
            if rule.get("enabled", True):
                lines.append(f"- NEVER use \"{rule['instead_of']}\". Use \"{rule['use']}\" instead. ({rule['reason']})")

        # Content rules
        cr = self._rules.get("content_rules", {})
        if cr.get("always_include_hotline"):
            hotline = cr.get("hotline_number", "1-888-373-7888")
            lines.append(f"- MUST include the National Hotline number: {hotline}")
        if cr.get("must_cite_sources"):
            lines.append("- MUST cite at least one source (article, org, or report)")
        if cr.get("never_identify_survivors"):
            lines.append("- MUST NOT name or identify specific trafficking survivors")
        if cr.get("no_sensationalized_imagery"):
            lines.append("- MUST NOT use sensationalized or graphic language")

        return "\n".join(lines)

    @traceable(name="Compliance Check")
    def check_compliance(self, state: AgentState) -> dict:
        """Run compliance check on the current post."""
        posts = state.get("campaign_posts", [])
        idx = state.get("current_post_index", 0)

        if not posts or idx >= len(posts):
            return {"status": "error"}

        post = CampaignPost(**posts[idx])
        logger.info("--- COMPLIANCE: Checking %s post ---", post.content_type)

        # Quick rule-based checks first (no LLM needed)
        quick_violations = self._quick_check(post.caption)

        # LLM-based deep check
        rules_prompt = self._build_rules_prompt()
        messages = [
            SystemMessage(content=(
                "You are a Compliance Reviewer for an anti-trafficking campaign.\n"
                "Check the post against the rules below. If violations exist, try to auto-fix them.\n\n"
                f"{rules_prompt}"
            )),
            HumanMessage(content=f"POST TO REVIEW:\n{post.caption}"),
        ]

        result: ComplianceResult = self.llm.invoke(messages)

        # Merge quick checks with LLM checks
        all_violations = quick_violations + result.violations
        passed = len(all_violations) == 0

        # If auto-fixable, apply the fix
        if result.auto_fixable and result.fixed_caption:
            logger.info("Auto-fixing compliance violations")
            post.caption = result.fixed_caption
            passed = True
            all_violations = []

        post.compliance_passed = passed
        post.compliance_violations = all_violations
        posts[idx] = post.model_dump()

        if passed:
            logger.info("Compliance PASSED for %s", post.content_type)
        else:
            logger.warning("Compliance FAILED: %s", all_violations)

        return {
            "campaign_posts": posts,
            "status": "compliance_checked",
        }

    def _quick_check(self, caption: str) -> list[str]:
        """Fast regex-based checks — no LLM needed."""
        violations = []
        cr = self._rules.get("content_rules", {})

        # Check hotline inclusion
        if cr.get("always_include_hotline"):
            hotline = cr.get("hotline_number", "1-888-373-7888")
            befree = cr.get("befree_text_line", "233733")
            if hotline not in caption and befree not in caption:
                violations.append(f"Missing National Hotline ({hotline}) or BeFree text line ({befree})")

        # Check banned language
        caption_lower = caption.lower()
        for rule in self._rules.get("language_rules", []):
            if rule.get("enabled", True):
                banned = rule["instead_of"].lower()
                if banned in caption_lower:
                    violations.append(f"Uses banned term \"{rule['instead_of']}\" — should use \"{rule['use']}\"")

        return violations
