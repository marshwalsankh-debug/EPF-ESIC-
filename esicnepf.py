import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="EPF & ESIC Dashboard", layout="wide")


# ---------------- CALCULATION ----------------
def calculate_contributions(salary):
    data = {}

    # EPF
    if salary <= 15000:
        data["epf_employee"] = salary * 0.12
        data["epf_employer"] = salary * 0.12
        data["epf_eligible"] = True
    else:
        data["epf_employee"] = 0
        data["epf_employer"] = 0
        data["epf_eligible"] = False

    # ESIC
    if salary <= 21000:
        data["esic_employee"] = salary * 0.0075
        data["esic_employer"] = salary * 0.0325
        data["esic_eligible"] = True
    else:
        data["esic_employee"] = 0
        data["esic_employer"] = 0
        data["esic_eligible"] = False

    return data


# ---------------- SAVE LEADS ----------------
def save_lead(name, email, phone, salary):
    lead = pd.DataFrame([{
        "Name": name,
        "Email": email,
        "Phone": phone,
        "Salary": salary,
        "Request_Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }])

    file_exists = os.path.isfile("leads.csv")

    lead.to_csv(
        "leads.csv",
        mode="a",
        header=not file_exists,
        index=False
    )


# ---------------- CHART ----------------
def show_chart(data):
    categories = ["EPF Employee", "EPF Employer", "ESIC Employee", "ESIC Employer"]

    values = [
        data["epf_employee"],
        data["epf_employer"],
        data["esic_employee"],
        data["esic_employer"]
    ]

    colors = [
        "#FDE68A",  # EPF Employee (Light Yellow)
        "#B45309",  # EPF Employer (Dark Yellow)
        "#93C5FD",  # ESIC Employee (Light Blue)
        "#1E3A8A"   # ESIC Employer (Dark Blue)
    ]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=categories,
        x=values,
        orientation='h',
        marker=dict(color=colors),
        text=[f"₹{v:.2f}" for v in values],
        textposition="auto"
    ))

    fig.update_layout(
        title="EPF & ESIC Contribution Breakdown",
        height=500,
        xaxis_title="Amount (₹)"
    )

    return fig


# ---------------- MENU ----------------
menu = st.sidebar.selectbox(
    "📂 Data Menu",
    ["Dashboard", "Employee Calculator", "Lead Generation", "View Requests", "About"]
)


# ---------------- DASHBOARD ----------------
if menu == "Dashboard":
    st.title("🏢 EPF & ESIC Payroll Dashboard")
    st.info("Use this system to calculate salary deductions and generate consultancy leads.")

# ---------------- EMPLOYEE CALCULATOR ----------------
elif menu == "Employee Calculator":
    st.title("👤 Salary Calculator")

    name = st.text_input("Employee Name")
    salary = st.number_input("Monthly Salary (₹)", min_value=0, step=1000)

    if st.button("Calculate"):
        data = calculate_contributions(salary)

        st.success(f"Report generated for {name}")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 🟡 EPF")
            st.write("Eligible:", "✅ Yes" if data["epf_eligible"] else "❌ No")
            st.write(f"Employee: ₹{data['epf_employee']:.2f}")
            st.write(f"Employer: ₹{data['epf_employer']:.2f}")

        with col2:
            st.markdown("### 🔵 ESIC")
            st.write("Eligible:", "✅ Yes" if data["esic_eligible"] else "❌ No")
            st.write(f"Employee: ₹{data['esic_employee']:.2f}")
            st.write(f"Employer: ₹{data['esic_employer']:.2f}")

        st.plotly_chart(show_chart(data), use_container_width=True)


# ---------------- LEAD GENERATION ----------------
elif menu == "Lead Generation":
    st.title("📞 Request a Personalised Call")
    st.write("Book consultation with **CA Tulsi Rawlani**")

    with st.form("lead_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        phone = st.text_input("Phone Number")
        salary = st.number_input("Monthly Salary (₹)", min_value=0, step=1000)

        submitted = st.form_submit_button("Request Call")

        if submitted:
            if name and email and phone:
                save_lead(name, email, phone, salary)
                st.success("✅ Your request has been submitted!")
                st.info("📞 Our team will contact you soon for consultation.")
            else:
                st.error("Please fill all required fields")


# ---------------- VIEW REQUESTS ----------------
elif menu == "View Requests":
    st.title("📋 Lead Requests - CA Tulsi Rawlani")

    if os.path.exists("leads.csv"):
        df = pd.read_csv("leads.csv")

        st.success(f"Total Requests: {len(df)}")
        st.dataframe(df, use_container_width=True)

        st.subheader("🔍 Filter by Salary")
        salary_filter = st.slider("Max Salary", 0, 200000, 50000)

        filtered = df[df["Salary"] <= salary_filter]
        st.dataframe(filtered, use_container_width=True)

    else:
        st.warning("No leads found yet.")


# ---------------- ABOUT ----------------
elif menu == "About":
    st.title("ℹ️ About This System")

    st.write("""
    This application provides:

    - EPF calculation (Employee + Employer)
    - ESIC calculation (Employee + Employer)
    - Salary breakdown dashboard
    - Lead generation system
    - CRM-style lead management

    Built using Streamlit + Plotly 🚀
    """)