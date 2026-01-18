"""Hybrid storage with localStorage + file fallback for ChurnPilot.

Tries browser localStorage first, falls back to local file storage if that fails.
"""

import json
import uuid
from datetime import date, datetime
from pathlib import Path

import streamlit as st
from pydantic import BaseModel

from .exceptions import StorageError
from .models import Card, CardData, SignupBonus
from .library import CardTemplate
from .normalize import normalize_issuer, match_to_library_template


STORAGE_KEY = 'churnpilot_cards'
FALLBACK_FILE = Path.home() / '.churnpilot' / 'cards.json'


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


def init_hybrid_storage():
    """Initialize storage - try localStorage, fallback to file."""
    if "cards_data" not in st.session_state:
        st.session_state.cards_data = []
        st.session_state.storage_initialized = False
        st.session_state.storage_type = None
        print(f"[DEBUG] Initialized empty cards_data")

    if not st.session_state.storage_initialized:
        print(f"[DEBUG] Loading data...")

        # Try localStorage first
        try:
            from streamlit_js_eval import streamlit_js_eval

            js_code = f"""
            (function() {{
                try {{
                    const data = localStorage.getItem('{STORAGE_KEY}');
                    if (data) {{
                        return JSON.parse(data);
                    }}
                }} catch (e) {{
                    console.error('[ChurnPilot] localStorage failed:', e);
                }}
                return null;
            }})()
            """

            stored_data = streamlit_js_eval(js=js_code, key="load_storage")

            if stored_data and isinstance(stored_data, list):
                st.session_state.cards_data = stored_data
                st.session_state.storage_type = 'localStorage'
                st.session_state.storage_initialized = True
                print(f"[DEBUG] Loaded {len(stored_data)} cards from localStorage")
                return
        except Exception as e:
            print(f"[DEBUG] localStorage failed: {e}")

        # Fallback to file
        try:
            if FALLBACK_FILE.exists():
                with open(FALLBACK_FILE, 'r') as f:
                    stored_data = json.load(f)
                    st.session_state.cards_data = stored_data
                    st.session_state.storage_type = 'file'
                    st.session_state.storage_initialized = True
                    print(f"[DEBUG] Loaded {len(stored_data)} cards from file")
                    st.info(f"📁 Loaded data from {FALLBACK_FILE}")
                    return
        except Exception as e:
            print(f"[DEBUG] File load failed: {e}")

        # Start fresh
        st.session_state.storage_initialized = True
        st.session_state.storage_type = 'file'  # Default to file for saving
        print(f"[DEBUG] Starting fresh, will use file storage")


def save_hybrid(cards_data: list[dict]):
    """Save to both localStorage and file for redundancy."""
    print(f"[DEBUG] Saving {len(cards_data)} cards...")

    # Update session state
    st.session_state.cards_data = cards_data

    # Try localStorage
    localStorage_success = False
    try:
        from streamlit_js_eval import streamlit_js_eval

        cards_json = json.dumps(_serialize_for_json(cards_data))
        js_code = f"""
        (function() {{
            try {{
                localStorage.setItem('{STORAGE_KEY}', `{cards_json}`);
                return {{success: true}};
            }} catch (e) {{
                console.error('[ChurnPilot] Save to localStorage failed:', e);
                return {{success: false, error: e.message}};
            }}
        }})()
        """

        result = streamlit_js_eval(js=js_code, key=f"save_storage_{len(cards_data)}_{hash(cards_json[:100]) % 10000}")
        if result and isinstance(result, dict) and result.get('success'):
            localStorage_success = True
            print(f"[DEBUG] Saved to localStorage")
    except Exception as e:
        print(f"[DEBUG] localStorage save failed: {e}")

    # Always save to file as backup
    try:
        FALLBACK_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(FALLBACK_FILE, 'w') as f:
            json.dump(_serialize_for_json(cards_data), f, indent=2)
        print(f"[DEBUG] Saved to file: {FALLBACK_FILE}")

        if not localStorage_success:
            st.toast(f"💾 Saved to {FALLBACK_FILE.name}")
    except Exception as e:
        print(f"[DEBUG] File save failed: {e}")
        if not localStorage_success:
            st.error(f"Failed to save data: {e}")


class HybridStorage:
    """Hybrid storage using localStorage + file fallback."""

    def __init__(self):
        """Initialize hybrid storage."""
        if "cards_data" not in st.session_state:
            st.session_state.cards_data = []

    def _load_cards(self) -> list[dict]:
        """Load raw card data from session state."""
        return st.session_state.cards_data

    def _save_cards(self, cards: list[dict]) -> None:
        """Save raw card data."""
        save_hybrid(cards)

    def get_all_cards(self) -> list[Card]:
        """Retrieve all stored cards."""
        raw_cards = self._load_cards()
        return [Card.model_validate(c) for c in raw_cards]

    def get_card(self, card_id: str) -> Card | None:
        """Retrieve a single card by ID."""
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
        """Add a new card from extracted data."""
        normalized_issuer = normalize_issuer(card_data.issuer)
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
        """Add a new card from a library template."""
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
        """Update an existing card."""
        cards = self._load_cards()
        serialized_updates = _serialize_for_json(updates)

        for i, card_data in enumerate(cards):
            if card_data.get("id") == card_id:
                cards[i].update(serialized_updates)
                self._save_cards(cards)
                return Card.model_validate(cards[i])

        return None

    def delete_card(self, card_id: str) -> bool:
        """Delete a card by ID."""
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
        """Import data from JSON string, replacing existing data."""
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
