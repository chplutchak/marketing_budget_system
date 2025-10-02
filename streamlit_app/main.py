import streamlit as st
import requests
import pandas as pd
from datetime import date, datetime
import plotly.express as px
import plotly.graph_objects as go
from calendar import month_name
import os

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

st.set_page_config(page_title="Marketing Budget Management", page_icon="💼", layout="wide")
st.title("💼 Marketing Budget Management System")

# Sidebar navigation
page = st.sidebar.selectbox(
    "Navigate to:",
    ["Getting Started", "Dashboard", "Budget Structure", "Budget Items", "Expenses", 
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
    ## Understanding the Budget Structure
    
    This system uses a **3-level hierarchy** to organize your marketing budget:
    
    ### Level 1: Department
    The top-level container - typically your entire marketing organization.
    - **Example:** "2026 Marketing Department"
    - **Purpose:** Overall marketing budget and high-level reporting
    
    ### Level 2: Program
    Strategic areas where marketing invests. Programs can be customer-facing or internal.
    - **Customer Acquisition Programs** - Lead generation, campaigns, advertising
    - **Infrastructure & Systems** - Brand refresh, website, CRM, tools
    - **Market Presence** - Trade shows, PR, industry engagement
    - **Product Marketing** - Product launches, sales enablement
    - **Customer Retention** - Customer marketing, success programs
    
    ### Level 3: Project/Campaign
    Specific initiatives within each program.
    - Under Customer Acquisition: "Q1 Google Ads", "LinkedIn ABM Campaign"
    - Under Infrastructure: "Brand Refresh 2026", "HubSpot Workflow Optimization"
    - Under Market Presence: "SOFT Conference 2026", "Industry Awards"
    
    ---
    
    ## Setup Workflow
    
    ### Step 1: Create Cost Centers (15 minutes)
    Cost centers are how you track spending by functional area - they're like QuickBooks "Classes".
    
    **Recommended cost centers for lab/manufacturing companies:**
    - **DM001** - Digital Marketing
    - **EV001** - Events & Trade Shows
    - **CM001** - Content Marketing
    - **TM001** - Technical Marketing
    - **PM001** - Product Marketing
    - **MT001** - Marketing Technology
    
    ### Step 2: Create Your Department (5 minutes)
    Create your Level 1 container:
    - Name: "2026 Marketing Department" (or your fiscal year)
    - Level: 1
    - Total Budget: Your annual marketing budget
    
    ### Step 3: Create Programs (15 minutes)
    Create 4-6 Level 2 programs that match how you think about marketing:
    - Each program should have a clear strategic purpose
    - Assign budget to each program
    - Parent: Select your Department
    - Level: 2
    
    ### Step 4: Create Projects/Campaigns (30 minutes)
    Under each program, create specific initiatives:
    - These are your actual campaigns, projects, or initiatives
    - Parent: Select the relevant Program
    - Level: 3
    
    ### Step 5: Add Budget Line Items (Ongoing)
    For each project, create detailed budget line items:
    - Specific expenses (Google Ads, booth rental, designer fees)
    - Assign to appropriate cost center
    - Include monthly distribution if known
    - Categorize (Digital Ads, Personnel, Events, Materials)
    
    ### Step 6: Track Expenses (Monthly)
    Record actual spending as it occurs:
    - Link to budget line items
    - Include vendor, invoice, payment method
    - System automatically calculates variance
    
    ### Step 7: Record ROI (Quarterly)
    For customer-facing campaigns:
    - Attribute revenue or results
    - Track performance metrics (leads, conversions)
    - Calculate ROI automatically
    
    ---
    
    ## Recommended Initial Programs for UTAK
    
    **1. Customer Acquisition Programs** ($200K)
    - Purpose: Generate and nurture leads
    - Projects: Google Ads campaigns, LinkedIn ABM, webinars, trade show lead gen
    
    **2. Infrastructure & Systems** ($100K)
    - Purpose: Marketing tools, systems, and capabilities
    - Projects: Brand refresh, website redesign, HubSpot optimization, CRM integration
    
    **3. Market Presence & PR** ($120K)
    - Purpose: Industry visibility and reputation
    - Projects: SOFT Conference, industry awards, PR agency, analyst relations
    
    **4. Product Marketing** ($50K)
    - Purpose: Product launches and sales enablement
    - Projects: New product launches, sales collateral, technical documentation
    
    **5. Technical Marketing** ($30K)
    - Purpose: Scientific and technical content
    - Projects: Application notes, white papers, technical webinars, laboratory demos
    
    ---
    
    ## Key Concepts
    
    **Program vs Project:**
    - **Programs** are ongoing strategic areas (like "Customer Acquisition")
    - **Projects** are specific initiatives with start/end dates (like "Q1 Google Ads")
    
    **When to create a new Project:**
    - Has a specific goal or deliverable
    - Has defined start and end dates
    - Can measure success/ROI
    - Budget is $5K+ (smaller items can be line items only)
    
    **Cost Center vs Program:**
    - **Cost Centers** = WHO owns it (Digital team, Events team)
    - **Programs** = WHAT strategic goal it supports (Acquisition, Infrastructure)
    - Budget items get assigned to BOTH
    
    ---
    
    ## QuickBooks Integration
    
    Export your budget items or expenses to CSV from their respective pages. In QuickBooks:
    1. Import the CSV file
    2. Map cost center codes to QuickBooks Classes
    3. Map categories to General Ledger accounts
    
    This keeps your detailed planning here while maintaining proper accounting in QuickBooks.
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
# Budget Structure Page (formerly Campaigns)
elif page == "Budget Structure":
    st.header("📁 Budget Structure (Department → Programs → Projects)")
    
    tab1, tab2 = st.tabs(["View Structure", "Create New"])
    
    with tab1:
        campaigns = api_get("/api/campaigns/")
        
        if campaigns:
            # Group by level for better organization
            level_1 = [c for c in campaigns if c['level'] == 1]
            level_2 = [c for c in campaigns if c['level'] == 2]
            level_3 = [c for c in campaigns if c['level'] == 3]
            
            if level_1:
                st.subheader("Level 1: Department")
                for campaign in level_1:
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        st.write(f"**📁 {campaign['name']}** - ${campaign['total_budget']:,.0f}")
                        st.caption(f"Overall marketing organization | {campaign.get('is_active', 'active')}")
                    
                    with col2:
                        if st.button("Edit", key=f"edit_camp_{campaign['id']}"):
                            st.session_state[f'editing_campaign_{campaign["id"]}'] = True
                    
                    with col3:
                        if st.button("Delete", key=f"del_camp_{campaign['id']}"):
                            budget_items = api_get(f"/api/budgets/campaign/{campaign['id']}")
                            if budget_items:
                                st.error(f"Cannot delete: Has {len(budget_items)} budget items")
                            elif api_delete(f"/api/campaigns/{campaign['id']}"):
                                st.success("Deleted!")
                                st.rerun()
                            else:
                                st.error("Delete failed")
                    
                    with st.expander("View Details"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**ID:** {campaign['id']}")
                            if campaign.get('description'):
                                st.write(f"**Description:** {campaign['description']}")
                        with col2:
                            st.write(f"**Budget:** ${campaign['total_budget']:,.0f}")
                            st.write(f"**Dates:** {campaign.get('start_date', 'N/A')} to {campaign.get('end_date', 'N/A')}")
                        
                        budget_items = api_get(f"/api/budgets/campaign/{campaign['id']}")
                        if budget_items:
                            st.write("**Budget Items:**")
                            for item in budget_items:
                                st.write(f"- {item['name']}: ${item['total_budget']:,.0f}")
                    
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
                                if st.form_submit_button("Save Changes"):
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
                                if st.form_submit_button("Cancel"):
                                    del st.session_state[f'editing_campaign_{campaign["id"]}']
                                    st.rerun()
                        
                        st.markdown("---")
            
            if level_2:
                st.subheader("Level 2: Programs")
                for campaign in level_2:
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        parent_name = next((c['name'] for c in campaigns if c['id'] == campaign.get('parent_id')), 'No Parent')
                        st.write(f"**📂 {campaign['name']}** - ${campaign['total_budget']:,.0f}")
                        st.caption(f"Under: {parent_name} | {campaign.get('is_active', 'active')}")
                    
                    with col2:
                        if st.button("Edit", key=f"edit_camp_{campaign['id']}"):
                            st.session_state[f'editing_campaign_{campaign["id"]}'] = True
                    
                    with col3:
                        if st.button("Delete", key=f"del_camp_{campaign['id']}"):
                            budget_items = api_get(f"/api/budgets/campaign/{campaign['id']}")
                            if budget_items:
                                st.error(f"Cannot delete: Has {len(budget_items)} budget items")
                            elif api_delete(f"/api/campaigns/{campaign['id']}"):
                                st.success("Deleted!")
                                st.rerun()
                            else:
                                st.error("Delete failed")
                    
                    with st.expander("View Details"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**ID:** {campaign['id']}")
                            if campaign.get('description'):
                                st.write(f"**Description:** {campaign['description']}")
                        with col2:
                            st.write(f"**Budget:** ${campaign['total_budget']:,.0f}")
                            st.write(f"**Dates:** {campaign.get('start_date', 'N/A')} to {campaign.get('end_date', 'N/A')}")
                        
                        budget_items = api_get(f"/api/budgets/campaign/{campaign['id']}")
                        if budget_items:
                            st.write("**Budget Items:**")
                            for item in budget_items:
                                st.write(f"- {item['name']}: ${item['total_budget']:,.0f}")
                    
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
                                if st.form_submit_button("Save Changes"):
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
                                if st.form_submit_button("Cancel"):
                                    del st.session_state[f'editing_campaign_{campaign["id"]}']
                                    st.rerun()
                        
                        st.markdown("---")
            
            if level_3:
                st.subheader("Level 3: Projects/Campaigns")
                for campaign in level_3:
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        parent_name = next((c['name'] for c in campaigns if c['id'] == campaign.get('parent_id')), 'No Parent')
                        st.write(f"**📄 {campaign['name']}** - ${campaign['total_budget']:,.0f}")
                        st.caption(f"Under: {parent_name} | {campaign.get('is_active', 'active')}")
                    
                    with col2:
                        if st.button("Edit", key=f"edit_camp_{campaign['id']}"):
                            st.session_state[f'editing_campaign_{campaign["id"]}'] = True
                    
                    with col3:
                        if st.button("Delete", key=f"del_camp_{campaign['id']}"):
                            budget_items = api_get(f"/api/budgets/campaign/{campaign['id']}")
                            if budget_items:
                                st.error(f"Cannot delete: Has {len(budget_items)} budget items")
                            elif api_delete(f"/api/campaigns/{campaign['id']}"):
                                st.success("Deleted!")
                                st.rerun()
                            else:
                                st.error("Delete failed")
                    
                    with st.expander("View Details"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**ID:** {campaign['id']}")
                            if campaign.get('description'):
                                st.write(f"**Description:** {campaign['description']}")
                        with col2:
                            st.write(f"**Budget:** ${campaign['total_budget']:,.0f}")
                            st.write(f"**Dates:** {campaign.get('start_date', 'N/A')} to {campaign.get('end_date', 'N/A')}")
                        
                        budget_items = api_get(f"/api/budgets/campaign/{campaign['id']}")
                        if budget_items:
                            st.write("**Budget Items:**")
                            for item in budget_items:
                                st.write(f"- {item['name']}: ${item['total_budget']:,.0f}")
                    
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
                                if st.form_submit_button("Save Changes"):
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
                                if st.form_submit_button("Cancel"):
                                    del st.session_state[f'editing_campaign_{campaign["id"]}']
                                    st.rerun()
                        
                        st.markdown("---")
        else:
            st.info("No structure created yet. Start by creating your Department (Level 1).")
    
    with tab2:
        campaigns = api_get("/api/campaigns/")
        
        with st.form("create_campaign"):
            st.subheader("Create New Budget Structure Item")
            
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Name*", placeholder="e.g., '2026 Marketing Department' or 'Customer Acquisition Programs'")
                description = st.text_area("Description", 
                    placeholder="Describe the purpose and scope of this department/program/project")
                parent_options = ["None (Top Level Department)"] + [f"{c['name']} (ID: {c['id']})" for c in campaigns]
                parent_selection = st.selectbox("Parent", parent_options,
                    help="Select a parent if this is a Program (Level 2) or Project (Level 3)")
            
            with col2:
                level = st.selectbox("Level", [1, 2, 3],
                    format_func=lambda x: {1: "1 - Department", 2: "2 - Program", 3: "3 - Project/Campaign"}[x],
                    help="Choose the organizational level")
                total_budget = st.number_input("Total Budget ($)*", min_value=0.0, value=0.0, format="%.2f")
                start_date = st.date_input("Start Date")
                end_date = st.date_input("End Date")
            
            # Dynamic helper text based on level
            if level == 1:
                st.info("**Level 1 - Department:** Your overall marketing organization. Usually one per fiscal year (e.g., '2026 Marketing Department').")
            elif level == 2:
                st.info("**Level 2 - Program:** Strategic investment areas like 'Customer Acquisition Programs', 'Infrastructure & Systems', 'Market Presence', etc.")
            else:
                st.info("**Level 3 - Project/Campaign:** Specific initiatives like 'Q1 Google Ads Campaign', 'Brand Refresh 2026', 'SOFT Conference', 'HubSpot Optimization'.")
            
            if st.form_submit_button("Create"):
                if not name:
                    st.error("Name is required")
                elif total_budget < 0:
                    st.error("Budget cannot be negative")
                else:
                    parent_id = None
                    if parent_selection != "None (Top Level Department)":
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
                        st.success(f"'{name}' created successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to create. Check that parent exists if selected.")

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

# Cost Centers Page
elif page == "Cost Centers":
    st.header("🏢 Cost Center Management")
    
    tab1, tab2 = st.tabs(["View & Manage", "Create New"])
    
    with tab1:
        cost_centers = api_get("/api/cost-centers/active")
        
        if cost_centers:
            for cc in cost_centers:
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.write(f"**🏢 {cc['name']}** ({cc['code']})")
                    st.caption(f"{cc['department']} | {'Active' if cc['is_active'] else 'Inactive'}")
                
                with col2:
                    if st.button("✏️ Edit", key=f"edit_cc_{cc['id']}"):
                        st.session_state[f'editing_cc_{cc["id"]}'] = True
                
                with col3:
                    if st.button("🗑️ Delete", key=f"del_cc_{cc['id']}"):
                        # Check if cost center has budget items
                        budget_items = api_get(f"/api/budgets/cost-center/{cc['id']}")
                        if budget_items:
                            st.error(f"Cannot delete: Cost center has {len(budget_items)} budget items")
                        elif api_delete(f"/api/cost-centers/{cc['id']}"):
                            st.success("Cost center deactivated!")
                            st.rerun()
                        else:
                            st.error("Delete failed")
                
                # Show details in expander
                with st.expander("View Details"):
                    st.write(f"**Code:** {cc['code']}")
                    st.write(f"**Department:** {cc['department']}")
                    if cc.get('description'):
                        st.write(f"**Description:** {cc['description']}")
                
                # Edit form
                if st.session_state.get(f'editing_cc_{cc["id"]}'):
                    with st.form(key=f"edit_form_cc_{cc['id']}"):
                        st.subheader(f"Edit: {cc['name']}")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            new_name = st.text_input("Name", value=cc['name'])
                            new_code = st.text_input("Code", value=cc['code'])
                        with col2:
                            new_dept = st.text_input("Department", value=cc['department'])
                            new_desc = st.text_area("Description", value=cc.get('description', ''))
                        
                        col_save, col_cancel = st.columns(2)
                        with col_save:
                            if st.form_submit_button("💾 Save Changes"):
                                update_data = {
                                    "name": new_name,
                                    "code": new_code,
                                    "department": new_dept,
                                    "description": new_desc
                                }
                                if api_put(f"/api/cost-centers/{cc['id']}", update_data):
                                    st.success("Updated!")
                                    del st.session_state[f'editing_cc_{cc["id"]}']
                                    st.rerun()
                                else:
                                    st.error("Update failed - code may already exist")
                        
                        with col_cancel:
                            if st.form_submit_button("❌ Cancel"):
                                del st.session_state[f'editing_cc_{cc["id"]}']
                                st.rerun()
                    
                    st.markdown("---")
        else:
            st.info("No cost centers found")
    
    with tab2:
        with st.form("create_cc"):
            st.subheader("Create New Cost Center")
            
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Name*", placeholder="e.g., Digital Marketing")
                code = st.text_input("Code*", placeholder="e.g., DM001")
            
            with col2:
                dept = st.text_input("Department", value="Marketing")
                desc = st.text_area("Description", 
                    placeholder="What types of expenses belong to this cost center?")
            
            if st.form_submit_button("Create Cost Center"):
                if not name or not code:
                    st.error("Name and Code are required")
                else:
                    data = {
                        "name": name,
                        "code": code,
                        "department": dept,
                        "description": desc
                    }
                    if api_post("/api/cost-centers/", data):
                        st.success(f"Cost center '{name}' created!")
                        st.rerun()
                    else:
                        st.error("Failed to create - code may already exist")

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