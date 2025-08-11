def build_tsd_prompt(jira_data, git_data, notes):
    jira_comments_formatted = "\n".join([
        f"- **{author}**: {comment.strip()}" for author, comment in jira_data.get("comments", [])
    ]) if jira_data.get("comments") else "- No comments available."

    # Format Attachments
    jira_attachments_formatted = (
        "| File Name | Uploaded By | Date | Download Link |\n"
        "|-----------|-------------|------|----------------|\n" +
        "\n".join([
            f"| {a['filename']} | {a['author']} | {a['created']} | [Download]({a['url']}) |"
            for a in jira_data.get("attachments", [])
        ])
    ) if jira_data.get("attachments") else "No attachments available."


    jira_labels = ', '.join(jira_data.get("labels", [])) or "None"
    jira_components = ', '.join(jira_data.get("components", [])) or "None"

    prompt = f"""
You are a senior software architect and documentation specialist.

You are tasked with writing a **production-ready Technical Specification Document (TSD)** in markdown format for a new feature being implemented.

---

## 🧾 Project Input (From JIRA + Git)

### 🔹 JIRA Ticket Information:
- **Ticket ID**: {jira_data.get('ticket_id')}
- **Title**: {jira_data.get('title')}
- **Status**: {jira_data.get('status')}
- **Created On**: {jira_data.get('created_on')}
- **Created By**: {jira_data.get('created_by')}
- **Assignee**: {jira_data.get('assignee')}
- **Reporter**: {jira_data.get('reporter')}
- **Labels**: {jira_labels}
- **Components**: {jira_components}

**Description:**
{jira_data.get("description")}

**📎 Attachments:**
| File Name | Uploaded By | Date | Download Link |
|-----------|-------------|------|----------------|
{jira_attachments_formatted}

**💬 Comments:**
{jira_comments_formatted}

---

### 🔹 Git PR Details:
- **Title**: {git_data.get('pr_title')}
- **Description**:
{git_data.get('pr_description')}
- **Files Changed**:
{chr(10).join(git_data.get('files_changed', []))}
- **Raised By**: {git_data.get('raised_by')} on {git_data.get('created_on')}
- **Approved By**: {', '.join(git_data.get('approved_by', []))}
- **Merged On**: {git_data.get('merged_on')}
- **PR Link**: {git_data.get('pr_link')}

---

### 🔹 Additional Notes:
{chr(10).join(notes) if notes else "N/A"}

---

## ✍️ Instruction:
Write a detailed and technical **15-section TSD** covering the following structure:

1. **Project Overview**
2. **Business Objective**
3. **Functional Requirements**
4. **User Journey / UX Flow**
5. **Architecture & Data Flow**
6. **Tech Stack**
7. **API & Module Design**
8. **Detailed File Change Summary**
9. **Integration Details**
10. **Deployment Strategy**
11. **Testing Plan**
12. **Known Limitations**
13. **Future Enhancements**
14. **Approval Summary**
15. **Appendix** (Include JIRA metadata, PR metadata, Attachments Table, and Comments List)

Use **markdown formatting**: bold headings, bullet points, tables
-Ensure to mention JIRA and Git title in TSD title
- Ensure each section has **minimum 10–15 lines** of content
- Include all attachments and comments clearly with given 
- Format "Appendix" with proper tables and subsections.
-strictly follow the format for attchment and comment section in apendix 
Make the TSD clear enough to hand over to a new developer.
mention approval summary in detail and and include JIRA information and GIT information in appndix

---

## 💬 Comments (Appendix Section - Do Not Omit):
{jira_comments_formatted}
"""

    return [
        {"role": "system", "content": "You are a professional technical writer and software architect."},
        {"role": "user", "content": prompt}
    ]