from datetime import date
from collections import Counter
import streamlit as st

from db import (
    get_conn, init_db, sign_in_or_create,
    add_log, get_recent_logs, delete_log,
    list_exercises, get_logs_by_exercise,
    list_dates, get_logs_by_date
)


st.set_page_config(
    page_title="Workout Log",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title("Workout Log")
st.caption("Private & Simple Tracking")

conn = get_conn()
init_db(conn)


with st.sidebar:
    st.header("Sign in / Create")
    user = st.text_input("Username").strip()
    pin = st.text_input("PIN", type="password").strip()

    if not user or not pin:
        st.info("Enter username and PIN to continue.")
        st.stop()

    if not sign_in_or_create(conn, user, pin):
        st.error("Wrong PIN.")
        st.stop()

    st.success(f"Signed in as **{user}**")


tab_log, tab_history, tab_ex, tab_date = st.tabs(
    ["Log", "History", "By Exercise", "By Date"]
)

with tab_log:
    st.subheader("Log a set")

    with st.form("log_form", clear_on_submit=False):
        day = st.date_input("Date", value=date.today())

        existing = list_exercises(conn, user)
        hint = "Keep names consistent."
        if existing:
            hint += " Existing: " + ", ".join(existing[:6]) + ("…" if len(existing) > 6 else "")

        exercise = st.text_input("Exercise", value="Bench Press", help=hint)

        c1, c2 = st.columns(2)
        with c1:
            weight = st.number_input("Weight", min_value=0.0, value=20.0, step=2.5)
        with c2:
            reps = st.number_input("Reps", min_value=1, value=8, step=1)

        submitted = st.form_submit_button("Add set", use_container_width=True)

        if submitted:
            if not exercise.strip():
                st.error("Exercise cannot be empty.")
            else:
                add_log(conn, user, day.isoformat(), exercise.strip(), weight, int(reps))
                st.success("Set logged.")
                st.rerun()


with tab_history:
    st.subheader("Recent sets")

    rows = get_recent_logs(conn, user, limit=50)
    if not rows:
        st.write("No entries yet.")
    else:
        table = [
            {"ID": i, "Date": d, "Exercise": ex, "Weight": w, "Reps": r}
            for i, d, ex, w, r in rows
        ]
        st.dataframe(table, use_container_width=True, hide_index=True)

        st.divider()
        st.subheader("Delete a set")
        st.caption("This action cannot be undone.")

        ids = [i for i, *_ in rows]
        del_id = st.selectbox("Select ID to delete", ids)

        if st.button("Delete selected set", type="secondary"):
            delete_log(conn, user, del_id)
            st.warning("Set deleted.")
            st.rerun()

with tab_ex:
    st.subheader("Exercise history")

    exercises = list_exercises(conn, user)
    if not exercises:
        st.info("Log some sets to view exercise history.")
    else:
        ex = st.selectbox("Exercise", exercises)
        hist = get_logs_by_exercise(conn, user, ex)

        st.caption(f"Total sets logged: {len(hist)}")

        hist_table = [
            {"ID": i, "Date": d, "Weight": w, "Reps": r}
            for i, d, w, r in hist
        ]
        st.dataframe(hist_table, use_container_width=True, hide_index=True)


with tab_date:
    st.subheader("Workout by date")

    dates = list_dates(conn, user)
    if not dates:
        st.info("Log some sets to view sessions by date.")
    else:
        chosen_day = st.selectbox("Date", dates)
        day_rows = get_logs_by_date(conn, user, chosen_day)

        counts = Counter(ex for _, ex, _, _ in day_rows)
        summary = " • ".join(f"{ex}: {cnt} sets" for ex, cnt in counts.items())

        st.caption(summary)
        st.caption(f"Total sets: {len(day_rows)}")

        day_table = [
            {"ID": i, "Exercise": ex, "Weight": w, "Reps": r}
            for i, ex, w, r in day_rows
        ]
        st.dataframe(day_table, use_container_width=True, hide_index=True)


