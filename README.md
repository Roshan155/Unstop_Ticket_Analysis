Coding Case — Ticket Cleaning & Categorization

How to run:
1) Requirements: Python 3.x, pandas, matplotlib
2) Run:  python unstop_solution.py
3) Outputs generated in the same folder:
   - tickets_cleaned.csv
   - summary_by_category.csv
   - summary_by_priority.csv
   - summary_by_sender_category.csv
   - ticket_count_by_category.png

Notes:
- We fixed common encoding artifacts (â€™ -> '). 
- We parse dates, deduplicate repeated emails from the same sender with identical subject+body (keeping earliest).
- We classify into categories: downtime/outage, billing/refund, account verification, login/password, integration/api, pricing, general.
- Priority is 'high' if text contains urgent/immediate/critical; otherwise 'normal'.
