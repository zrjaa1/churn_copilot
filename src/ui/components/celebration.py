"""Celebration/Confetti component for achievements.

Provides satisfying visual feedback when users complete
signup bonuses, hit spending goals, or achieve milestones.
"""

import streamlit as st
from typing import Optional, Literal
from streamlit.components.v1 import html


# Confetti CSS and JavaScript
CELEBRATION_CSS = """
<style>
/* Celebration Container */
.celebration-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 9999;
    overflow: hidden;
}

/* Confetti Piece */
.confetti {
    position: absolute;
    width: 10px;
    height: 10px;
    opacity: 0;
    animation: confetti-fall 3s ease-out forwards;
}

.confetti.circle { border-radius: 50%; }
.confetti.square { border-radius: 2px; }
.confetti.rectangle { width: 6px; height: 12px; border-radius: 1px; }

@keyframes confetti-fall {
    0% {
        opacity: 1;
        transform: translateY(-100vh) rotate(0deg);
    }
    10% {
        opacity: 1;
    }
    100% {
        opacity: 0;
        transform: translateY(100vh) rotate(720deg);
    }
}

/* Achievement Card */
.achievement-card {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    border-radius: 16px;
    padding: 32px;
    text-align: center;
    position: relative;
    overflow: hidden;
    animation: achievement-pop 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

@keyframes achievement-pop {
    0% { transform: scale(0.8); opacity: 0; }
    50% { transform: scale(1.05); }
    100% { transform: scale(1); opacity: 1; }
}

.achievement-card::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: conic-gradient(from 0deg, transparent, rgba(99, 102, 241, 0.1), transparent 30%);
    animation: achievement-spin 3s linear infinite;
}

@keyframes achievement-spin {
    100% { transform: rotate(360deg); }
}

.achievement-icon {
    font-size: 4rem;
    margin-bottom: 16px;
    position: relative;
    z-index: 1;
    animation: achievement-bounce 0.6s ease-out;
}

@keyframes achievement-bounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-20px); }
}

.achievement-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: white;
    margin-bottom: 8px;
    position: relative;
    z-index: 1;
}

.achievement-subtitle {
    font-size: 1rem;
    color: rgba(255, 255, 255, 0.7);
    margin-bottom: 16px;
    position: relative;
    z-index: 1;
}

.achievement-value {
    font-size: 2rem;
    font-weight: 800;
    background: linear-gradient(90deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    position: relative;
    z-index: 1;
    animation: value-glow 2s ease-in-out infinite;
}

@keyframes value-glow {
    0%, 100% { filter: brightness(1); }
    50% { filter: brightness(1.2); }
}

/* Success Toast Enhancement */
.success-toast {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    color: white;
    padding: 16px 24px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    gap: 12px;
    box-shadow: 0 8px 32px rgba(16, 185, 129, 0.3);
    animation: toast-slide 0.5s ease-out;
}

@keyframes toast-slide {
    from { transform: translateX(100%); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}

.success-toast-icon {
    font-size: 1.5rem;
}

.success-toast-text {
    font-weight: 600;
}

/* Milestone Badge */
.milestone-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 16px;
    background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
    border-radius: 20px;
    font-weight: 600;
    color: #78350f;
    box-shadow: 0 4px 12px rgba(251, 191, 36, 0.3);
    animation: badge-shine 2s ease-in-out infinite;
}

@keyframes badge-shine {
    0%, 100% { box-shadow: 0 4px 12px rgba(251, 191, 36, 0.3); }
    50% { box-shadow: 0 4px 24px rgba(251, 191, 36, 0.5); }
}

/* Streak Counter */
.streak-counter {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 12px 20px;
    background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
    border-radius: 12px;
    color: white;
}

.streak-flame {
    font-size: 1.5rem;
    animation: flame-flicker 0.5s ease-in-out infinite;
}

@keyframes flame-flicker {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.1); }
}

.streak-number {
    font-size: 1.5rem;
    font-weight: 800;
}

.streak-label {
    font-size: 0.875rem;
    opacity: 0.9;
}
</style>
"""

# JavaScript for confetti generation
CONFETTI_JS = """
<script>
function createConfetti(count = 100) {
    const container = document.getElementById('confetti-container');
    if (!container) return;

    const colors = ['#6366f1', '#a855f7', '#ec4899', '#10b981', '#fbbf24', '#f97316'];
    const shapes = ['circle', 'square', 'rectangle'];

    for (let i = 0; i < count; i++) {
        const confetti = document.createElement('div');
        confetti.className = 'confetti ' + shapes[Math.floor(Math.random() * shapes.length)];
        confetti.style.left = Math.random() * 100 + '%';
        confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
        confetti.style.animationDelay = Math.random() * 2 + 's';
        confetti.style.animationDuration = (Math.random() * 2 + 2) + 's';
        container.appendChild(confetti);
    }

    // Clean up after animation
    setTimeout(() => {
        container.innerHTML = '';
    }, 5000);
}

// Auto-trigger if flagged
if (document.getElementById('trigger-confetti')) {
    createConfetti(150);
}
</script>
"""


def inject_celebration_css():
    """Inject celebration CSS styles."""
    st.markdown(CELEBRATION_CSS, unsafe_allow_html=True)


def trigger_confetti(count: int = 100):
    """Trigger a confetti animation.

    Args:
        count: Number of confetti pieces to generate.
    """
    inject_celebration_css()

    # Create confetti container and trigger script
    html_content = f"""
    <div id="confetti-container" class="celebration-overlay"></div>
    <div id="trigger-confetti" style="display:none;"></div>
    {CONFETTI_JS}
    """
    html(html_content, height=0)


def render_achievement_card(
    icon: str = "🎉",
    title: str = "Achievement Unlocked!",
    subtitle: Optional[str] = None,
    value: Optional[str] = None,
    show_confetti: bool = True,
):
    """Render a celebration achievement card.

    Args:
        icon: Emoji or icon for the achievement.
        title: Achievement title.
        subtitle: Optional subtitle/description.
        value: Optional value to highlight (e.g., points earned).
        show_confetti: Whether to trigger confetti animation.
    """
    inject_celebration_css()

    subtitle_html = f'<div class="achievement-subtitle">{subtitle}</div>' if subtitle else ""
    value_html = f'<div class="achievement-value">{value}</div>' if value else ""

    st.markdown(
        f"""
        <div class="achievement-card">
            <div class="achievement-icon">{icon}</div>
            <div class="achievement-title">{title}</div>
            {subtitle_html}
            {value_html}
        </div>
        """,
        unsafe_allow_html=True,
    )

    if show_confetti:
        trigger_confetti(150)


def render_sub_completion_celebration(
    card_name: str,
    points_earned: str,
    spend_completed: float,
):
    """Render a signup bonus completion celebration.

    Args:
        card_name: Name of the card.
        points_earned: Points or cash earned.
        spend_completed: Total spend that was completed.
    """
    render_achievement_card(
        icon="🏆",
        title="Signup Bonus Complete!",
        subtitle=f"{card_name} • ${spend_completed:,.0f} spent",
        value=points_earned,
        show_confetti=True,
    )


def render_milestone_badge(
    text: str,
    icon: str = "⭐",
):
    """Render a milestone badge.

    Args:
        text: Badge text.
        icon: Badge icon.
    """
    inject_celebration_css()

    st.markdown(
        f"""
        <div class="milestone-badge">
            <span>{icon}</span>
            <span>{text}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_streak_counter(
    streak: int,
    label: str = "day streak",
):
    """Render a streak counter with flame animation.

    Args:
        streak: Current streak count.
        label: Label for the streak.
    """
    inject_celebration_css()

    st.markdown(
        f"""
        <div class="streak-counter">
            <span class="streak-flame">🔥</span>
            <span class="streak-number">{streak}</span>
            <span class="streak-label">{label}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_success_message(
    text: str,
    icon: str = "✓",
):
    """Render an enhanced success message.

    Args:
        text: Success message text.
        icon: Icon to display.
    """
    inject_celebration_css()

    st.markdown(
        f"""
        <div class="success-toast">
            <span class="success-toast-icon">{icon}</span>
            <span class="success-toast-text">{text}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_benefit_completion_celebration(
    benefit_name: str,
    value: float,
    card_name: str,
):
    """Render a benefit redemption celebration (smaller than SUB).

    Args:
        benefit_name: Name of the benefit.
        value: Value of the benefit.
        card_name: Name of the card.
    """
    inject_celebration_css()

    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                    border-radius: 12px; padding: 16px; margin: 8px 0;
                    display: flex; align-items: center; gap: 16px;
                    animation: achievement-pop 0.5s ease-out;">
            <div style="font-size: 2rem;">✓</div>
            <div>
                <div style="color: white; font-weight: 600; font-size: 1rem;">
                    {benefit_name} Redeemed!
                </div>
                <div style="color: rgba(255,255,255,0.8); font-size: 0.875rem;">
                    ${value:,.0f} from {card_name}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
