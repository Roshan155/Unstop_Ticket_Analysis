#!/usr/bin/env python3
# Unstop Case: Ticket Cleaning & Categorization
import pandas as pd
import matplotlib.pyplot as plt

data = [
    {"sender":"eve@startup.io","subject":"Help required with account verification","body":"Do you support integration with third-party APIs? Specifically, Iâ€™m looking for CRM integration options.","sent_date":"8/19/2025 0:58"},
    {"sender":"diana@client.co","subject":"General query about subscription","body":"Hi team, I am unable to log into my account since yesterday. Could you please help me resolve this issue?","sent_date":"8/25/2025 0:58"},
    {"sender":"eve@startup.io","subject":"Immediate support needed for billing error","body":"Hello, I wanted to understand the pricing tiers better. Could you share a detailed breakdown?","sent_date":"8/20/2025 12:58"},
    {"sender":"alice@example.com","subject":"Urgent request: system access blocked","body":"Hi team, I am unable to log into my account since yesterday. Could you please help me resolve this issue?","sent_date":"8/21/2025 21:58"},
    {"sender":"eve@startup.io","subject":"Question: integration with API","body":"Despite multiple attempts, I cannot reset my password. The reset link doesnâ€™t seem to work.","sent_date":"8/20/2025 4:58"},
    {"sender":"alice@example.com","subject":"Critical help needed for downtime","body":"Hi team, I am unable to log into my account since yesterday. Could you please help me resolve this issue?","sent_date":"8/18/2025 8:58"},
    {"sender":"diana@client.co","subject":"Help required with account verification","body":"There is a billing error where I was charged twice. This needs immediate correction.","sent_date":"8/20/2025 19:58"},
    {"sender":"diana@client.co","subject":"Support needed for login issue","body":"I am facing issues with verifying my account. The verification email never arrived. Can you assist?","sent_date":"8/23/2025 6:58"},
    {"sender":"alice@example.com","subject":"General query about subscription","body":"Our servers are down, and we need immediate support. This is highly critical.","sent_date":"8/26/2025 2:58"},
    {"sender":"alice@example.com","subject":"Help required with account verification","body":"Do you support integration with third-party APIs? Specifically, Iâ€™m looking for CRM integration options.","sent_date":"8/21/2025 13:58"},
    {"sender":"diana@client.co","subject":"Support needed for login issue","body":"Hi team, I am unable to log into my account since yesterday. Could you please help me resolve this issue?","sent_date":"8/26/2025 15:58"},
    {"sender":"alice@example.com","subject":"Help required with account verification","body":"Do you support integration with third-party APIs? Specifically, Iâ€™m looking for CRM integration options.","sent_date":"8/24/2025 5:58"},
    {"sender":"eve@startup.io","subject":"Critical help needed for downtime","body":"Our servers are down, and we need immediate support. This is highly critical.","sent_date":"8/21/2025 19:58"},
    {"sender":"alice@example.com","subject":"Query about product pricing","body":"There is a billing error where I was charged twice. This needs immediate correction.","sent_date":"8/24/2025 13:58"},
    {"sender":"alice@example.com","subject":"General query about subscription","body":"I am facing issues with verifying my account. The verification email never arrived. Can you assist?","sent_date":"8/26/2025 1:58"},
    {"sender":"alice@example.com","subject":"Immediate support needed for billing error","body":"Despite multiple attempts, I cannot reset my password. The reset link doesnâ€™t seem to work.","sent_date":"8/19/2025 7:58"},
    {"sender":"charlie@partner.org","subject":"Help required with account verification","body":"This is urgent â€“ our system is completely inaccessible, and this is affecting our operations.","sent_date":"8/18/2025 0:58"},
    {"sender":"diana@client.co","subject":"Request for refund process clarification","body":"Could you clarify the steps involved in requesting a refund? I submitted one last week but have no update.","sent_date":"8/22/2025 17:58"},
    {"sender":"eve@startup.io","subject":"Query about product pricing","body":"Our servers are down, and we need immediate support. This is highly critical.","sent_date":"8/22/2025 9:58"},
    {"sender":"bob@customer.com","subject":"Urgent request: system access blocked","body":"Despite multiple attempts, I cannot reset my password. The reset link doesnâ€™t seem to work.","sent_date":"8/19/2025 13:58"},
]

def fix_mojibake(text: str) -> str:
    if not isinstance(text, str):
        return text
    replacements = {
        "â€™": "'",
        "â€“": "-",
        "â€œ": '"',
        "â€": '"',
        "â€˜": "'",
        "â€": '"',
    }
    for bad, good in replacements.items():
        text = text.replace(bad, good)
    return text

def categorize(subject: str, body: str) -> str:
    t = f"{subject} {body}".lower()
    if any(k in t for k in ["server is down", "servers are down", "system access blocked", "inaccessible", "downtime", "system is completely inaccessible", "system access"]):
        return "downtime/outage"
    if any(k in t for k in ["billing", "charged twice", "refund"]):
        return "billing/refund"
    if any(k in t for k in ["verify", "verification"]):
        return "account verification"
    if any(k in t for k in ["login", "log into", "password", "reset link"]):
        return "login/password"
    if any(k in t for k in ["integration", "api", "crm"]):
        return "integration/api"
    if any(k in t for k in ["pricing", "tiers", "breakdown"]):
        return "pricing"
    return "general"

def priority(subject: str, body: str) -> str:
    t = f"{subject} {body}".lower()
    if any(k in t for k in ["urgent", "immediate", "critical", "highly critical"]):
        return "high"
    return "normal"

# Build DataFrame
df = pd.DataFrame(data)
for col in ["subject", "body"]:
    df[col] = df[col].apply(fix_mojibake)
df["sender"] = df["sender"].str.strip().str.lower()
df["sent_dt"] = pd.to_datetime(df["sent_date"], dayfirst=False, errors="coerce")
df = df.drop(columns=["sent_date"])

# Sort and deduplicate (keep earliest per sender+subject+body)
df = df.sort_values("sent_dt", ascending=True)
df = df.drop_duplicates(subset=["sender", "subject", "body"], keep="first").reset_index(drop=True)

# Categorize & prioritize
df["category"] = df.apply(lambda r: categorize(r["subject"], r["body"]), axis=1)
df["priority"] = df.apply(lambda r: priority(r["subject"], r["body"]), axis=1)

# Save outputs
df.to_csv("tickets_cleaned.csv", index=False)
by_category = df.groupby("category").size().reset_index(name="count").sort_values("count", ascending=False)
by_priority = df.groupby("priority").size().reset_index(name="count").sort_values("count", ascending=False)
by_sender_category = df.groupby(["sender","category"]).size().reset_index(name="count").sort_values(["sender","count"], ascending=[True, False])

by_category.to_csv("summary_by_category.csv", index=False)
by_priority.to_csv("summary_by_priority.csv", index=False)
by_sender_category.to_csv("summary_by_sender_category.csv", index=False)

# Optional simple chart
plt.figure()
plt.bar(by_category["category"], by_category["count"])
plt.title("Ticket Count by Category")
plt.xlabel("Category")
plt.ylabel("Count")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("ticket_count_by_category.png")
print("Saved: tickets_cleaned.csv, summary_by_category.csv, summary_by_priority.csv, summary_by_sender_category.csv, ticket_count_by_category.png")
