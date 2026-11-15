# Architecture Fitness Functions with Python & pytest-archon

This repository contains a self-contained demonstration of automated architectural fitness functions in Python using [pytest-archon](https://github.com/jwbargsten/pytest-archon).

It demonstrates how package dependencies and architectural boundaries can be enforced directly in unit tests and automated CI pipelines, serving as the Python counterpart to Java's well-known [ArchUnit](https://www.archunit.org/).

---

## 🏛️ Architecture Overview

The demo follows a Clean Architecture / Onion Architecture package layout under `src/shop`:

```
src/
└── shop/
    ├── model/         <-- Core Domain Entities (Pure POPOs)
    │   └── order.py
    ├── adapters/      <-- Secondary / Infrastructure Adapters (Database, external APIs)
    │   └── repository.py
    ├── services/      <-- Application Business Services / Orchestration
    │   ├── order_service.py
    │   └── payment.py
    └── ui/            <-- Entry points / CLI / Web Controllers
        └── cli.py
```

### 🎯 SOLL vs. ⚠️ IST Architecture

![SOLL vs IST Architecture Diagram](docs/images/pytest_archon_soll_ist.svg)

### Architectural Rules Enforced by Tests:

1. **Pure Domain Model (`shop.model`):**
   - The domain model represents the core business logic.
   - It **MUST NOT** import anything from `shop.services`, `shop.adapters`, or `shop.ui`.
2. **Asymmetric Dependency Flow:**
   - `shop.services` **MAY** import `shop.model` and `shop.adapters`.
   - `shop.model` and `shop.adapters` **MUST NOT** import `shop.services` (prevents cyclic dependencies and domain leakage).
3. **UI Isolation (`shop.ui`):**
   - `shop.ui` may call `services` and `model`.
   - Backend layers (`model`, `services`, `adapters`) **MUST NEVER** depend on `shop.ui`.

---

## 🚀 Quickstart

### 1. Prerequisites & Virtual Environment

Python 3.9+ is required.

```bash
# Clone the repository and navigate into it
cd python-archunit-demo

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies (pytest & pytest-archon)
pip install -r requirements.txt
```

### 2. Run the Architectural Fitness Tests (All Green 🟢)

```bash
pytest
```

Output:
```text
tests/test_architecture.py::test_model_must_not_depend_on_other_packages PASSED [ 25%]
tests/test_architecture.py::test_services_may_use_model_but_model_cannot_use_services PASSED [ 50%]
tests/test_architecture.py::test_services_may_use_adapters_but_adapters_cannot_use_services PASSED [ 75%]
tests/test_architecture.py::test_ui_isolation PASSED                     [100%]

============================== 4 passed in 0.01s ===============================
```

---

## 🔴 Live Classroom Demo: Simulating an Architectural Violation

To demonstrate how the automated architecture test catches an illegal dependency:

1. Open [`src/shop/model/order.py`](src/shop/model/order.py).
2. Uncomment line 18:
   ```python
   from shop.services.payment import PaymentService  # ❌ FORBIDDEN DEPENDENCY!
   ```
3. Re-run `pytest`:
   ```bash
   pytest
   ```
4. Observe the test failure:
   ```text
   FAILED Rule 'pure_domain_model':
   - module 'shop.model' has FORBIDDEN import shop.services.payment (matched by glob pattern /shop.services*/)
       from shop.model ↣ shop.model.order ↣ shop.services.payment
   ```
5. Comment line 18 out again and re-run `pytest` to see it turn **Green** again.

---

## 🔍 How the Fitness Functions are Written

In [`tests/test_architecture.py`](tests/test_architecture.py):

```python
from pytest_archon import archrule

def test_model_must_not_depend_on_other_packages():
    """Domain model must remain pure."""
    (
        archrule("pure_domain_model")
        .match("shop.model*")
        .should_not_import("shop.services*")
        .should_not_import("shop.adapters*")
        .should_not_import("shop.ui*")
        .check("shop")
    )

def test_services_may_use_model_but_model_cannot_use_services():
    """Asymmetric dependency: services can call model, but model cannot call services."""
    (
        archrule("model_cannot_depend_on_services")
        .match("shop.model*")
        .should_not_import("shop.services*")
        .check("shop")
    )
```

---

## 🔄 CI/CD Integration

Because `pytest-archon` integrates directly into standard `pytest`, you can add it to any GitHub Actions / GitLab CI pipeline as a build gate:

```yaml
# .github/workflows/architecture.yml
name: Architecture Fitness Functions
on: [push, pull_request]

jobs:
  arch-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest tests/test_architecture.py
```

