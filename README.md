Vendor Pipeline Backend (Django, LLM-Powered)

A production-ready Django REST API for multi-phase, AI-powered vendor evaluation, risk scoring, and compliance mapping.
Modular, LLM-integrated, and optimized for enterprise automation workflows.

🚦 TL;DR — Quickstart
git clone https://github.com/harjin2005/Vendors_pipeline.git
cd Vendors_pipeline

python -m venv venv
venv\Scripts\activate  # Windows
# OR source venv/bin/activate (Mac/Linux)

pip install -r requirements.txt

copy .env.example .env   # Create .env
python manage.py migrate
python manage.py runserver


API will run at: http://127.0.0.1:8000/

📦 Project Structure
vendor_pipeline_django/
│
├── pipeline/
│   ├── models.py
│   ├── views.py
│   ├── tasks/        # Phase 1–5 logic
│   ├── services/     # LLM, vendor collectors, utils
│   └── prompts/      # Prompt templates
│
├── vendor_pipeline/
│   ├── settings.py
│   └── urls.py
│
├── requirements.txt
├── manage.py
└── .env (user-provided, not in repo)

1. 🛠️ Local Setup
1.1 Clone & Environment Setup
git clone https://github.com/harjin2005/Vendors_pipeline.git
cd Vendors_pipeline

python -m venv venv
venv\Scripts\activate

1.2 Install Dependencies
pip install -r requirements.txt

1.3 Configure Environment

Copy the example file:

copy .env.example .env


Edit .env and fill in your secrets:

AZURE_OPENAI_DEPLOYMENT_NAME=YOUR_DEPLOYMENT
AZURE_OPENAI_API_KEY=YOUR_API_KEY
AZURE_OPENAI_ENDPOINT=https://YOUR_RESOURCE.azure.com/

DJANGO_SECRET_KEY=YOUR_SECRET

DB_HOST=localhost
DB_NAME=vendor_pipeline
DB_USER=postgres
DB_PASSWORD=pass


Never commit .env to the repository.

1.4 Run Database Migrations
python manage.py migrate

1.5 Start the API
python manage.py runserver


Visit: http://127.0.0.1:8000/

2. ✔️ Vendor Pipeline Usage
2.1 Create a New Evaluation Task

POST /api/tasks/

Example body:

{
  "user_id": "abc123",
  "task_description": "Evaluate vendor ABC for cybersecurity compliance"
}


Returns: Task ID

2.2 Run Each Pipeline Phase

Run in order:

Phase 1 — Vendor Discovery
POST /api/tasks/{task_id}/phase1/

Phase 2 — Timeline Analysis
POST /api/tasks/{task_id}/phase2/

Phase 3 — Subtask Decomposition
POST /api/tasks/{task_id}/phase3/

Phase 4 — Capability Mapping
POST /api/tasks/{task_id}/phase4/

Phase 5 — Final LLM Risk & Compliance Assessment
POST /api/tasks/{task_id}/phase5/


Each phase enriches and stores the results.

2.3 Retrieve Final Combined Report
GET /api/tasks/{task_id}/report/


Sample Python/Windows CMD Test Commands
1. Create a Vendor Task (Phase 0)
text
curl -X POST http://127.0.0.1:8000/api/tasks/ ^
-H "Content-Type: application/json" ^
-d "{\"user_id\": \"testuser01\", \"task_description\": \"Assess SAP vendor for compliance\"}"
2. Run Phase 1 (Discovery)
text
curl -X POST http://127.0.0.1:8000/api/tasks/1/phase1/
(Replace 1 with the actual task id returned in step 1)

3. Run Phase 2 (Timeline Analysis)
text
curl -X POST http://127.0.0.1:8000/api/tasks/1/phase2/
4. Run Phase 3 (Subtask Decomposition)
text
curl -X POST http://127.0.0.1:8000/api/tasks/1/phase3/
5. Run Phase 4 (Capability Mapping)
text
curl -X POST http://127.0.0.1:8000/api/tasks/1/phase4/
6. Run Phase 5 (AI Risk Final LLM Analysis)
text
curl -X POST http://127.0.0.1:8000/api/tasks/1/phase5/
7. Get Final Vendor Report
text
curl http://127.0.0.1:8000/api/tasks/1/report/

Batch Pipeline Example (Windows CMD)
:: === Pipeline Demo Batch ===
curl -X POST http://127.0.0.1:8000/api/tasks/ ^
-H "Content-Type: application/json" ^
-d "{\"user_id\": \"demo\", \"task_description\": \"Vendor Y automation\"}"

curl -X POST http://127.0.0.1:8000/api/tasks/2/phase1/
curl -X POST http://127.0.0.1:8000/api/tasks/2/phase2/
curl -X POST http://127.0.0.1:8000/api/tasks/2/phase3/
curl -X POST http://127.0.0.1:8000/api/tasks/2/phase4/
curl -X POST http://127.0.0.1:8000/api/tasks/2/phase5/
curl http://127.0.0.1:8000/api/tasks/2/report/


Returns a merged JSON report including:

All phase outputs

AI scoring

Risk, gap, and compliance summary

Vendor intelligence insights

3. 🧑‍💻 Developer Notes

Modular, extensible architecture

Business logic in: /pipeline/tasks/ and /pipeline/services/

Add new phases by:

Creating a prompt in /pipeline/prompts/

Adding logic under /pipeline/tasks/

Registering a new API endpoint

Perfect for AI automation products and SaaS platforms.

4. 🏆 Example CLI Workflow (httpie)
# Start server
python manage.py runserver

# Create a new vendor task
http POST http://127.0.0.1:8000/api/tasks/ \
    user_id="demo" \
    task_description="Vendor Z assessment"

# Run all 5 phases
http POST http://127.0.0.1:8000/api/tasks/{id}/phase1/
http POST http://127.0.0.1:8000/api/tasks/{id}/phase2/
http POST http://127.0.0.1:8000/api/tasks/{id}/phase3/
http POST http://127.0.0.1:8000/api/tasks/{id}/phase4/
http POST http://127.0.0.1:8000/api/tasks/{id}/phase5/

# Fetch final report
http GET http://127.0.0.1:8000/api/tasks/{id}/report/


Also compatible with:
curl, Postman, Insomnia, and Swagger UI (if enabled).

5. 🛡️ Security Best Practices

Keep .env secret — never push to GitHub

API keys are loaded securely at runtime

Add authentication before deploying to production

Use HTTPS + reverse proxy (Nginx) for enterprise setups

6. 🔥 Advanced / Production Deployment

Use Postgres/MySQL in production

Deploy via Gunicorn or Uvicorn + Nginx

Add CI/CD (GitHub Actions recommended)

Optional Docker scaling (compose not included)

Add JWT/OAuth authentication for clients

7. 🤝 Community & Support

For issues or contributions, open a GitHub issue or PR.
Maintainer: Harjinder Singh

8. 📜 License

MIT License

“Build fast, test smarter, automate everything.”
