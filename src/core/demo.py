"""Demo data for showcasing ChurnPilot capabilities.

Provides realistic sample cards that demonstrate the full feature set
to first-time users before they add their own cards.
"""

from datetime import date, timedelta
from typing import List

from src.core.models import Card, Credit, SignupBonus, CreditUsage


def get_demo_cards() -> List[Card]:
    """Generate demo cards that showcase all features.

    Returns:
        List of realistic demo cards with various states.
    """
    today = date.today()

    cards = [
        # Card 1: Amex Platinum - Flagship card with many credits
        Card(
            id="demo_amex_platinum",
            name="The Platinum Card from American Express",
            nickname="Amex Plat",
            issuer="American Express",
            annual_fee=695,
            opened_date=today - timedelta(days=45),
            annual_fee_date=today + timedelta(days=320),
            signup_bonus=SignupBonus(
                points_or_cash="150,000 points",
                spend_requirement=6000,
                time_period_days=180,
                deadline=today + timedelta(days=135),  # Active SUB in progress
            ),
            sub_achieved=False,
            spend_progress=3200,  # About halfway there
            credits=[
                Credit(name="Uber Cash", amount=15, frequency="monthly", notes="$35 in Dec"),
                Credit(name="Digital Entertainment", amount=20, frequency="monthly", notes="Disney+, Hulu, ESPN+"),
                Credit(name="Saks Fifth Avenue", amount=50, frequency="semi-annual", notes="Jan-Jun, Jul-Dec"),
                Credit(name="Airline Fee Credit", amount=200, frequency="annual", notes="Incidental fees only"),
                Credit(name="Hotel Credit", amount=200, frequency="annual", notes="FHR or THC prepaid"),
                Credit(name="CLEAR Plus", amount=189, frequency="annual"),
                Credit(name="Walmart+", amount=155, frequency="annual"),
            ],
            credit_usage={
                "Uber Cash": CreditUsage(last_used_period="2026-01"),
                "Digital Entertainment": CreditUsage(last_used_period="2026-01"),
            },
            is_business=False,
        ),

        # Card 2: Chase Sapphire Reserve - Shows retention offer
        Card(
            id="demo_csr",
            name="Chase Sapphire Reserve",
            nickname="CSR",
            issuer="Chase",
            annual_fee=550,
            opened_date=today - timedelta(days=400),
            annual_fee_date=today + timedelta(days=25),  # AF coming up soon!
            signup_bonus=None,
            sub_achieved=True,
            credits=[
                Credit(name="Travel Credit", amount=300, frequency="annual", notes="Resets each cardmember year"),
                Credit(name="DoorDash DashPass", amount=0, frequency="annual", notes="Free membership"),
                Credit(name="Lyft Pink", amount=0, frequency="annual", notes="Free membership"),
            ],
            credit_usage={
                "Travel Credit": CreditUsage(last_used_period="2026"),
            },
            is_business=False,
            notes="Call for retention offer before AF hits!",
        ),

        # Card 3: Amex Gold - Active monthly credits
        Card(
            id="demo_amex_gold",
            name="American Express Gold Card",
            nickname="Amex Gold",
            issuer="American Express",
            annual_fee=250,
            opened_date=today - timedelta(days=180),
            annual_fee_date=today + timedelta(days=185),
            signup_bonus=SignupBonus(
                points_or_cash="60,000 points",
                spend_requirement=6000,
                time_period_days=180,
                deadline=today - timedelta(days=10),  # Already achieved
            ),
            sub_achieved=True,
            spend_progress=6000,
            credits=[
                Credit(name="Uber Cash", amount=10, frequency="monthly"),
                Credit(name="Dining Credit", amount=10, frequency="monthly", notes="Grubhub, Seamless, etc."),
                Credit(name="Dunkin' Credit", amount=7, frequency="monthly"),
            ],
            credit_usage={
                # Uber Cash NOT used yet this period!
                "Dining Credit": CreditUsage(last_used_period="2026-01"),
            },
            is_business=False,
        ),

        # Card 4: Chase Ink Preferred - Business card (doesn't count for 5/24)
        Card(
            id="demo_cip",
            name="Chase Ink Business Preferred",
            nickname="CIP",
            issuer="Chase",
            annual_fee=95,
            opened_date=today - timedelta(days=60),
            annual_fee_date=today + timedelta(days=305),
            signup_bonus=SignupBonus(
                points_or_cash="100,000 points",
                spend_requirement=8000,
                time_period_days=90,
                deadline=today + timedelta(days=30),  # Deadline approaching!
            ),
            sub_achieved=False,
            spend_progress=5500,  # Close but cutting it tight
            credits=[],
            is_business=True,  # Doesn't count toward 5/24
        ),

        # Card 5: Capital One Venture X - Shows variety of issuers
        Card(
            id="demo_venture_x",
            name="Capital One Venture X",
            nickname="Venture X",
            issuer="Capital One",
            annual_fee=395,
            opened_date=today - timedelta(days=300),
            annual_fee_date=today + timedelta(days=65),
            signup_bonus=None,
            sub_achieved=True,
            credits=[
                Credit(name="Travel Credit", amount=300, frequency="annual", notes="Capital One Travel portal"),
                Credit(name="Anniversary Bonus", amount=0, frequency="annual", notes="10K miles on anniversary"),
            ],
            credit_usage={
                # Travel Credit not used yet
            },
            is_business=False,
        ),

        # Card 6: Citi Premier - Another issuer
        Card(
            id="demo_citi_premier",
            name="Citi Premier Card",
            nickname="Citi Premier",
            issuer="Citi",
            annual_fee=95,
            opened_date=today - timedelta(days=500),
            annual_fee_date=today + timedelta(days=230),
            signup_bonus=None,
            sub_achieved=True,
            credits=[
                Credit(name="Hotel Credit", amount=100, frequency="annual", notes="Hotels.com bookings"),
            ],
            is_business=False,
        ),

        # Card 7: Chase Freedom Unlimited - No annual fee
        Card(
            id="demo_cfu",
            name="Chase Freedom Unlimited",
            nickname="CFU",
            issuer="Chase",
            annual_fee=0,
            opened_date=today - timedelta(days=700),
            annual_fee_date=None,
            signup_bonus=None,
            sub_achieved=True,
            credits=[],
            is_business=False,
        ),

        # Card 8: Amex Business Platinum - High value biz card
        Card(
            id="demo_biz_plat",
            name="Business Platinum Card from American Express",
            nickname="Biz Plat",
            issuer="American Express",
            annual_fee=695,
            opened_date=today - timedelta(days=200),
            annual_fee_date=today + timedelta(days=165),
            signup_bonus=SignupBonus(
                points_or_cash="150,000 points",
                spend_requirement=20000,
                time_period_days=90,
                deadline=today - timedelta(days=50),
            ),
            sub_achieved=True,
            spend_progress=20000,
            credits=[
                Credit(name="Dell Credit", amount=200, frequency="semi-annual", notes="Q1-Q2, Q3-Q4"),
                Credit(name="Indeed Credit", amount=360, frequency="annual", notes="Job postings"),
                Credit(name="Adobe Creative Cloud", amount=150, frequency="annual"),
                Credit(name="Wireless Credit", amount=10, frequency="monthly", notes="AT&T, T-Mobile, Verizon"),
            ],
            credit_usage={
                "Wireless Credit": CreditUsage(last_used_period="2026-01"),
                # Dell Credit not used yet this half
            },
            is_business=True,
        ),
    ]

    return cards


def get_demo_summary() -> dict:
    """Get summary statistics for demo data.

    Returns:
        Dictionary with summary stats to show value proposition.
    """
    cards = get_demo_cards()

    # Calculate stats
    total_annual_fees = sum(c.annual_fee for c in cards)

    total_credits_value = 0
    for card in cards:
        for credit in card.credits:
            if credit.frequency == "monthly":
                total_credits_value += credit.amount * 12
            elif credit.frequency == "quarterly":
                total_credits_value += credit.amount * 4
            elif credit.frequency in ["semi-annual", "semi-annually"]:
                total_credits_value += credit.amount * 2
            else:
                total_credits_value += credit.amount

    # Pending SUBs
    pending_subs = [c for c in cards if c.signup_bonus and not c.sub_achieved]

    # Urgent deadlines
    today = date.today()
    urgent_deadlines = []
    for card in cards:
        if card.signup_bonus and card.signup_bonus.deadline and not card.sub_achieved:
            days_left = (card.signup_bonus.deadline - today).days
            if 0 <= days_left <= 30:
                urgent_deadlines.append({
                    "card": card.nickname or card.name,
                    "type": "SUB",
                    "days": days_left,
                })
        if card.annual_fee_date:
            days_left = (card.annual_fee_date - today).days
            if 0 <= days_left <= 30:
                urgent_deadlines.append({
                    "card": card.nickname or card.name,
                    "type": "AF",
                    "days": days_left,
                })

    # 5/24 count
    personal_cards = [c for c in cards if not c.is_business and not c.closed_date]
    recent_personal = [
        c for c in personal_cards
        if c.opened_date and (today - c.opened_date).days < 730
    ]

    return {
        "card_count": len(cards),
        "total_annual_fees": total_annual_fees,
        "total_credits_value": total_credits_value,
        "net_value": total_credits_value - total_annual_fees,
        "pending_sub_count": len(pending_subs),
        "urgent_deadlines": urgent_deadlines,
        "five_twenty_four_count": len(recent_personal),
    }
