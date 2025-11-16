<div align="center">

# 🚀 Vendor Pipeline Backend
### AI-Powered Vendor Evaluation & Risk Assessment System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?style=for-the-badge&logo=python)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/Django-4.2+-green.svg?style=for-the-badge&logo=django)](https://www.djangoproject.com/)
[![Azure OpenAI](https://img.shields.io/badge/Azure-OpenAI-orange.svg?style=for-the-badge&logo=microsoft-azure)](https://azure.microsoft.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

**Enterprise-grade Django REST API for intelligent vendor evaluation, compliance mapping, and risk scoring powered by LLMs**

[Quick Start](#-quick-start) • [Features](#-features) • [API Docs](#-api-endpoints) • [Examples](#-usage-examples) • [Deploy](#-deployment)

</div>

---

## 🎯 What is This?

Ever wondered how to automatically evaluate vendors for compliance, security risks, and capabilities using AI? This pipeline does exactly that!

**Think of it as your AI-powered vendor assessment assistant** that:
- 🔍 Discovers vendor intelligence automatically
- 📊 Analyzes historical timelines and patterns
- 🧠 Uses Azure OpenAI to assess risks and compliance
- 📝 Generates comprehensive evaluation reports
- ⚡ Provides a clean REST API for integration

Perfect for **security teams, procurement, and compliance officers** who need to assess vendors at scale.

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🤖 AI-Powered
- **Azure OpenAI Integration**
- Intelligent risk scoring
- Natural language analysis
- Automated compliance checks

</td>
<td width="50%">

### 🏗️ Production-Ready
- **Django REST Framework**
- Modular architecture
- PostgreSQL/SQLite support
- Comprehensive logging

</td>
</tr>
<tr>
<td width="50%">

### 📊 5-Phase Pipeline
1. **Discovery** - Vendor intelligence gathering
2. **Timeline** - Historical analysis
3. **Decomposition** - Capability breakdown
4. **Mapping** - Gap analysis
5. **Assessment** - Final AI evaluation

</td>
<td width="50%">

### 🔌 Easy Integration
- **RESTful API**
- JSON responses
- Clear documentation
- Copy-paste commands

</td>
</tr>
</table>

---

## 🚦 Quick Start

### ⚡ Get Running in 5 Minutes

```bash
# 1️⃣ Clone the repo
git clone https://github.com/harjin2005/Vendors_pipeline.git
cd Vendors_pipeline

# 2️⃣ Set up virtual environment
python -m venv venv
venv\\Scripts\\activate          # Windows
# source venv/bin/activate     # Mac/Linux

# 3️⃣ Install dependencies
pip install -r requirements.txt

# 4️⃣ Configure environment
copy .env.example .env         # Windows
# cp .env.example .env         # Mac/Linux

# Edit .env with your Azure OpenAI credentials

# 5️⃣ Set up database
python manage.py migrate

# 6️⃣ Start the server
python manage.py runserver
```

✅ **You're ready!** API running at `http://127.0.0.1:8000/`

---

## 📁 Project Structure

```
Vendors_pipeline/
│
├── 🎯 vendor_pipeline/              # Django settings
│   ├── settings.py                  # Configuration
│   ├── urls.py                      # URL routing
│   └── wsgi.py                      # WSGI config
│
├── 🔧 pipeline/                     # Main app
│   ├── models.py                    # Database models
│   ├── views.py                     # API endpoints
│   ├── serializers.py               # Data serialization
│   │
│   ├── 📦 tasks/                    # Phase implementations
│   │   ├── phase1_discovery.py      # Vendor discovery
│   │   ├── phase2_timeline.py       # Timeline analysis
│   │   ├── phase3_subtask.py        # Subtask decomposition
│   │   ├── phase4_capability.py     # Capability mapping
│   │   └── phase5_assessment.py     # Final AI assessment
│   │
│   ├── 🛠️ services/                 # Business logic
│   │   ├── llm_service.py           # Azure OpenAI integration
│   │   ├── vendor_collector.py      # Data collection
│   │   └── utils.py                 # Helper functions
│   │
│   └── 💬 prompts/                 # LLM prompts
│       └── phase*.txt               # Prompt templates
│
├── 📋 requirements.txt              # Dependencies
├── 🔧 manage.py                     # Django CLI
├── 🔒 .env.example                  # Environment template
└── 📖 README.md                     # You are here!
```

---

## 🔌 API Endpoints

| Method | Endpoint | What It Does | Example |
|--------|----------|--------------|---------|  
| `POST` | `/api/tasks/` | Create new evaluation | Create task for "SAP vendor" |
| `GET` | `/api/tasks/{id}/` | Get task details | Check task status |
| `POST` | `/api/tasks/{id}/phase1/` | 🔍 Run Discovery | Find vendor info |
| `POST` | `/api/tasks/{id}/phase2/` | 📈 Run Timeline | Analyze history |
| `POST` | `/api/tasks/{id}/phase3/` | 🧩 Run Decomposition | Break down capabilities |
| `POST` | `/api/tasks/{id}/phase4/` | 🗺️ Run Mapping | Map capabilities |
| `POST` | `/api/tasks/{id}/phase5/` | 🤖 Run AI Assessment | Final risk analysis |
| `GET` | `/api/tasks/{id}/report/` | 📄 Get Full Report | Complete evaluation |

---

## 💻 Usage Examples

### 📌 Example 1: Quick Test (Windows)

```cmd
REM Create a vendor evaluation task
curl -X POST http://127.0.0.1:8000/api/tasks/ ^
  -H "Content-Type: application/json" ^
  -d "{\"user_id\": \"demo\", \"task_description\": \"Evaluate Microsoft Azure for security compliance\"}"

REM Response will give you a task ID, use it below (e.g., ID = 1)

REM Run the pipeline phases
curl -X POST http://127.0.0.1:8000/api/tasks/1/phase1/
curl -X POST http://127.0.0.1:8000/api/tasks/1/phase2/
curl -X POST http://127.0.0.1:8000/api/tasks/1/phase3/
curl -X POST http://127.0.0.1:8000/api/tasks/1/phase4/
curl -X POST http://127.0.0.1:8000/api/tasks/1/phase5/

REM Get final report
curl http://127.0.0.1:8000/api/tasks/1/report/
```

### 🚀 Example 2: Automated Pipeline (Windows Batch Script)

Create `run_pipeline.bat`:

```batch
@echo off
echo.
echo ========================================
echo   🚀 Vendor Pipeline Automation
echo ========================================
echo.

echo 📝 Creating evaluation task...
curl -X POST http://127.0.0.1:8000/api/tasks/ ^
  -H "Content-Type: application/json" ^
  -d "{\"user_id\": \"automation\", \"task_description\": \"Assess vendor for ISO 27001 compliance\"}"
echo.

REM Replace with actual task ID from response
set TASK_ID=1

echo.
echo 🔍 Phase 1: Vendor Discovery...
curl -s -X POST http://127.0.0.1:8000/api/tasks/%TASK_ID%/phase1/
echo ✅ Phase 1 Complete
echo.

echo 📊 Phase 2: Timeline Analysis...
curl -s -X POST http://127.0.0.1:8000/api/tasks/%TASK_ID%/phase2/
echo ✅ Phase 2 Complete
echo.

echo 🧩 Phase 3: Subtask Decomposition...
curl -s -X POST http://127.0.0.1:8000/api/tasks/%TASK_ID%/phase3/
echo ✅ Phase 3 Complete
echo.

echo 🗺️ Phase 4: Capability Mapping...
curl -s -X POST http://127.0.0.1:8000/api/tasks/%TASK_ID%/phase4/
echo ✅ Phase 4 Complete
echo.

echo 🤖 Phase 5: AI Risk Assessment...
curl -s -X POST http://127.0.0.1:8000/api/tasks/%TASK_ID%/phase5/
echo ✅ Phase 5 Complete
echo.

echo 📄 Fetching Final Report...
curl http://127.0.0.1:8000/api/tasks/%TASK_ID%/report/ > report_%TASK_ID%.json
echo.

echo ========================================
echo   ✨ Pipeline Complete!
echo   📄 Report saved: report_%TASK_ID%.json
echo ========================================
```

**Run it:**
```cmd
run_pipeline.bat
```

### 🐧 Example 3: Linux/Mac Automation

Create `run_pipeline.sh`:

```bash
#!/bin/bash

echo ""
echo "========================================"
echo "  🚀 Vendor Pipeline Automation"
echo "========================================"
echo ""

echo "📝 Creating evaluation task..."
RESPONSE=$(curl -s -X POST http://127.0.0.1:8000/api/tasks/ \
  -H "Content-Type: application/json" \
  -d '{"user_id": "automation", "task_description": "Vendor compliance assessment"}')

TASK_ID=$(echo $RESPONSE | grep -o '"id":[0-9]*' | grep -o '[0-9]*')
echo "✅ Task created with ID: $TASK_ID"
echo ""

echo "🔍 Phase 1: Discovery..."
curl -s -X POST http://127.0.0.1:8000/api/tasks/$TASK_ID/phase1/ > /dev/null
echo "✅ Complete"

echo "📊 Phase 2: Timeline..."
curl -s -X POST http://127.0.0.1:8000/api/tasks/$TASK_ID/phase2/ > /dev/null
echo "✅ Complete"

echo "🧩 Phase 3: Decomposition..."
curl -s -X POST http://127.0.0.1:8000/api/tasks/$TASK_ID/phase3/ > /dev/null
echo "✅ Complete"

echo "🗺️ Phase 4: Mapping..."
curl -s -X POST http://127.0.0.1:8000/api/tasks/$TASK_ID/phase4/ > /dev/null
echo "✅ Complete"

echo "🤖 Phase 5: Assessment..."
curl -s -X POST http://127.0.0.1:8000/api/tasks/$TASK_ID/phase5/ > /dev/null
echo "✅ Complete"

echo ""
echo "📄 Generating final report..."
curl -s http://127.0.0.1:8000/api/tasks/$TASK_ID/report/ | jq '.' > report_$TASK_ID.json

echo ""
echo "========================================"
echo "  ✨ Pipeline Complete!"
echo "  📄 Report: report_$TASK_ID.json"
echo "========================================"
```

**Make it executable and run:**
```bash
chmod +x run_pipeline.sh
./run_pipeline.sh
```

---

## ⚙️ Configuration

### 🔐 Environment Variables

Create `.env` file in project root:

```env
# 🔑 Azure OpenAI Configuration
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/

# 🔧 Django Settings
DJANGO_SECRET_KEY=your-django-secret-key
DEBUG=True                              # Set False in production
ALLOWED_HOSTS=localhost,127.0.0.1

# 💾 Database (SQLite for development)
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# 💾 Database (PostgreSQL for production)
# DB_ENGINE=django.db.backends.postgresql
# DB_HOST=localhost
# DB_PORT=5432
# DB_NAME=vendor_pipeline
# DB_USER=postgres
# DB_PASSWORD=your-secure-password
```

### 🔑 Generate Django Secret Key

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## 🚀 Deployment

### 🐳 Docker Deployment

**Dockerfile:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static files & migrate
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

EXPOSE 8000

# Run with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "vendor_pipeline.wsgi:application"]
```

**Build & Run:**
```bash
# Build image
docker build -t vendor-pipeline .

# Run container
docker run -p 8000:8000 --env-file .env vendor-pipeline
```

### ☁️ Production Checklist

- [ ] Set `DEBUG=False` in `.env`
- [ ] Update `ALLOWED_HOSTS` with your domain
- [ ] Use PostgreSQL instead of SQLite
- [ ] Set up HTTPS with SSL certificate
- [ ] Configure Nginx reverse proxy
- [ ] Enable Django security middleware
- [ ] Set up monitoring & logging
- [ ] Implement JWT/OAuth authentication
- [ ] Configure CORS for frontend
- [ ] Set up automated backups

---

## 👨‍💻 Development

### 🧪 Running Tests

```bash
# Run all tests
python manage.py test

# Run specific phase test
python manage.py test pipeline.tests.test_phase1
```

### 🔧 Useful Commands

```bash
# Create superuser
python manage.py createsuperuser

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Start Django shell
python manage.py shell

# Collect static files
python manage.py collectstatic
```

---

## 🔒 Security

- ❌ **Never commit `.env` file** - Add it to `.gitignore`
- 🔑 **Rotate API keys regularly**
- 🔒 **Use environment variables** for all secrets
- 🏛️ **Implement authentication** before production
- 🔐 **Enable HTTPS** in production
- 🛡️ **Use Django security middleware**
- 📊 **Monitor API usage** and rate limits

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📜 License

MIT License - see [LICENSE](LICENSE) file for details

---

## 🚀 Built With

- **Django REST Framework** - Backend API
- **Azure OpenAI** - LLM Intelligence
- **PostgreSQL** - Production Database
- **Gunicorn** - WSGI Server
- **Docker** - Containerization

---

## 📞 Support

For issues, questions, or contributions:
- 🐛 **Open an issue** on GitHub
- 📧 **Email**: [Your Email]
- 👤 **Maintainer**: Harjinder Singh ([@harjin2005](https://github.com/harjin2005))

---

<div align="center">

**⭐ Star this repo if you find it helpful!**

*"Build fast, test smarter, automate everything."*

Made with ❤️ for the AI & Automation Community

</div>
