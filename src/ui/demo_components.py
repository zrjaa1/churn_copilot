"""Demo page to showcase the UI component library."""

import streamlit as st
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

st.set_page_config(
    page_title="Component Library Demo",
    page_icon="🎨",
    layout="wide",
)

# Inject all CSS upfront in one block
st.markdown("""
<style>
/* ========== LOADING STYLES ========== */
.loading-spinner {
    display: inline-block;
    border-radius: 50%;
    border: 3px solid #e9ecef;
    border-top-color: #0066cc;
    animation: spin 0.8s linear infinite;
    width: 32px;
    height: 32px;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

.spinner-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 24px;
    gap: 12px;
}

.spinner-label {
    font-size: 0.875rem;
    color: #6c757d;
}

/* Pulse Dots */
.pulse-container {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 16px;
}

.pulse-dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: #0066cc;
    animation: pulse 1.4s ease-in-out infinite;
}

.pulse-dot:nth-child(1) { animation-delay: 0s; }
.pulse-dot:nth-child(2) { animation-delay: 0.2s; }
.pulse-dot:nth-child(3) { animation-delay: 0.4s; }

@keyframes pulse {
    0%, 80%, 100% { transform: scale(0.6); opacity: 0.5; }
    40% { transform: scale(1); opacity: 1; }
}

/* Skeleton */
.skeleton {
    background: linear-gradient(90deg, #e9ecef 25%, #f8f9fa 50%, #e9ecef 75%);
    background-size: 200% 100%;
    animation: shimmer 1.5s ease-in-out infinite;
    border-radius: 4px;
}

@keyframes shimmer {
    0% { background-position: 200% 0; }
    100% { background-position: -200% 0; }
}

.skeleton-card {
    background: white;
    border-radius: 12px;
    padding: 16px;
    border: 1px solid #e9ecef;
    margin-bottom: 12px;
}

.skeleton-header {
    display: flex;
    align-items: center;
    margin-bottom: 16px;
}

.skeleton-avatar {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    margin-right: 12px;
}

.skeleton-text {
    height: 16px;
    margin-bottom: 8px;
    border-radius: 4px;
}

/* ========== EMPTY STATE STYLES ========== */
.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 48px 24px;
    text-align: center;
}

.empty-icon {
    font-size: 4rem;
    margin-bottom: 24px;
    animation: float 3s ease-in-out infinite;
}

@keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
}

.empty-title {
    font-size: 1.25rem;
    font-weight: 600;
    color: #212529;
    margin-bottom: 8px;
}

.empty-description {
    font-size: 0.9375rem;
    color: #6c757d;
    max-width: 360px;
    margin-bottom: 24px;
}

/* ========== PROGRESS STYLES ========== */
.progress-steps {
    display: flex;
    justify-content: space-between;
    position: relative;
    padding: 20px 0;
}

.progress-step {
    display: flex;
    flex-direction: column;
    align-items: center;
    flex: 1;
}

.step-circle {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    margin-bottom: 8px;
}

.step-circle.completed {
    background: #28a745;
    color: white;
}

.step-circle.current {
    background: #0066cc;
    color: white;
    box-shadow: 0 4px 12px rgba(0,102,204,0.3);
}

.step-circle.pending {
    background: #f8f9fa;
    border: 2px solid #dee2e6;
    color: #6c757d;
}

.step-label {
    font-size: 0.8125rem;
    font-weight: 500;
}

/* Mini Progress */
.mini-progress {
    display: flex;
    align-items: center;
    gap: 8px;
}

.mini-bar {
    width: 100px;
    height: 6px;
    background: #e9ecef;
    border-radius: 3px;
    overflow: hidden;
}

.mini-fill {
    height: 100%;
    background: #0066cc;
    transition: width 0.3s;
}

/* ========== NOTIFICATION STYLES ========== */
.badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 20px;
    height: 20px;
    padding: 0 6px;
    border-radius: 10px;
    font-size: 0.75rem;
    font-weight: 700;
    color: white;
}

.badge-error { background: #dc3545; }
.badge-warning { background: #ffc107; color: #212529; }
.badge-info { background: #0066cc; }

.status-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    display: inline-block;
}

.status-online { background: #28a745; }
.status-busy { background: #dc3545; }
.status-offline { background: #6c757d; }

/* ========== FORM STYLES ========== */
.field-label {
    font-size: 0.875rem;
    font-weight: 600;
    color: #212529;
    margin-bottom: 6px;
}

.field-required {
    color: #dc3545;
    margin-left: 4px;
}

.field-help {
    font-size: 0.8125rem;
    color: #6c757d;
    margin-top: 4px;
}

.field-error {
    font-size: 0.8125rem;
    color: #dc3545;
    margin-top: 4px;
}

.field-success {
    font-size: 0.8125rem;
    color: #28a745;
    margin-top: 4px;
}

/* ========== TOUCH BUTTON STYLES ========== */
.touch-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 12px 24px;
    border-radius: 12px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.15s ease;
    border: none;
    min-height: 48px;
}

.touch-btn:active {
    transform: scale(0.97);
}

.touch-btn-primary {
    background: linear-gradient(135deg, #0066cc 0%, #0052a3 100%);
    color: white;
}

.touch-btn-danger {
    background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
    color: white;
}

.touch-btn-success {
    background: linear-gradient(135deg, #28a745 0%, #1e7e34 100%);
    color: white;
}

.touch-btn-secondary {
    background: #f8f9fa;
    color: #495057;
    border: 1px solid #dee2e6;
}
</style>
""", unsafe_allow_html=True)

st.title("🎨 UI Component Library Demo")
st.caption("Preview all the reusable components")

# Tabs for different component categories
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Loading States",
    "Empty States",
    "Progress",
    "Notifications",
    "Forms",
    "Interactive",
])

with tab1:
    st.header("Loading States")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Spinner")
        st.markdown("""
        <div class="spinner-container">
            <div class="loading-spinner"></div>
            <span class="spinner-label">Loading...</span>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.subheader("Pulse Dots")
        st.markdown("""
        <div class="pulse-container">
            <div class="pulse-dot"></div>
            <div class="pulse-dot"></div>
            <div class="pulse-dot"></div>
            <span style="margin-left: 12px; color: #6c757d;">Processing...</span>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.subheader("Status Indicators")
        st.markdown("""
        <div style="display: flex; flex-direction: column; gap: 12px; padding: 16px;">
            <div><span class="status-dot status-online"></span> <span style="margin-left: 8px;">Connected</span></div>
            <div><span class="status-dot status-busy"></span> <span style="margin-left: 8px;">Syncing</span></div>
            <div><span class="status-dot status-offline"></span> <span style="margin-left: 8px;">Offline</span></div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    st.subheader("Skeleton Cards")
    st.caption("These shimmer indefinitely - they're placeholder UI shown while content loads. This is the intended behavior!")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="skeleton-card">
            <div class="skeleton-header">
                <div class="skeleton skeleton-avatar"></div>
                <div style="flex: 1;">
                    <div class="skeleton skeleton-text" style="width: 70%;"></div>
                    <div class="skeleton skeleton-text" style="width: 40%; height: 12px;"></div>
                </div>
            </div>
            <div class="skeleton skeleton-text" style="width: 100%;"></div>
            <div class="skeleton skeleton-text" style="width: 100%;"></div>
            <div class="skeleton skeleton-text" style="width: 60%;"></div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="skeleton-card">
            <div class="skeleton skeleton-text" style="width: 80%; height: 20px;"></div>
            <div class="skeleton skeleton-text" style="width: 100%;"></div>
            <div class="skeleton skeleton-text" style="width: 100%;"></div>
            <div class="skeleton skeleton-text" style="width: 45%;"></div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="skeleton-card">
            <div class="skeleton-header">
                <div class="skeleton skeleton-avatar"></div>
                <div style="flex: 1;">
                    <div class="skeleton skeleton-text" style="width: 60%;"></div>
                    <div class="skeleton skeleton-text" style="width: 30%; height: 12px;"></div>
                </div>
            </div>
            <div class="skeleton skeleton-text" style="width: 90%;"></div>
            <div class="skeleton skeleton-text" style="width: 70%;"></div>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    st.header("Empty States")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("No Cards")
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">💳</div>
            <div class="empty-title">No cards yet</div>
            <div class="empty-description">Add your first credit card to start tracking benefits and deadlines</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Add Card", type="primary", key="empty1_btn"):
            st.toast("Would open Add Card form!", icon="💳")

    with col2:
        st.subheader("No Search Results")
        st.markdown("""
        <div class="empty-state" style="padding: 32px 16px;">
            <div class="empty-icon">🔍</div>
            <div class="empty-title">No matches found</div>
            <div class="empty-description">Try adjusting your search terms</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Clear Search", type="secondary", key="empty2_btn"):
            st.toast("Search cleared!", icon="🔍")

    st.divider()

    st.subheader("Other Empty State Icons")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div style="text-align: center; font-size: 3rem;">📭</div><p style="text-align: center;">Inbox</p>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div style="text-align: center; font-size: 3rem;">📊</div><p style="text-align: center;">Charts</p>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div style="text-align: center; font-size: 3rem;">⚠️</div><p style="text-align: center;">Error</p>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div style="text-align: center; font-size: 3rem;">✓</div><p style="text-align: center;">Success</p>', unsafe_allow_html=True)

with tab3:
    st.header("Progress Indicators")

    st.subheader("Step Progress")
    st.markdown("""
    <div class="progress-steps">
        <div class="progress-step">
            <div class="step-circle completed">✓</div>
            <span class="step-label" style="color: #28a745;">Card Info</span>
        </div>
        <div class="progress-step">
            <div class="step-circle completed">✓</div>
            <span class="step-label" style="color: #28a745;">Benefits</span>
        </div>
        <div class="progress-step">
            <div class="step-circle current">3</div>
            <span class="step-label" style="color: #0066cc;">Review</span>
        </div>
        <div class="progress-step">
            <div class="step-circle pending">4</div>
            <span class="step-label" style="color: #6c757d;">Confirm</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Mini Progress Bars")

        st.markdown("""
        <div class="mini-progress" style="margin-bottom: 16px;">
            <span style="color: #6c757d; font-size: 0.8rem; width: 120px;">Benefits used</span>
            <div class="mini-bar">
                <div class="mini-fill" style="width: 70%;"></div>
            </div>
            <span style="font-weight: 600; color: #0066cc;">70%</span>
        </div>
        <div class="mini-progress" style="margin-bottom: 16px;">
            <span style="color: #6c757d; font-size: 0.8rem; width: 120px;">Cards added</span>
            <div class="mini-bar">
                <div class="mini-fill" style="width: 60%; background: #28a745;"></div>
            </div>
            <span style="font-weight: 600; color: #28a745;">3/5</span>
        </div>
        <div class="mini-progress">
            <span style="color: #6c757d; font-size: 0.8rem; width: 120px;">SUB progress</span>
            <div class="mini-bar">
                <div class="mini-fill" style="width: 45%; background: #ffc107;"></div>
            </div>
            <span style="font-weight: 600; color: #856404;">45%</span>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.subheader("Completion Card")
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 12px; padding: 16px; background: #f8f9fa; border-radius: 12px;">
            <div style="font-size: 1.5rem;">✓</div>
            <div style="flex: 1;">
                <div style="font-weight: 600; margin-bottom: 4px;">Monthly credits redeemed</div>
                <div class="mini-bar" style="width: 100%; height: 8px;">
                    <div class="mini-fill" style="width: 80%; background: #28a745;"></div>
                </div>
            </div>
            <div style="font-weight: 700; color: #28a745; font-size: 1.1rem;">8/10</div>
        </div>
        """, unsafe_allow_html=True)

with tab4:
    st.header("Notifications")

    st.subheader("Toast Messages (click to trigger)")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("✓ Success", type="primary", use_container_width=True):
            st.toast("Card saved successfully!", icon="✓")

    with col2:
        if st.button("✕ Error", use_container_width=True):
            st.toast("Failed to save card", icon="❌")

    with col3:
        if st.button("⚠ Warning", use_container_width=True):
            st.toast("Deadline approaching!", icon="⚠️")

    with col4:
        if st.button("ℹ Info", use_container_width=True):
            st.toast("Tip: Swipe cards to delete", icon="ℹ️")

    st.divider()

    st.subheader("Notification Badges")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 8px;">
            <span>Alerts</span>
            <span class="badge badge-error">5</span>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 8px;">
            <span>Warnings</span>
            <span class="badge badge-warning">12</span>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 8px;">
            <span>Messages</span>
            <span class="badge badge-info">99+</span>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    st.subheader("Snackbar with Action")
    col1, col2 = st.columns([4, 1])
    with col1:
        st.info("Card deleted")
    with col2:
        if st.button("Undo"):
            st.toast("Card restored!", icon="↩️")

with tab5:
    st.header("Form Components")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Text Input with Validation")

        st.markdown('<div class="field-label">Card Name <span class="field-required">*</span></div>', unsafe_allow_html=True)
        name = st.text_input("Name", label_visibility="collapsed", placeholder="e.g., Chase Sapphire Preferred", key="form_name")
        if not name:
            st.markdown('<div class="field-error">⚠ Card name is required</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="field-success">✓ Looks good!</div>', unsafe_allow_html=True)

        st.write("")

        st.markdown('<div class="field-label">Card Nickname</div>', unsafe_allow_html=True)
        nickname = st.text_input("Nickname", label_visibility="collapsed", placeholder="e.g., P2's Card", key="form_nick")
        st.markdown('<div class="field-help">Optional - helps identify your cards</div>', unsafe_allow_html=True)

    with col2:
        st.subheader("Number Inputs")

        st.markdown('<div class="field-label">Annual Fee <span class="field-required">*</span></div>', unsafe_allow_html=True)
        fee = st.number_input("Fee", min_value=0.0, value=95.0, label_visibility="collapsed", key="form_fee")
        st.markdown('<div class="field-success">✓ Valid amount</div>', unsafe_allow_html=True)

        st.write("")

        st.markdown('<div class="field-label">Spend Requirement</div>', unsafe_allow_html=True)
        spend = st.number_input("Spend", min_value=0.0, value=4000.0, step=500.0, label_visibility="collapsed", key="form_spend")
        st.markdown('<div class="field-help">Minimum spend for signup bonus</div>', unsafe_allow_html=True)

with tab6:
    st.header("Interactive Components")

    st.subheader("Collapsible Sections")

    with st.expander("📋 Show card details"):
        st.write("**Card Name:** Chase Sapphire Preferred")
        st.write("**Annual Fee:** $95")
        st.write("**Opened:** January 2024")

    with st.expander("💰 Show benefits"):
        st.write("- $50 Hotel Credit")
        st.write("- 3x on Dining")
        st.write("- 2x on Travel")

    st.divider()

    st.subheader("Touch-Style Buttons")
    st.caption("These buttons have mobile-friendly touch feedback")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("💾 Save", type="primary", use_container_width=True, key="touch1"):
            st.toast("Saved!", icon="✓")

    with col2:
        if st.button("🗑 Delete", use_container_width=True, key="touch2"):
            st.toast("Deleted!", icon="🗑")

    with col3:
        if st.button("📦 Archive", use_container_width=True, key="touch3"):
            st.toast("Archived!", icon="📦")

    with col4:
        if st.button("✓ Complete", use_container_width=True, key="touch4"):
            st.toast("Completed!", icon="🎉")

    st.divider()

    st.subheader("Card Actions Preview")
    st.caption("How cards would look with quick action buttons")

    st.markdown("""
    <div style="background: white; border-radius: 12px; padding: 16px; border: 1px solid #e9ecef; margin-bottom: 12px;">
        <div style="display: flex; justify-content: space-between; align-items: start;">
            <div>
                <div style="font-weight: 600; color: #124A8D;">Chase</div>
                <div style="font-size: 1.1rem; font-weight: 500;">Sapphire Preferred</div>
            </div>
            <div style="text-align: right;">
                <span style="background: #fff3cd; color: #856404; padding: 2px 8px; border-radius: 12px; font-size: 0.75rem;">SUB 45d</span>
            </div>
        </div>
        <div style="margin-top: 12px; padding-top: 12px; border-top: 1px solid #e9ecef; display: flex; gap: 8px;">
            <button style="background: #e7f3ff; color: #0066cc; border: none; padding: 6px 12px; border-radius: 16px; font-size: 0.8rem; cursor: pointer;">✎ Edit</button>
            <button style="background: #d4edda; color: #155724; border: none; padding: 6px 12px; border-radius: 16px; font-size: 0.8rem; cursor: pointer;">✓ Complete</button>
            <button style="background: #f8d7da; color: #721c24; border: none; padding: 6px 12px; border-radius: 16px; font-size: 0.8rem; cursor: pointer;">🗑 Delete</button>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.divider()
st.caption("These components are available in `src/ui/components/` for use throughout the app.")
st.caption("The component library provides Python functions that generate this CSS + HTML automatically.")
