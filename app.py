import streamlit as st
import pandas as pd
import plotly.express as px

# ---------- Page setup ----------
st.set_page_config(page_title="Student Performance Dashboard", layout="wide")

st.title("📊 Student Performance Dashboard")
st.write("Periodic Test 2 — Computer Science (25 marks)")

# ---------- Load data ----------
df = pd.read_csv("students.csv")

# ---------- Sidebar filters ----------
st.sidebar.header("🎛 Filters")

section = st.sidebar.selectbox("Section", options=["All"] + sorted(df["Section"].unique().tolist()))
min_marks = st.sidebar.slider("Minimum marks", 0, 25, 0)

filtered_df = df.copy()
if section != "All":
    filtered_df = filtered_df[filtered_df["Section"] == section]
filtered_df = filtered_df[filtered_df["Marks"] >= min_marks]

# ---------- Metric cards ----------
col1, col2, col3, col4 = st.columns(4)
col1.metric("Class Average", round(filtered_df["Marks"].mean(), 1) if len(filtered_df) else 0)
col2.metric("Highest Score", filtered_df["Marks"].max() if len(filtered_df) else 0)
col3.metric("At Risk (<12)", int((filtered_df["Marks"] < 12).sum()))
pass_rate = round((filtered_df["Marks"] >= 10).mean() * 100, 1) if len(filtered_df) else 0
col4.metric("Pass Rate", f"{pass_rate}%")

st.divider()

# ---------- Charts ----------
chart_col1, chart_col2 = st.columns([1.3, 1])

with chart_col1:
    st.subheader("Marks by Student")
    st.bar_chart(filtered_df.set_index("Name")["Marks"])

with chart_col2:
    st.subheader("Grade Distribution")

    def grade(m):
        if m >= 20: return "A (20-25)"
        elif m >= 15: return "B (15-19)"
        elif m >= 10: return "C (10-14)"
        else: return "D (<10)"

    filtered_df["Grade"] = filtered_df["Marks"].apply(grade)
    grade_counts = filtered_df["Grade"].value_counts().reset_index()
    grade_counts.columns = ["Grade", "Count"]

    fig = px.pie(grade_counts, names="Grade", values="Count")
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# ---------- Table ----------
st.subheader("Student-wise Detail")
st.dataframe(filtered_df.sort_values("Marks", ascending=False), use_container_width=True)
