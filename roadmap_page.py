
import streamlit as st
from core.roadmap import build_roadmap


def render():
    st.markdown(
        '<div class="eyebrow">PERSONALIZED SKILL DEVELOPMENT</div>'
        '<h1>Career roadmap</h1>'
        '<p class="muted">A practical sequence based on the missing skills '
        'for your chosen role.</p>',
        unsafe_allow_html=True
    )

    results = st.session_state.get("job_results", [])

    if not results:
        st.info("Roadmap तयार करण्यासाठी आधी resume analyze करा.")
        return

    role = st.selectbox(
        "Target job role",
        [r["title"] for r in results],
        key="roadmap_target_role"
    )

    selected = next(r for r in results if r["title"] == role)

    st.metric("Current match score", f"{selected['score']}%")

    st.write(
        "Priority skill gaps:",
        ", ".join(
            selected["missing_required"]
            or selected["missing_preferred"]
        ) or "No required gaps detected"
    )

    roadmap = build_roadmap(selected)

    total_tasks = sum(len(item["tasks"]) for item in roadmap)
    completed_tasks = 0

    st.markdown("## Your learning progress")

    progress_placeholder = st.empty()

    for week_index, item in enumerate(roadmap):
        with st.container(border=True):
            st.markdown(f"### {item['week']} · {item['focus']}")

            for task_index, task in enumerate(item["tasks"]):
                task_key = (
                    f"roadmap_{role}_{week_index}_{task_index}_{task}"
                )

                col1, col2 = st.columns([0.8, 0.2])

                with col1:
                    is_done = st.checkbox(
                        task,
                        key=task_key
                    )

                with col2:
                    if is_done:
                        st.success("Done")
                        completed_tasks += 1
                    else:
                        st.caption("Pending")

    if total_tasks > 0:
        progress = completed_tasks / total_tasks

        progress_placeholder.progress(
            progress,
            text=f"{completed_tasks} of {total_tasks} tasks completed"
        )

        if completed_tasks == total_tasks:
            st.success(
                "🎉 Roadmap Complete! All tasks have been completed."
            )
            st.balloons()
        else:
            st.info(
                f"Keep going! {total_tasks - completed_tasks} "
                "task(s) remaining."
            )
    else:
        st.info("या role साठी सध्या कोणतेही roadmap tasks उपलब्ध नाहीत.")

    st.caption(
        "Roadmap is a starter plan generated from detected skill gaps. "
        "Adjust it to your time, current knowledge and target job requirements."
    )
