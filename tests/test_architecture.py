"""
Architecture Fitness Functions for the 'shop' application.

These tests enforce architectural constraints and package dependency rules
using pytest-archon (the Python equivalent of Java's ArchUnit).

Enforced rules:
1. Pure Domain Model: 'shop.model' must NOT depend on any other shop package
   (services, adapters, ui, etc.).
2. Directional Layering / Dependency Inversion:
   - 'shop.services' MAY import 'shop.model' and 'shop.adapters'
   - But 'shop.adapters' and 'shop.model' MUST NOT import 'shop.services'
3. UI Separation: 'shop.ui' may access services and models, but no backend layer
   may ever access 'shop.ui'.
"""

import pytest
from pytest_archon import archrule


# ==============================================================================
# USE CASE 1: Pure Domain Model (Strict Isolation)
# ==============================================================================
def test_model_must_not_depend_on_other_packages():
    """
    USE CASE 1: The 'model' namespace represents pure domain business logic.
    It MUST NOT depend on any other namespace of the application.
    
    DEMO:
    To see this test FAIL (Red):
      In `src/shop/model/order.py`, uncomment:
        `from shop.services.payment import PaymentService`
      and run `pytest`.
    
    To see this test PASS (Green):
      Comment the import out again and re-run `pytest`.
    """
    (
        archrule(
            "pure_domain_model",
            comment="The domain model must not import services, adapters, or UI",
        )
        .match("shop.model*")
        .should_not_import("shop.services*")
        .should_not_import("shop.adapters*")
        .should_not_import("shop.ui*")
        .check("shop")
    )


# ==============================================================================
# USE CASE 2: Asymmetric Dependency (One namespace may use another, but not vice-versa)
# ==============================================================================
def test_services_may_use_model_but_model_cannot_use_services():
    """
    USE CASE 2: Asymmetric Dependency.
    - 'services' is an orchestration layer and IS ALLOWED to import 'model'.
    - 'model' is NEVER allowed to import 'services'.
    """
    # 1. Negative constraint: model cannot import services
    (
        archrule(
            "model_cannot_depend_on_services",
            comment="Domain model entities cannot call application services",
        )
        .match("shop.model*")
        .should_not_import("shop.services*")
        .check("shop")
    )


def test_services_may_use_adapters_but_adapters_cannot_use_services():
    """
    Another Asymmetric Dependency example:
    - 'services' uses 'adapters' (e.g. repositories for data persistence).
    - But 'adapters' MUST NOT depend on 'services' (prevents cyclic dependencies).
    """
    (
        archrule(
            "adapters_must_not_depend_on_services",
            comment="Persistence adapters must not depend back on application services",
        )
        .match("shop.adapters*")
        .should_not_import("shop.services*")
        .check("shop")
    )


# ==============================================================================
# USE CASE 3: Clean UI Layer Isolation
# ==============================================================================
def test_ui_isolation():
    """
    Core business logic must not depend on UI presentations:
    - Neither 'model', 'services', nor 'adapters' may import 'shop.ui'.
    """
    (
        archrule(
            "no_ui_leakage",
            comment="No backend module may depend on the UI layer",
        )
        .match("shop.model*")
        .match("shop.services*")
        .match("shop.adapters*")
        .should_not_import("shop.ui*")
        .check("shop")
    )
