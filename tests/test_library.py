"""Unit tests for the card library module.

Run with: pytest tests/test_library.py -v
"""

import pytest
from src.core.library import (
    CardTemplate,
    CARD_LIBRARY,
    get_all_templates,
    get_template,
    get_template_choices,
)
from src.core.models import Credit


class TestCardTemplate:
    """Tests for CardTemplate model."""

    def test_card_template_creation(self):
        """Test creating a CardTemplate with all fields."""
        template = CardTemplate(
            id="test_card",
            name="Test Card",
            issuer="Test Bank",
            annual_fee=100,
            credits=[
                Credit(name="Test Credit", amount=10.0, frequency="monthly"),
            ],
        )

        assert template.id == "test_card"
        assert template.name == "Test Card"
        assert template.issuer == "Test Bank"
        assert template.annual_fee == 100
        assert len(template.credits) == 1
        assert template.credits[0].name == "Test Credit"

    def test_card_template_default_credits(self):
        """Test that credits defaults to empty list."""
        template = CardTemplate(
            id="minimal",
            name="Minimal Card",
            issuer="Bank",
            annual_fee=0,
        )

        assert template.credits == []

    def test_card_template_with_multiple_credits(self):
        """Test template with multiple credits."""
        credits = [
            Credit(name="Credit A", amount=10.0, frequency="monthly"),
            Credit(name="Credit B", amount=50.0, frequency="annual"),
            Credit(name="Credit C", amount=25.0, frequency="quarterly", notes="Some note"),
        ]
        template = CardTemplate(
            id="multi_credit",
            name="Multi Credit Card",
            issuer="Bank",
            annual_fee=200,
            credits=credits,
        )

        assert len(template.credits) == 3
        assert template.credits[2].notes == "Some note"


class TestCardLibrary:
    """Tests for the CARD_LIBRARY constant."""

    def test_library_not_empty(self):
        """Test that the library has at least one template."""
        assert len(CARD_LIBRARY) > 0

    def test_amex_platinum_exists(self):
        """Test that Amex Platinum template exists."""
        assert "amex_platinum" in CARD_LIBRARY

    def test_amex_platinum_basic_fields(self):
        """Test Amex Platinum has correct basic fields."""
        template = CARD_LIBRARY["amex_platinum"]

        assert template.id == "amex_platinum"
        assert "Platinum" in template.name
        assert template.issuer == "American Express"
        assert template.annual_fee >= 695  # May vary (currently $895)

    def test_amex_platinum_has_credits(self):
        """Test Amex Platinum has expected credits."""
        template = CARD_LIBRARY["amex_platinum"]

        assert len(template.credits) >= 5, "Amex Platinum should have many credits"

        # Check for some expected credit names
        credit_names = [c.name.lower() for c in template.credits]
        expected_credits = ["uber", "saks", "airline", "digital", "hotel"]

        for expected in expected_credits:
            found = any(expected in name for name in credit_names)
            assert found, f"Expected to find '{expected}' credit"

    def test_amex_platinum_uber_credit(self):
        """Test Amex Platinum Uber credit exists."""
        template = CARD_LIBRARY["amex_platinum"]
        uber_credits = [c for c in template.credits if "uber" in c.name.lower()]

        assert len(uber_credits) >= 1, "Should have at least one Uber credit"

        # Check that at least one has expected properties
        uber = uber_credits[0]
        assert uber.amount > 0
        assert uber.frequency in ["monthly", "annual"]

    def test_amex_platinum_saks_credit(self):
        """Test Amex Platinum Saks credit exists."""
        template = CARD_LIBRARY["amex_platinum"]
        saks_credits = [c for c in template.credits if "saks" in c.name.lower()]

        assert len(saks_credits) >= 1
        assert saks_credits[0].amount > 0

    def test_all_templates_have_required_fields(self):
        """Test all templates have required fields."""
        for template_id, template in CARD_LIBRARY.items():
            assert template.id, f"{template_id}: missing id"
            assert template.name, f"{template_id}: missing name"
            assert template.issuer, f"{template_id}: missing issuer"
            assert template.annual_fee >= 0, f"{template_id}: invalid annual_fee"


class TestGetAllTemplates:
    """Tests for get_all_templates function."""

    def test_returns_list(self):
        """Test that get_all_templates returns a list."""
        result = get_all_templates()
        assert isinstance(result, list)

    def test_returns_card_templates(self):
        """Test that returned items are CardTemplate instances."""
        templates = get_all_templates()
        for template in templates:
            assert isinstance(template, CardTemplate)

    def test_returns_all_templates(self):
        """Test that all library templates are returned."""
        templates = get_all_templates()
        assert len(templates) == len(CARD_LIBRARY)

    def test_templates_match_library(self):
        """Test that returned templates match library entries."""
        templates = get_all_templates()
        template_ids = {t.id for t in templates}
        library_ids = set(CARD_LIBRARY.keys())
        assert template_ids == library_ids


class TestGetTemplate:
    """Tests for get_template function."""

    def test_get_existing_template(self):
        """Test getting an existing template by ID."""
        template = get_template("amex_platinum")

        assert template is not None
        assert template.id == "amex_platinum"
        assert "Platinum" in template.name

    def test_get_nonexistent_template(self):
        """Test getting a non-existent template returns None."""
        result = get_template("nonexistent_card")
        assert result is None

    def test_get_template_with_empty_string(self):
        """Test getting template with empty string returns None."""
        result = get_template("")
        assert result is None

    def test_get_template_case_sensitive(self):
        """Test that template lookup is case-sensitive."""
        # Lowercase should work
        result_lower = get_template("amex_platinum")
        assert result_lower is not None

        # Uppercase should not match
        result_upper = get_template("AMEX_PLATINUM")
        assert result_upper is None


class TestGetTemplateChoices:
    """Tests for get_template_choices function."""

    def test_returns_list_of_tuples(self):
        """Test that function returns list of tuples."""
        choices = get_template_choices()

        assert isinstance(choices, list)
        assert len(choices) > 0

        for choice in choices:
            assert isinstance(choice, tuple)
            assert len(choice) == 2

    def test_tuple_format(self):
        """Test that tuples contain (id, display_name)."""
        choices = get_template_choices()

        for template_id, display_name in choices:
            assert isinstance(template_id, str)
            assert isinstance(display_name, str)
            # Display name should contain template name and issuer
            assert "(" in display_name and ")" in display_name

    def test_amex_platinum_choice(self):
        """Test Amex Platinum is in choices with correct format."""
        choices = get_template_choices()
        amex_choices = [(id, name) for id, name in choices if id == "amex_platinum"]

        assert len(amex_choices) == 1

        template_id, display_name = amex_choices[0]
        assert template_id == "amex_platinum"
        assert "Platinum" in display_name
        assert "American Express" in display_name

    def test_choices_match_library(self):
        """Test that choices cover all library templates."""
        choices = get_template_choices()
        choice_ids = {id for id, _ in choices}

        assert choice_ids == set(CARD_LIBRARY.keys())


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
