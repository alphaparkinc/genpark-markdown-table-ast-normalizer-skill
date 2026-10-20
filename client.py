"""Markdown Table AST Normalizer.
100% Python Standard Library.
"""
import re
import io
import csv

class MarkdownTableAstNormalizer:
    """Normalizes erratic LLM Markdown tables and exports to CSV/JSON."""

    @classmethod
    def parse_and_normalize(cls, markdown_table: str) -> dict:
        lines = [line.strip() for line in markdown_table.strip().split("\n") if line.strip()]
        table_lines = [l for l in lines if l.startswith("|") and l.endswith("|")]
        if len(table_lines) < 2:
            return {"success": False, "error": "Insufficient markdown table lines"}

        headers = [c.strip() for c in table_lines[0].strip("|").split("|")]

        data_rows = []
        for line in table_lines[1:]:
            cells = [c.strip() for c in line.strip("|").split("|")]
            if all(re.match(r'^:?-+:?$', c) for c in cells):
                continue
            if len(cells) < len(headers):
                cells += [""] * (len(headers) - len(cells))
            else:
                cells = cells[:len(headers)]
            data_rows.append(cells)

        records = [dict(zip(headers, row)) for row in data_rows]

        csv_out = io.StringIO()
        writer = csv.writer(csv_out)
        writer.writerow(headers)
        writer.writerows(data_rows)

        col_widths = [len(h) for h in headers]
        for row in data_rows:
            for i, val in enumerate(row):
                col_widths[i] = max(col_widths[i], len(val))

        sep_line = "| " + " | ".join(["-" * w for w in col_widths]) + " |"
        header_line = "| " + " | ".join([headers[i].ljust(col_widths[i]) for i in range(len(headers))]) + " |"
        body_lines = ["| " + " | ".join([row[i].ljust(col_widths[i]) for i in range(len(headers))]) + " |" for row in data_rows]
        normalized_md = "\n".join([header_line, sep_line] + body_lines)

        return {
            "success": True,
            "headers": headers,
            "rows_count": len(data_rows),
            "normalized_markdown": normalized_md,
            "csv": csv_out.getvalue(),
            "records": records
        }
