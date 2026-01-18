"""Browser localStorage-based storage for ChurnPilot.

This module provides data persistence using browser localStorage,
ensuring each user's data is stored in their own browser and persists
across sessions and app redeployments.
"""

import json
import uuid
from datetime import date, datetime

import streamlit as st
from pydantic import BaseModel
from streamlit_js_eval import streamlit_js_eval

from .exceptions import StorageError
from .models import Card, CardData, SignupBonus
from .library import CardTemplate
from .normalize import normalize_issuer, match_to_library_template


STORAGE_KEY = 'churnpilot_cards'


def _serialize_for_json(obj):
    """Recursively convert Pydantic models and other types for JSON serialization."""
    if isinstance(obj, BaseModel):
        return obj.model_dump()
    elif isinstance(obj, dict):
        return {k: _serialize_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_serialize_for_json(item) for item in obj]
    elif isinstance(obj, (date, datetime)):
        return obj.isoformat()
    else:
        return obj


def init_browser_storage():
    """Initialize browser storage and load data from localStorage.

    Call this once at app startup to load user's data from browser.
    """
    if "cards_data" not in st.session_state:
        st.session_state.cards_data = []
        st.session_state.storage_initialized = False

    # Only load from localStorage once per session
    if not st.session_state.storage_initialized:
        try:
            # Read from localStorage using streamlit-js-eval
            js_code = f"""
            (function() {{
                try {{
                    const data = localStorage.getItem('{STORAGE_KEY}');
                    if (data) {{
                        return JSON.parse(data);
                    }}
                }} catch (e) {{
                    console.error('[ChurnPilot] Failed to load from localStorage:', e);
                }}
                return null;
            }})()
            """

            stored_data = streamlit_js_eval(js=js_code, key="load_storage")

            if stored_data and isinstance(stored_data, list):
                st.session_state.cards_data = stored_data
                st.session_state.storage_initialized = True
        except Exception as e:
            # If localStorage fails (e.g., in testing), just use empty list
            st.session_state.cards_data = []
            st.session_state.storage_initialized = True


def save_to_browser(cards_data: list[dict]):
    """Save cards data to browser localStorage."""
    # Update session state
    st.session_state.cards_data = cards_data

    # Serialize for JavaScript
    cards_json = json.dumps(_serialize_for_json(cards_data))

    # JavaScript to save to localStorage
    js_code = f"""
    (function() {{
        try {{
            localStorage.setItem('{STORAGE_KEY}', '{cards_json.replace("'", "\\'")}');
            console.log('[ChurnPilot] Saved', JSON.parse('{cards_json.replace("'", "\\'")}').length, 'cards to localStorage');
            return true;
        }} catch (e) {{
            console.error('[ChurnPilot] Failed to save to localStorage:', e);
            return false;
        }}
    }})()
    """

    try:
        streamlit_js_eval(js=js_code, key=f"save_storage_{len(cards_data)}")
    except Exception:
        # If JavaScript eval fails, data is still in session state
        pass


class BrowserStorage:
    """Browser localStorage-based storage for card data.

    Stores data in the user's browser localStorage, ensuring:
    - Each user has their own isolated data
    - Data persists across browser sessions
    - Data persists across app redeployments
    - No shared data between users
    """

    def __init__(self):
        """Initialize browser storage."""
        # Ensure session state is initialized
        if "cards_data" not in st.session_state:
            st.session_state.cards_data = []

    def _load_cards(self) -> list[dict]:
        """Load raw card data from session state (synced with browser)."""
        return st.session_state.cards_data

    def _save_cards(self, cards: list[dict]) -> None:
        """Save raw card data to session state and browser localStorage."""
        save_to_browser(cards)

    def get_all_cards(self) -> list[Card]:
        """Retrieve all stored cards.

        Returns:
            List of Card objects.
        """
        raw_cards = self._load_cards()
        return [Card.model_validate(c) for c in raw_cards]

    def get_card(self, card_id: str) -> Card | None:
        """Retrieve a single card by ID.

        Args:
            card_id: Unique card identifier.

        Returns:
            Card object if found, None otherwise.
        """
        cards = self._load_cards()
        for card_data in cards:
            if card_data.get("id") == card_id:
                return Card(**card_data)
        return None

    def add_card(
        self,
        card_data: CardData,
        opened_date: date | None = None,
        raw_text: str | None = None,
    ) -> Card:
        """Add a new card from extracted data.

        Args:
            card_data: Extracted card data from AI.
            opened_date: When the card was opened.
            raw_text: Original text used for extraction.

        Returns:
            The created Card object with generated ID.
        """
        # Normalize issuer
        normalized_issuer = normalize_issuer(card_data.issuer)

        # Try to match to library template
        template_id = match_to_library_template(card_data.name, normalized_issuer)

        card = Card(
            id=str(uuid.uuid4()),
            name=card_data.name,
            issuer=normalized_issuer,
            annual_fee=card_data.annual_fee,
            signup_bonus=card_data.signup_bonus,
            credits=card_data.credits,
            opened_date=opened_date,
            raw_text=raw_text,
            template_id=template_id,
            created_at=datetime.now(),
        )

        cards = self._load_cards()
        cards.append(card.model_dump())
        self._save_cards(cards)

        return card

    def add_card_from_template(
        self,
        template: CardTemplate,
        nickname: str | None = None,
        opened_date: date | None = None,
        signup_bonus: SignupBonus | None = None,
    ) -> Card:
        """Add a new card from a library template.

        Args:
            template: Card template from the library.
            nickname: User-defined nickname for the card.
            opened_date: When the card was opened.
            signup_bonus: Optional signup bonus details.

        Returns:
            The created Card object with generated ID.
        """
        card = Card(
            id=str(uuid.uuid4()),
            name=template.name,
            nickname=nickname,
            issuer=template.issuer,
            annual_fee=template.annual_fee,
            signup_bonus=signup_bonus,
            credits=template.credits,
            opened_date=opened_date,
            template_id=template.id,
            created_at=datetime.now(),
        )

        cards = self._load_cards()
        cards.append(card.model_dump())
        self._save_cards(cards)

        return card

    def update_card(self, card_id: str, updates: dict) -> Card | None:
        """Update an existing card.

        Args:
            card_id: Card to update.
            updates: Dictionary of fields to update.

        Returns:
            Updated Card object, or None if not found.
        """
        cards = self._load_cards()

        # Serialize any Pydantic models in the updates to dicts
        serialized_updates = _serialize_for_json(updates)

        for i, card_data in enumerate(cards):
            if card_data.get("id") == card_id:
                cards[i].update(serialized_updates)
                self._save_cards(cards)
                return Card.model_validate(cards[i])

        return None

    def delete_card(self, card_id: str) -> bool:
        """Delete a card by ID.

        Args:
            card_id: Card to delete.

        Returns:
            True if deleted, False if not found.
        """
        cards = self._load_cards()
        original_len = len(cards)

        cards = [c for c in cards if c.get("id") != card_id]

        if len(cards) < original_len:
            self._save_cards(cards)
            return True

        return False

    def export_data(self) -> str:
        """Export all data as JSON string."""
        cards = self._load_cards()
        return json.dumps(_serialize_for_json(cards), indent=2)

    def import_data(self, json_data: str) -> int:
        """Import data from JSON string, replacing existing data.

        Returns:
            Number of cards imported
        """
        try:
            cards = json.loads(json_data)
            if not isinstance(cards, list):
                raise ValueError("Import data must be a JSON array")

            self._save_cards(cards)
            return len(cards)
        except json.JSONDecodeError as e:
            raise StorageError(f"Invalid JSON: {e}")
        except Exception as e:
            raise StorageError(f"Import failed: {e}")
