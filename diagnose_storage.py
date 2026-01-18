"""Diagnostic tool to figure out why localStorage isn't working."""

import streamlit as st

st.set_page_config(page_title="ChurnPilot Storage Diagnostic", page_icon="🔧")

st.title("🔧 ChurnPilot Storage Diagnostic")

st.markdown("""
This page will help diagnose localStorage issues.
""")

# Check 1: pyarrow
st.header("1. Check Dependencies")
try:
    import pyarrow
    st.success(f"✓ pyarrow installed: {pyarrow.__version__}")
except ImportError:
    st.error("✗ pyarrow NOT installed - localStorage won't work!")
    st.code("pip install pyarrow")

try:
    from streamlit_js_eval import streamlit_js_eval
    st.success("✓ streamlit-js-eval installed")
except ImportError:
    st.error("✗ streamlit-js-eval NOT installed")
    st.code("pip install streamlit-js-eval")

# Check 2: Test localStorage with simple sync JS
st.header("2. Test localStorage (Simple Sync JS)")

if st.button("Test Write & Read"):
    try:
        from streamlit_js_eval import streamlit_js_eval

        # Simple synchronous test - no Promises
        js_code = """
        (function() {
            try {
                localStorage.setItem('churnpilot_test', 'test_12345');
                var value = localStorage.getItem('churnpilot_test');
                return {
                    success: true,
                    written: 'test_12345',
                    read: value,
                    match: value === 'test_12345'
                };
            } catch (e) {
                return {
                    success: false,
                    error: e.message
                };
            }
        })()
        """

        result = streamlit_js_eval(js=js_code, key="test_localstorage_sync")

        if result is None:
            st.warning("⚠️ streamlit_js_eval returned None")
            st.info("This may be a timing issue. Try clicking the button again.")
        elif result.get('success'):
            if result.get('match'):
                st.success("✓ localStorage write/read works!")
                st.json(result)
            else:
                st.warning("⚠️ localStorage write succeeded but read mismatch")
                st.json(result)
        else:
            st.error("✗ localStorage failed")
            st.json(result)
    except Exception as e:
        st.error(f"✗ Exception: {e}")

# Check 3: Test fire-and-forget save (new method)
st.header("3. Test Fire-and-Forget Save")

if st.button("Test HTML Injection Save"):
    try:
        from streamlit.components.v1 import html
        import json

        test_data = [{"id": "test", "name": "Test Card"}]
        data_json = json.dumps(test_data)
        data_escaped = data_json.replace('\\', '\\\\').replace("'", "\\'")

        save_script = f"""
        <script>
        (function() {{
            try {{
                localStorage.setItem('churnpilot_test_html', '{data_escaped}');
                console.log('[Test] Saved via HTML injection');
            }} catch (e) {{
                console.error('[Test] Save error:', e);
            }}
        }})();
        </script>
        """

        html(save_script, height=0, width=0)
        st.success("✓ HTML injection executed (check browser console for confirmation)")
        st.info("Now click 'Verify HTML Save' to check if it worked")
    except Exception as e:
        st.error(f"✗ Exception: {e}")

if st.button("Verify HTML Save"):
    try:
        from streamlit_js_eval import streamlit_js_eval

        js_code = """
        (function() {
            try {
                var data = localStorage.getItem('churnpilot_test_html');
                if (data) {
                    return JSON.parse(data);
                }
                return null;
            } catch (e) {
                return {error: e.message};
            }
        })()
        """

        result = streamlit_js_eval(js=js_code, key="verify_html_save")

        if result is None:
            st.warning("⚠️ streamlit_js_eval returned None - timing issue")
        elif isinstance(result, list):
            st.success(f"✓ HTML save worked! Found {len(result)} items")
            st.json(result)
        elif isinstance(result, dict) and result.get('error'):
            st.error(f"✗ Error: {result.get('error')}")
        else:
            st.info(f"Result: {result}")
    except Exception as e:
        st.error(f"✗ Exception: {e}")

# Check 4: View current data
st.header("4. View Current ChurnPilot Data")

if st.button("Check ChurnPilot Cards"):
    try:
        from streamlit_js_eval import streamlit_js_eval

        js_code = """
        (function() {
            try {
                var data = localStorage.getItem('churnpilot_cards');
                if (data) {
                    var parsed = JSON.parse(data);
                    return {
                        found: true,
                        count: parsed.length,
                        size: data.length,
                        cards: parsed
                    };
                } else {
                    return {found: false};
                }
            } catch (e) {
                return {error: e.message};
            }
        })()
        """

        result = streamlit_js_eval(js=js_code, key="check_churnpilot_data")

        if result is None:
            st.warning("⚠️ streamlit_js_eval returned None")
        elif result.get('found'):
            st.success(f"✓ Found {result.get('count')} cards in localStorage")
            with st.expander("View cards data"):
                st.json(result.get('cards', []))
        elif result.get('error'):
            st.error(f"✗ Error: {result.get('error')}")
        else:
            st.info("No ChurnPilot data found in localStorage")
    except Exception as e:
        st.error(f"✗ Exception: {e}")

# Check 5: Clear test data
st.header("5. Clear Test Data")

col1, col2 = st.columns(2)

with col1:
    if st.button("Clear Test Keys Only"):
        try:
            from streamlit.components.v1 import html

            clear_script = """
            <script>
            localStorage.removeItem('churnpilot_test');
            localStorage.removeItem('churnpilot_test_html');
            console.log('[Test] Cleared test keys');
            </script>
            """

            html(clear_script, height=0, width=0)
            st.success("✓ Cleared test keys")
        except Exception as e:
            st.error(f"✗ Exception: {e}")

with col2:
    if st.button("⚠️ Clear ALL ChurnPilot Data"):
        try:
            from streamlit.components.v1 import html

            clear_script = """
            <script>
            localStorage.removeItem('churnpilot_cards');
            localStorage.removeItem('churnpilot_test');
            localStorage.removeItem('churnpilot_test_html');
            console.log('[Test] Cleared all ChurnPilot data');
            </script>
            """

            html(clear_script, height=0, width=0)
            st.warning("⚠️ Cleared ALL ChurnPilot data - app will start fresh")
        except Exception as e:
            st.error(f"✗ Exception: {e}")

# Check 6: Session state
st.header("6. Session State")

st.write("Current session state:")
st.json({
    "cards_data_count": len(st.session_state.get('cards_data', [])),
    "storage_initialized": st.session_state.get('storage_initialized', False),
})

# Recommendations
st.header("7. Recommendations")

st.markdown("""
**New Approach Used:**
- Saving now uses `st.components.v1.html()` (fire-and-forget, more reliable)
- Loading still uses `streamlit_js_eval()` with simple sync JS (no Promises)
- Session state is ALWAYS updated first (immediate use)
- localStorage is for persistence across sessions

**If tests pass but main app doesn't work:**
- Session state should work for within-session use
- localStorage is for browser restart persistence
- Check browser console (F12) for errors

**If streamlit_js_eval returns None:**
- This is a known timing issue
- Click the button again - it often works on second try
- The new fire-and-forget save method avoids this issue

**Testing Persistence:**
1. Use main app to add a card
2. Card should appear immediately (session state)
3. Close browser, reopen app
4. Card should reload from localStorage
""")

# Browser info
st.header("8. Browser Information")

try:
    from streamlit_js_eval import streamlit_js_eval

    js_code = """
    (function() {
        return {
            userAgent: navigator.userAgent.substring(0, 100),
            cookieEnabled: navigator.cookieEnabled,
            localStorage: typeof localStorage !== 'undefined'
        };
    })()
    """

    result = streamlit_js_eval(js=js_code, key="browser_info")
    if result:
        st.json(result)
    else:
        st.warning("Could not get browser info")
except Exception as e:
    st.error(f"Exception: {e}")
