"""Hero/Welcome component for first-time users.

Provides a stunning first impression with professional branding,
value proposition, and clear calls-to-action.
"""

import streamlit as st
from typing import Optional, Callable, List
from dataclasses import dataclass


# CSS for hero section styling
HERO_CSS = """
<style>
/* Hero Container */
.hero-container {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    border-radius: 24px;
    padding: 48px 40px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
}

/* Animated background elements */
.hero-container::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -20%;
    width: 60%;
    height: 200%;
    background: radial-gradient(circle, rgba(99, 102, 241, 0.15) 0%, transparent 70%);
    animation: pulse-glow 4s ease-in-out infinite;
}

.hero-container::after {
    content: '';
    position: absolute;
    bottom: -30%;
    left: -10%;
    width: 40%;
    height: 150%;
    background: radial-gradient(circle, rgba(16, 185, 129, 0.1) 0%, transparent 70%);
    animation: pulse-glow 5s ease-in-out infinite reverse;
}

@keyframes pulse-glow {
    0%, 100% { opacity: 0.5; transform: scale(1); }
    50% { opacity: 1; transform: scale(1.1); }
}

/* Logo and Brand */
.hero-brand {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 24px;
    position: relative;
    z-index: 1;
}

.hero-logo {
    width: 64px;
    height: 64px;
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%);
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 32px;
    box-shadow: 0 8px 32px rgba(99, 102, 241, 0.4);
    animation: logo-float 3s ease-in-out infinite;
}

@keyframes logo-float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-6px); }
}

.hero-title {
    font-size: 2rem;
    font-weight: 800;
    color: white;
    margin: 0;
    letter-spacing: -0.5px;
}

.hero-subtitle {
    font-size: 0.9rem;
    color: rgba(255, 255, 255, 0.6);
    margin: 0;
    text-transform: uppercase;
    letter-spacing: 2px;
}

/* Tagline */
.hero-tagline {
    font-size: 1.75rem;
    font-weight: 700;
    color: white;
    margin: 0 0 12px;
    position: relative;
    z-index: 1;
    line-height: 1.3;
}

.hero-highlight {
    background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero-description {
    font-size: 1.1rem;
    color: rgba(255, 255, 255, 0.8);
    margin: 0 0 32px;
    max-width: 600px;
    line-height: 1.6;
    position: relative;
    z-index: 1;
}

/* Stats Row */
.hero-stats {
    display: flex;
    gap: 32px;
    margin-bottom: 32px;
    position: relative;
    z-index: 1;
}

.hero-stat {
    text-align: center;
}

.hero-stat-value {
    font-size: 2rem;
    font-weight: 800;
    background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero-stat-label {
    font-size: 0.75rem;
    color: rgba(255, 255, 255, 0.5);
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* Feature Grid */
.hero-features {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 16px;
    margin-bottom: 32px;
    position: relative;
    z-index: 1;
}

.hero-feature {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 16px;
    transition: all 0.3s ease;
}

.hero-feature:hover {
    background: rgba(255, 255, 255, 0.1);
    transform: translateY(-4px);
    border-color: rgba(99, 102, 241, 0.5);
}

.hero-feature-icon {
    font-size: 1.5rem;
    margin-bottom: 8px;
}

.hero-feature-title {
    font-size: 0.95rem;
    font-weight: 600;
    color: white;
    margin: 0 0 4px;
}

.hero-feature-desc {
    font-size: 0.8rem;
    color: rgba(255, 255, 255, 0.6);
    margin: 0;
    line-height: 1.4;
}

/* Social Proof */
.hero-social-proof {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-top: 24px;
    padding-top: 24px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    position: relative;
    z-index: 1;
}

.hero-avatars {
    display: flex;
    margin-right: 8px;
}

.hero-avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
    border: 2px solid #1a1a2e;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    margin-left: -8px;
}

.hero-avatar:first-child {
    margin-left: 0;
}

.hero-social-text {
    font-size: 0.875rem;
    color: rgba(255, 255, 255, 0.7);
}

/* Quick Start Card */
.quick-start-card {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(168, 85, 247, 0.1) 100%);
    border: 1px solid rgba(99, 102, 241, 0.3);
    border-radius: 16px;
    padding: 24px;
    margin-top: 24px;
}

.quick-start-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: #6366f1;
    margin: 0 0 16px;
}

.quick-start-step {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    margin-bottom: 12px;
}

.quick-start-number {
    width: 24px;
    height: 24px;
    background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.75rem;
    font-weight: 700;
    color: white;
    flex-shrink: 0;
}

.quick-start-text {
    font-size: 0.9rem;
    color: #9ca3af;
    line-height: 1.5;
}

/* Responsive */
@media (max-width: 768px) {
    .hero-container { padding: 32px 24px; }
    .hero-tagline { font-size: 1.5rem; }
    .hero-features { grid-template-columns: 1fr; }
    .hero-stats { flex-wrap: wrap; gap: 24px; }
}
</style>
"""


@dataclass
class HeroFeature:
    """A feature to highlight in the hero section."""
    icon: str
    title: str
    description: str


# Default features for ChurnPilot
DEFAULT_FEATURES = [
    HeroFeature(
        icon="🎯",
        title="Never Miss a SUB",
        description="Track spend requirements and deadlines with smart alerts"
    ),
    HeroFeature(
        icon="💰",
        title="Maximize Benefits",
        description="Track monthly credits so you never leave money on the table"
    ),
    HeroFeature(
        icon="📊",
        title="Chase 5/24 Tracker",
        description="Know exactly when you can apply for more Chase cards"
    ),
    HeroFeature(
        icon="🤖",
        title="AI-Powered",
        description="Paste any card offer and let AI extract all the details"
    ),
]


def inject_hero_css():
    """Inject hero CSS styles."""
    st.markdown(HERO_CSS, unsafe_allow_html=True)


def render_hero(
    show_demo_button: bool = True,
    demo_callback: Optional[Callable] = None,
    add_card_callback: Optional[Callable] = None,
    features: Optional[List[HeroFeature]] = None,
    template_count: int = 40,
) -> Optional[str]:
    """Render the hero/welcome section for first-time users."""
    inject_hero_css()

    if features is None:
        features = DEFAULT_FEATURES

    clicked = None

    # Build feature HTML - single line to avoid Streamlit parsing issues
    features_html = "".join([
        f'<div class="hero-feature"><div class="hero-feature-icon">{f.icon}</div><div class="hero-feature-title">{f.title}</div><p class="hero-feature-desc">{f.description}</p></div>'
        for f in features
    ])

    # Build the complete hero HTML as a single string (no line breaks in tags)
    hero_html = f'''<div class="hero-container">
<div class="hero-brand"><div class="hero-logo">✈️</div><div><h1 class="hero-title">ChurnPilot</h1><p class="hero-subtitle">Credit Card Intelligence</p></div></div>
<h2 class="hero-tagline">Stop leaving <span class="hero-highlight">thousands of dollars</span><br>on the table</h2>
<p class="hero-description">The smart dashboard for credit card enthusiasts. Track signup bonuses, maximize benefits, and never miss a deadline again.</p>
<div class="hero-stats"><div class="hero-stat"><div class="hero-stat-value">{template_count}+</div><div class="hero-stat-label">Card Templates</div></div><div class="hero-stat"><div class="hero-stat-value">$10K+</div><div class="hero-stat-label">Avg Annual Value</div></div><div class="hero-stat"><div class="hero-stat-value">5/24</div><div class="hero-stat-label">Rule Tracker</div></div></div>
<div class="hero-features">{features_html}</div>
<div class="hero-social-proof"><div class="hero-avatars"><div class="hero-avatar">🧑‍💼</div><div class="hero-avatar">👩‍💻</div><div class="hero-avatar">🧑‍🔬</div><div class="hero-avatar">👨‍✈️</div></div><span class="hero-social-text">Built for churners tracking <strong>10-50+ cards</strong> across multiple issuers</span></div>
</div>'''

    st.markdown(hero_html, unsafe_allow_html=True)

    # Action buttons using Streamlit for interactivity
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if show_demo_button:
                if st.button(
                    "🎮 Try Demo Mode",
                    key="hero_demo_btn",
                    type="secondary",
                    use_container_width=True,
                ):
                    clicked = "demo"
                    if demo_callback:
                        demo_callback()

        with btn_col2:
            if st.button(
                "➕ Add Your First Card",
                key="hero_add_btn",
                type="primary",
                use_container_width=True,
            ):
                clicked = "add"
                if add_card_callback:
                    add_card_callback()

    # Quick start guide - also as single-line HTML
    quick_start_html = '''<div class="quick-start-card">
<div class="quick-start-title">⚡ Quick Start</div>
<div class="quick-start-step"><div class="quick-start-number">1</div><div class="quick-start-text"><strong>Add your cards</strong> - Select from our library of 40+ templates, or paste any card offer URL for AI extraction</div></div>
<div class="quick-start-step"><div class="quick-start-number">2</div><div class="quick-start-text"><strong>Track your benefits</strong> - Mark monthly credits as used so you never forget to redeem them</div></div>
<div class="quick-start-step"><div class="quick-start-number">3</div><div class="quick-start-text"><strong>Hit your SUBs</strong> - Get reminders when spend deadlines approach and celebrate when you hit the bonus</div></div>
</div>'''

    st.markdown(quick_start_html, unsafe_allow_html=True)

    return clicked


def render_demo_banner(
    exit_callback: Optional[Callable] = None,
) -> bool:
    """Render a banner indicating demo mode is active."""
    col1, col2 = st.columns([4, 1])

    with col1:
        st.info("🎮 **Demo Mode** - Explore with sample data. Your real cards will be separate.")

    with col2:
        if st.button("Exit Demo", key="exit_demo_btn", type="secondary"):
            if exit_callback:
                exit_callback()
            return True

    return False
