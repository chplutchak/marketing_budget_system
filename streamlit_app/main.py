import streamlit as st
import requests
import pandas as pd
from datetime import date, datetime
import plotly.express as px
import plotly.graph_objects as go
from calendar import month_name

API_BASE_URL = "http://localhost:8000"

st.set_page_config(page_title="Marketing Budget Management", page_icon="💼", layout="wide")
st.title("💼 Marketing Budget Management System")

# Sidebar navigation
page = st.sidebar.selectbox(
    "Navigate to:",
    ["Getting Started", "Dashboard", "Campaigns", "Budget Items", "Expenses", 
     "Budget vs Actual", "ROI Tracking", "Cost Centers"]
)

# API Helper Functions
def api_get(endpoint):
    try:
        response = requests.get(f"{API_BASE_URL}{endpoint}")
        return response.json() if response.status_code == 200 else []
    except: return []

def api_post(endpoint, data):
    try:
        response = requests.post(f"{API_BASE_URL}{endpoint}", json=data)
        return response.json() if response.status_code == 200 else None
    except: return None    

def api_put(endpoint, data):
    try:
        response = requests.put(f"{API_BASE_URL}{endpoint}", json=data)
        return response.json() if response.status_code == 200 else None
    except: return None

def api_delete(endpoint):
    try:
        response = requests.delete(f"{API_BASE_URL}{endpoint}")
        return response.status_code == 200
    except: return False

# Getting Started Page
if page == "Getting Started":
    st.header("Getting Started with Budget Management")
    
    st.markdown("""
    ## Complete Budget Management Workflow
    
    ### Step 1: Set Up Cost Centers
    **What:** Functional areas for tracking spending (like QuickBooks Classes)  
    **Examples:** Digital Marketing (DM001), Events (EV001), Content (CC001)  
    **Why:** Report spending by area and assign accountability
    
    ### Step 2: Create Campaign Hierarchy
    **Structure:**
    - **Level 1:** Department (e.g., "2026 Marketing Department")
    - **Level 2:** Campaign Category (e.g., "Digital Marketing")  
    - **Level 3:** Specific Campaigns (e.g., "Q1 Google Ads")
    
    ### Step 3: Add Budget Line Items
    - Specific expenses within campaigns
    - Include monthly distribution
    - Assign category and cost center
    
    ### Step 4: Track Actual Expenses
    - Record real spending as it happens
    - Link to budget line items
    - Track vendor, invoice, payment method
    
    ### Step 5: Monitor Budget vs Actual
    - Monthly variance analysis
    - Identify overspending early
    - Adjust forecasts based on actuals
    
    ### Step 6: Calculate ROI
    - Attribute revenue to campaigns
    - Track performance metrics (leads, conversions)
    - Determine campaign effectiveness
    
    ---
    
    ## UTAK Example Structure
    
    ```
    2026 Marketing ($500K)
    ├── Digital Marketing ($200K)
    │   └── Q1 Google Ads ($25K)
    │       └── ACTUAL: $8,200 spent in Jan (Budget: $8,000)
    │       └── ROI: 250% (Generated $28,500 revenue)
    ├── Trade Shows ($150K)
    │   └── SOFT Conference ($45K)
    │       └── ACTUAL: $42,000 spent
    │       └── ROI: 180% (3 new contracts)
    ```
    
    **Cost Centers:** DM001 (Digital), EV001 (Events), CC001 (Content), RD001 (R&D Marketing)
    
    ---
    
    ## QuickBooks Integration
    Export to CSV from Budget Items or Expenses pages, then import into QuickBooks.
    """)

# Dashboard Page  
elif page == "Dashboard":
    st.header("📊 Dashboard Overview")
    
    campaigns = api_get("/api/campaigns/")
    budget_items = api_get("/api/budgets/with-relations")
    expenses = api_get("/api/expenses/with-details")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Campaigns", len(campaigns))
    with col2:
        total_budget = sum(b.get('total_budget', 0) for b in budget_items)
        st.metric("Total Budget", f"${total_budget:,.0f}")
    with col3:
        total_spent = sum(e.get('amount', 0) for e in expenses)
        st.metric("Total Spent", f"${total_spent:,.0f}")
    with col4:
        variance = total_spent - total_budget
        st.metric("Variance", f"${variance:,.0f}", 
                 delta=f"{(variance/total_budget*100):.1f}%" if total_budget > 0 else "0%")
    
    if budget_items:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Budget by Category")
            cat_budget = {}
            for item in budget_items:
                cat = item.get('category', 'Other')
                cat_budget[cat] = cat_budget.get(cat, 0) + item.get('total_budget', 0)
            
            fig = px.pie(values=list(cat_budget.values()), names=list(cat_budget.keys()))
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Spending by Category")
            cat_actual = {}
            for exp in expenses:
                cat = exp.get('category', 'Other')
                cat_actual[cat] = cat_actual.get(cat, 0) + exp.get('amount', 0)
            
            fig = px.pie(values=list(cat_actual.values()), names=list(cat_actual.keys()))
            st.plotly_chart(fig, use_container_width=True)

# Campaigns Page
elif page == "Campaigns":
    st.header("📁 Campaign Management")
    
    tab1, tab2 = st.tabs(["View & Manage Campaigns", "Create Campaign"])
    
    with tab1:
        campaigns = api_get("/api/campaigns/")
        
        if campaigns:
            for campaign in campaigns:
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.write(f"**📁 {campaign['name']}** - ${campaign['total_budget']:,.0f}")
                    st.caption(f"Level {campaign['level']} | {campaign.get('is_active', 'active')}")
                
                with col2:
                    if st.button("✏️ Edit", key=f"edit_camp_{campaign['id']}"):
                        st.session_state[f'editing_campaign_{campaign["id"]}'] = True
                
                with col3:
                    if st.button("🗑️ Delete", key=f"del_camp_{campaign['id']}"):
                        # Check if campaign has budget items
                        budget_items = api_get(f"/api/budgets/campaign/{campaign['id']}")
                        if budget_items:
                            st.error(f"Cannot delete: Campaign has {len(budget_items)} budget items")
                        elif api_delete(f"/api/campaigns/{campaign['id']}"):
                            st.success("Deleted!")
                            st.rerun()
                        else:
                            st.error("Delete failed")
                
                # Show campaign details
                with st.expander("View Details"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**ID:** {campaign['id']}")
                        st.write(f"**Level:** {campaign['level']}")
                        if campaign.get('description'):
                            st.write(f"**Description:** {campaign['description']}")
                    with col2:
                        st.write(f"**Budget:** ${campaign['total_budget']:,.0f}")
                        st.write(f"**Start:** {campaign.get('start_date', 'N/A')}")
                        st.write(f"**End:** {campaign.get('end_date', 'N/A')}")
                    
                    # Show associated budget items
                    budget_items = api_get(f"/api/budgets/campaign/{campaign['id']}")
                    if budget_items:
                        st.write("**Budget Items:**")
                        for item in budget_items:
                            st.write(f"- {item['name']}: ${item['total_budget']:,.0f}")
                
                # Edit form
                if st.session_state.get(f'editing_campaign_{campaign["id"]}'):
                    with st.form(key=f"edit_form_campaign_{campaign['id']}"):
                        st.subheader(f"Edit: {campaign['name']}")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            new_name = st.text_input("Name", value=campaign['name'])
                            new_desc = st.text_area("Description", value=campaign.get('description', ''))
                            new_budget = st.number_input("Total Budget", value=float(campaign['total_budget']), format="%.2f")
                        with col2:
                            new_status = st.selectbox("Status", ["active", "inactive", "completed"], 
                                                     index=["active", "inactive", "completed"].index(campaign.get('is_active', 'active')))
                            new_start = st.date_input("Start Date", value=datetime.fromisoformat(campaign['start_date']).date() if campaign.get('start_date') else date.today())
                            new_end = st.date_input("End Date", value=datetime.fromisoformat(campaign['end_date']).date() if campaign.get('end_date') else date.today())
                        
                        col_save, col_cancel = st.columns(2)
                        with col_save:
                            if st.form_submit_button("💾 Save Changes"):
                                update_data = {
                                    "name": new_name,
                                    "description": new_desc,
                                    "total_budget": float(new_budget),
                                    "is_active": new_status,
                                    "start_date": new_start.isoformat(),
                                    "end_date": new_end.isoformat()
                                }
                                if api_put(f"/api/campaigns/{campaign['id']}", update_data):
                                    st.success("Updated!")
                                    del st.session_state[f'editing_campaign_{campaign["id"]}']
                                    st.rerun()
                                else:
                                    st.error("Update failed")
                        
                        with col_cancel:
                            if st.form_submit_button("❌ Cancel"):
                                del st.session_state[f'editing_campaign_{campaign["id"]}']
                                st.rerun()
                    
                    st.markdown("---")
        else:
            st.info("No campaigns found")
    
    with tab2:
        campaigns = api_get("/api/campaigns/")
        
        with st.form("create_campaign"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Campaign Name*")
                description = st.text_area("Description")
                parent_options = ["None (Root Campaign)"] + [f"{c['name']} (ID: {c['id']})" for c in campaigns]
                parent_selection = st.selectbox("Parent Campaign", parent_options)
            
            with col2:
                level = st.number_input("Level", min_value=1, max_value=5, value=1)
                total_budget = st.number_input("Total Budget ($)", min_value=0.0, value=0.0, format="%.2f")
                start_date = st.date_input("Start Date")
                end_date = st.date_input("End Date")
            
            if st.form_submit_button("Create Campaign"):
                if not name:
                    st.error("Campaign name is required")
                elif total_budget < 0:
                    st.error("Budget cannot be negative")
                else:
                    parent_id = None
                    if parent_selection != "None (Root Campaign)":
                        parent_id = int(parent_selection.split("ID: ")[1].split(")")[0])
                    
                    data = {
                        "name": name,
                        "description": description,
                        "parent_id": parent_id,
                        "level": level,
                        "total_budget": float(total_budget),
                        "start_date": start_date.isoformat(),
                        "end_date": end_date.isoformat(),
                        "is_active": "active"
                    }
                    
                    if api_post("/api/campaigns/", data):
                        st.success(f"Campaign '{name}' created!")
                        st.rerun()
                    else:
                        st.error("Failed to create campaign")

# Budget Items Page
elif page == "Budget Items":
    st.header("💰 Budget Line Items")
    
    tab1, tab2 = st.tabs(["View & Manage", "Create New"])
    
    with tab1:
        items = api_get("/api/budgets/with-relations")
        
        if items:
            # Export button
            if st.button("Export to CSV"):
                df = pd.DataFrame(items)
                csv = df.to_csv(index=False)
                st.download_button("Download", csv, f"budget_{date.today()}.csv", "text/csv")
            
            st.subheader(f"Total Budget: ${sum(i['total_budget'] for i in items):,.0f}")
            
            # Display each budget item with edit/delete options
            for item in items:
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                
                with col1:
                    st.write(f"**{item['name']}** - ${item['total_budget']:,.0f}")
                    st.caption(f"{item.get('campaign_name', 'N/A')} | {item['category']} | {item.get('cost_center_name', 'N/A')}")
                
                with col2:
                    st.write("")  # Spacing
                
                with col3:
                    if st.button("✏️ Edit", key=f"edit_budget_{item['id']}"):
                        st.session_state[f'editing_budget_{item["id"]}'] = True
                
                with col4:
                    if st.button("🗑️ Delete", key=f"del_budget_{item['id']}"):
                        if api_delete(f"/api/budgets/{item['id']}"):
                            st.success("Deleted!")
                            st.rerun()
                        else:
                            st.error("Delete failed")
                
                # Edit form
                if st.session_state.get(f'editing_budget_{item["id"]}'):
                    with st.form(key=f"edit_form_budget_{item['id']}"):
                        st.subheader(f"Edit: {item['name']}")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            new_name = st.text_input("Name", value=item['name'])
                            new_category = st.text_input("Category", value=item['category'])
                        with col2:
                            new_budget = st.number_input("Total Budget", value=float(item['total_budget']), format="%.2f")
                            new_desc = st.text_area("Description", value=item.get('description', ''))
                        
                        col_save, col_cancel = st.columns(2)
                        with col_save:
                            if st.form_submit_button("💾 Save Changes"):
                                update_data = {
                                    "name": new_name,
                                    "category": new_category,
                                    "total_budget": float(new_budget),
                                    "description": new_desc
                                }
                                if api_put(f"/api/budgets/{item['id']}", update_data):
                                    st.success("Updated!")
                                    del st.session_state[f'editing_budget_{item["id"]}']
                                    st.rerun()
                                else:
                                    st.error("Update failed")
                        
                        with col_cancel:
                            if st.form_submit_button("❌ Cancel"):
                                del st.session_state[f'editing_budget_{item["id"]}']
                                st.rerun()
                    
                    st.markdown("---")
        else:
            st.info("No budget items found")
    
    with tab2:
        campaigns = api_get("/api/campaigns/")
        cost_centers = api_get("/api/cost-centers/active")
        
        if campaigns and cost_centers:
            with st.form("create_budget_item"):
                name = st.text_input("Name*")
                category = st.text_input("Category*")
                campaign_id = st.selectbox("Campaign", [c['id'] for c in campaigns], 
                                          format_func=lambda x: next(c['name'] for c in campaigns if c['id']==x))
                cc_id = st.selectbox("Cost Center", [c['id'] for c in cost_centers],
                                    format_func=lambda x: next(c['name'] for c in cost_centers if c['id']==x))
                total = st.number_input("Total Budget", 0.0, format="%.2f")
                
                if st.form_submit_button("Create"):
                    data = {"name": name, "category": category, "campaign_id": campaign_id,
                           "cost_center_id": cc_id, "total_budget": float(total)}
                    if api_post("/api/budgets/", data):
                        st.success("Created!")
                        st.rerun()

# Expenses Page
elif page == "Expenses":
    st.header("💸 Expense Tracking")
    
    tab1, tab2 = st.tabs(["View & Manage Expenses", "Record New Expense"])
    
    with tab1:
        expenses = api_get("/api/expenses/with-details")
        
        if expenses:
            # Export and summary
            col1, col2 = st.columns([1, 3])
            with col1:
                if st.button("Export to CSV"):
                    df = pd.DataFrame(expenses)
                    csv = df.to_csv(index=False)
                    st.download_button("Download", csv, f"expenses_{date.today()}.csv", "text/csv")
            with col2:
                st.metric("Total Expenses", f"${sum(e['amount'] for e in expenses):,.2f}")
            
            st.markdown("---")
            
            # Display each expense with edit/delete
            for exp in expenses:
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                
                with col1:
                    st.write(f"**${exp['amount']:,.2f}** - {exp.get('budget_item_name', 'N/A')}")
                    caption_parts = [exp['expense_date']]
                    if exp.get('vendor'):
                        caption_parts.append(exp['vendor'])
                    if exp.get('category'):
                        caption_parts.append(exp['category'])
                    st.caption(" | ".join(caption_parts))
                
                with col2:
                    st.write("")  # Spacing
                
                with col3:
                    if st.button("✏️ Edit", key=f"edit_exp_{exp['id']}"):
                        st.session_state[f'editing_expense_{exp["id"]}'] = True
                
                with col4:
                    if st.button("🗑️ Delete", key=f"del_exp_{exp['id']}"):
                        if api_delete(f"/api/expenses/{exp['id']}"):
                            st.success("Deleted!")
                            st.rerun()
                        else:
                            st.error("Delete failed")
                
                # Edit form
                if st.session_state.get(f'editing_expense_{exp["id"]}'):
                    with st.form(key=f"edit_form_expense_{exp['id']}"):
                        st.subheader(f"Edit Expense: ${exp['amount']:,.2f}")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            new_amount = st.number_input("Amount ($)", value=float(exp['amount']), format="%.2f")
                            new_date = st.date_input("Expense Date", value=datetime.fromisoformat(exp['expense_date']).date())
                            new_vendor = st.text_input("Vendor", value=exp.get('vendor', ''))
                        with col2:
                            new_invoice = st.text_input("Invoice #", value=exp.get('invoice_number', ''))
                            new_payment = st.text_input("Payment Method", value=exp.get('payment_method', ''))
                            new_desc = st.text_area("Description", value=exp.get('description', ''))
                        
                        col_save, col_cancel = st.columns(2)
                        with col_save:
                            if st.form_submit_button("💾 Save Changes"):
                                update_data = {
                                    "amount": float(new_amount),
                                    "expense_date": new_date.isoformat(),
                                    "vendor": new_vendor,
                                    "invoice_number": new_invoice,
                                    "payment_method": new_payment,
                                    "description": new_desc
                                }
                                if api_put(f"/api/expenses/{exp['id']}", update_data):
                                    st.success("Updated!")
                                    del st.session_state[f'editing_expense_{exp["id"]}']
                                    st.rerun()
                                else:
                                    st.error("Update failed")
                        
                        with col_cancel:
                            if st.form_submit_button("❌ Cancel"):
                                del st.session_state[f'editing_expense_{exp["id"]}']
                                st.rerun()
                    
                    st.markdown("---")
        else:
            st.info("No expenses recorded yet")
    
    with tab2:
        budget_items = api_get("/api/budgets/with-relations")
        
        if budget_items:
            with st.form("record_expense"):
                st.subheader("Record New Expense")
                
                col1, col2 = st.columns(2)
                with col1:
                    budget_item_id = st.selectbox("Budget Item*", [b['id'] for b in budget_items],
                                                 format_func=lambda x: next(b['name'] for b in budget_items if b['id']==x))
                    amount = st.number_input("Amount ($)*", 0.0, format="%.2f")
                    expense_date = st.date_input("Expense Date*")
                
                with col2:
                    vendor = st.text_input("Vendor")
                    invoice = st.text_input("Invoice #")
                    payment = st.selectbox("Payment Method", 
                                         ["", "Credit Card", "Check", "ACH", "Wire", "Cash"])
                
                description = st.text_area("Description/Notes")
                
                if st.form_submit_button("Record Expense"):
                    if amount <= 0:
                        st.error("Amount must be greater than 0")
                    else:
                        data = {
                            "budget_item_id": budget_item_id,
                            "amount": float(amount),
                            "expense_date": expense_date.isoformat(),
                            "description": description,
                            "vendor": vendor,
                            "invoice_number": invoice,
                            "payment_method": payment if payment else None
                        }
                        
                        if api_post("/api/expenses/", data):
                            st.success(f"Expense of ${amount:,.2f} recorded!")
                            st.rerun()
                        else:
                            st.error("Failed to record expense")
        else:
            st.warning("Create budget items first")

# Budget vs Actual Page
elif page == "Budget vs Actual":
    st.header("📈 Budget vs Actual Variance Analysis")
    
    # Month/Year selection
    col1, col2 = st.columns(2)
    with col1:
        selected_year = st.selectbox("Year", [2024, 2025, 2026], index=1)
    with col2:
        selected_month = st.selectbox("Month", range(1, 13), 
                                     format_func=lambda x: month_name[x])
    
    # Get budget items
    budget_items = api_get("/api/budgets/with-relations")
    
    if budget_items:
        variance_data = []
        
        for item in budget_items:
            # Get monthly budget
            monthly_budget = 0.0
            if item.get('monthly_budget') and str(selected_month) in item['monthly_budget']:
                monthly_budget = float(item['monthly_budget'][str(selected_month)])
            
            # Get actual expenses for this month
            expenses = api_get(f"/api/expenses/month/{selected_year}/{selected_month}")
            item_expenses = [e for e in expenses if e.get('budget_item_id') == item['id']]
            actual = sum(e.get('amount', 0) for e in item_expenses)
            
            variance = actual - monthly_budget
            variance_pct = (variance / monthly_budget * 100) if monthly_budget > 0 else 0
            
            variance_data.append({
                "Budget Item": item['name'],
                "Campaign": item.get('campaign_name', 'N/A'),
                "Category": item['category'],
                "Budgeted": monthly_budget,
                "Actual": actual,
                "Variance": variance,
                "Variance %": variance_pct,
                "Status": "🔴 Over" if variance > 0 else "🟢 Under" if variance < 0 else "✅ On Track"
            })
        
        if variance_data:
            df = pd.DataFrame(variance_data)
            
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Budgeted", f"${df['Budgeted'].sum():,.0f}")
            with col2:
                st.metric("Total Actual", f"${df['Actual'].sum():,.0f}")
            with col3:
                total_var = df['Variance'].sum()
                st.metric("Total Variance", f"${total_var:,.0f}")
            with col4:
                over_budget = len(df[df['Variance'] > 0])
                st.metric("Items Over Budget", over_budget)
            
            # Variance chart
            st.subheader("Variance by Budget Item")
            fig = px.bar(df, x='Budget Item', y='Variance', color='Status',
                        color_discrete_map={"🔴 Over": "#ff4b4b", "🟢 Under": "#00cc00", "✅ On Track": "#0068c9"})
            st.plotly_chart(fig, use_container_width=True)
            
            # Detailed table
            st.subheader("Detailed Variance Report")
            # Format currency columns
            for col in ['Budgeted', 'Actual', 'Variance']:
                df[col] = df[col].apply(lambda x: f"${x:,.2f}")
            df['Variance %'] = df['Variance %'].apply(lambda x: f"{x:.1f}%")
            
            st.dataframe(df, use_container_width=True)

# ROI Tracking Page
elif page == "ROI Tracking":
    st.header("📊 ROI Tracking & Campaign Performance")
    
    tab1, tab2 = st.tabs(["View & Manage ROI", "Record New ROI"])
    
    with tab1:
        roi_metrics = api_get("/api/roi/with-campaign")
        
        if roi_metrics:
            st.subheader("ROI Performance Summary")
            
            df = pd.DataFrame(roi_metrics)
            
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                total_cost = df['total_cost'].sum()
                st.metric("Total Investment", f"${total_cost:,.0f}")
            with col2:
                total_revenue = df['revenue_attributed'].sum()
                st.metric("Total Revenue", f"${total_revenue:,.0f}")
            with col3:
                avg_roi = df['roi_percentage'].mean()
                st.metric("Average ROI", f"{avg_roi:.1f}%")
            with col4:
                positive_roi = len(df[df['roi_percentage'] > 0])
                st.metric("Positive ROI Campaigns", f"{positive_roi}/{len(df)}")
            
            # ROI by campaign chart
            st.subheader("ROI by Campaign")
            fig = px.bar(df, x='campaign_name', y='roi_percentage', 
                        color='roi_percentage',
                        color_continuous_scale=['red', 'yellow', 'green'],
                        labels={'roi_percentage': 'ROI %', 'campaign_name': 'Campaign'})
            st.plotly_chart(fig, use_container_width=True)
            
            # Individual ROI metrics with edit/delete
            st.subheader("ROI Metrics Details")
            for roi in roi_metrics:
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                
                with col1:
                    st.write(f"**{roi.get('campaign_name', 'N/A')}** - ROI: {roi.get('roi_percentage', 0):.1f}%")
                    st.caption(f"Cost: ${roi['total_cost']:,.0f} | Revenue: ${roi['revenue_attributed']:,.0f} | {roi['period_start']} to {roi['period_end']}")
                
                with col2:
                    st.write("")
                
                with col3:
                    if st.button("✏️ Edit", key=f"edit_roi_{roi['id']}"):
                        st.session_state[f'editing_roi_{roi["id"]}'] = True
                
                with col4:
                    if st.button("🗑️ Delete", key=f"del_roi_{roi['id']}"):
                        if api_delete(f"/api/roi/{roi['id']}"):
                            st.success("Deleted!")
                            st.rerun()
                        else:
                            st.error("Delete failed")
                
                # Edit form
                if st.session_state.get(f'editing_roi_{roi["id"]}'):
                    with st.form(key=f"edit_form_roi_{roi['id']}"):
                        st.subheader(f"Edit ROI: {roi.get('campaign_name', 'N/A')}")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            new_cost = st.number_input("Total Cost ($)", value=float(roi['total_cost']), format="%.2f")
                            new_revenue = st.number_input("Revenue ($)", value=float(roi['revenue_attributed']), format="%.2f")
                        with col2:
                            new_notes = st.text_area("Notes", value=roi.get('attribution_notes', ''))
                        
                        col_save, col_cancel = st.columns(2)
                        with col_save:
                            if st.form_submit_button("💾 Save Changes"):
                                update_data = {
                                    "total_cost": float(new_cost),
                                    "revenue_attributed": float(new_revenue),
                                    "attribution_notes": new_notes
                                }
                                if api_put(f"/api/roi/{roi['id']}", update_data):
                                    st.success("Updated!")
                                    del st.session_state[f'editing_roi_{roi["id"]}']
                                    st.rerun()
                                else:
                                    st.error("Update failed")
                        
                        with col_cancel:
                            if st.form_submit_button("❌ Cancel"):
                                del st.session_state[f'editing_roi_{roi["id"]}']
                                st.rerun()
                    
                    st.markdown("---")
        else:
            st.info("No ROI metrics recorded yet")
    
    with tab2:
        campaigns = api_get("/api/campaigns/")
        
        if campaigns:
            with st.form("record_roi"):
                st.subheader("Record Campaign ROI")
                
                col1, col2 = st.columns(2)
                with col1:
                    campaign_id = st.selectbox("Campaign*", [c['id'] for c in campaigns],
                                             format_func=lambda x: next(c['name'] for c in campaigns if c['id']==x))
                    total_cost = st.number_input("Total Cost ($)*", 0.0, format="%.2f")
                    revenue = st.number_input("Revenue Attributed ($)*", 0.0, format="%.2f")
                
                with col2:
                    period_start = st.date_input("Period Start*")
                    period_end = st.date_input("Period End*")
                    attribution = st.selectbox("Attribution Method", 
                                             ["last_touch", "first_touch", "linear", "time_decay"])
                
                # Performance metrics
                st.subheader("Performance Metrics (Optional)")
                col1, col2, col3 = st.columns(3)
                with col1:
                    leads = st.number_input("Leads Generated", 0, step=1)
                with col2:
                    conversions = st.number_input("Conversions", 0, step=1)
                with col3:
                    cpa = st.number_input("Cost Per Acquisition ($)", 0.0, format="%.2f")
                
                notes = st.text_area("Notes")
                
                if st.form_submit_button("Record ROI"):
                    if total_cost <= 0:
                        st.error("Total cost must be greater than 0")
                    elif revenue < 0:
                        st.error("Revenue cannot be negative")
                    else:
                        perf_metrics = {}
                        if leads > 0: perf_metrics['leads'] = leads
                        if conversions > 0: perf_metrics['conversions'] = conversions
                        if cpa > 0: perf_metrics['cpa'] = cpa
                        
                        roi_pct = ((revenue - total_cost) / total_cost * 100) if total_cost > 0 else 0
                        
                        data = {
                            "campaign_id": campaign_id,
                            "calculation_date": date.today().isoformat(),
                            "period_start": period_start.isoformat(),
                            "period_end": period_end.isoformat(),
                            "total_cost": float(total_cost),
                            "revenue_attributed": float(revenue),
                            "performance_metrics": perf_metrics if perf_metrics else None,
                            "attribution_method": attribution,
                            "attribution_notes": notes
                        }
                        
                        if api_post("/api/roi/", data):
                            st.success(f"ROI recorded! ROI: {roi_pct:.1f}%")
                            st.rerun()
                        else:
                            st.error("Failed to record ROI")
        else:
            st.warning("Create campaigns first")

# Cost Centers Page (keeping existing)
elif page == "Cost Centers":
    st.header("🏢 Cost Center Management")
    
    tab1, tab2 = st.tabs(["View", "Create"])
    
    with tab1:
        cost_centers = api_get("/api/cost-centers/active")
        for cc in cost_centers:
            with st.expander(f"🏢 {cc['name']} ({cc['code']})"):
                st.write(f"**Department:** {cc['department']}")
                if cc.get('description'):
                    st.write(f"**Description:** {cc['description']}")
    
    with tab2:
        with st.form("create_cc"):
            name = st.text_input("Name*")
            code = st.text_input("Code*")
            dept = st.text_input("Department", "Marketing")
            desc = st.text_area("Description")
            
            if st.form_submit_button("Create"):
                data = {"name": name, "code": code, "department": dept, "description": desc}
                if api_post("/api/cost-centers/", data):
                    st.success("Created!")
                    st.rerun()

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("### API Status")
try:
    if requests.get(f"{API_BASE_URL}/health").status_code == 200:
        st.sidebar.success("✅ API Connected")
    else:
        st.sidebar.error("❌ API Error")
except:
    st.sidebar.error("❌ API Offline")