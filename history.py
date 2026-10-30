
import streamlit as st
import json
import pandas as pd
from database.db import get_history, delete_history


def render():
    st.markdown(
        '<div class="eyebrow">SAVED ANALYSES</div>'
        '<h1>History</h1>'
        '<p class="muted">Your recent analyses for this account.</p>',
        unsafe_allow_html=True
    )

    user_id = st.session_state.user_id
    rows = get_history(user_id)

    if not rows:
        st.info("अजून saved analysis नाही.")
        return

    for row in rows:
        history_id = row["id"]

        with st.expander(
            f"{row['filename']} · {row['created_at']}"
        ):
            skills = json.loads(row["skills_json"])
            results = json.loads(row["results_json"])

            st.write(
                "Detected skills:",
                ", ".join(skills) or "None detected"
            )

            st.dataframe(
                pd.DataFrame([
                    {
                        "Role": r["title"],
                        "Match": r["score"],
                        "Category": r["category"]
                    }
                    for r in results
                ]),
                use_container_width=True,
                hide_index=True
            )

            confirm_key = f"confirm_delete_{history_id}"

            if not st.session_state.get(confirm_key, False):
                if st.button(
                    "🗑️ Delete Analysis",
                    key=f"delete_{history_id}"
                ):
                    st.session_state[confirm_key] = True
                    st.rerun()

            else:
                st.warning(
                    "Are you sure you want to delete this analysis?"
                )

                col1, col2 = st.columns(2)

                with col1:
                    if st.button(
                        "Yes, Delete",
                        key=f"confirm_{history_id}"
                    ):
                        delete_history(history_id, user_id)
                        st.session_state.pop(confirm_key, None)
                        st.success("Analysis deleted successfully.")
                        st.rerun()

                with col2:
                    if st.button(
                        "Cancel",
                        key=f"cancel_{history_id}"
                    ):
                        st.session_state.pop(confirm_key, None)
                        st.rerun()
