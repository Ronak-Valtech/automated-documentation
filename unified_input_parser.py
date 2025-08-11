import re

def parse_tsd_input(text):
    git_data = {}
    notes = []

    # PR fields
    git_data["pr_link"] = re.search(r"GitHub PR Link:\s*(.+)", text).group(1).strip()
    git_data["pr_title"] = re.search(r"PR Title:\s*(.+)", text).group(1).strip()
    git_data["pr_description"] = re.search(r"PR Description:\s*(.+?)Files Changed:", text, re.DOTALL).group(1).strip()
    git_data["files_changed"] = re.findall(r"- (/.+)", text)
    git_data["raised_by"] = re.search(r"PR Raised By:\s*(.+)", text).group(1).strip()
    git_data["created_on"] = re.search(r"PR Created On:\s*(.+)", text).group(1).strip()
    git_data["approved_by"] = [x.strip() for x in re.search(r"PR Approved By:\s*(.+)", text).group(1).split(",")]
    git_data["merged_on"] = re.search(r"PR Merged On:\s*(.+)", text).group(1).strip()

    # Notes section
    notes_match = re.search(r"Additional Notes:\s*(.+)", text, re.DOTALL)
    if notes_match:
        notes = [line.strip("- ").strip() for line in notes_match.group(1).strip().splitlines() if line.strip()]

    return {"git": git_data, "notes": notes}
