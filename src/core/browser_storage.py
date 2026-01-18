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

from .exceptions import StorageError
from .models import Card, CardData


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

    # JavaScript to sync with localStorage
    storage_html = """
    <script>
    // Load from localStorage on startup
    const STORAGE_KEY = 'churnpilot_cards';

    function loadFromStorage() {
        try {
            const data = localStorage.getItem(STORAGE_KEY);
            if (data) {
                const cards = JSON.parse(data);
                console.log('[ChurnPilot] Loaded', cards.length, 'cards from localStorage');
                return cards;
            }
        } catch (e) {
            console.error('[ChurnPilot] Failed to load from localStorage:', e);
        }
        return null;
    }

    function saveToStorage(cards) {
        try {
            localStorage.setItem(STORAGE_KEY, JSON.stringify(cards));
            console.log('[ChurnPilot] Saved', cards.length, 'cards to localStorage');
        } catch (e) {
            console.error('[ChurnPilot] Failed to save to localStorage:', e);
        }
    }

    // Expose functions globally for Streamlit to call
    window.churnPilotLoadData = loadFromStorage;
    window.churnPilotSaveData = saveToStorage;

    // Try to load data immediately
    const storedData = loadFromStorage();
    if (storedData) {
        // Store in a div that Streamlit can read
        const dataDiv = document.createElement('div');
        dataDiv.id = 'churnpilot-data';
        dataDiv.style.display = 'none';
        dataDiv.textContent = JSON.stringify(storedData);
        document.body.appendChild(dataDiv);
    }
    </script>
    """

    st.components.v1.html(storage_html, height=0)


def save_to_browser(cards_data: list[dict]):
    """Save cards data to browser localStorage."""
    # Update session state
    st.session_state.cards_data = cards_data

    # Serialize for JavaScript
    cards_json = json.dumps(_serialize_for_json(cards_data), separators=(',', ':'))

    # JavaScript to save
    save_html = f"""
    <script>
    if (window.churnPilotSaveData) {{
        window.churnPilotSaveData({cards_json});
    }} else {{
        // Fallback if function not loaded yet
        try {{
            localStorage.setItem('churnpilot_cards', '{cards_json}');
        }} catch(e) {{
            console.error('[ChurnPilot] Save failed:', e);
        }}
    }}
    </script>
    """

    st.components.v1.html(save_html, height=0)


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
        """Get all cards from storage."""
        raw_cards = self._load_cards()
        return [Card(**card_data) for card_data in raw_cards]

    def get_card(self, card_id: str) -> Card | None:
        """Get a specific card by ID."""
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
        """Add a new card to storage."""
        cards = self._load_cards()

        # Create card ID
        card_id = str(uuid.uuid4())

        # Build card object
        card = Card(
            id=card_id,
            name=card_data.name,
            issuer=card_data.issuer,
            annual_fee=card_data.annual_fee,
            signup_bonus=card_data.signup_bonus,
            credits=card_data.credits,
            opened_date=opened_date,
            created_at=datetime.now(),
            raw_extraction=raw_text,
        )

        # Serialize and add
        cards.append(card.model_dump())
        self._save_cards(cards)

        return card

    def update_card(self, card_id: str, updates: dict) -> None:
        """Update an existing card."""
        cards = self._load_cards()

        # Find and update card
        found = False
        for i, card_data in enumerate(cards):
            if card_data.get("id") == card_id:
                card_data.update(updates)
                cards[i] = card_data
                found = True
                break

        if not found:
            raise StorageError(f"Card {card_id} not found")

        self._save_cards(cards)

    def delete_card(self, card_id: str) -> None:
        """Delete a card from storage."""
        cards = self._load_cards()
        cards = [c for c in cards if c.get("id") != card_id]
        self._save_cards(cards)

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
