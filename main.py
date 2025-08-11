
import os
from dotenv import load_dotenv
from jira_client import get_jira_ticket
from tsd_prompt_builder import build_tsd_prompt
from openai_api import generate_tsd_document
from utils import save_tsd_as_pdf
from unified_input_parser import parse_tsd_input

def main():
    load_dotenv()
    ticket_id = input("🔍 Enter JIRA Ticket ID (e.g., AICOE-1201): ").strip()
    jira_data = get_jira_ticket(ticket_id)
    print("✅ Ticket data fetched successfully!\n")

    for key, value in jira_data.items():
        if isinstance(value, list):
            if key == "attachments":
                print(f"📎 {key.capitalize()}:")
                for a in value:
                    print(f"   - {a['filename']} ({a['created']}) by {a['author']}: {a['url']}")
            elif key == "comments":
                print(f"💬 {key.capitalize()}:")
                for author, comment in value:
                    print(f"   - {author}: {comment[:120]}...")
            else:
                print(f"🔹 {key}: {', '.join(value)}")
        else:
            print(f"🔹 {key}: {value}")

    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(current_dir, "data", "tsd_input_document_AICOE-1012.txt")
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"❌ Git input file not found at {input_path}")

    with open(input_path, "r", encoding="utf-8") as f:
        input_text = f.read()

    parsed = parse_tsd_input(input_text)
    messages = build_tsd_prompt(jira_data, parsed["git"], parsed["notes"])
    tsd_markdown = generate_tsd_document(messages)
    output_path = os.path.join("data", f"{ticket_id}_TSD.pdf")
    save_tsd_as_pdf(tsd_markdown, output_path=output_path)
    print(f"📄 TSD generated and saved to: {output_path}")

if __name__ == "__main__":
    main()
