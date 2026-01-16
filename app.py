import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

import tracker as db

st.set_page_config(page_title="Expense Tracker", layout="centered")
db.create_table()

st.title("💸 Expense Tracker")

st.subheader("Add an expense")

with st.form("add_expense", clear_on_submit=True):
    expense_date = st.date_input("Date", value=date.today())
    category = st.text_input("Category", placeholder="Food, Transport, etc.")
    amount = st.number_input("Amount", min_value=0.0, step=0.01)
    submitted = st.form_submit_button("Add")

if submitted:
    if category.strip() == "":
        st.error("Category cannot be empty")
    else:
        db.add_expense(expense_date.isoformat(), category.strip(), float(amount))
        st.success("Expense added")
        st.rerun()


st.subheader("All expenses (edit / delete)")

rows_all = db.get_all_expenses()

if rows_all:
    df_all = pd.DataFrame(rows_all, columns=["ID", "Date", "Category", "Amount"])
    st.dataframe(df_all, use_container_width=True, hide_index=True)

    expense_ids = df_all["ID"].tolist()

    selected_id = st.selectbox("Select expense ID", expense_ids)


    current = df_all[df_all["ID"] == selected_id].iloc[0]
    current_date = current["Date"]
    current_category = current["Category"]
    current_amount = float(current["Amount"])

    st.subheader("Update selected expense")

    with st.form("update_expense"):
        new_date = st.date_input("New date", value=pd.to_datetime(current_date).date())
        new_category = st.text_input("New category", value=str(current_category))
        new_amount = st.number_input("New amount", min_value=0.0, step=0.01, value=current_amount)

        update_btn = st.form_submit_button("Update")

    if update_btn:
        if new_category.strip() == "":
            st.error("Category cannot be empty")
        else:
            db.update_expense(
                int(selected_id),
                new_date.isoformat(),
                new_category.strip(),
                float(new_amount),
            )
            st.success("Expense updated")
            st.rerun()


    st.subheader("Delete selected expense")

    if st.button("Delete"):
        db.delete_expense(int(selected_id))
        st.success("Expense deleted")
        st.rerun()

else:
    st.info("No expenses yet.")


st.subheader("Monthly summary")

month = st.text_input("Month (YYYY-MM)", value=date.today().strftime("%Y-%m"))

if month:
    total, rows = db.get_monthly_summary(month)

    if rows:
        df = pd.DataFrame(rows, columns=["Category", "Amount"])
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.metric("Total spent", f"${total:.2f}")

        fig, ax = plt.subplots()
        ax.pie(df["Amount"], labels=df["Category"], autopct="%1.1f%%")
        ax.set_title(f"Spending Breakdown ({month})")
        st.pyplot(fig)


        st.subheader("Spending over time")

        daily_rows = db.get_daily_totals(month)
        if daily_rows:
            daily_df = pd.DataFrame(daily_rows, columns=["Date", "Total"])
            daily_df["Date"] = pd.to_datetime(daily_df["Date"]).dt.strftime("%b %d")
            daily_df = daily_df.sort_values("Date")

            st.line_chart(daily_df.set_index("Date")["Total"])
        else:
            st.info("No daily spending data to plot.")
    else:
        st.info("No expenses recorded for this month.")
