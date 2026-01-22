import streamlit as st
import requests
from datetime import date, datetime
import pandas as pd
import os

# API Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


def api_get(endpoint):
    """Make GET request to API"""
    try:
        response = requests.get(f"{API_BASE_URL}{endpoint}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return None

def api_get(endpoint):
    """Make GET request to API"""
    try:
        response = requests.get(f"{API_BASE_URL}{endpoint}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return None


def api_post(endpoint, data):
    """Make POST request to API"""
    try:
        response = requests.post(f"{API_BASE_URL}{endpoint}", json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return None


def api_put(endpoint, data):
    """Make PUT request to API"""
    try:
        response = requests.put(f"{API_BASE_URL}{endpoint}", json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return None


def api_delete(endpoint):
    """Make DELETE request to API"""
    try:
        response = requests.delete(f"{API_BASE_URL}{endpoint}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return None


# Page Configuration
st.title("🔬 R&D Initiative Tracker")

# Sidebar filters
st.sidebar.header("Filters")
stage_filter = st.sidebar.selectbox(
    "Stage",
    ["All", "feasibility", "validation", "development", "launch_prep", "launched", "on_hold", "cancelled"]
)
priority_filter = st.sidebar.selectbox(
    "Priority",
    ["All", "low", "medium", "high", "critical"]
)
is_active_filter = st.sidebar.selectbox(
    "Status",
    ["All", "active", "inactive", "completed"]
)

# Build query parameters
params = []
if stage_filter != "All":
    params.append(f"stage={stage_filter}")
if priority_filter != "All":
    params.append(f"priority={priority_filter}")
if is_active_filter != "All":
    params.append(f"is_active={is_active_filter}")

query_string = "&" + "&".join(params) if params else ""

# Fetch initiatives
initiatives = api_get(f"/api/rd/initiatives?{query_string}")

# Main content tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "➕ New Initiative", "💰 Expenses & Revenue", "📈 ROI Analysis"])

# ==================
# TAB 1: OVERVIEW
# ==================
with tab1:
    if initiatives:
        st.subheader(f"Active Initiatives ({len(initiatives)})")
        
        # Create initiative cards
        for initiative in initiatives:
            with st.expander(f"**{initiative['name']}** - {initiative['stage'].title()} ({initiative['priority'].upper()})"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write("**Details**")
                    st.write(f"Lead: {initiative.get('lead_owner', 'Unassigned')}")
                    st.write(f"Target Market: {initiative.get('target_market', 'Not specified')}")
                    if initiative.get('target_price'):
                        st.write(f"Target Price: ${initiative['target_price']:,.2f}")
                    if initiative.get('target_margin'):
                        st.write(f"Target Margin: {initiative['target_margin']}%")
                
                with col2:
                    st.write("**Timeline**")
                    if initiative.get('start_date'):
                        st.write(f"Started: {initiative['start_date']}")
                    if initiative.get('target_launch_date'):
                        st.write(f"Target Launch: {initiative['target_launch_date']}")
                    if initiative.get('actual_launch_date'):
                        st.write(f"Launched: {initiative['actual_launch_date']}")
                
                with col3:
                    st.write("**Actions**")
                    if st.button(f"View Details", key=f"view_{initiative['id']}"):
                        st.session_state['selected_initiative'] = initiative['id']
                        st.rerun()
                    if st.button(f"🗑️ Delete", key=f"delete_{initiative['id']}"):
                        if api_delete(f"/api/rd/initiatives/{initiative['id']}"):
                            st.success("Initiative deleted!")
                            st.rerun()
    else:
        st.info("No initiatives found. Create your first R&D initiative in the 'New Initiative' tab!")

# ==================
# TAB 2: NEW INITIATIVE
# ==================
with tab2:
    st.subheader("Create New R&D Initiative")
    
    with st.form("new_initiative_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Initiative Name*", placeholder="PEth Stock Product Development")
            description = st.text_area("Description", placeholder="Develop standardized PEth QC product...")
            stage = st.selectbox("Stage", ["feasibility", "validation", "development", "launch_prep", "launched"])
            priority = st.selectbox("Priority", ["low", "medium", "high", "critical"])
            lead_owner = st.text_input("Lead Owner", placeholder="Chy Plutchak")
        
        with col2:
            target_market = st.text_area("Target Market", placeholder="Clinical labs performing alcohol monitoring...")
            market_size_estimate = st.number_input("Market Size Estimate ($)", min_value=0.0, step=1000.0)
            target_price = st.number_input("Target Price ($)", min_value=0.0, step=10.0)
            target_margin = st.number_input("Target Margin (%)", min_value=0.0, max_value=100.0, step=1.0)
            start_date = st.date_input("Start Date")
            target_launch_date = st.date_input("Target Launch Date")
        
        submit = st.form_submit_button("Create Initiative")
        
        if submit:
            if not name:
                st.error("Initiative name is required!")
            else:
                data = {
                    "name": name,
                    "description": description,
                    "stage": stage,
                    "priority": priority,
                    "lead_owner": lead_owner,
                    "target_market": target_market,
                    "market_size_estimate": market_size_estimate if market_size_estimate > 0 else None,
                    "target_price": target_price if target_price > 0 else None,
                    "target_margin": target_margin if target_margin > 0 else None,
                    "start_date": start_date.isoformat(),
                    "target_launch_date": target_launch_date.isoformat(),
                }
                
                result = api_post("/api/rd/initiatives", data)
                if result:
                    st.success(f"Initiative '{name}' created successfully!")
                    st.rerun()

# ==================
# TAB 3: EXPENSES & REVENUE
# ==================
with tab3:
    if initiatives:
        selected_initiative = st.selectbox(
            "Select Initiative",
            options=initiatives,
            format_func=lambda x: x['name']
        )
        
        if selected_initiative:
            initiative_id = selected_initiative['id']
            
            col1, col2 = st.columns(2)
            
            # EXPENSES
            with col1:
                st.subheader("💸 Expenses")
                
                with st.expander("➕ Add Expense"):
                    with st.form(f"expense_form_{initiative_id}"):
                        expense_category = st.selectbox("Category", ["Samples", "Travel", "Materials", "Staffing", "Marketing", "Other"])
                        expense_description = st.text_input("Description")
                        amount = st.number_input("Amount ($)", min_value=0.0, step=10.0)
                        expense_date = st.date_input("Date", value=date.today())
                        department = st.selectbox("Department", ["Marketing", "Sales", "Ops", "Manufacturing"])
                        
                        if st.form_submit_button("Add Expense"):
                            expense_data = {
                                "initiative_id": initiative_id,
                                "expense_category": expense_category,
                                "expense_description": expense_description,
                                "amount": amount,
                                "expense_date": expense_date.isoformat(),
                                "department": department
                            }
                            if api_post("/api/rd/expenses", expense_data):
                                st.success("Expense added!")
                                st.rerun()
                
                # Show expenses
                expenses = api_get(f"/api/rd/expenses/initiative/{initiative_id}")
                if expenses:
                    expense_df = pd.DataFrame(expenses)
                    st.dataframe(expense_df[['expense_category', 'amount', 'expense_date', 'department']], use_container_width=True)
                    
                    total_expenses = api_get(f"/api/rd/expenses/initiative/{initiative_id}/total")
                    if total_expenses:
                        st.metric("Total Expenses", f"${total_expenses['total_expenses']:,.2f}")
                else:
                    st.info("No expenses recorded yet.")
            
            # REVENUE
            with col2:
                st.subheader("💰 Revenue")
                
                with st.expander("➕ Add Revenue"):
                    with st.form(f"revenue_form_{initiative_id}"):
                        customer_name = st.text_input("Customer Name")
                        order_number = st.text_input("Order Number")
                        order_value = st.number_input("Order Value ($)", min_value=0.0, step=100.0)
                        order_date = st.date_input("Order Date", value=date.today())
                        product_launched = st.selectbox("Product Launched?", ["no", "yes"])
                        
                        if st.form_submit_button("Add Revenue"):
                            revenue_data = {
                                "initiative_id": initiative_id,
                                "customer_name": customer_name,
                                "order_number": order_number,
                                "order_value": order_value,
                                "order_date": order_date.isoformat(),
                                "product_launched": product_launched
                            }
                            if api_post("/api/rd/revenue", revenue_data):
                                st.success("Revenue added!")
                                st.rerun()
                
                # Show revenue
                revenue = api_get(f"/api/rd/revenue/initiative/{initiative_id}")
                if revenue:
                    revenue_df = pd.DataFrame(revenue)
                    st.dataframe(revenue_df[['customer_name', 'order_value', 'order_date']], use_container_width=True)
                    
                    total_revenue = api_get(f"/api/rd/revenue/initiative/{initiative_id}/total")
                    if total_revenue:
                        st.metric("Total Revenue", f"${total_revenue['total_revenue']:,.2f}")
                else:
                    st.info("No revenue recorded yet.")
    else:
        st.info("Create an initiative first!")

# ==================
# TAB 4: ROI ANALYSIS
# ==================
with tab4:
    if initiatives:
        st.subheader("ROI Summary")
        
        for initiative in initiatives:
            initiative_id = initiative['id']
            
            # Get expenses and revenue
            total_expenses_data = api_get(f"/api/rd/expenses/initiative/{initiative_id}/total")
            total_revenue_data = api_get(f"/api/rd/revenue/initiative/{initiative_id}/total")
            
            total_expenses = total_expenses_data.get('total_expenses', 0) if total_expenses_data else 0
            total_revenue = total_revenue_data.get('total_revenue', 0) if total_revenue_data else 0
            
            if total_expenses > 0 or total_revenue > 0:
                with st.expander(f"**{initiative['name']}**"):
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Total Investment", f"${total_expenses:,.2f}")
                    
                    with col2:
                        st.metric("Total Revenue", f"${total_revenue:,.2f}")
                    
                    with col3:
                        net = total_revenue - total_expenses
                        st.metric("Net Profit/Loss", f"${net:,.2f}", delta=None)
                    
                    with col4:
                        if total_expenses > 0:
                            roi = ((total_revenue - total_expenses) / total_expenses) * 100
                            st.metric("ROI", f"{roi:.1f}%")
                        else:
                            st.metric("ROI", "N/A")
    else:
        st.info("No initiatives to analyze.")

# API Status
st.sidebar.markdown("---")
st.sidebar.markdown("### API Status")
try:
    health = api_get("/health")
    if health:
        st.sidebar.success("✅ API Connected")
    else:
        st.sidebar.error("❌ API Error")
except:
    st.sidebar.error("❌ API Offline")