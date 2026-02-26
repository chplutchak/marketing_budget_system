import streamlit as st
from datetime import date, datetime
import calendar
import requests
import os

# API base URL
API_URL = os.getenv("API_URL", "http://localhost:8000")

# API Helper Functions
def get_calendar_with_activities(year: int, month: int):
    """Fetch calendar and activities from API"""
    try:
        response = requests.get(f"{API_URL}/api/marketing-calendar/calendars/{year}/{month}")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"Error fetching calendar: {str(e)}")
        return None

def get_all_calendars(year: int):
    """Fetch all calendars for a year"""
    try:
        response = requests.get(f"{API_URL}/api/marketing-calendar/calendars/year/{year}")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        st.error(f"Error fetching calendars: {str(e)}")
        return []

def toggle_activity_completion(activity_id: int):
    """Toggle activity completion status"""
    try:
        response = requests.patch(f"{API_URL}/api/marketing-calendar/activities/{activity_id}/toggle")
        return response.status_code == 200
    except Exception as e:
        st.error(f"Error toggling activity: {str(e)}")
        return False

def create_activity(calendar_id: int, week_number: int, activity_name: str, day_of_week: str, order: int = 0):
    """Create a new activity"""
    try:
        payload = {
            "calendar_id": calendar_id,
            "week_number": week_number,
            "activity_name": activity_name,
            "day_of_week": day_of_week,
            "order_in_week": order,
            "is_completed": False
        }
        response = requests.post(f"{API_URL}/api/marketing-calendar/activities/", json=payload)
        return response.status_code == 200
    except Exception as e:
        st.error(f"Error creating activity: {str(e)}")
        return False

def update_activity(activity_id: int, activity_name: str = None, day_of_week: str = None):
    """Update an existing activity"""
    try:
        payload = {}
        if activity_name:
            payload["activity_name"] = activity_name
        if day_of_week:
            payload["day_of_week"] = day_of_week
        
        response = requests.put(f"{API_URL}/api/marketing-calendar/activities/{activity_id}", json=payload)
        return response.status_code == 200
    except Exception as e:
        st.error(f"Error updating activity: {str(e)}")
        return False

def delete_activity(activity_id: int):
    """Delete an activity"""
    try:
        response = requests.delete(f"{API_URL}/api/marketing-calendar/activities/{activity_id}")
        return response.status_code == 200
    except Exception as e:
        st.error(f"Error deleting activity: {str(e)}")
        return False

def update_calendar_focus(calendar_id: int, focus: str, major_campaigns: list):
    """Update calendar focus and campaigns"""
    try:
        payload = {
            "focus": focus,
            "major_campaigns": major_campaigns
        }
        response = requests.put(f"{API_URL}/api/marketing-calendar/calendars/{calendar_id}", json=payload)
        return response.status_code == 200
    except Exception as e:
        st.error(f"Error updating calendar: {str(e)}")
        return False

def get_budget_by_year(year: int):
    """Fetch budget for a specific year"""
    try:
        response = requests.get(f"{API_URL}/api/marketing-budget/budgets/year/{year}")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"Error fetching budget: {str(e)}")
        return None

def get_categories_by_year(year: int):
    """Fetch all budget categories for a year"""
    try:
        response = requests.get(f"{API_URL}/api/marketing-budget/categories/year/{year}")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        st.error(f"Error fetching categories: {str(e)}")
        return []

def update_budget_totals(budget_id: int, total_budget: float, fixed_costs: float, flexible_budget: float):
    """Update budget totals"""
    try:
        payload = {
            "total_budget": total_budget,
            "fixed_costs": fixed_costs,
            "flexible_budget": flexible_budget
        }
        response = requests.put(f"{API_URL}/api/marketing-budget/budgets/{budget_id}", json=payload)
        return response.status_code == 200
    except Exception as e:
        st.error(f"Error updating budget: {str(e)}")
        return False

def update_category(category_id: int, amount: float = None, description: str = None, breakdown: dict = None):
    """Update a budget category"""
    try:
        payload = {}
        if amount is not None:
            payload["amount"] = amount
        if description is not None:
            payload["description"] = description
        if breakdown is not None:
            payload["breakdown"] = breakdown
        
        response = requests.put(f"{API_URL}/api/marketing-budget/categories/{category_id}", json=payload)
        return response.status_code == 200
    except Exception as e:
        st.error(f"Error updating category: {str(e)}")
        return False

def show():
    # Initialize session state
    if 'selected_month' not in st.session_state:
        st.session_state.selected_month = 1
    if 'edit_mode' not in st.session_state:
        st.session_state.edit_mode = False
    
    # Header with better spacing
    col1, col2 = st.columns([4, 1.5])
    with col1:
        st.title("📋 Marketing Plan 2026")
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            """
            <style>
            [data-testid="stToggle"] label {
                white-space: nowrap !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        st.session_state.edit_mode = st.toggle("✏️ Edit Mode", value=st.session_state.edit_mode)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🎯 Strategic Foundation",
        "💰 Budget",
        "📱 Channels", 
        "📅 Marketing Calendar",
        "📊 KPIs"
    ])
    
    # ==========================================
    # TAB 1: STRATEGIC FOUNDATION
    # ==========================================
    with tab1:
        # Big metrics at top
        st.markdown("### 2026 Targets")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Revenue Target", "$7.1M", delta="$X.XX current")
        with col2:
            st.metric("New Leads/Month", "60-80", delta="+10-30 vs current")
        with col3:
            st.metric("Website Conversion", "2%", delta="+1.4% vs 0.6%")
        with col4:
            st.metric("R&D Partnerships", "3 by June", delta="New initiative")
        
        st.divider()
        
        # Target Audiences - Card Style
        st.markdown("### 🎯 Target Audiences (Priority Order)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style='background-color: #1f77b4; padding: 20px; border-radius: 10px; color: white;'>
                <h4 style='margin-top: 0; color: white;'>🥇 PRIMARY</h4>
                <h3 style='color: white;'>Clinical Labs at Large Healthcare</h3>
                <p style='margin-bottom: 0;'><b>Examples:</b> Millennium, Mayo, Quest<br>
                <b>Cycle:</b> 6+ months<br>
                <b>Strategy:</b> ABM, technical content, relationship building</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            st.markdown("""
            <div style='background-color: #ff7f0e; padding: 20px; border-radius: 10px; color: white;'>
                <h4 style='margin-top: 0; color: white;'>🥉 TERTIARY</h4>
                <h3 style='color: white;'>R&D Partnership Targets</h3>
                <p style='margin-bottom: 0;'><b>Count:</b> 11 identified organizations<br>
                <b>Cycle:</b> 6-12 months<br>
                <b>Strategy:</b> Targeted outreach, capability presentations</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style='background-color: #2ca02c; padding: 20px; border-radius: 10px; color: white;'>
                <h4 style='margin-top: 0; color: white;'>🥈 SECONDARY</h4>
                <h3 style='color: white;'>Toxicology Labs</h3>
                <p style='margin-bottom: 0;'><b>Type:</b> Independent tox labs, hospital tox<br>
                <b>Cycle:</b> 3-6 months<br>
                <b>Strategy:</b> Product campaigns, sample programs</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            st.markdown("""
            <div style='background-color: #9467bd; padding: 20px; border-radius: 10px; color: white;'>
                <h4 style='margin-top: 0; color: white;'>♻️ ONGOING</h4>
                <h3 style='color: white;'>Existing Customers</h3>
                <p style='margin-bottom: 0;'><b>Count:</b> 213 active customers<br>
                <b>Value:</b> $7.2M portfolio<br>
                <b>Strategy:</b> Upsell, cross-sell, retention</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        # Marketing Objectives
        st.markdown("### ✅ Marketing Objectives")
        
        objectives = [
            ("📈", "Lead Generation", "60-80 new contacts/month", "HubSpot tracking"),
            ("🎤", "Thought Leadership", "Consistent LinkedIn presence", "Engagement metrics"),
            ("🚀", "Product Launches", "2 products ready for SOFT (Sept)", "Launch metrics"),
            ("💻", "Website Conversion", "2%+ conversion rate (80+ forms/month)", "GA4 tracking"),
            ("💼", "LinkedIn Presence", "3 posts/week, +500 followers", "LinkedIn analytics")
        ]
        
        for icon, title, target, measurement in objectives:
            col1, col2, col3 = st.columns([1, 3, 2])
            with col1:
                st.markdown(f"<h2 style='margin: 0;'>{icon}</h2>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"**{title}**")
                st.caption(target)
            with col3:
                st.caption(f"📊 {measurement}")
            st.divider()
    
    # ==========================================
    # TAB 2: BUDGET
    # ==========================================
    with tab2:
        # Fetch budget data
        budget_data = get_budget_by_year(2026)
        categories_data = get_categories_by_year(2026)
        
        if not budget_data:
            st.warning("No budget data found. Please run the budget migration script.")
            if st.button("📝 Run Migration Instructions"):
                st.code("python scripts/migrate_budget_data.py", language="bash")
        else:
            # Top level budget with edit capability
            st.markdown("### 💰 2026 Marketing Budget")
            
            if st.session_state.edit_mode:
                with st.expander("✏️ Edit Budget Totals", expanded=False):
                    col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
                    
                    with col1:
                        new_total = st.number_input(
                            "Total Budget",
                            value=float(budget_data["total_budget"]),
                            step=1000.0,
                            format="%.0f",
                            label_visibility="visible"
                        )
                    
                    with col2:
                        new_fixed = st.number_input(
                            "Fixed Costs",
                            value=float(budget_data["fixed_costs"]),
                            step=1000.0,
                            format="%.0f",
                            label_visibility="visible"
                        )
                    
                    with col3:
                        new_flexible = st.number_input(
                            "Flexible Budget",
                            value=float(budget_data["flexible_budget"]),
                            step=1000.0,
                            format="%.0f",
                            label_visibility="visible"
                        )
                    
                    with col4:
                        st.markdown("<br>", unsafe_allow_html=True)
                        if st.button("💾 Save", use_container_width=True):
                            if update_budget_totals(budget_data["id"], new_total, new_fixed, new_flexible):
                                st.success("✓ Saved!")
                                st.rerun()
            
            # Display totals
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Budget", f"${budget_data['total_budget']:,.0f}")
            with col2:
                fixed_pct = (budget_data['fixed_costs'] / budget_data['total_budget'] * 100)
                st.metric("Fixed Costs", f"${budget_data['fixed_costs']:,.0f}", delta=f"{fixed_pct:.1f}%")
            with col3:
                flex_pct = (budget_data['flexible_budget'] / budget_data['total_budget'] * 100)
                st.metric("Flexible Budget", f"${budget_data['flexible_budget']:,.0f}", delta=f"{flex_pct:.1f}%")
            
            st.divider()
            
            # Fixed Costs Cards
            fixed_total = budget_data.get('fixed_costs', 0)
            st.markdown(f"### 🔒 Fixed Costs (${fixed_total:,.0f})")
            
            fixed_categories = [c for c in categories_data if c['category_type'] == 'fixed']
            
            if fixed_categories:
                cols = st.columns(4)
                for idx, category in enumerate(fixed_categories):
                    with cols[idx % 4]:
                        if st.session_state.edit_mode:
                            with st.expander(f"✏️ Edit {category['category_name']}"):
                                new_amount = st.number_input(
                                    "Amount:",
                                    value=float(category['amount']),
                                    step=100.0,
                                    key=f"fixed_{category['id']}_amt"
                                )
                                new_desc = st.text_input(
                                    "Description:",
                                    value=category.get('description', ''),
                                    key=f"fixed_{category['id']}_desc"
                                )
                                if st.button("💾 Save", key=f"save_fixed_{category['id']}"):
                                    if update_category(category['id'], amount=new_amount, description=new_desc):
                                        st.success("✓ Saved!")
                                        st.rerun()
                        
                        st.markdown(f"""
                        <div style='background-color: #f0f2f6; padding: 15px; border-radius: 10px; text-align: center;'>
                            <h3 style='color: #1f77b4; margin: 0;'>${category['amount']:,.0f}</h3>
                            <p style='margin: 5px 0; color: #1f77b4;'><b>{category['category_name']}</b></p>
                            <p style='margin: 0; color: #1f77b4; font-size: 0.9em;'>{category.get('description', '')}</p>
                        </div>
                        """, unsafe_allow_html=True)
            
            st.divider()
            
            # Flexible Budget Cards
            flex_total = budget_data.get('flexible_budget', 0)
            st.markdown(f"### 💸 Flexible Budget (${flex_total:,.0f})")
            
            flexible_categories = [c for c in categories_data if c['category_type'] == 'flexible']
            
            if flexible_categories:
                # Color mapping for flexible categories
                color_map = {
                    "Convention Support": {"bg": "#fff4e6", "border": "#ff7f0e", "text": "#ff7f0e"},
                    "R&D / Direct Mail": {"bg": "#fef0f0", "border": "#d62728", "text": "#d62728"},
                    "Content Production": {"bg": "#e8f4f8", "border": "#1f77b4", "text": "#1f77b4"},
                    "LinkedIn Ads": {"bg": "#e8f8e8", "border": "#2ca02c", "text": "#2ca02c"},
                    "Tools/Software": {"bg": "#f0f0f0", "border": "#7f7f7f", "text": "#7f7f7f"},
                    "Buffer": {"bg": "#f8f8e8", "border": "#bcbd22", "text": "#bcbd22"}
                }
                
                col1, col2, col3 = st.columns(3)
                
                for idx, category in enumerate(flexible_categories):
                    colors = color_map.get(category['category_name'], {"bg": "#f0f0f0", "border": "#7f7f7f", "text": "#7f7f7f"})
                    
                    with [col1, col2, col3][idx % 3]:
                        if st.session_state.edit_mode:
                            with st.expander(f"✏️ Edit {category['category_name']}"):
                                new_amount = st.number_input(
                                    "Amount:",
                                    value=float(category['amount']),
                                    step=100.0,
                                    key=f"flex_{category['id']}_amt"
                                )
                                new_desc = st.text_input(
                                    "Description:",
                                    value=category.get('description', ''),
                                    key=f"flex_{category['id']}_desc"
                                )
                                
                                # Edit breakdown if exists
                                if category.get('breakdown'):
                                    st.markdown("**Breakdown:**")
                                    breakdown_str = "\n".join([f"{k}: {v}" for k, v in category['breakdown'].items()])
                                    new_breakdown_text = st.text_area(
                                        "Breakdown (format: Item: Amount)",
                                        value=breakdown_str,
                                        key=f"flex_{category['id']}_breakdown"
                                    )
                                    
                                    # Parse breakdown
                                    new_breakdown = {}
                                    for line in new_breakdown_text.split('\n'):
                                        if ':' in line:
                                            key, val = line.split(':', 1)
                                            try:
                                                new_breakdown[key.strip()] = float(val.strip())
                                            except:
                                                pass
                                else:
                                    new_breakdown = None
                                
                                if st.button("💾 Save", key=f"save_flex_{category['id']}"):
                                    if update_category(
                                        category['id'],
                                        amount=new_amount,
                                        description=new_desc,
                                        breakdown=new_breakdown
                                    ):
                                        st.success("✓ Saved!")
                                        st.rerun()
                        
                        # Build breakdown display
                        breakdown_html = ""
                        if category.get('breakdown'):
                            breakdown_items = [f"• {k}: ${v:,.0f}" for k, v in category['breakdown'].items()]
                            breakdown_html = "<br>".join(breakdown_items)
                        
                        st.markdown(f"""
                        <div style='background-color: {colors["bg"]}; padding: 15px; border-radius: 10px; border-left: 5px solid {colors["border"]}; margin-bottom: 15px;'>
                            <h3 style='color: {colors["text"]}; margin: 0;'>${category['amount']:,.0f}</h3>
                            <p style='margin: 5px 0; color: {colors["text"]};'><b>{category['category_name']}</b></p>
                            <p style='margin: 0; color: {colors["text"]}; font-size: 0.85em;'>{breakdown_html if breakdown_html else category.get('description', '')}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown("<br>", unsafe_allow_html=True)
            
            st.divider()
            
            # Quarterly Distribution
            st.markdown("### 📊 Quarterly Budget Distribution")
            
            quarterly = budget_data.get('quarterly_distribution', {})
            
            if quarterly:
                col1, col2, col3, col4 = st.columns(4)
                
                for col, (quarter, data) in zip([col1, col2, col3, col4], quarterly.items()):
                    with col:
                        if st.session_state.edit_mode:
                            with st.expander(f"✏️ Edit {quarter}"):
                                st.info("Quarterly distribution editing coming soon")
                        
                        st.markdown(f"""
                        <div style='background-color: {data.get('color', '#1f77b4')}; padding: 20px; border-radius: 10px; color: white; text-align: center;'>
                            <h3 style='margin: 0; color: white;'>{quarter}</h3>
                            <h2 style='margin: 10px 0; color: white;'>${data.get('total', 0):,}</h2>
                            <p style='margin: 0; font-size: 0.9em;'>{data.get('focus', '')}</p>
                        </div>
                        """, unsafe_allow_html=True)
    
    # ==========================================
    # TAB 3: CHANNELS (TACTICAL FOCUS)
    # ==========================================
    with tab3:
        st.markdown("### 📱 Channel Execution Plan")
        
        channels = [
            {
                "name": "LinkedIn Organic",
                "icon": "💼",
                "color": "#0077b5",
                "frequency": "3 posts/week",
                "days": "Monday, Wednesday, Friday",
                "time": "~3 hrs/week",
                "budget": "Time only",
                "tactics": [
                    "Mon: Industry insights, trends",
                    "Wed: UTAK capabilities, customer stories",
                    "Fri: Lighter content, team highlights"
                ]
            },
            {
                "name": "Email Campaigns",
                "icon": "📧",
                "color": "#ea4335",
                "frequency": "1 campaign/week",
                "days": "Every Tuesday",
                "time": "~2-4 hrs/week",
                "budget": "HubSpot (included)",
                "tactics": [
                    "Week 1: Educational content",
                    "Week 2: Product spotlight",
                    "Week 3: Customer success story",
                    "Week 4: Offer/CTA"
                ]
            },
            {
                "name": "LinkedIn Ads",
                "icon": "🎯",
                "color": "#0077b5",
                "frequency": "Always-on",
                "days": "Continuous",
                "time": "~1 hr/week",
                "budget": "$17,000/year",
                "tactics": [
                    "ABM to 11 R&D targets: $12k",
                    "Sponsored thought leadership: $5k",
                    "Weekly monitoring & optimization"
                ]
            },
            {
                "name": "Direct Mail",
                "icon": "📬",
                "color": "#f4b400",
                "frequency": "Quarterly",
                "days": "Month 2 of each quarter",
                "time": "~4 hrs/quarter",
                "budget": "$13,000/year",
                "tactics": [
                    "Sample programs to target accounts",
                    "Product announcements",
                    "Personalized high-value outreach"
                ]
            },
            {
                "name": "Conventions",
                "icon": "🎪",
                "color": "#34a853",
                "frequency": "3 per year",
                "days": "MATT (Q1), CAT (Q2), SOFT (Q3)",
                "time": "~1 week each",
                "budget": "$55,000/year",
                "tactics": [
                    "Pre-event email campaigns",
                    "Booth presence & demos",
                    "48-hour follow-up blitz"
                ]
            },
            {
                "name": "Website/SEO",
                "icon": "🌐",
                "color": "#4285f4",
                "frequency": "Ongoing",
                "days": "Continuous optimization",
                "time": "Vendor-managed",
                "budget": "$60,000/year",
                "tactics": [
                    "CaliNetworks: SEO monitoring",
                    "Product page optimization",
                    "Content updates for AI search"
                ]
            }
        ]
        
        col1, col2 = st.columns(2)
        
        for i, channel in enumerate(channels):
            with col1 if i % 2 == 0 else col2:
                st.markdown(f"""
                <div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid {channel['color']}; margin-bottom: 15px;'>
                    <h3 style='margin: 0 0 10px 0; color: #2c3e50;'>{channel['icon']} {channel['name']}</h3>
                    <p style='margin: 5px 0; color: #2c3e50;'><b>Frequency:</b> {channel['frequency']}</p>
                    <p style='margin: 5px 0; color: #2c3e50;'><b>When:</b> {channel['days']}</p>
                    <p style='margin: 5px 0; color: #2c3e50;'><b>Time:</b> {channel['time']}</p>
                    <p style='margin: 5px 0; color: #2c3e50;'><b>Budget:</b> {channel['budget']}</p>
                    <hr style='margin: 10px 0;'>
                    <p style='margin: 5px 0; font-size: 0.9em; color: #2c3e50;'><b>Tactics:</b></p>
                    <ul style='margin: 0; padding-left: 20px; color: #2c3e50;'>
                        {''.join(f"<li>{tactic}</li>" for tactic in channel['tactics'])}
                    </ul>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
    
    # ==========================================
    # TAB 4: INTERACTIVE MARKETING CALENDAR (API-DRIVEN)
    # ==========================================
    with tab4:
        st.markdown("### 📅 2026 Marketing Calendar")
        
        # Year overview with major milestones
        st.markdown("#### Year Overview - Major Milestones")
        
        # Fetch all calendars for the year
        all_calendars = get_all_calendars(2026)
        
        if all_calendars:
            # Group by quarter
            quarters = {
                "Q1": [c for c in all_calendars if c["month"] in [1, 2, 3]],
                "Q2": [c for c in all_calendars if c["month"] in [4, 5, 6]],
                "Q3": [c for c in all_calendars if c["month"] in [7, 8, 9]],
                "Q4": [c for c in all_calendars if c["month"] in [10, 11, 12]]
            }
            
            quarter_colors = {
                "Q1": "#1f77b4",
                "Q2": "#ff7f0e",
                "Q3": "#2ca02c",
                "Q4": "#d62728"
            }
            
            cols = st.columns(4)
            for col, (quarter, calendars) in zip(cols, quarters.items()):
                with col:
                    st.markdown(f"""
                    <div style='background-color: {quarter_colors[quarter]}; padding: 15px; border-radius: 10px; color: white;'>
                        <h4 style='margin: 0; color: white; text-align: center;'>{quarter}</h4>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Show all major campaigns from this quarter
                    all_campaigns = []
                    for cal in calendars:
                        if cal.get("major_campaigns"):
                            all_campaigns.extend(cal["major_campaigns"])
                    
                    for campaign in list(dict.fromkeys(all_campaigns)):  # Remove duplicates while preserving order
                        st.markdown(f"• {campaign}")
        else:
            st.warning("No calendar data found. Please run the migration script first.")
        
        st.divider()
        
        # Month selector
        st.markdown("#### Monthly View - Detailed Activities")
        
        month_names = ["January", "February", "March", "April", "May", "June",
                      "July", "August", "September", "October", "November", "December"]
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            selected_month = st.selectbox(
                "Select Month:",
                range(1, 13),
                format_func=lambda x: month_names[x-1],
                index=st.session_state.selected_month - 1,
                key="month_selector"
            )
            st.session_state.selected_month = selected_month
        
        # Fetch calendar data for selected month
        calendar_data = get_calendar_with_activities(2026, selected_month)
        
        if not calendar_data:
            st.warning(f"No calendar data found for {month_names[selected_month-1]} 2026")
            
            if st.session_state.edit_mode:
                st.info("📝 Run the migration script to populate calendar data, or create calendar entries via the API")
        else:
            # Display month header
            st.markdown(f"### {month_names[selected_month-1]} 2026")
            
            # Edit focus and campaigns
            if st.session_state.edit_mode:
                with st.expander("✏️ Edit Monthly Focus & Campaigns", expanded=False):
                    new_focus = st.text_input(
                        "Monthly Focus:",
                        value=calendar_data.get("focus", ""),
                        key="focus_input"
                    )
                    
                    campaigns_text = "\n".join(calendar_data.get("major_campaigns", []))
                    new_campaigns = st.text_area(
                        "Major Campaigns (one per line):",
                        value=campaigns_text,
                        key="campaigns_input",
                        height=100
                    )
                    
                    if st.button("💾 Save Changes", key="save_focus"):
                        campaigns_list = [c.strip() for c in new_campaigns.split("\n") if c.strip()]
                        if update_calendar_focus(calendar_data["id"], new_focus, campaigns_list):
                            st.success("✓ Updated successfully!")
                            st.rerun()
            
            # Display focus and campaigns
            col1, col2 = st.columns([2, 1])
            with col1:
                st.info(f"**Focus:** {calendar_data.get('focus', 'N/A')}")
            with col2:
                campaigns = calendar_data.get("major_campaigns", [])
                st.info(f"**Major Campaigns:** {', '.join(campaigns) if campaigns else 'None'}")
            
            st.divider()
            
            # Group activities by week
            activities = calendar_data.get("activities", [])
            activities_by_week = {}
            for activity in activities:
                week = activity["week_number"]
                if week not in activities_by_week:
                    activities_by_week[week] = []
                activities_by_week[week].append(activity)
            
            # Sort activities within each week by order
            for week in activities_by_week:
                activities_by_week[week].sort(key=lambda x: x["order_in_week"])
            
            # Display weekly activities
            for week in range(1, 5):  # Weeks 1-4
                st.markdown(f"#### Week {week}")
                
                week_activities = activities_by_week.get(week, [])
                
                # Add new activity button in edit mode
                if st.session_state.edit_mode:
                    with st.expander(f"➕ Add New Activity to Week {week}"):
                        with st.form(key=f"form_week_{week}", clear_on_submit=True):
                            new_activity_name = st.text_input(
                                "Activity Name:",
                                placeholder="e.g., LinkedIn: Industry Insights/Trends",
                                key=f"new_act_name_week{week}"
                            )
                            
                            new_day = st.selectbox(
                                "Day of Week:",
                                options=["monday", "tuesday", "wednesday", "thursday", "friday"],
                                format_func=lambda x: x.title(),
                                key=f"new_day_week{week}"
                            )
                            
                            submitted = st.form_submit_button("➕ Add Activity")
                            
                            if submitted and new_activity_name:
                                order = len(week_activities)
                                if create_activity(calendar_data["id"], week, new_activity_name, new_day, order):
                                    st.success("✓ Activity added!")
                                    st.rerun()
                            elif submitted:
                                st.error("Please enter an activity name")
                
                # Display activities
                if not week_activities:
                    st.caption("No activities for this week")
                else:
                    for activity in week_activities:
                        col1, col2, col3, col4 = st.columns([0.5, 3, 1, 0.5])
                        
                        with col1:
                            # Checkbox for completion
                            is_complete = activity["is_completed"]
                            new_state = st.checkbox(
                                f"Complete {activity['activity_name']}",
                                value=is_complete,
                                key=f"check_{activity['id']}",
                                label_visibility="collapsed"
                            )
                            
                            if new_state != is_complete:
                                if toggle_activity_completion(activity["id"]):
                                    st.rerun()
                        
                        with col2:
                            if st.session_state.edit_mode:
                                # Editable activity name
                                new_name = st.text_input(
                                    "Activity",
                                    value=activity["activity_name"],
                                    key=f"edit_{activity['id']}",
                                    label_visibility="collapsed"
                                )
                                
                                if new_name != activity["activity_name"]:
                                    # Show save button
                                    if st.button("💾", key=f"save_{activity['id']}", help="Save changes"):
                                        if update_activity(activity["id"], activity_name=new_name):
                                            st.success("✓ Saved!")
                                            st.rerun()
                            else:
                                # Display only
                                if is_complete:
                                    st.markdown(f"~~{activity['activity_name']}~~")
                                else:
                                    st.markdown(f"**{activity['activity_name']}**")
                        
                        with col3:
                            # Day of week badge
                            day_colors = {
                                "monday": "#1f77b4",
                                "tuesday": "#ff7f0e",
                                "wednesday": "#2ca02c",
                                "thursday": "#d62728",
                                "friday": "#9467bd"
                            }
                            color = day_colors.get(activity["day_of_week"], "#7f7f7f")
                            
                            if st.session_state.edit_mode:
                                # Editable day
                                new_day = st.selectbox(
                                    "Day",
                                    options=["monday", "tuesday", "wednesday", "thursday", "friday"],
                                    index=["monday", "tuesday", "wednesday", "thursday", "friday"].index(activity["day_of_week"]),
                                    format_func=lambda x: x.title(),
                                    key=f"day_{activity['id']}",
                                    label_visibility="collapsed"
                                )
                                
                                if new_day != activity["day_of_week"]:
                                    if update_activity(activity["id"], day_of_week=new_day):
                                        st.rerun()
                            else:
                                st.markdown(
                                    f"<span style='background-color: {color}; color: white; padding: 3px 10px; border-radius: 5px; font-size: 0.85em;'>{activity['day_of_week'].title()}</span>",
                                    unsafe_allow_html=True
                                )
                        
                        with col4:
                            # Delete button in edit mode
                            if st.session_state.edit_mode:
                                if st.button("🗑️", key=f"del_{activity['id']}", help="Delete activity"):
                                    if delete_activity(activity["id"]):
                                        st.success("✓ Deleted!")
                                        st.rerun()
                
                st.divider()
    
    # ==========================================
    # TAB 5: KPIs (SIMPLIFIED)
    # ==========================================
    with tab5:
        st.markdown("### 📊 Key Metrics & Success Criteria")
        
        st.info("💡 **Full analytics workflows and dashboards available in KPI Dashboard and Analytics Review pages**")
        
        # Success Metrics Table
        st.markdown("#### 2026 Targets")
        
        metrics_table = {
            "Metric": [
                "Website Traffic",
                "Website Conversion Rate",
                "Monthly New Leads",
                "Email Open Rate",
                "Email Click Rate",
                "LinkedIn Followers",
                "LinkedIn Engagement",
                "Convention Leads (SOFT)",
                "R&D Partnerships",
                "Marketing ROI"
            ],
            "Current Baseline": [
                "~4,000 users/month",
                "0.6% (26 forms/month)",
                "~50 contacts",
                "20-33%",
                "~3-5%",
                "TBD",
                "TBD",
                "Historical data",
                "0",
                "N/A"
            ],
            "2026 Target": [
                "4,500-5,000 users/month",
                "2% (80+ forms/month)",
                "60-80 contacts",
                "Maintain 20-33%",
                "3-5%",
                "+500 followers",
                "2-3% engagement rate",
                "50+ qualified leads",
                "3 by mid-year",
                "3:1 ($600k pipeline)"
            ],
            "Measurement": [
                "GA4 - Weekly review",
                "GA4 - Weekly review",
                "HubSpot - Weekly tracking",
                "HubSpot - Campaign reports",
                "HubSpot - Campaign reports",
                "LinkedIn Analytics",
                "LinkedIn Analytics",
                "Convention tracking",
                "Sales tracking",
                "Revenue attribution"
            ]
        }
        
        st.table(metrics_table)
        
        st.divider()
        
        # Review Cadence
        st.markdown("#### Analytics Review Cadence")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style='background-color: #e8f4f8; padding: 15px; border-radius: 10px; color: #2c3e50;'>
                <h4 style='color: #2c3e50;'>📅 Weekly</h4>
                <p><b>Time:</b> 30-45 min<br>
                <b>When:</b> Monday morning<br>
                <b>Focus:</b> Quick health check</p>
                <ul style='font-size: 0.9em; margin-top: 10px;'>
                    <li>Website users</li>
                    <li>Form submissions</li>
                    <li>Email performance</li>
                    <li>LinkedIn metrics</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style='background-color: #fff4e6; padding: 15px; border-radius: 10px; color: #2c3e50;'>
                <h4 style='color: #2c3e50;'>📊 Monthly</h4>
                <p><b>Time:</b> 2-3 hours<br>
                <b>When:</b> First week<br>
                <b>Focus:</b> Deep dive & trends</p>
                <ul style='font-size: 0.9em; margin-top: 10px;'>
                    <li>All metrics trended</li>
                    <li>Campaign review</li>
                    <li>Budget pacing</li>
                    <li>Adjustments</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style='background-color: #e8f8e8; padding: 15px; border-radius: 10px; color: #2c3e50;'>
                <h4 style='color: #2c3e50;'>📈 Quarterly</h4>
                <p><b>Time:</b> Half day<br>
                <b>When:</b> After quarter close<br>
                <b>Focus:</b> Strategic assessment</p>
                <ul style='font-size: 0.9em; margin-top: 10px;'>
                    <li>Goal progress</li>
                    <li>Channel ROI</li>
                    <li>Competition</li>
                    <li>Reforecasting</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        # Red Flags
        st.markdown("#### 🚨 Red Flags - When to Take Action")
        
        red_flags_data = {
            "⚠️ Severity": ["🔴 IMMEDIATE", "🔴 IMMEDIATE", "🟡 THIS WEEK", "🟡 THIS WEEK", "🟢 MONTHLY"],
            "Issue": [
                "Website down or forms broken",
                "Zero submissions for 3+ days",
                "Conversion rate drops 30%+",
                "Email opens below 15%",
                "Traffic declining 2-3 months"
            ],
            "Action": [
                "Test forms, check website immediately",
                "Investigate funnel, check for technical issues",
                "Analyze conversion path, review CTAs",
                "Review subject lines, list health, send times",
                "Review SEO with CaliNetworks, content audit"
            ]
        }
        
        st.table(red_flags_data)

if __name__ == "__main__":
    show()