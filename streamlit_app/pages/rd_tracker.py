import streamlit as st
import requests
from datetime import date, datetime
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# API Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# ============================================================================
# CAPITALIZED DROPDOWN OPTIONS (NEW)
# ============================================================================

INITIATIVE_TYPES = ["New Product", "Revision"]
MATRIX_TYPES = ["Whole Blood", "Urine", "Serum", "SMx Whole Blood", "SMx Urine", "SMx Serum", "Other"]
STAGES = ["Feasibility", "Validation", "Development", "Launch Prep", "Launched", "On Hold", "Cancelled"]
PRIORITIES = ["Low", "Medium", "High", "Critical"]
DEPARTMENTS = ["Marketing", "Operations", "Manufacturing", "Sales", "R&D"]
TEAM_ROLES = ["Lead", "Support", "Reviewer", "Stakeholder"]
INTEREST_TIMELINES = ["Immediate", "30 Days", "90 Days", "Future"]
SAMPLE_TYPES = ["Trial Batch", "Demo Sample", "Validation Sample"]
MILESTONE_STATUSES = ["Not Started", "In Progress", "Completed", "Delayed", "Blocked"]
YES_NO_OPTIONS = ["Yes", "No", "Needs Research"]

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def format_display_value(value: str) -> str:
    """Convert snake_case or lowercase to Title Case for display"""
    if not value:
        return ""
    return value.replace("_", " ").title()


def to_snake_case(value: str) -> str:
    """Convert Title Case to snake_case for API"""
    if not value:
        return ""
    return value.lower().replace(" ", "_")


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


# ============================================================================
# TEAM MANAGEMENT COMPONENT (NEW)
# ============================================================================

def display_initiative_team(initiative_id: int):
    """Display and manage team members for an initiative"""
    st.markdown("### 👥 Team Members")
    st.write("")
    
    # Fetch current team
    team_members = api_get(f"/api/rd/initiatives/{initiative_id}/team") or []
    
    # Display team members by department
    if team_members:
        # Group by department
        by_dept = {}
        for member in team_members:
            dept = member['department']
            if dept not in by_dept:
                by_dept[dept] = []
            by_dept[dept].append(member)
        
        # Display in columns
        cols = st.columns(len(DEPARTMENTS))
        for idx, dept in enumerate(DEPARTMENTS):
            with cols[idx]:
                st.markdown(f"**{dept}**")
                if dept in by_dept:
                    for member in by_dept[dept]:
                        col_a, col_b = st.columns([4, 1])
                        with col_a:
                            role_badge = f" *({member['role']})*" if member.get('role') else ""
                            st.write(f"• {member['person_name']}{role_badge}")
                        with col_b:
                            if st.button("🗑️", key=f"del_team_{member['id']}", help="Remove"):
                                if api_delete(f"/api/rd/team/{member['id']}"):
                                    st.rerun()
                else:
                    st.caption("*No one assigned*")
    else:
        st.info("ℹ️ No team members assigned yet")
    
    st.divider()
    
    # Add new team member form
    with st.expander("➕ Add Team Member"):
        with st.form(f"add_team_{initiative_id}"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                department = st.selectbox("Department*", DEPARTMENTS, key=f"team_dept_{initiative_id}")
            
            with col2:
                person_name = st.text_input("Person Name*", key=f"team_person_{initiative_id}")
            
            with col3:
                role = st.selectbox("Role", TEAM_ROLES, key=f"team_role_{initiative_id}")
            
            submitted = st.form_submit_button("Add to Team")
            
            if submitted:
                if not person_name:
                    st.error("Person name is required")
                else:
                    payload = {
                        "initiative_id": initiative_id,
                        "department": department,
                        "person_name": person_name,
                        "role": role
                    }
                    
                    if api_post(f"/api/rd/initiatives/{initiative_id}/team", payload):
                        st.success(f"✅ Added {person_name} to {department}")
                        st.rerun()


# ============================================================================
# MAIN APP
# ============================================================================

# Page title
st.title("🔬 R&D Initiative Tracker")

# Initialize session state
if 'selected_initiative' not in st.session_state:
    st.session_state['selected_initiative'] = None
if 'view_mode' not in st.session_state:
    st.session_state['view_mode'] = 'list'

# Sidebar filters - UPDATED WITH CAPITALIZED OPTIONS
st.sidebar.header("Filters")
stage_filter = st.sidebar.selectbox(
    "Stage",
    ["All"] + STAGES,
    format_func=lambda x: x if x == "All" else x
)
priority_filter = st.sidebar.selectbox(
    "Priority",
    ["All"] + PRIORITIES,
    format_func=lambda x: x if x == "All" else x
)
is_active_filter = st.sidebar.selectbox(
    "Status",
    ["All", "Active", "Inactive", "Completed"]
)

# Build query parameters
params = []
if stage_filter != "All":
    params.append(f"stage={to_snake_case(stage_filter)}")
if priority_filter != "All":
    params.append(f"priority={priority_filter.lower()}")
if is_active_filter != "All":
    params.append(f"is_active={is_active_filter.lower()}")

query_string = "&" + "&".join(params) if params else ""

# Fetch initiatives
initiatives = api_get(f"/api/rd/initiatives?{query_string}")

# Back button if in detail view
if st.session_state['view_mode'] == 'detail' and st.session_state['selected_initiative']:
    if st.button("← Back to List"):
        st.session_state['view_mode'] = 'list'
        st.session_state['selected_initiative'] = None
        st.rerun()
    
    st.divider()

# ===================
# DETAIL VIEW MODE
# ===================
if st.session_state['view_mode'] == 'detail' and st.session_state['selected_initiative']:
    initiative_id = st.session_state['selected_initiative']
    initiative = api_get(f"/api/rd/initiatives/{initiative_id}")
    
    if initiative:
        st.header(f"📋 {initiative['name']}")
        
        st.write("")  # Spacing
        
        # Key metrics at top - UPDATED WITH FORMATTED DISPLAY
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Type", format_display_value(initiative.get('initiative_type', 'new_product')))
        with col2:
            st.metric("Matrix", format_display_value(initiative.get('matrix_type', 'Not set')))
        with col3:
            st.metric("Stage", format_display_value(initiative['stage']))
        with col4:
            st.metric("Priority", format_display_value(initiative['priority']))
        with col5:
            status_color = "🟢" if initiative['is_active'] == 'active' else "🔴"
            st.metric("Status", f"{status_color} {format_display_value(initiative['is_active'])}")
        
        if initiative.get('part_number'):
            st.caption(f"Part Number: {initiative['part_number']}")
        
        st.divider()
        
        # Tabs for detailed information - ADDED TEAM TAB
        detail_tabs = st.tabs([
            "📄 Overview", 
            "👥 Team",  # NEW TAB
            "🏭 Feasibility", 
            "🎯 Customers", 
            "🧪 Samples", 
            "💰 Financials",
            "📅 Milestones"
        ])
        
        # TAB: Overview
        with detail_tabs[0]:
            st.write("")  # Spacing
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Project Details")
                st.write("")
                st.write(f"**Description:** {initiative.get('description', 'No description')}")
                st.write("")
                st.write(f"**Lead:** {initiative.get('lead_owner', 'Unassigned')}")
                st.write(f"**Target Market:** {initiative.get('target_market', 'Not specified')}")
                
                if initiative.get('market_size_estimate'):
                    st.write("")
                    st.write(f"**Market Size:** ${initiative['market_size_estimate']:,.0f}")
            
            with col2:
                st.subheader("Business Case")
                st.write("")
                if initiative.get('target_price'):
                    st.write(f"**Target Price:** ${initiative['target_price']:,.2f}")
                if initiative.get('target_margin'):
                    st.write(f"**Target Margin:** {initiative['target_margin']}%")
                
                st.write("")
                st.write("**Timeline:**")
                if initiative.get('start_date'):
                    st.write(f"- Started: {initiative['start_date']}")
                if initiative.get('target_launch_date'):
                    st.write(f"- Target Launch: {initiative['target_launch_date']}")
                if initiative.get('actual_launch_date'):
                    st.write(f"- Actual Launch: {initiative['actual_launch_date']}")
        
        # TAB: Team (NEW)
        with detail_tabs[1]:
            st.write("")
            display_initiative_team(initiative_id)
        
        # TAB: Feasibility - UPDATED WITH NEW FIELDS
        with detail_tabs[2]:
            st.write("")  # Spacing
            
            feasibility = api_get(f"/api/rd/feasibility/initiative/{initiative_id}")
            
            if feasibility:
                # Familiarity Checks (NEW)
                st.subheader("Familiarity Assessment")
                st.write("")
                
                col1, col2 = st.columns(2)
                with col1:
                    matrix_fam = feasibility.get('matrix_familiar')
                    if matrix_fam is not None:
                        st.write(f"**Matrix Familiar:** {'✅ Yes' if matrix_fam else '❌ No'}")
                    else:
                        st.write("**Matrix Familiar:** Not assessed")
                
                with col2:
                    analyte_fam = feasibility.get('analyte_familiar')
                    if analyte_fam is not None:
                        st.write(f"**Analyte Familiar:** {'✅ Yes' if analyte_fam else '❌ No'}")
                    else:
                        st.write("**Analyte Familiar:** Not assessed")
                
                # NEW FIELDS
                if feasibility.get('target_instruments'):
                    st.write("")
                    st.write(f"**Target Instruments:** {feasibility['target_instruments']}")
                
                if feasibility.get('document_references'):
                    st.write("")
                    st.write(f"**Document References:** {feasibility['document_references']}")
                
                st.divider()
                
                # Manufacturing Assessment
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Manufacturing Assessment")
                    st.write("")
                    st.write(f"**Is Manufacturable:** {format_display_value(feasibility.get('is_manufacturable', 'Unknown'))}")
                    st.write(f"**Complexity:** {format_display_value(feasibility.get('manufacturing_complexity', 'Unknown'))}")
                    if feasibility.get('estimated_lead_time_days'):
                        st.write(f"**Lead Time:** {feasibility['estimated_lead_time_days']} days")
                    if feasibility.get('moq'):
                        st.write(f"**MOQ:** {feasibility['moq']} units")
                
                with col2:
                    st.subheader("Cost Estimates")
                    st.write("")
                    if feasibility.get('estimated_cogs'):
                        st.write(f"**COGS:** ${feasibility['estimated_cogs']:,.2f}/unit")
                    if feasibility.get('estimated_development_cost'):
                        st.write(f"**Development Cost:** ${feasibility['estimated_development_cost']:,.2f}")
                    if feasibility.get('estimated_sample_cost'):
                        st.write(f"**Sample Cost:** ${feasibility['estimated_sample_cost']:,.2f}/unit")
                
                if feasibility.get('feasibility_notes'):
                    st.write("")
                    st.subheader("Notes")
                    st.write(feasibility['feasibility_notes'])
            else:
                st.info("No feasibility assessment yet.")
                
                st.write("")
                
                # UPDATED FORM WITH NEW FIELDS
                with st.expander("➕ Add Feasibility Assessment"):
                    with st.form("feasibility_form"):
                        st.write("**Familiarity Checks**")
                        col1, col2 = st.columns(2)
                        with col1:
                            matrix_fam = st.checkbox("Matrix Familiar?", value=False)
                        with col2:
                            analyte_fam = st.checkbox("Analyte Familiar?", value=False)
                        
                        target_instruments = st.text_area("Target Instruments", 
                            placeholder="LCMS, GC-MS, ELISA, etc. (determines vial volume needs)")
                        document_refs = st.text_area("Document References", 
                            placeholder="Links to SOPs, prior projects, technical specs...")
                        
                        st.divider()
                        
                        st.write("**Manufacturing Assessment**")
                        is_manu = st.selectbox("Is Manufacturable?", YES_NO_OPTIONS)
                        complexity = st.selectbox("Complexity", ["Low", "Medium", "High"])
                        lead_time = st.number_input("Lead Time (days)", min_value=0, step=1)
                        moq_val = st.number_input("MOQ", min_value=0, step=1)
                        cogs = st.number_input("Estimated COGS ($)", min_value=0.0, step=1.0)
                        notes = st.text_area("Notes")
                        
                        if st.form_submit_button("Save Feasibility"):
                            feas_data = {
                                "initiative_id": initiative_id,
                                "matrix_familiar": matrix_fam,
                                "analyte_familiar": analyte_fam,
                                "target_instruments": target_instruments if target_instruments else None,
                                "document_references": document_refs if document_refs else None,
                                "is_manufacturable": to_snake_case(is_manu),
                                "manufacturing_complexity": complexity.lower(),
                                "estimated_lead_time_days": lead_time if lead_time > 0 else None,
                                "moq": moq_val if moq_val > 0 else None,
                                "estimated_cogs": cogs if cogs > 0 else None,
                                "feasibility_notes": notes
                            }
                            if api_post("/api/rd/feasibility", feas_data):
                                st.success("Feasibility assessment saved!")
                                st.rerun()
        
        # TAB: Customers - UPDATED WITH NEW FIELDS
        with detail_tabs[3]:
            st.write("")  # Spacing
            
            customers = api_get(f"/api/rd/customers/initiative/{initiative_id}")
            
            st.subheader("Customer Interest")
            st.write("")
            
            if customers:
                # Summary metrics
                high_interest = len([c for c in customers if c['interest_level'] in ['highly_interested', 'committed']])
                ordered = len([c for c in customers if c['interest_level'] == 'ordered'])
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Contacts", len(customers))
                with col2:
                    st.metric("High Interest", high_interest)
                with col3:
                    st.metric("Converted to Orders", ordered)
                
                st.write("")
                
                # Customer list
                for customer in customers:
                    with st.expander(f"{customer['customer_name']} - {format_display_value(customer['interest_level'])}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write("**Contact Info:**")
                            st.write(f"Contact: {customer.get('contact_person', 'N/A')}")
                            st.write(f"Email: {customer.get('contact_email', 'N/A')}")
                            st.write(f"Last Contact: {customer.get('last_contact_date', 'Never')}")
                            if customer.get('next_follow_up_date'):
                                st.write(f"Next Follow-Up: {customer['next_follow_up_date']}")
                        
                        with col2:
                            st.write("**Strategic Intel:**")
                            # NEW FIELDS
                            if customer.get('current_product_used'):
                                st.write(f"Currently Using: {customer['current_product_used']}")
                            if customer.get('testing_method'):
                                st.write(f"Testing Method: {customer['testing_method']}")
                            if customer.get('interest_timeline'):
                                st.write(f"Timeline: {format_display_value(customer['interest_timeline'])}")
                            if customer.get('historical_order_volume'):
                                st.write(f"Historical Orders: ${customer['historical_order_volume']:,.2f}")
            else:
                st.info("No customer contacts yet.")
            
            st.write("")
            
            # UPDATED FORM WITH NEW FIELDS
            with st.expander("➕ Add Customer Contact"):
                with st.form(f"customer_form_{initiative_id}"):
                    cust_name = st.text_input("Customer Name*")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        contact_person = st.text_input("Contact Person")
                        contact_email = st.text_input("Contact Email")
                        interest = st.selectbox("Interest Level", 
                            ["Interested", "Highly Interested", "Committed", "Testing", "Ordered", "Not Interested"],
                            format_func=lambda x: x)
                    
                    with col2:
                        # NEW FIELDS
                        current_product = st.text_input("Currently Using", placeholder="Vendor/Product")
                        testing_method = st.text_input("Testing Method", placeholder="LCMS, ELISA, GC-MS, etc.")
                        timeline = st.selectbox("Interest Timeline", INTEREST_TIMELINES)
                    
                    if st.form_submit_button("Add Customer"):
                        if cust_name:
                            cust_data = {
                                "initiative_id": initiative_id,
                                "customer_name": cust_name,
                                "contact_person": contact_person,
                                "contact_email": contact_email,
                                "interest_level": to_snake_case(interest),
                                "current_product_used": current_product if current_product else None,
                                "testing_method": testing_method if testing_method else None,
                                "interest_timeline": to_snake_case(timeline)
                            }
                            if api_post("/api/rd/customers", cust_data):
                                st.success("Customer added!")
                                st.rerun()
        
        # TAB: Samples - UPDATED WITH NEW FIELDS
        with detail_tabs[4]:
            st.write("")  # Spacing
            
            samples = api_get(f"/api/rd/samples/initiative/{initiative_id}")
            
            st.subheader("Sample Tracking")
            st.write("")
            
            if samples:
                # Conversion metrics
                total_samples = len(samples)
                converted = len([s for s in samples if s['converted_to_order'] == 'yes'])
                conversion_rate = (converted / total_samples * 100) if total_samples > 0 else 0
                total_sample_cost = sum([s['sample_cost'] for s in samples])
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Samples Sent", total_samples)
                with col2:
                    st.metric("Converted", converted)
                with col3:
                    st.metric("Conversion Rate", f"{conversion_rate:.1f}%")
                with col4:
                    st.metric("Total Sample Cost", f"${total_sample_cost:,.2f}")
                
                st.write("")
                
                # Sample table - ADDED NEW COLUMNS
                sample_df = pd.DataFrame(samples)
                display_cols = ['recipient_name', 'sample_type', 'part_number', 'ship_date', 'sample_cost', 'converted_to_order']
                st.dataframe(sample_df[display_cols], use_container_width=True, height=250)
            else:
                st.info("No samples sent yet.")
            
            st.write("")
            
            # UPDATED FORM WITH NEW FIELDS
            with st.expander("➕ Log Sample"):
                with st.form(f"sample_form_{initiative_id}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        recip = st.text_input("Recipient Name*")
                        samp_type = st.selectbox("Type", SAMPLE_TYPES)
                        part_num = st.text_input("Part Number", placeholder="UTAK part number")  # NEW
                    
                    with col2:
                        samp_cost = st.number_input("Sample Cost ($)", min_value=0.0, step=10.0)
                        ship_dt = st.date_input("Ship Date", value=date.today())
                        doc_ref = st.text_input("Document Reference", placeholder="Link to IFU or specs")  # NEW
                    
                    if st.form_submit_button("Log Sample"):
                        if recip:
                            samp_data = {
                                "initiative_id": initiative_id,
                                "sample_type": to_snake_case(samp_type),
                                "recipient_name": recip,
                                "part_number": part_num if part_num else None,
                                "document_reference": doc_ref if doc_ref else None,
                                "sample_cost": samp_cost,
                                "ship_date": ship_dt.isoformat()
                            }
                            if api_post("/api/rd/samples", samp_data):
                                st.success("Sample logged!")
                                st.rerun()
        
        # TAB: Financials (unchanged)
        with detail_tabs[5]:
            st.write("")  # Spacing
            
            expenses = api_get(f"/api/rd/expenses/initiative/{initiative_id}")
            revenue = api_get(f"/api/rd/revenue/initiative/{initiative_id}")
            
            # Get totals
            total_exp_data = api_get(f"/api/rd/expenses/initiative/{initiative_id}/total")
            total_rev_data = api_get(f"/api/rd/revenue/initiative/{initiative_id}/total")
            
            total_expenses = total_exp_data.get('total_expenses', 0) if total_exp_data else 0
            total_revenue = total_rev_data.get('total_revenue', 0) if total_rev_data else 0
            net_profit = total_revenue - total_expenses
            roi = ((net_profit / total_expenses) * 100) if total_expenses > 0 else 0
            
            # Financial summary
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Investment", f"${total_expenses:,.2f}")
            with col2:
                st.metric("Total Revenue", f"${total_revenue:,.2f}")
            with col3:
                st.metric("Net Profit/Loss", f"${net_profit:,.2f}")
            with col4:
                st.metric("ROI", f"{roi:.1f}%")
            
            st.divider()
            
            # Expense breakdown chart
            if expenses:
                st.subheader("Expense Breakdown")
                st.write("")
                
                expense_df = pd.DataFrame(expenses)
                expense_by_cat = expense_df.groupby('expense_category')['amount'].sum().reset_index()
                
                fig = px.pie(expense_by_cat, values='amount', names='expense_category', 
                            title="Expenses by Category", hole=0.4)
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True)
                
                st.write("")
                
                # Expense timeline
                expense_df['expense_date'] = pd.to_datetime(expense_df['expense_date'])
                expense_timeline = expense_df.sort_values('expense_date')
                
                fig2 = px.line(expense_timeline, x='expense_date', y='amount', 
                              title="Spending Over Time", markers=True)
                fig2.update_layout(yaxis_title="Amount ($)", xaxis_title="Date")
                st.plotly_chart(fig2, use_container_width=True)
            
            st.write("")
            
            # Revenue by customer
            if revenue:
                st.subheader("Revenue by Customer")
                st.write("")
                
                revenue_df = pd.DataFrame(revenue)
                revenue_by_cust = revenue_df.groupby('customer_name')['order_value'].sum().reset_index()
                
                fig3 = px.bar(revenue_by_cust, x='customer_name', y='order_value',
                             title="Revenue by Customer", color='order_value',
                             color_continuous_scale='Greens')
                fig3.update_layout(yaxis_title="Revenue ($)", xaxis_title="Customer")
                st.plotly_chart(fig3, use_container_width=True)
        
        # TAB: Milestones - ENHANCED WITH BETTER UI
        with detail_tabs[6]:
            st.write("")  # Spacing
            
            milestones = api_get(f"/api/rd/milestones/initiative/{initiative_id}")
            
            st.subheader("Project Milestones")
            st.write("")
            
            if milestones:
                # Calculate progress
                total = len(milestones)
                completed = len([m for m in milestones if m['status'] == 'completed'])
                in_progress = len([m for m in milestones if m['status'] == 'in_progress'])
                progress_pct = (completed / total * 100) if total > 0 else 0
                
                # Progress bar
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.progress(progress_pct / 100)
                with col2:
                    st.metric("Complete", f"{completed}/{total}")
                with col3:
                    st.metric("In Progress", in_progress)
                
                st.write("")
                st.divider()
                st.write("")
                
                # Checklist-style display
                for milestone in sorted(milestones, key=lambda x: (x.get('target_date') or '9999-12-31')):
                    status = milestone['status']
                    
                    # Status emoji and color
                    if status == 'completed':
                        emoji = "✅"
                    elif status == 'in_progress':
                        emoji = "⚙️"
                    elif status == 'blocked':
                        emoji = "🚫"
                    elif status == 'delayed':
                        emoji = "⏰"
                    else:  # pending/not_started
                        emoji = "⚪"
                    
                    # Create expandable milestone
                    with st.expander(f"{emoji} {milestone['milestone_name']}", expanded=False):
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            # Status selector with capitalized options
                            status_map = {
                                "not_started": "Not Started",
                                "in_progress": "In Progress", 
                                "completed": "Completed",
                                "delayed": "Delayed",
                                "blocked": "Blocked"
                            }
                            status_display = [status_map.get(s, s) for s in ["not_started", "in_progress", "completed", "delayed", "blocked"]]
                            current_display = status_map.get(status, status)
                            
                            new_status_display = st.selectbox(
                                "Status",
                                status_display,
                                index=status_display.index(current_display),
                                key=f"status_{milestone['id']}"
                            )
                            
                            # Convert back to snake_case
                            new_status = to_snake_case(new_status_display)
                            
                            # Update if changed
                            if new_status != status:
                                update_data = {"status": new_status}
                                if new_status == 'completed' and not milestone.get('actual_date'):
                                    update_data['actual_date'] = date.today().isoformat()
                                
                                if api_put(f"/api/rd/milestones/{milestone['id']}", update_data):
                                    st.success("Status updated!")
                                    st.rerun()
                        
                        with col2:
                            st.write(f"**Type:** {format_display_value(milestone['milestone_type'])}")
                            st.write(f"**Owner:** {milestone.get('owner', 'Unassigned')}")
                        
                        st.write("")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if milestone.get('target_date'):
                                st.write(f"**Target:** {milestone['target_date']}")
                        with col2:
                            if milestone.get('actual_date'):
                                st.write(f"**Completed:** {milestone['actual_date']}")
                        
                        if milestone.get('notes'):
                            st.write("")
                            st.write(f"**Notes:** {milestone['notes']}")
                        
                        if milestone.get('blockers'):
                            st.warning(f"**Blockers:** {milestone['blockers']}")
            else:
                st.info("No milestones defined yet.")
            
            st.write("")
            
            with st.expander("➕ Add Milestone"):
                with st.form(f"milestone_form_{initiative_id}"):
                    m_name = st.text_input("Milestone Name*")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        m_type = st.selectbox("Type", 
                            ["Feasibility Complete", "Samples Ready", "Validation Done", 
                             "Launch Materials Ready", "Launched"])
                        m_target = st.date_input("Target Date")
                    
                    with col2:
                        m_owner = st.text_input("Owner")
                        m_status = st.selectbox("Initial Status", MILESTONE_STATUSES)
                    
                    if st.form_submit_button("Add Milestone"):
                        if m_name:
                            m_data = {
                                "initiative_id": initiative_id,
                                "milestone_name": m_name,
                                "milestone_type": to_snake_case(m_type),
                                "target_date": m_target.isoformat(),
                                "owner": m_owner,
                                "status": to_snake_case(m_status)
                            }
                            if api_post("/api/rd/milestones", m_data):
                                st.success("Milestone added!")
                                st.rerun()

# ===================
# LIST VIEW MODE
# ===================
else:
    # Reset view mode when in list mode
    st.session_state['view_mode'] = 'list'
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "➕ New Initiative", "💸 Expenses & Revenue", "📈 ROI Analysis"])
    
    # TAB 1: OVERVIEW - UPDATED WITH FORMATTED DISPLAY
    with tab1:
        st.write("")  # Spacing
        
        if initiatives:
            st.subheader(f"Active Initiatives ({len(initiatives)})")
            
            st.write("")
            
            for initiative in initiatives:
                # Display with formatted values
                init_type = format_display_value(initiative.get('initiative_type', 'new_product'))
                matrix_display = format_display_value(initiative.get('matrix_type', ''))
                header = f"**{initiative['name']}** {f'({matrix_display})' if matrix_display else ''} - {init_type} - {format_display_value(initiative['stage'])} ({format_display_value(initiative['priority'])})"
                
                with st.expander(header):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write("**Details**")
                        if initiative.get('part_number'):
                            st.write(f"Part #: {initiative['part_number']}")
                        st.write(f"Lead: {initiative.get('lead_owner', 'Unassigned')}")
                        target_market = initiative.get('target_market', 'Not specified')
                        st.write(f"Target Market: {target_market[:50]}{'...' if len(target_market) > 50 else ''}")
                        if initiative.get('target_price'):
                            st.write(f"Target Price: ${initiative['target_price']:,.2f}")
                    
                    with col2:
                        st.write("**Timeline**")
                        if initiative.get('start_date'):
                            st.write(f"Started: {initiative['start_date']}")
                        if initiative.get('target_launch_date'):
                            st.write(f"Target Launch: {initiative['target_launch_date']}")
                    
                    with col3:
                        st.write("**Actions**")
                        st.write("")
                        if st.button("👁️ View Details", key=f"view_{initiative['id']}"):
                            st.session_state['selected_initiative'] = initiative['id']
                            st.session_state['view_mode'] = 'detail'
                            st.rerun()
                        if st.button("🗑️ Delete", key=f"delete_{initiative['id']}"):
                            if api_delete(f"/api/rd/initiatives/{initiative['id']}"):
                                st.success("Initiative deleted!")
                                st.rerun()
        else:
            st.info("No initiatives found. Create your first R&D initiative!")
    
    # TAB 2: NEW INITIATIVE - COMPLETELY UPDATED WITH ALL NEW FIELDS
    with tab2:
        st.write("")  # Spacing
        
        st.subheader("Create New R&D Initiative")
        
        st.write("")
        
        # Move Initiative Type OUTSIDE form so it can trigger conditional updates
        init_type = st.selectbox("Initiative Type*", INITIATIVE_TYPES, key="create_init_type")
        
        # Show helper text based on selection
        if init_type == "Revision":
            st.caption("💡 Revising an existing product - Part number required")
        else:
            st.caption("💡 Creating a brand new product")
        
        with st.form("new_initiative_form"):
            # Conditional: Part Number only shows for Revision
            if init_type == "Revision":
                st.write("**Product Revision Details**")
                part_number = st.text_input("Part Number*", 
                    placeholder="UTAK part number",
                    help="Required for product revisions")
                st.write("")
            else:
                part_number = None
            
            # Matrix Selection (NEW)
            st.write("**Matrix Information**")
            matrix_type = st.selectbox("Matrix Type*", MATRIX_TYPES)
            
            matrix_other = None
            if matrix_type == "Other":
                matrix_other = st.text_input("Describe Other Matrix*", placeholder="e.g., Oral fluid, hair, etc.")
            
            st.divider()
            
            # Rest of the form - WITH CAPITALIZED DROPDOWNS
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Initiative Name*", placeholder="PEth Stock Product Development")
                description = st.text_area("Description", placeholder="Develop standardized PEth QC product...", height=100)
                stage = st.selectbox("Stage", STAGES)
                priority = st.selectbox("Priority", PRIORITIES)
                lead_owner = st.text_input("Lead Owner", placeholder="Chy Plutchak")
            
            with col2:
                # Conditional: Target Market only for New Product
                if init_type == "New Product":
                    target_market = st.text_area("Target Market", placeholder="Clinical labs performing alcohol monitoring...", height=100)
                    market_size_estimate = st.number_input("Market Size Estimate ($)", min_value=0.0, step=1000.0)
                else:
                    target_market = None
                    market_size_estimate = None
                
                target_price = st.number_input("Target Price ($)", min_value=0.0, step=10.0)
                target_margin = st.number_input("Target Margin (%)", min_value=0.0, max_value=100.0, step=1.0)
                start_date = st.date_input("Start Date")
                target_launch_date = st.date_input("Target Launch Date")
            
            st.write("")
            st.divider()
            
            # Optional Team Assignment (NEW)
            with st.expander("➕ Optional: Add Initial Team Members"):
                st.caption("You can add team members now or later in the detail view. Just fill in the ones you want to add.")
                st.write("")
                
                # Show 3 optional team member slots
                team_members = []
                
                for i in range(3):
                    st.write(f"**Team Member {i+1}** (optional)")
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        dept = st.selectbox(f"Department", DEPARTMENTS, key=f"create_dept_{i}", label_visibility="collapsed")
                    with col_b:
                        person = st.text_input(f"Name", key=f"create_person_{i}", placeholder="e.g., Chy Plutchak", label_visibility="collapsed")
                    with col_c:
                        role = st.selectbox(f"Role", TEAM_ROLES, key=f"create_role_{i}", label_visibility="collapsed")
                    
                    if person:  # Only add if name is provided
                        team_members.append({
                            "department": dept,
                            "person_name": person,
                            "role": role
                        })
                    
                    if i < 2:  # Don't add divider after last one
                        st.write("")
            
            st.write("")
            submit = st.form_submit_button("Create Initiative", use_container_width=True, type="primary")
            
            if submit:
                # Validation
                errors = []
                if not name:
                    errors.append("Initiative name is required")
                if init_type == "Revision" and not part_number:
                    errors.append("Part number is required for revisions")
                if matrix_type == "Other" and not matrix_other:
                    errors.append("Please describe the other matrix type")
                
                if errors:
                    for error in errors:
                        st.error(error)
                else:
                    data = {
                        "name": name,
                        "description": description,
                        "initiative_type": to_snake_case(init_type),
                        "part_number": part_number if part_number else None,
                        "matrix_type": to_snake_case(matrix_type),
                        "matrix_other_description": matrix_other if matrix_type == "Other" else None,
                        "stage": to_snake_case(stage),
                        "priority": priority.lower(),
                        "lead_owner": lead_owner,
                        "target_market": target_market if target_market else None,
                        "market_size_estimate": market_size_estimate if market_size_estimate and market_size_estimate > 0 else None,
                        "target_price": target_price if target_price > 0 else None,
                        "target_margin": target_margin if target_margin > 0 else None,
                        "start_date": start_date.isoformat(),
                        "target_launch_date": target_launch_date.isoformat(),
                    }
                    
                    result = api_post("/api/rd/initiatives", data)
                    if result:
                        st.success(f"Initiative '{name}' created successfully!")
                        
                        # Add team members if any were specified
                        if team_members:
                            initiative_id = result['id']
                            success_count = 0
                            for member in team_members:
                                member['initiative_id'] = initiative_id
                                if api_post(f"/api/rd/initiatives/{initiative_id}/team", member):
                                    success_count += 1
                            
                            if success_count > 0:
                                st.success(f"Added {success_count} team member(s)!")
                        
                        st.rerun()
    
    # TAB 3: EXPENSES & REVENUE (unchanged)
    with tab3:
        st.write("")  # Spacing
        
        if initiatives:
            selected_initiative = st.selectbox(
                "Select Initiative",
                options=initiatives,
                format_func=lambda x: x['name']
            )
            
            st.write("")
            st.divider()
            
            if selected_initiative:
                initiative_id = selected_initiative['id']
                
                col1, col2 = st.columns(2)
                
                # EXPENSES
                with col1:
                    st.subheader("💸 Expenses")
                    
                    st.write("")
                    
                    with st.expander("➕ Add Expense"):
                        with st.form(f"expense_form_{initiative_id}"):
                            expense_category = st.selectbox("Category", ["Samples", "Travel", "Materials", "Staffing", "Marketing", "Other"])
                            expense_description = st.text_input("Description")
                            amount = st.number_input("Amount ($)", min_value=0.0, step=10.0)
                            expense_date = st.date_input("Date", value=date.today())
                            department = st.selectbox("Department", DEPARTMENTS)
                            
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
                    
                    st.write("")
                    
                    # Show expenses
                    expenses = api_get(f"/api/rd/expenses/initiative/{initiative_id}")
                    if expenses:
                        expense_df = pd.DataFrame(expenses)
                        st.dataframe(expense_df[['expense_category', 'amount', 'expense_date', 'department']], 
                                   use_container_width=True, height=250)
                        
                        st.write("")
                        
                        total_expenses = api_get(f"/api/rd/expenses/initiative/{initiative_id}/total")
                        if total_expenses:
                            st.metric("Total Expenses", f"${total_expenses['total_expenses']:,.2f}")
                    else:
                        st.info("No expenses recorded yet.")
                
                # REVENUE
                with col2:
                    st.subheader("💰 Revenue")
                    
                    st.write("")
                    
                    with st.expander("➕ Add Revenue"):
                        with st.form(f"revenue_form_{initiative_id}"):
                            customer_name = st.text_input("Customer Name")
                            order_number = st.text_input("Order Number")
                            order_value = st.number_input("Order Value ($)", min_value=0.0, step=100.0)
                            order_date = st.date_input("Order Date", value=date.today())
                            product_launched = st.selectbox("Product Launched?", ["No", "Yes"])
                            
                            if st.form_submit_button("Add Revenue"):
                                revenue_data = {
                                    "initiative_id": initiative_id,
                                    "customer_name": customer_name,
                                    "order_number": order_number,
                                    "order_value": order_value,
                                    "order_date": order_date.isoformat(),
                                    "product_launched": product_launched.lower()
                                }
                                if api_post("/api/rd/revenue", revenue_data):
                                    st.success("Revenue added!")
                                    st.rerun()
                    
                    st.write("")
                    
                    # Show revenue
                    revenue = api_get(f"/api/rd/revenue/initiative/{initiative_id}")
                    if revenue:
                        revenue_df = pd.DataFrame(revenue)
                        st.dataframe(revenue_df[['customer_name', 'order_value', 'order_date']], 
                                   use_container_width=True, height=250)
                        
                        st.write("")
                        
                        total_revenue = api_get(f"/api/rd/revenue/initiative/{initiative_id}/total")
                        if total_revenue:
                            st.metric("Total Revenue", f"${total_revenue['total_revenue']:,.2f}")
                    else:
                        st.info("No revenue recorded yet.")
        else:
            st.info("Create an initiative first!")
    
    # TAB 4: ROI ANALYSIS (unchanged from original - keeping all charts and analytics)
    with tab4:
        st.write("")  # Spacing
        
        if initiatives:
            st.header("📊 ROI & Decision Analytics")
            
            st.write("")
            
            # Collect all data first
            initiative_data = []
            for init in initiatives:
                exp_data = api_get(f"/api/rd/expenses/initiative/{init['id']}/total")
                rev_data = api_get(f"/api/rd/revenue/initiative/{init['id']}/total")
                samples = api_get(f"/api/rd/samples/initiative/{init['id']}")
                
                expenses = exp_data.get('total_expenses', 0) if exp_data else 0
                revenue = rev_data.get('total_revenue', 0) if rev_data else 0
                net = revenue - expenses
                roi = ((net / expenses) * 100) if expenses > 0 else 0
                
                sample_count = len(samples) if samples else 0
                converted = len([s for s in samples if s['converted_to_order'] == 'yes']) if samples else 0
                conversion_rate = (converted / sample_count * 100) if sample_count > 0 else 0
                
                initiative_data.append({
                    'name': init['name'],
                    'id': init['id'],
                    'stage': init['stage'],
                    'priority': init['priority'],
                    'expenses': expenses,
                    'revenue': revenue,
                    'net': net,
                    'roi': roi,
                    'samples': sample_count,
                    'converted': converted,
                    'conversion_rate': conversion_rate
                })
            
            # Portfolio-level metrics
            total_invested = sum([d['expenses'] for d in initiative_data])
            total_returned = sum([d['revenue'] for d in initiative_data])
            total_net = total_returned - total_invested
            portfolio_roi = ((total_net / total_invested) * 100) if total_invested > 0 else 0
            
            # Big metrics at top
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("💰 Portfolio Investment", f"${total_invested:,.0f}")
            with col2:
                st.metric("📈 Portfolio Revenue", f"${total_returned:,.0f}")
            with col3:
                st.metric("💵 Net Profit", f"${total_net:,.0f}")
            with col4:
                st.metric("🎯 Portfolio ROI", f"{portfolio_roi:.1f}%")
            
            st.divider()
            
            # Visual comparison charts
            st.subheader("Initiative Comparison")
            
            st.write("")
            
            if len(initiative_data) > 0:
                df = pd.DataFrame(initiative_data)
                
                # ROI comparison bar chart
                fig1 = go.Figure()
                
                colors = ['green' if x >= 0 else 'red' for x in df['roi']]
                
                fig1.add_trace(go.Bar(
                    x=df['name'],
                    y=df['roi'],
                    marker_color=colors,
                    text=df['roi'].round(1),
                    texttemplate='%{text}%',
                    textposition='outside'
                ))
                
                fig1.update_layout(
                    title="ROI Comparison by Initiative",
                    xaxis_title="Initiative",
                    yaxis_title="ROI (%)",
                    showlegend=False,
                    height=400
                )
                
                st.plotly_chart(fig1, use_container_width=True)
                
                st.write("")
                
                # Investment vs Revenue scatter
                fig2 = px.scatter(df, x='expenses', y='revenue', 
                                 size='roi', color='stage',
                                 hover_data=['name', 'roi', 'net'],
                                 title="Investment vs Revenue Analysis",
                                 labels={'expenses': 'Investment ($)', 'revenue': 'Revenue ($)'})
                
                # Add break-even line
                max_val = max(df['expenses'].max(), df['revenue'].max())
                fig2.add_trace(go.Scatter(
                    x=[0, max_val],
                    y=[0, max_val],
                    mode='lines',
                    line=dict(color='gray', dash='dash'),
                    name='Break-even Line',
                    showlegend=True
                ))
                
                st.plotly_chart(fig2, use_container_width=True)
                
                st.write("")
                
                # Sample conversion funnel
                if any(d['samples'] > 0 for d in initiative_data):
                    total_samples = sum([d['samples'] for d in initiative_data])
                    total_converted = sum([d['converted'] for d in initiative_data])
                    
                    funnel_data = pd.DataFrame({
                        'Stage': ['Samples Sent', 'Converted to Orders'],
                        'Count': [total_samples, total_converted]
                    })
                    
                    fig3 = go.Figure(go.Funnel(
                        y=funnel_data['Stage'],
                        x=funnel_data['Count'],
                        textinfo="value+percent initial",
                        marker=dict(color=["lightblue", "lightgreen"])
                    ))
                    
                    fig3.update_layout(
                        title="Portfolio Sample Conversion Funnel",
                        height=300
                    )
                    
                    st.plotly_chart(fig3, use_container_width=True)
            
            st.divider()
            
            # Detailed initiative cards
            st.subheader("Initiative Deep Dive")
            
            st.write("")
            
            for data in initiative_data:
                if data['expenses'] > 0 or data['revenue'] > 0:
                    # Determine status color
                    if data['roi'] >= 50:
                        status_color = "🟢 Strong Performer"
                    elif data['roi'] >= 0:
                        status_color = "🟡 Positive ROI"
                    else:
                        status_color = "🔴 Needs Review"
                    
                    with st.expander(f"**{data['name']}** - {status_color}"):
                        # Metrics row
                        col1, col2, col3, col4, col5 = st.columns(5)
                        
                        with col1:
                            st.metric("Investment", f"${data['expenses']:,.0f}")
                        with col2:
                            st.metric("Revenue", f"${data['revenue']:,.0f}")
                        with col3:
                            st.metric("Net", f"${data['net']:,.0f}")
                        with col4:
                            st.metric("ROI", f"{data['roi']:.1f}%")
                        with col5:
                            if data['samples'] > 0:
                                st.metric("Conversion", f"{data['conversion_rate']:.0f}%")
                            else:
                                st.metric("Samples", "0")
                        
                        st.write("")
                        
                        # Decision guidance
                        st.write("**📊 Decision Guidance:**")
                        
                        recommendations = []
                        
                        # ROI-based
                        if data['roi'] < 0 and data['expenses'] > 5000:
                            recommendations.append("⚠️ **High-cost, negative ROI** - Consider go/no-go decision")
                        elif data['roi'] > 100:
                            recommendations.append("✅ **Exceptional ROI** - Scale up investment")
                        elif data['roi'] > 25:
                            recommendations.append("✅ **Strong performance** - Continue current strategy")
                        
                        # Stage-based
                        if data['stage'] == 'feasibility' and data['expenses'] > 3000:
                            recommendations.append("⚠️ **High feasibility costs** - Make launch decision soon")
                        elif data['stage'] == 'launched' and data['revenue'] < 10000:
                            recommendations.append("📢 **Launched but low revenue** - Increase marketing efforts")
                        
                        # Sample conversion
                        if data['samples'] > 5 and data['conversion_rate'] < 20:
                            recommendations.append("⚠️ **Low sample conversion** - Review product-market fit")
                        elif data['samples'] > 0 and data['conversion_rate'] > 50:
                            recommendations.append("✅ **Strong conversion rate** - Send more samples")
                        
                        # Cost efficiency
                        if data['samples'] > 0:
                            cost_per_sample = data['expenses'] / data['samples']
                            if cost_per_sample > 500:
                                recommendations.append("💰 **High cost per sample** - Optimize sample production")
                        
                        if recommendations:
                            for rec in recommendations:
                                st.write(f"• {rec}")
                        else:
                            st.write("• ✅ No major concerns - initiative tracking as expected")
                        
                        st.write("")
                        
                        # Quick actions
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button(f"📋 View Full Details", key=f"detail_from_roi_{data['id']}"):
                                st.session_state['selected_initiative'] = data['id']
                                st.session_state['view_mode'] = 'detail'
                                st.rerun()
                        with col2:
                            if data['stage'] in ['feasibility', 'validation']:
                                st.write("**Stage:** Early - Monitor closely")
                            elif data['stage'] == 'launched':
                                st.write("**Stage:** Live - Scale if profitable")
        else:
            st.info("No initiatives to analyze. Create your first initiative!")

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