"""Test script for hybrid storage to verify it works without running Streamlit."""

import json
from pathlib import Path
from datetime import date

# Test without Streamlit
print("Testing hybrid storage without Streamlit...")
print()

# Check if fallback file exists
FALLBACK_FILE = Path.home() / '.churnpilot' / 'cards.json'
print(f"Fallback file location: {FALLBACK_FILE}")
print(f"File exists: {FALLBACK_FILE.exists()}")

if FALLBACK_FILE.exists():
    try:
        with open(FALLBACK_FILE, 'r') as f:
            data = json.load(f)
        print(f"[OK] File is readable")
        print(f"[OK] Contains {len(data)} cards")
        print()

        if data:
            print("First card:")
            first_card = data[0]
            print(f"  Name: {first_card.get('name')}")
            print(f"  Issuer: {first_card.get('issuer')}")
            print(f"  Annual Fee: ${first_card.get('annual_fee')}")
            print(f"  Opened: {first_card.get('opened_date')}")
            print(f"  ID: {first_card.get('id')}")
    except Exception as e:
        print(f"X Error reading file: {e}")
else:
    print("i No data file yet - will be created when you add a card")
    print()

# Test with mock session state
print()
print("="*50)
print("Testing HybridStorage class with mock...")
print()

# Create a mock for streamlit
class MockSessionState:
    def __init__(self):
        self._data = {
            'cards_data': [],
            'storage_initialized': False,
            'storage_type': None
        }

    def __contains__(self, key):
        return key in self._data

    def __getattr__(self, key):
        if key.startswith('_'):
            return object.__getattribute__(self, key)
        return self._data.get(key)

    def __setattr__(self, key, value):
        if key.startswith('_'):
            object.__setattr__(self, key, value)
        else:
            self._data[key] = value

class MockStreamlit:
    def __init__(self):
        self.session_state = MockSessionState()

    def info(self, msg):
        print(f"[INFO] {msg}")

    def warning(self, msg):
        print(f"[WARNING] {msg}")

    def success(self, msg):
        print(f"[SUCCESS] {msg}")

    def error(self, msg):
        print(f"[ERROR] {msg}")

    def toast(self, msg):
        print(f"[TOAST] {msg}")

import sys
import src.core.hybrid_storage as hs

# Mock streamlit module
sys.modules['streamlit'] = MockStreamlit()
hs.st = MockStreamlit()

print("Testing basic operations...")

# Initialize storage
hs.init_hybrid_storage()
print(f"[OK] Initialized storage")
print(f"  Type: {hs.st.session_state.storage_type}")
print(f"  Cards loaded: {len(hs.st.session_state.cards_data)}")
print()

# Create a test card
from src.core.models import Card, CardData, SignupBonus
from src.core.library import get_template

print("Testing add card from template...")
template = get_template("amex_platinum")
storage = hs.HybridStorage()

test_card = Card(
    id="test-12345",
    name=template.name,
    issuer=template.issuer,
    annual_fee=template.annual_fee,
    credits=template.credits,
    opened_date=date(2024, 1, 15),
    template_id=template.id,
)

# Add to storage
cards = storage._load_cards()
cards.append(test_card.model_dump())
storage._save_cards(cards)

print(f"[OK] Added test card")
print()

# Verify it was saved
print("Verifying file was written...")
if FALLBACK_FILE.exists():
    with open(FALLBACK_FILE, 'r') as f:
        saved_data = json.load(f)
    print(f"[OK] File contains {len(saved_data)} cards")

    # Check if our test card is there
    test_card_found = any(c['id'] == 'test-12345' for c in saved_data)
    if test_card_found:
        print(f"[OK] Test card found in file!")
    else:
        print(f"[FAIL] Test card NOT found in file")
else:
    print(f"[FAIL] File was not created")

print()
print("="*50)
print("Test complete!")
print()
print("NEXT STEPS:")
print("1. Run: streamlit run src/ui/app.py")
print("2. Add a card from library")
print(f"3. Close Streamlit and check {FALLBACK_FILE}")
print("4. Restart Streamlit - card should load from file")
