"""Unit tests for CardStorage.add_card_from_template and Card nickname field.

Run with: pytest tests/test_storage_library.py -v
"""

import pytest
import tempfile
import shutil
from datetime import date
from pathlib import Path

from src.core.storage import CardStorage
from src.core.models import Card, SignupBonus, Credit
from src.core.library import CardTemplate, get_template


class TestCardNickname:
    """Tests for Card model nickname field."""

    def test_card_with_nickname(self):
        """Test creating a Card with a nickname."""
        card = Card(
            id="test-123",
            name="Test Card",
            nickname="My Test Card",
            issuer="Test Bank",
            annual_fee=100,
        )

        assert card.nickname == "My Test Card"

    def test_card_without_nickname(self):
        """Test creating a Card without nickname defaults to None."""
        card = Card(
            id="test-123",
            name="Test Card",
            issuer="Test Bank",
            annual_fee=100,
        )

        assert card.nickname is None

    def test_card_nickname_empty_string(self):
        """Test that empty string nickname is allowed."""
        card = Card(
            id="test-123",
            name="Test Card",
            nickname="",
            issuer="Test Bank",
            annual_fee=100,
        )

        assert card.nickname == ""

    def test_card_serialization_with_nickname(self):
        """Test that nickname is included in serialization."""
        card = Card(
            id="test-123",
            name="Test Card",
            nickname="P2's Card",
            issuer="Test Bank",
            annual_fee=100,
        )

        data = card.model_dump()
        assert "nickname" in data
        assert data["nickname"] == "P2's Card"

    def test_card_deserialization_with_nickname(self):
        """Test that nickname is restored from dict."""
        data = {
            "id": "test-123",
            "name": "Test Card",
            "nickname": "Restored Nickname",
            "issuer": "Test Bank",
            "annual_fee": 100,
        }

        card = Card.model_validate(data)
        assert card.nickname == "Restored Nickname"


class TestAddCardFromTemplate:
    """Tests for CardStorage.add_card_from_template method."""

    @pytest.fixture
    def temp_storage(self):
        """Create a temporary storage directory for tests."""
        temp_dir = tempfile.mkdtemp()
        storage = CardStorage(data_dir=temp_dir)
        yield storage
        # Cleanup
        shutil.rmtree(temp_dir, ignore_errors=True)

    @pytest.fixture
    def sample_template(self):
        """Create a sample template for testing."""
        return CardTemplate(
            id="test_card",
            name="Test Card",
            issuer="Test Bank",
            annual_fee=95,
            credits=[
                Credit(name="Monthly Credit", amount=10.0, frequency="monthly"),
                Credit(name="Annual Credit", amount=100.0, frequency="annual"),
            ],
        )

    def test_add_card_from_template_basic(self, temp_storage, sample_template):
        """Test basic card creation from template."""
        card = temp_storage.add_card_from_template(template=sample_template)

        assert card.name == "Test Card"
        assert card.issuer == "Test Bank"
        assert card.annual_fee == 95
        assert len(card.credits) == 2
        assert card.id is not None  # Should have generated UUID

    def test_add_card_from_template_with_nickname(self, temp_storage, sample_template):
        """Test adding card with nickname."""
        card = temp_storage.add_card_from_template(
            template=sample_template,
            nickname="My Primary Card",
        )

        assert card.nickname == "My Primary Card"
        assert card.name == "Test Card"

    def test_add_card_from_template_without_nickname(self, temp_storage, sample_template):
        """Test adding card without nickname results in None."""
        card = temp_storage.add_card_from_template(template=sample_template)

        assert card.nickname is None

    def test_add_card_from_template_with_opened_date(self, temp_storage, sample_template):
        """Test adding card with opened date."""
        opened = date(2024, 1, 15)
        card = temp_storage.add_card_from_template(
            template=sample_template,
            opened_date=opened,
        )

        assert card.opened_date == opened

    def test_add_card_from_template_with_signup_bonus(self, temp_storage, sample_template):
        """Test adding card with signup bonus."""
        sub = SignupBonus(
            points_or_cash="80,000 points",
            spend_requirement=6000.0,
            time_period_days=90,
        )
        card = temp_storage.add_card_from_template(
            template=sample_template,
            signup_bonus=sub,
        )

        assert card.signup_bonus is not None
        assert card.signup_bonus.points_or_cash == "80,000 points"
        assert card.signup_bonus.spend_requirement == 6000.0

    def test_add_card_from_template_all_fields(self, temp_storage, sample_template):
        """Test adding card with all optional fields."""
        sub = SignupBonus(
            points_or_cash="50,000 points",
            spend_requirement=4000.0,
            time_period_days=90,
        )
        opened = date(2024, 6, 1)

        card = temp_storage.add_card_from_template(
            template=sample_template,
            nickname="Work Card",
            opened_date=opened,
            signup_bonus=sub,
        )

        assert card.nickname == "Work Card"
        assert card.opened_date == opened
        assert card.signup_bonus.points_or_cash == "50,000 points"
        assert card.name == "Test Card"
        assert len(card.credits) == 2

    def test_add_card_from_template_persists(self, temp_storage, sample_template):
        """Test that added card is persisted to storage."""
        card = temp_storage.add_card_from_template(
            template=sample_template,
            nickname="Persisted Card",
        )

        # Retrieve from storage
        all_cards = temp_storage.get_all_cards()
        assert len(all_cards) == 1
        assert all_cards[0].id == card.id
        assert all_cards[0].nickname == "Persisted Card"

    def test_add_card_from_template_generates_unique_ids(self, temp_storage, sample_template):
        """Test that each added card gets a unique ID."""
        card1 = temp_storage.add_card_from_template(template=sample_template)
        card2 = temp_storage.add_card_from_template(template=sample_template)

        assert card1.id != card2.id

    def test_add_card_from_template_credits_copied(self, temp_storage, sample_template):
        """Test that template credits are properly copied to card."""
        card = temp_storage.add_card_from_template(template=sample_template)

        assert len(card.credits) == 2
        credit_names = [c.name for c in card.credits]
        assert "Monthly Credit" in credit_names
        assert "Annual Credit" in credit_names

    def test_add_card_from_amex_platinum_template(self, temp_storage):
        """Test adding card from real Amex Platinum template."""
        template = get_template("amex_platinum")
        assert template is not None

        card = temp_storage.add_card_from_template(
            template=template,
            nickname="P1 Plat",
            opened_date=date(2024, 3, 15),
        )

        assert "Platinum" in card.name
        assert card.issuer == "American Express"
        assert card.annual_fee >= 695  # May vary (currently $895)
        assert card.nickname == "P1 Plat"
        assert len(card.credits) >= 5  # Should have many credits


class TestStorageWithNickname:
    """Test storage operations with nickname field."""

    @pytest.fixture
    def temp_storage(self):
        """Create a temporary storage directory for tests."""
        temp_dir = tempfile.mkdtemp()
        storage = CardStorage(data_dir=temp_dir)
        yield storage
        shutil.rmtree(temp_dir, ignore_errors=True)

    def test_nickname_survives_storage_roundtrip(self, temp_storage):
        """Test that nickname is preserved through save/load cycle."""
        template = CardTemplate(
            id="test",
            name="Test",
            issuer="Bank",
            annual_fee=0,
        )

        card = temp_storage.add_card_from_template(
            template=template,
            nickname="Special Name",
        )

        # Create new storage instance pointing to same directory
        new_storage = CardStorage(data_dir=temp_storage.data_dir)
        loaded_cards = new_storage.get_all_cards()

        assert len(loaded_cards) == 1
        assert loaded_cards[0].nickname == "Special Name"

    def test_get_card_returns_nickname(self, temp_storage):
        """Test that get_card returns card with nickname."""
        template = CardTemplate(
            id="test",
            name="Test",
            issuer="Bank",
            annual_fee=0,
        )

        card = temp_storage.add_card_from_template(
            template=template,
            nickname="Retrievable",
        )

        retrieved = temp_storage.get_card(card.id)
        assert retrieved is not None
        assert retrieved.nickname == "Retrievable"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
