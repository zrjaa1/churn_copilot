"""Data migration script to fix existing card data.

Fixes:
1. Normalize issuer names (e.g., "Chase Sapphire Preferred Credit Card" → "Chase")
2. Update annual fee dates to current year based on opened_date
3. Backs up original data before modification
"""

import json
import sys
from datetime import date, datetime
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.core.normalize import normalize_issuer
from src.core.storage import CardStorage


def migrate_cards():
    """Migrate existing card data to fix common issues."""
    storage = CardStorage()

    print("[*] Loading existing cards...")
    raw_cards = storage._load_cards()
    print(f"   Found {len(raw_cards)} cards")

    if not raw_cards:
        print("   No cards to migrate")
        return

    # Backup original data
    backup_path = Path("data/cards.json.backup")
    backup_path.parent.mkdir(exist_ok=True)
    with open(backup_path, 'w') as f:
        json.dump(raw_cards, f, indent=2, default=str)
    print(f"[OK] Backed up original data to {backup_path}")

    # Track changes
    issuer_updates = 0
    fee_date_updates = 0

    print("\n[*] Migrating cards...")
    for i, card in enumerate(raw_cards, 1):
        card_name = card.get('name', f'Card #{i}')
        changes = []

        # Fix 1: Normalize issuer
        old_issuer = card.get('issuer', '')
        if old_issuer and (old_issuer == card.get('name') or ' ' in old_issuer):
            # Issuer looks like it might be the full card name
            new_issuer = normalize_issuer(card.get('name', ''))
            if new_issuer != old_issuer:
                card['issuer'] = new_issuer
                changes.append(f"issuer: '{old_issuer}' → '{new_issuer}'")
                issuer_updates += 1

        # Fix 2: Update annual fee dates
        opened_date_str = card.get('opened_date')
        annual_fee = card.get('annual_fee', 0)

        if opened_date_str and annual_fee > 0:
            try:
                opened_date = datetime.strptime(opened_date_str, "%Y-%m-%d").date()

                # Calculate what the fee date should be (same month/day, current or next year)
                current_year = date.today().year
                fee_month = opened_date.month
                fee_day = opened_date.day

                # Try current year
                try:
                    current_year_fee_date = date(current_year, fee_month, fee_day)
                except ValueError:
                    # Handle Feb 29 on non-leap years
                    current_year_fee_date = date(current_year, fee_month, 28)

                # If already passed, use next year
                if current_year_fee_date < date.today():
                    try:
                        next_fee_date = date(current_year + 1, fee_month, fee_day)
                    except ValueError:
                        next_fee_date = date(current_year + 1, fee_month, 28)
                else:
                    next_fee_date = current_year_fee_date

                old_fee_date = card.get('annual_fee_date')
                new_fee_date = next_fee_date.strftime("%Y-%m-%d")

                if old_fee_date != new_fee_date:
                    card['annual_fee_date'] = new_fee_date
                    changes.append(f"fee date: {old_fee_date} → {new_fee_date}")
                    fee_date_updates += 1
            except:
                pass

        if changes:
            print(f"   {card_name}")
            for change in changes:
                print(f"      - {change}")

    # Save updated data
    storage._save_cards(raw_cards)

    print(f"\n[OK] Migration complete!")
    print(f"   - {issuer_updates} issuers normalized")
    print(f"   - {fee_date_updates} annual fee dates updated")
    print(f"   - Original data backed up to {backup_path}")


if __name__ == "__main__":
    migrate_cards()
