"""Core business logic - framework agnostic."""

from .models import Card, SignupBonus, Credit, CardData
from .storage import CardStorage
from .preprocessor import preprocess_text, get_char_reduction
from .fetcher import fetch_card_page, get_allowed_domains
from .pipeline import extract_from_url, extract_from_text
from .library import CardTemplate, get_all_templates, get_template, get_template_choices

__all__ = [
    # Models
    "Card",
    "SignupBonus",
    "Credit",
    "CardData",
    "CardTemplate",
    # Storage
    "CardStorage",
    # Extraction pipeline (main API)
    "extract_from_url",
    "extract_from_text",
    # Card library
    "get_all_templates",
    "get_template",
    "get_template_choices",
    # Utilities
    "fetch_card_page",
    "get_allowed_domains",
    "preprocess_text",
    "get_char_reduction",
]
