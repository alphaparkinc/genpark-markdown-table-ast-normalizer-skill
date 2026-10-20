"""Example usage for Markdown Table AST Normalizer."""
from client import MarkdownTableAstNormalizer
import json

raw_table = """
| Product | Category | Units Sold |
|---|---|---|
| Robot Vacuum | AI Gadgets | 4,200 |
| SaaS Platform | Service | 18,900 |
"""

res = MarkdownTableAstNormalizer.parse_and_normalize(raw_table)
print("Normalized Markdown:
" + res["normalized_markdown"])
print("
JSON Records:
" + json.dumps(res["records"], indent=2))
