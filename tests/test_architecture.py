"""
Architecture Fitness Functions for the 'shop' application.

These tests enforce architectural rules using pytest-archon:

Demo Workflow for Students:
---------------------------
1. Base state: All tests PASS (Green).
2. Demo Step 1 (Model Isolation):
   - Uncomment forbidden import in `src/shop/model/order.py`.
   - ONLY `test_model_must_not_depend_on_other_packages` fails!
3. Demo Step 2 (UI Layer Isolation):
   - Re-comment step 1.
   - Uncomment forbidden import in `src/shop/services/order_service.py`.
   - ONLY `test_ui_isolation` fails!
4. Demo Step 3 (Transitive Dependency Analysis):
   - Demonstrates direct vs. transitive imports:
     - Direct check passes for adapters.
     - Transitive check reveals how a corrupt model transitively poisons adapters!
"""

import pytest
from pytest_archon import archrule


# ==============================================================================
# DEMO STEP 1: Pure Data Model / Entities (Direct Isolation)
# ==============================================================================
def test_model_must_not_depend_on_other_packages():
    """
    STEP 1: The 'model' namespace contains pure data structures and entities.
    It must not import from 'services', 'adapters', or 'ui'.

    DEMO:
    In `src/shop/model/order.py`, uncomment:
      `from shop.services.payment import PaymentService`
    -> Running `pytest` will fail ONLY this test!
    """
    (
        archrule(
            "pure_data_model",
            comment="The data model must not directly import services, adapters, or UI",
        )
        .match("shop.model*")
        .should_not_import("shop.services*")
        .should_not_import("shop.adapters*")
        .should_not_import("shop.ui*")
        .check("shop", only_direct_imports=True)
    )


# ==============================================================================
# DEMO STEP 2: Clean UI Layer Isolation
# ==============================================================================
def test_ui_isolation():
    """
    STEP 2: Backend layers must never depend on the UI presentation layer.

    DEMO:
    In `src/shop/services/order_service.py`, uncomment:
      `from shop.ui.cli import run_cli_checkout_demo`
    -> Running `pytest` will fail ONLY this test!
    """
    (
        archrule(
            "no_ui_leakage",
            comment="Backend layers must not directly import the UI layer",
        )
        .match("shop.model*")
        .match("shop.services*")
        .match("shop.adapters*")
        .should_not_import("shop.ui*")
        .check("shop", only_direct_imports=True)
    )


# ==============================================================================
# DEMO STEP 3: Directional Layering (Adapters must not depend on Services)
# Direct vs. Transitive Comparison
# ==============================================================================
def test_adapters_must_not_depend_directly_on_services():
    """
    Direct check: Persistence adapters must not directly import services.
    Even if 'model' accidentally imports 'services', this test stays GREEN
    because 'adapters' does not directly import 'services'.
    """
    (
        archrule(
            "adapters_direct_isolation",
            comment="Adapters must not directly import application services",
        )
        .match("shop.adapters*")
        .should_not_import("shop.services*")
        .check("shop", only_direct_imports=True)
    )


# ==============================================================================
# DEMO STEP 3: Transitive Dependency Analysis (Aha-Effekt)
# ==============================================================================
def test_transitive_dependency_leakage():
    """
    STEP 3 (Transitive Analysis):
    Shows the difference between direct and transitive inspection.

    Without `only_direct_imports=True`, pytest-archon traverses the entire import chain!
    When 'model/order.py' imports 'PaymentService', then 'adapters' (which imports 'order.py')
    transitively inherits the dependency to 'services':
      shop.adapters.repository -> shop.model.order -> shop.services.payment
    """
    (
        archrule(
            "adapters_transitive_cleanliness",
            comment="Adapters must not transitively depend on services via model",
        )
        .match("shop.adapters*")
        .should_not_import("shop.services*")
        .check("shop")  # checks transitive dependency graph!
    )
