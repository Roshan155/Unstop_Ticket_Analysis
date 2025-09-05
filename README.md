Coding Case — Ticket Cleaning & Categorization

repo Structure :
unstop-ticket-analysis/
│
├── README.md
├── unstop_solution.py
├── data/
│   └── sample_input.csv         
├── outputs/
│   ├── tickets_cleaned.csv
│   ├── summary_by_category.csv
│   ├── summary_by_priority.csv
│   └── summary_by_sender_category.csv

Notes:
- We fixed common encoding artifacts (â€™ -> '). 
- We parse dates, deduplicate repeated emails from the same sender with identical subject+body (keeping earliest).
- We classify into categories: downtime/outage, billing/refund, account verification, login/password, integration/api, pricing, general.
- Priority is 'high' if text contains urgent/immediate/critical; otherwise 'normal'.
