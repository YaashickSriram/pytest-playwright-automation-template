# Automation Framework Template

A production-grade **Business Process Validation Framework** built with
Playwright + pytest + Allure. Designed to be adopted by any project team
in minutes, with Sauce Demo and ReqRes.in reference implementations
included out of the box.

---

## Table of Contents

- [What You Get](#what-you-get)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Project Setup](#project-setup)
- [First Run — Verify Everything Works](#first-run--verify-everything-works)
- [Reference Implementations](#reference-implementations)
- [Running Tests](#running-tests)
- [Allure Reports](#allure-reports)
- [Adapting the Framework to Your Application](#adapting-the-framework-to-your-application)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)

---

## What You Get

**Framework infrastructure (ready to use):**
- Layered architecture: Test → Workflow → Page → Service → Data → Utility
- Multi-environment config switching with `.env` secret resolution
- Structured dual-output logging (console + file)
- Allure reporting with automatic step decoration
- Auto screenshot capture on test failure
- Parallel test execution via pytest-xdist
- Base classes for pages, workflows, API clients, validators, factories

**Reference implementations (ready to run):**
- **UI tests** — 11 Sauce Demo scenarios (login + shopping flows)
- **API tests** — 5 ReqRes.in scenarios (full CRUD coverage)
- All demonstrating correct framework usage patterns

**What you build:**
- Your application-specific page objects, workflows, factories, and tests

---

## Architecture

The framework is organised in six layers. Each layer has one responsibility.

| Layer | Responsibility | Example Files |
|---|---|---|
| **Test** | Business intent — what to test | `tests/login/test_login.py` |
| **Workflow** | Orchestration — how to sequence actions | `workflows/login_workflow.py` |
| **Page** | UI interactions — owns all selectors | `pages/login_page.py` |
| **Service** | External systems + structured assertions | `services/api/`, `services/validators/` |
| **Data** | Factories and fixtures — test data contracts | `data/factories/user_factory.py` |
| **Utility** | Logging, Allure, screenshots, waits | `utils/logger.py` |

**Key rule:** When something changes in your application, exactly **one file**
changes in the framework. If a button's selector changes — only the page object
changes. If credentials change — only `.env` changes. If a business flow changes —
only the workflow changes.

---

## Prerequisites

| Tool | Version | How to install |
|---|---|---|
| Python | 3.11+ | https://python.org |
| Microsoft Edge | Latest | Pre-installed on Windows 11 |
| Java JDK | 21 (LTS) | Via Scoop (see below) |
| Allure CLI | 2.39+ | Via Scoop (see below) |
| Git | Latest | https://git-scm.com |

**Install Scoop (Windows, no admin required):**

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression
```

**Install Java and Allure via Scoop:**

```powershell
scoop bucket add java
scoop install temurin21-jdk
scoop install allure
```

Verify:

```powershell
java -version
allure --version
```

---

## Project Setup

### 1. Clone or extract the framework

```powershell
cd automation-framework-template
```

### 2. Create and activate virtual environment

```powershell
python -m venv venv
venv\Scripts\activate
```

Your prompt should show `(venv)` prefix.

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Install Playwright browser

```powershell
playwright install chromium
```

### 5. Create your `.env` file from the template

```powershell
copy .env.example .env
```

The provided `.env.example` is pre-configured for Sauce Demo and ReqRes.in.
No changes needed to run the reference tests.

### 6. Verify installation

```powershell
python -c "
from pages.base_page import BasePage
from workflows.base_workflow import BaseWorkflow
from services.api.base_client import BaseAPIClient
from services.validators.base_validator import BaseValidator
from data.factories.base_factory import BaseFactory
print('All framework base classes loaded successfully')
"
```

---

## First Run — Verify Everything Works

### Run the API test suite (fastest, no browser)

```powershell
pytest tests/api_examples/ -v --env=dev
```

Expected: 5 tests pass in under 5 seconds.

### Run the UI test suite (with browser visible)

```powershell
pytest tests/login/ tests/shopping/ -v --env=dev --headed --slowmo=300
```

Expected: 11 tests pass. Edge opens, performs each flow visually.

### Run everything together

```powershell
pytest tests/ -v --env=dev
```

Expected: 16 tests pass (5 API + 6 shopping + 5 login).

---

## Reference Implementations

### Sauce Demo UI Tests (11 scenarios)

**Login module** (`tests/login/test_login.py`):
- Standard user happy path
- Locked out user rejection
- Invalid credentials rejection
- Empty credentials validation
- Logout flow

**Shopping module** (`tests/shopping/test_shopping.py`):
- Add single product to cart
- Add multiple products
- Remove product from cart
- Cart contents verification
- Add all catalog products
- Parametrized per-product validation (6 products × 1 test = 6 result rows)

### ReqRes.in API Tests (5 scenarios)

**Users API** (`tests/api_examples/test_reqres_api.py`):
- List users (pagination)
- Get single user by ID
- Create user (POST)
- Update user (PUT)
- Delete user (DELETE)

---

## Running Tests

### By folder

```powershell
pytest tests/login/ -v --env=dev
pytest tests/shopping/ -v --env=dev
pytest tests/api_examples/ -v --env=dev
```

### By suite tag

```powershell
pytest -m smoke --env=dev           # fastest gate — core flows
pytest -m critical --env=dev        # PR merge gate
pytest -m regression --env=dev      # full coverage
pytest -m "login" --env=dev         # login module only
pytest -m "shopping" --env=dev      # shopping module only
pytest -m "api" --env=dev           # API tests only
```

### Combined markers

```powershell
pytest -m "critical and not api" --env=dev
pytest -m "smoke or critical" --env=dev
```

### Headed browser (visible — demo/debugging)

```powershell
pytest tests/login/ -v --env=dev --headed --slowmo=500
```

### Parallel execution

```powershell
pytest tests/ -v --env=dev -n 2       # 2 workers
pytest tests/ -v --env=dev -n auto    # auto-detect CPU count
```

### Switch environments

```powershell
pytest tests/ --env=uat       # loads config/environments/uat.yaml
pytest tests/ --env=dev       # loads config/environments/dev.yaml
```

---

## Allure Reports

```powershell
# Run tests
pytest tests/ -v --env=dev

# Generate HTML report
allure generate reports/allure-results --output reports/allure-report --clean

# Serve report in browser (auto-opens)
allure serve reports/allure-results
```

The report provides:
- Overview with pass rate, trend, duration
- Suites view — tests grouped by folder
- Behaviors view — tests grouped by `@allure.feature` and `@allure.story`
- Timeline with per-test duration
- Attachments (step logs, screenshots, API payloads)

---

## Adapting the Framework to Your Application

The reference implementations are intentionally simple so you can see the
patterns clearly. To adapt the framework to your project:

### Step 1 — Update `.env` and `dev.yaml`

```ini
# .env
APP_BASE_URL=https://your-app-url.com
APP_ADMIN_USER=your_admin
APP_ADMIN_PASS=your_password
```

```yaml
# config/environments/dev.yaml
base_url: "${APP_BASE_URL}"
users:
  admin:
    username: "${APP_ADMIN_USER}"
    password: "${APP_ADMIN_PASS}"
```

### Step 2 — Create your first page object

```python
# pages/your_login_page.py
from pages.base_page import BasePage
from utils.allure_helper import step

class YourLoginPage(BasePage):
    USERNAME_INPUT = "#your-username-field"
    PASSWORD_INPUT = "#your-password-field"
    LOGIN_BUTTON   = "#your-login-button"

    @step("Enter credentials")
    def login(self, username, password):
        self.fill(self.USERNAME_INPUT, username)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
```

### Step 3 — Create your workflow

```python
# workflows/your_login_workflow.py
from workflows.base_workflow import BaseWorkflow
from pages.your_login_page import YourLoginPage

class YourLoginWorkflow(BaseWorkflow):
    def __init__(self, page, app_config):
        super().__init__(page, app_config)
        self.login_page = YourLoginPage(page, base_url=self.base_url)

    def login(self, username, password):
        self.base_page.navigate("/login")
        self.login_page.login(username, password)
```

### Step 4 — Create your test

```python
# tests/your_module/test_your_feature.py
import pytest
import allure
from workflows.your_login_workflow import YourLoginWorkflow

@pytest.fixture
def workflow(page, app_config):
    return YourLoginWorkflow(page, app_config)

@pytest.mark.smoke
@allure.feature("Your Feature")
def test_login(workflow, app_config):
    creds = app_config["users"]["admin"]
    workflow.login(creds["username"], creds["password"])
    # assertions here
```

### Step 5 — Run it

```powershell
pytest tests/your_module/ -v --env=dev --headed
```

### What you should NOT modify

| File | Why |
|---|---|
| `conftest.py` (root) | Fixture wiring — framework level |
| `pytest.ini` | Add markers only, no other changes |
| `pages/base_page.py` | Framework base class |
| `workflows/base_workflow.py` | Framework base class |
| `services/validators/base_validator.py` | Framework base class |
| `services/api/base_client.py` | Framework base class |
| `data/factories/base_factory.py` | Framework base class |
| `utils/*` | Framework utilities |
| `config/config_loader.py` | Framework config engine |

If you find yourself needing to modify these, raise an issue — the pattern
should extend them via inheritance, not modify them.

---

## Project Structure

```
automation-framework-template/
│
├── tests/                              # Test layer — business intent only
│   ├── login/
│   │   └── test_login.py               # 5 Sauce Demo login scenarios
│   ├── shopping/
│   │   └── test_shopping.py            # 6 Sauce Demo shopping scenarios
│   └── api_examples/
│       └── test_reqres_api.py          # 5 ReqRes.in API scenarios
│
├── pages/                              # Page Object Model — owns selectors
│   ├── base_page.py                    # 20+ reusable browser interactions
│   ├── login_page.py                   # Sauce Demo login page
│   ├── inventory_page.py               # Sauce Demo inventory page
│   └── cart_page.py                    # Sauce Demo cart page
│
├── workflows/                          # Business orchestration layer
│   ├── base_workflow.py                # Config access, step logging
│   ├── login_workflow.py               # Sauce Demo login orchestration
│   └── shopping_workflow.py            # Sauce Demo shopping orchestration
│
├── services/
│   ├── api/
│   │   ├── base_client.py              # Generic HTTP client
│   │   └── reqres_api_client.py        # ReqRes.in API client example
│   └── validators/
│       ├── base_validator.py           # Structured ✓ PASS / ✗ FAIL engine
│       └── login_validator.py          # Login-specific assertions example
│
├── data/
│   ├── factories/
│   │   ├── base_factory.py             # Data generation base
│   │   ├── user_factory.py             # Sauce Demo user credentials
│   │   └── product_factory.py          # Sauce Demo product catalog
│   └── fixtures/                       # (Place JSON fixtures here)
│
├── config/
│   ├── environments/
│   │   ├── dev.yaml                    # Dev environment profile
│   │   └── uat.yaml                    # UAT environment profile
│   ├── config_loader.py                # Singleton config + secret resolution
│   └── settings.py                     # Global paths and constants
│
├── utils/
│   ├── logger.py                       # Structured logging
│   ├── allure_helper.py                # @step decorator + attachments
│   ├── screenshot_helper.py            # Auto-capture on failure
│   └── waiter.py                       # Condition-based wait strategies
│
├── reports/                            # Runtime artifacts (git-ignored)
│   ├── allure-results/
│   ├── allure-report/
│   ├── screenshots/
│   └── execution.log
│
├── conftest.py                         # Root fixtures + failure hook
├── pytest.ini                          # Markers, test paths, Allure config
├── requirements.txt                    # Pinned dependencies
├── .env.example                        # Template — copy to .env
├── .gitignore
└── README.md                           # This file
```

---

## Troubleshooting

### Sauce Demo tests fail with network error

Sauce Demo (`https://www.saucedemo.com`) is a public site but requires internet
access. If you are on a corporate network with proxy restrictions, configure
Playwright proxy settings or whitelist `saucedemo.com`.

### ReqRes.in API tests return 401

ReqRes requires an API key header. The `.env.example` includes a free key.
Make sure you copied `.env.example` to `.env`.

### `Allure CLI not found`

Verify Allure is installed and on your PATH:
```powershell
allure --version
```
If missing, install via Scoop as described in Prerequisites.

### Browser launch fails

The framework uses system Microsoft Edge by default (`channel="msedge"`).
If Edge is not installed, change `conftest.py` to use Chromium:
```python
browser = p.chromium.launch(headless=headless, slow_mo=slowmo)
```

### `KeyError` when loading config

Check that your `.env` file exists in the project root and contains the
expected variables. Compare with `.env.example`.

### Allure report shows no data

Ensure `--alluredir=reports/allure-results` is in `pytest.ini` under `addopts`.
This is set by default. Run `pytest` and check that `reports/allure-results/`
is populated.

---

## Dependencies

```
playwright==1.58.0
pytest==8.2.0
pytest-playwright==0.5.0
pytest-xdist==3.5.0
allure-pytest==2.13.5
PyYAML==6.0.1
python-dotenv==1.0.1
requests==2.32.3
```

---

## Contact

For framework questions, raise an issue in the template repository.
For adoption support in your project, contact the QA Automation platform owner.
