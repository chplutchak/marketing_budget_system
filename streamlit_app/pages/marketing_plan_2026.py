import streamlit as st
from datetime import date, datetime
import calendar
import json
import os

# For storing calendar completion state
STATE_FILE = "calendar_state.json"

def load_calendar_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_calendar_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f)

def show():
    st.title("📋 Marketing Plan 2026")
    
    # Initialize session state for calendar
    if 'calendar_state' not in st.session_state:
        st.session_state.calendar_state = load_calendar_state()
    
    if 'selected_month' not in st.session_state:
        st.session_state.selected_month = 1
    
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
        # Top level budget
        st.markdown("### 💰 2026 Marketing Budget")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Budget", "$213,000")
        with col2:
            st.metric("Fixed Costs", "$115,232", delta="54.1%")
        with col3:
            st.metric("Flexible Budget", "$97,768", delta="45.9%")
        
        st.divider()
        
        # Fixed Costs Cards
        st.markdown("### 🔒 Fixed Costs ($115,232)")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div style='background-color: #f0f2f6; padding: 15px; border-radius: 10px; text-align: center;'>
                <h3 style='color: #1f77b4; margin: 0;'>$24,450</h3>
                <p style='margin: 5px 0; color: #1f77b4;'><b>CaliNetworks</b></p>
                <p style='margin: 0; color: #1f77b4; font-size: 0.9em;'>SEO + Content</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style='background-color: #f0f2f6; padding: 15px; border-radius: 10px; text-align: center;'>
                <h3 style='color: #1f77b4; margin: 0;'>$40,711</h3>
                <p style='margin: 5px 0; color: #1f77b4;'><b>Conventions</b></p>
                <p style='margin: 0; color: #1f77b4; font-size: 0.9em;'>MATT, CAT, SOFT</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style='background-color: #f0f2f6; padding: 15px; border-radius: 10px; text-align: center;'>
                <h3 style='color: #1f77b4; margin: 0;'>$26,875</h3>
                <p style='margin: 5px 0; color: #1f77b4;'><b>HubSpot</b></p>
                <p style='margin: 0; color: #1f77b4; font-size: 0.9em;'>CRM + Marketing</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div style='background-color: #f0f2f6; padding: 15px; border-radius: 10px; text-align: center;'>
                <h3 style='color: #1f77b4; margin: 0;'>$23,196</h3>
                <p style='margin: 5px 0; color: #1f77b4;'><b>Designer</b></p>
                <p style='margin: 0; color: #1f77b4; font-size: 0.9em;'>All creative</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        # Flexible Budget Cards
        st.markdown("### 💸 Flexible Budget ($97,768)")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style='background-color: #fff4e6; padding: 15px; border-radius: 10px; border-left: 5px solid #ff7f0e;'>
                <h3 style='color: #ff7f0e; margin: 0;'>$30,000</h3>
                <p style='margin: 5px 0; color: #ff7f0e;'><b>Convention Support</b></p>
                <p style='margin: 0; color: #ff7f0e; font-size: 0.85em;'>• Materials: $25k<br>• Pre/post campaigns: $5k</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown("""
            <div style='background-color: #fef0f0; padding: 15px; border-radius: 10px; border-left: 5px solid #d62728;'>
                <h3 style='color: #d62728; margin: 0;'>$30,000</h3>
                <p style='margin: 5px 0;color: #d62728;'><b>R&D / Direct Mail</b></p>
                <p style='margin: 0; color: #d62728; font-size: 0.85em;'>• Sample programs: $15k<br>• Account mailers: $5k</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style='background-color: #e8f4f8; padding: 15px; border-radius: 10px; border-left: 5px solid #1f77b4;'>
                <h3 style='color: #1f77b4; margin: 0;'>$20,000</h3>
                <p style='margin: 5px 0; color: #1f77b4;'><b>Content Production</b></p>
                <p style='margin: 0; color: #1f77b4; font-size: 0.85em;'>• Copywriting: $8k<br>• Technical writing: $6k<br>• Photo/video: $4k<br>• Stock assets: $2k</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown("""
            <div style='background-color: #e8f8e8; padding: 15px; border-radius: 10px; border-left: 5px solid #2ca02c;'>
                <h3 style='color: #2ca02c; margin: 0;'>$11,768</h3>
                <p style='margin: 5px 0; color: #2ca02c;'><b>LinkedIn Ads</b></p>
                <p style='margin: 0; color: #2ca02c; font-size: 0.85em;'>• ABM campaigns: $5.8k<br>• Sponsored content: $5.8k</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style='background-color: #f0f0f0; padding: 15px; border-radius: 10px; border-left: 5px solid #7f7f7f;'>
                <h3 style='color: #7f7f7f; margin: 0;'>$3,000</h3>
                <p style='margin: 5px 0; color: #7f7f7f;'><b>Tools/Software</b></p>
                <p style='margin: 0; color: #7f7f7f; font-size: 0.85em;'>• Various sales tools: $3k</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown("""
            <div style='background-color: #f8f8e8; padding: 15px; border-radius: 10px; border-left: 5px solid #bcbd22;'>
                <h3 style='color: #bcbd22; margin: 0;'>$3,000</h3>
                <p style='margin: 5px 0; color: #bcbd22;'><b>Buffer</b></p>
                <p style='margin: 0; color: #bcbd22; font-size: 0.85em;'>Contingency for opportunities</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        # Quarterly Distribution
        st.markdown("### 📊 Quarterly Budget Distribution")
        
        quarters_data = {
            "Q1": {"total": 48300, "color": "#1f77b4", "focus": "Website launch, Product #1, MATT"},
            "Q2": {"total": 51300, "color": "#ff7f0e", "focus": "Product #2, CAT, R&D push"},
            "Q3": {"total": 58300, "color": "#2ca02c", "focus": "SOFT prep & execution (heaviest)"},
            "Q4": {"total": 42100, "color": "#d62728", "focus": "SOFT follow-up, nurture, planning"}
        }
        
        col1, col2, col3, col4 = st.columns(4)
        
        for col, (quarter, data) in zip([col1, col2, col3, col4], quarters_data.items()):
            with col:
                st.markdown(f"""
                <div style='background-color: {data['color']}; padding: 20px; border-radius: 10px; color: white; text-align: center;'>
                    <h3 style='margin: 0; color: white;'>{quarter}</h3>
                    <h2 style='margin: 10px 0; color: white;'>${data['total']:,}</h2>
                    <p style='margin: 0; font-size: 0.9em;'>{data['focus']}</p>
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
    # TAB 4: INTERACTIVE MARKETING CALENDAR
    # ==========================================
    with tab4:
        st.markdown("### 📅 2026 Marketing Calendar")
        
        # Year overview with major milestones
        st.markdown("#### Year Overview - Major Milestones")
        
        timeline_data = [
            {"month": "Q1", "color": "#1f77b4", "events": ["Website Launch", "Product #1 Launch", "MATT Convention"]},
            {"month": "Q2", "color": "#ff7f0e", "events": ["Product #2 Launch", "CAT Convention", "3 R&D Partnerships Closed"]},
            {"month": "Q3", "color": "#2ca02c", "events": ["SOFT/TIAFT (Sept)", "Biggest Lead Gen Event", "Showcase Both Products"]},
            {"month": "Q4", "color": "#d62728", "events": ["SOFT Lead Nurture", "2027 Planning", "Year-End Campaigns"]}
        ]
        
        cols = st.columns(4)
        for col, quarter in zip(cols, timeline_data):
            with col:
                st.markdown(f"""
                <div style='background-color: {quarter['color']}; padding: 15px; border-radius: 10px; color: white;'>
                    <h4 style='margin: 0; color: white; text-align: center;'>{quarter['month']}</h4>
                </div>
                """, unsafe_allow_html=True)
                for event in quarter['events']:
                    st.markdown(f"• {event}")
        
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
        
        # Monthly activities template
        monthly_activities = {
            1: {  # January
                "focus": "Foundation Setting",
                "major_campaigns": ["Website Launch", "New Year Customer Outreach"],
                "weekly_tasks": {
                    "Week 1": [
                        ("LinkedIn: Industry Insights/Trends", "monday", False),
                        ("Email: Educational Content", "tuesday", False),
                        ("LinkedIn: UTAK Story/Customer Success", "wednesday", False),
                        ("LinkedIn: Team Highlights/Culture", "friday", False),
                        ("Monthly Review", "friday", False)
                    ],
                    "Week 2": [
                        ("LinkedIn: Industry Insights/Trends", "monday", False),
                        ("Email: Product Spotlight", "tuesday", False),
                        ("LinkedIn: UTAK Story/Customer Success", "wednesday", False),
                        ("LinkedIn: Team Highlights/Culture", "friday", False),
                        ("Content Planning", "friday", False)
                    ],
                    "Week 3": [
                        ("LinkedIn: Industry Insights/Trends", "monday", False),
                        ("Email: Customer Success Story", "tuesday", False),
                        ("LinkedIn: UTAK Story/Customer Success", "wednesday", False),
                        ("LinkedIn: Team Highlights/Culture", "friday", False),
                        ("Direct Mail Planning", "thursday", False)
                    ],
                    "Week 4": [
                        ("LinkedIn: Industry Insights/Trends", "monday", False),
                        ("Email: Offer/CTA (Samples, Consult)", "tuesday", False),
                        ("LinkedIn: UTAK Story/Customer Success", "wednesday", False),
                        ("Product #1 Launch Prep", "thursday", False),
                        ("LinkedIn: Team Highlights/Culture", "friday", False)
                    ]
                }
            },
            2: {  # February
                "focus": "Product Launch #1 Execution",
                "major_campaigns": ["Product #1 Launch Campaign", "MATT Prep"],
                "weekly_tasks": {
                    "Week 1": [
                        ("LinkedIn: Industry Insights/Trends", "monday", False),
                        ("Email: Educational Content", "tuesday", False),
                        ("LinkedIn: UTAK Story/Customer Success", "wednesday", False),
                        ("LinkedIn: Team Highlights/Culture", "friday", False),
                        ("Monthly Review", "friday", False)
                    ],
                    "Week 2": [
                        ("LinkedIn: Product #1 Launch Announcement", "monday", False),
                        ("Email: Product #1 Launch Campaign", "tuesday", False),
                        ("LinkedIn: Product #1 Features/Benefits", "wednesday", False),
                        ("LinkedIn: Team Behind Product #1", "friday", False),
                        ("Direct Mail Execution - Product #1", "thursday", False)
                    ],
                    "Week 3": [
                        ("LinkedIn: Industry Insights/Trends", "monday", False),
                        ("Email: Customer Success Story", "tuesday", False),
                        ("LinkedIn: Early Product #1 Customer Story", "wednesday", False),
                        ("LinkedIn: Team Highlights/Culture", "friday", False),
                        ("MATT Materials Prep", "thursday", False)
                    ],
                    "Week 4": [
                        ("LinkedIn: MATT Preview/What to Expect", "monday", False),
                        ("Email: Offer/CTA (Samples, Consult)", "tuesday", False),
                        ("LinkedIn: UTAK at MATT - Booth Info", "wednesday", False),
                        ("LinkedIn: Team Heading to MATT", "friday", False),
                        ("MATT Pre-Event Campaign Launch", "thursday", False)
                    ]
                }
            },
            3: {  # March
                "focus": "MATT Convention & Q1 Close",
                "major_campaigns": ["MATT Convention", "Q1 Reporting"],
                "weekly_tasks": {
                    "Week 1": [
                        ("LinkedIn: Final MATT Reminder", "monday", False),
                        ("Email: Meet Us at MATT", "tuesday", False),
                        ("LinkedIn: Live Updates from MATT", "wednesday", False),
                        ("MATT Convention Days", "thursday", False),
                        ("MATT Follow-up Emails Start", "friday", False)
                    ],
                    "Week 2": [
                        ("LinkedIn: MATT Recap & Highlights", "monday", False),
                        ("Email: Product Spotlight", "tuesday", False),
                        ("LinkedIn: MATT Key Takeaways", "wednesday", False),
                        ("LinkedIn: Thank You MATT Attendees", "friday", False),
                        ("MATT Lead Nurture Setup", "thursday", False)
                    ],
                    "Week 3": [
                        ("LinkedIn: Industry Insights from MATT", "monday", False),
                        ("Email: Customer Success Story", "tuesday", False),
                        ("LinkedIn: UTAK Story/Customer Success", "wednesday", False),
                        ("LinkedIn: Team Highlights/Culture", "friday", False),
                        ("Q2 Planning Kickoff", "thursday", False)
                    ],
                    "Week 4": [
                        ("LinkedIn: Q1 Wins & Learnings", "monday", False),
                        ("Email: Offer/CTA (Samples, Consult)", "tuesday", False),
                        ("LinkedIn: Looking Ahead to Q2", "wednesday", False),
                        ("LinkedIn: Team Q1 Celebration", "friday", False),
                        ("Q1 Performance Report", "thursday", False)
                    ]
                }
            },
            4: {  # April
                "focus": "Product #2 Development & R&D Push",
                "major_campaigns": ["Product #2 Prep", "R&D Outreach Campaign"],
                "weekly_tasks": {
                    "Week 1": [
                        ("LinkedIn: Industry Insights/Trends", "monday", False),
                        ("Email: Educational Content", "tuesday", False),
                        ("LinkedIn: UTAK Story/Customer Success", "wednesday", False),
                        ("LinkedIn: Team Highlights/Culture", "friday", False),
                        ("Monthly Review", "friday", False)
                    ],
                    "Week 2": [
                        ("LinkedIn: R&D Partnership Value Prop", "monday", False),
                        ("Email: R&D Partnership Opportunities", "tuesday", False),
                        ("LinkedIn: UTAK R&D Capabilities", "wednesday", False),
                        ("LinkedIn: Team - R&D Focus", "friday", False),
                        ("Direct Mail Planning - R&D Targets", "thursday", False)
                    ],
                    "Week 3": [
                        ("LinkedIn: Industry Insights/Trends", "monday", False),
                        ("Email: Customer Success Story", "tuesday", False),
                        ("LinkedIn: Custom-to-Stock Success Story", "wednesday", False),
                        ("LinkedIn: Team Highlights/Culture", "friday", False),
                        ("Product #2 Content Development", "thursday", False)
                    ],
                    "Week 4": [
                        ("LinkedIn: Sneak Peek Product #2", "monday", False),
                        ("Email: Offer/CTA (Samples, Consult)", "tuesday", False),
                        ("LinkedIn: UTAK Innovation Process", "wednesday", False),
                        ("LinkedIn: Team Behind Product #2", "friday", False),
                        ("CAT Convention Prep Start", "thursday", False)
                    ]
                }
            },
            5: {  # May
                "focus": "Product #2 Launch & CAT",
                "major_campaigns": ["Product #2 Launch", "CAT Prep"],
                "weekly_tasks": {
                    "Week 1": [
                        ("LinkedIn: Industry Insights/Trends", "monday", False),
                        ("Email: Educational Content", "tuesday", False),
                        ("LinkedIn: UTAK Story/Customer Success", "wednesday", False),
                        ("LinkedIn: Team Highlights/Culture", "friday", False),
                        ("Monthly Review", "friday", False)
                    ],
                    "Week 2": [
                        ("LinkedIn: Product #2 Launch Announcement", "monday", False),
                        ("Email: Product #2 Launch Campaign", "tuesday", False),
                        ("LinkedIn: Product #2 Technical Deep Dive", "wednesday", False),
                        ("LinkedIn: Product #2 Applications", "friday", False),
                        ("Direct Mail Execution - Product #2", "thursday", False)
                    ],
                    "Week 3": [
                        ("LinkedIn: Product #2 vs Alternatives", "monday", False),
                        ("Email: Customer Success Story", "tuesday", False),
                        ("LinkedIn: Both Products Together Value", "wednesday", False),
                        ("LinkedIn: Team CAT Prep", "friday", False),
                        ("CAT Materials Preparation", "thursday", False)
                    ],
                    "Week 4": [
                        ("LinkedIn: CAT Preview/Meet Us There", "monday", False),
                        ("Email: CAT Pre-Event - Meet UTAK", "tuesday", False),
                        ("LinkedIn: What We're Showcasing at CAT", "wednesday", False),
                        ("LinkedIn: Team Heading to CAT", "friday", False),
                        ("CAT Pre-Event Campaign", "thursday", False)
                    ]
                }
            },
            6: {  # June
                "focus": "CAT Convention & Mid-Year Review",
                "major_campaigns": ["CAT Convention", "R&D Partnership Check-in", "Mid-Year Reporting"],
                "weekly_tasks": {
                    "Week 1": [
                        ("LinkedIn: Final CAT Reminder", "monday", False),
                        ("Email: Last Chance - Visit UTAK at CAT", "tuesday", False),
                        ("LinkedIn: Live from CAT", "wednesday", False),
                        ("CAT Convention Days", "thursday", False),
                        ("CAT Follow-up Emails Start", "friday", False)
                    ],
                    "Week 2": [
                        ("LinkedIn: CAT Recap & Key Moments", "monday", False),
                        ("Email: Product Spotlight", "tuesday", False),
                        ("LinkedIn: CAT Connections & Learnings", "wednesday", False),
                        ("LinkedIn: Thank You CAT Attendees", "friday", False),
                        ("R&D Partnership Status Review", "thursday", False)
                    ],
                    "Week 3": [
                        ("LinkedIn: Mid-Year Industry Trends", "monday", False),
                        ("Email: Customer Success Story", "tuesday", False),
                        ("LinkedIn: UTAK First Half Achievements", "wednesday", False),
                        ("LinkedIn: Team Mid-Year Celebration", "friday", False),
                        ("Q3 SOFT Planning Begins", "thursday", False)
                    ],
                    "Week 4": [
                        ("LinkedIn: Looking Ahead to H2", "monday", False),
                        ("Email: Offer/CTA (Samples, Consult)", "tuesday", False),
                        ("LinkedIn: SOFT September Preview", "wednesday", False),
                        ("LinkedIn: Team Gearing Up for SOFT", "friday", False),
                        ("Mid-Year Performance Report", "thursday", False)
                    ]
                }
            },
            7: {  # July
                "focus": "SOFT Preparation Begins",
                "major_campaigns": ["SOFT Pre-Event Campaign Launch"],
                "weekly_tasks": {
                    "Week 1": [
                        ("LinkedIn: Industry Insights/Trends", "monday", False),
                        ("Email: Educational Content", "tuesday", False),
                        ("LinkedIn: UTAK Story/Customer Success", "wednesday", False),
                        ("LinkedIn: Team Highlights/Culture", "friday", False),
                        ("Monthly Review", "friday", False)
                    ],
                    "Week 2": [
                        ("LinkedIn: SOFT September Announcement", "monday", False),
                        ("Email: SOFT Pre-Event Wave 1", "tuesday", False),
                        ("LinkedIn: Why Attend SOFT", "wednesday", False),
                        ("LinkedIn: Team SOFT Prep Begins", "friday", False),
                        ("Direct Mail Planning - SOFT Targets", "thursday", False)
                    ],
                    "Week 3": [
                        ("LinkedIn: SOFT Session Previews", "monday", False),
                        ("Email: Customer Success Story", "tuesday", False),
                        ("LinkedIn: What UTAK is Bringing to SOFT", "wednesday", False),
                        ("LinkedIn: Team Highlights/Culture", "friday", False),
                        ("SOFT Materials Design Start", "thursday", False)
                    ],
                    "Week 4": [
                        ("LinkedIn: SOFT Networking Preview", "monday", False),
                        ("Email: Offer/CTA (Samples, Consult)", "tuesday", False),
                        ("LinkedIn: UTAK SOFT History/Highlights", "wednesday", False),
                        ("LinkedIn: Team Countdown to SOFT", "friday", False),
                        ("SOFT Booth Design Finalize", "thursday", False)
                    ]
                }
            },
            8: {  # August
                "focus": "SOFT Final Prep",
                "major_campaigns": ["SOFT Direct Mail", "SOFT Pre-Event Intensifies"],
                "weekly_tasks": {
                    "Week 1": [
                        ("LinkedIn: 30 Days to SOFT", "monday", False),
                        ("Email: SOFT Pre-Event Wave 2", "tuesday", False),
                        ("LinkedIn: UTAK Booth Location & Details", "wednesday", False),
                        ("LinkedIn: Meet the UTAK SOFT Team", "friday", False),
                        ("Monthly Review", "friday", False)
                    ],
                    "Week 2": [
                        ("LinkedIn: SOFT Product Showcase Preview", "monday", False),
                        ("Email: Product Spotlight", "tuesday", False),
                        ("LinkedIn: Schedule Your SOFT Meeting", "wednesday", False),
                        ("LinkedIn: SOFT Demos & Presentations", "friday", False),
                        ("Direct Mail Execution - SOFT VIPs", "thursday", False)
                    ],
                    "Week 3": [
                        ("LinkedIn: 2 Weeks to SOFT", "monday", False),
                        ("Email: SOFT Pre-Event Wave 3", "tuesday", False),
                        ("LinkedIn: SOFT Must-See Sessions", "wednesday", False),
                        ("LinkedIn: Team Final SOFT Prep", "friday", False),
                        ("SOFT Booth Materials Complete", "thursday", False)
                    ],
                    "Week 4": [
                        ("LinkedIn: Final Week - SOFT Countdown", "monday", False),
                        ("Email: Final SOFT Reminder - Visit Us", "tuesday", False),
                        ("LinkedIn: UTAK SOFT Schedule", "wednesday", False),
                        ("LinkedIn: Team Traveling to SOFT", "friday", False),
                        ("SOFT Prep Complete - Travel", "thursday", False)
                    ]
                }
            },
            9: {  # September
                "focus": "SOFT/TIAFT - BIGGEST EVENT",
                "major_campaigns": ["SOFT Convention", "Product Showcase", "Aggressive Follow-up"],
                "weekly_tasks": {
                    "Week 1": [
                        ("LinkedIn: SOFT This Week!", "monday", False),
                        ("Email: Last Call - Meet UTAK at SOFT", "tuesday", False),
                        ("LinkedIn: En Route to SOFT", "wednesday", False),
                        ("SOFT Setup Day", "thursday", False),
                        ("SOFT Convention Day 1", "friday", False)
                    ],
                    "Week 2": [
                        ("LinkedIn: Live from SOFT - Day 2", "monday", False),
                        ("LinkedIn: SOFT Day 3 Highlights", "tuesday", False),
                        ("LinkedIn: SOFT Wrap-up & Thank Yous", "wednesday", False),
                        ("SOFT Travel Back", "thursday", False),
                        ("Lead Data Entry Begins", "friday", False)
                    ],
                    "Week 3": [
                        ("LinkedIn: SOFT Top 5 Takeaways", "monday", False),
                        ("Email: SOFT Follow-up Wave 1", "tuesday", False),
                        ("LinkedIn: SOFT Connections Recap", "wednesday", False),
                        ("LinkedIn: Thank You SOFT Attendees", "friday", False),
                        ("SOFT Follow-up Calls Start", "thursday", False)
                    ],
                    "Week 4": [
                        ("LinkedIn: SOFT Learnings Applied", "monday", False),
                        ("Email: SOFT Follow-up Wave 2", "tuesday", False),
                        ("LinkedIn: SOFT Lead Stories Begin", "wednesday", False),
                        ("LinkedIn: Team Post-SOFT Debrief", "friday", False),
                        ("Q3 Performance Report", "thursday", False)
                    ]
                }
            },
            10: {  # October
                "focus": "SOFT Lead Nurture & Q4 Planning",
                "major_campaigns": ["SOFT Lead Nurture", "Q4 Campaign Planning"],
                "weekly_tasks": {
                    "Week 1": [
                        ("LinkedIn: Industry Insights/Trends", "monday", False),
                        ("Email: Educational Content", "tuesday", False),
                        ("LinkedIn: UTAK Story/Customer Success", "wednesday", False),
                        ("LinkedIn: Team Highlights/Culture", "friday", False),
                        ("Monthly Review", "friday", False)
                    ],
                    "Week 2": [
                        ("LinkedIn: SOFT Success Story #1", "monday", False),
                        ("Email: SOFT Lead Follow-up Campaign", "tuesday", False),
                        ("LinkedIn: Implementing SOFT Insights", "wednesday", False),
                        ("LinkedIn: Team Q4 Focus", "friday", False),
                        ("Q4 Campaign Planning Workshop", "thursday", False)
                    ],
                    "Week 3": [
                        ("LinkedIn: Industry Insights/Trends", "monday", False),
                        ("Email: Customer Success Story", "tuesday", False),
                        ("LinkedIn: UTAK Story/Customer Success", "wednesday", False),
                        ("LinkedIn: Team Highlights/Culture", "friday", False),
                        ("2027 Budget Development Start", "thursday", False)
                    ],
                    "Week 4": [
                        ("LinkedIn: Q4 Priorities Preview", "monday", False),
                        ("Email: Offer/CTA (Samples, Consult)", "tuesday", False),
                        ("LinkedIn: Year-End Planning", "wednesday", False),
                        ("LinkedIn: Team Preparing for Year-End", "friday", False),
                        ("2027 Strategic Planning", "thursday", False)
                    ]
                }
            },
            11: {  # November
                "focus": "Year-End Push & 2027 Planning",
                "major_campaigns": ["Year-End Campaign", "Customer Retention"],
                "weekly_tasks": {
                    "Week 1": [
                        ("LinkedIn: Industry Insights/Trends", "monday", False),
                        ("Email: Educational Content", "tuesday", False),
                        ("LinkedIn: UTAK Story/Customer Success", "wednesday", False),
                        ("LinkedIn: Team Highlights/Culture", "friday", False),
                        ("Monthly Review", "friday", False)
                    ],
                    "Week 2": [
                        ("LinkedIn: Year-End Planning Tips", "monday", False),
                        ("Email: Year-End Special Offer", "tuesday", False),
                        ("LinkedIn: 2026 UTAK Wins", "wednesday", False),
                        ("LinkedIn: Team Gratitude", "friday", False),
                        ("Direct Mail Planning - Year-End", "thursday", False)
                    ],
                    "Week 3": [
                        ("LinkedIn: Industry Year in Review", "monday", False),
                        ("Email: Customer Success Story", "tuesday", False),
                        ("LinkedIn: Customer Appreciation", "wednesday", False),
                        ("LinkedIn: Team Year-End Reflections", "friday", False),
                        ("2027 Budget Finalization", "thursday", False)
                    ],
                    "Week 4": [
                        ("LinkedIn: Getting Ready for 2027", "monday", False),
                        ("Email: Offer/CTA (Samples, Consult)", "tuesday", False),
                        ("LinkedIn: UTAK 2027 Preview", "wednesday", False),
                        ("LinkedIn: Team Holiday Prep", "friday", False),
                        ("2027 Marketing Plan Draft", "thursday", False)
                    ]
                }
            },
            12: {  # December
                "focus": "Year-End & 2027 Prep",
                "major_campaigns": ["Customer Appreciation", "2027 Kickoff Planning"],
                "weekly_tasks": {
                    "Week 1": [
                        ("LinkedIn: Industry Insights/Trends", "monday", False),
                        ("Email: Customer Appreciation", "tuesday", False),
                        ("LinkedIn: Thank You 2026", "wednesday", False),
                        ("LinkedIn: Team Year in Review", "friday", False),
                        ("Monthly Review", "friday", False)
                    ],
                    "Week 2": [
                        ("LinkedIn: 2026 Top Moments", "monday", False),
                        ("Email: Product Spotlight", "tuesday", False),
                        ("LinkedIn: Customer Stories of 2026", "wednesday", False),
                        ("LinkedIn: Team Holiday Spirit", "friday", False),
                        ("Direct Mail Execution - Appreciation", "thursday", False)
                    ],
                    "Week 3": [
                        ("LinkedIn: Looking Forward to 2027", "monday", False),
                        ("Email: Customer Success Story", "tuesday", False),
                        ("LinkedIn: UTAK 2027 Goals", "wednesday", False),
                        ("LinkedIn: Team Holiday Message", "friday", False),
                        ("Annual Performance Review", "thursday", False)
                    ],
                    "Week 4": [
                        ("LinkedIn: Happy Holidays from UTAK", "monday", False),
                        ("Email: Year-End Thank You", "tuesday", False),
                        ("LinkedIn: 2026 Thank You Message", "wednesday", False),
                        ("LinkedIn: Team 2027 Kickoff Preview", "friday", False),
                        ("2026 Annual Report Complete", "thursday", False)
                    ]
                }
            }
        }
        
        # Display selected month
        month_data = monthly_activities.get(selected_month, {})
        
        st.markdown(f"### {month_names[selected_month-1]} 2026")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.info(f"**Focus:** {month_data.get('focus', 'N/A')}")
        with col2:
            st.info(f"**Major Campaigns:** {', '.join(month_data.get('major_campaigns', []))}")
        
        st.divider()
        
        # Weekly checklist
        for week, tasks in month_data.get('weekly_tasks', {}).items():
            st.markdown(f"#### {week}")
            
            for i, (task, day, completed) in enumerate(tasks):
                task_key = f"{selected_month}_{week}_{i}"
                
                # Get completion state
                is_complete = st.session_state.calendar_state.get(task_key, False)
                
                col1, col2, col3 = st.columns([0.5, 3, 1])
                
                with col1:
                    # Checkbox for completion
                    new_state = st.checkbox(
                        f"Complete {task}",
                        value=is_complete, 
                        key=f"check_{task_key}", 
                        label_visibility="collapsed"
                    )
                    if new_state != is_complete:
                        st.session_state.calendar_state[task_key] = new_state
                        save_calendar_state(st.session_state.calendar_state)
                
                with col2:
                    if is_complete:
                        st.markdown(f"~~{task}~~")
                    else:
                        st.markdown(f"**{task}**")
                
                with col3:
                    day_colors = {
                        "monday": "#1f77b4",
                        "tuesday": "#ff7f0e",
                        "wednesday": "#2ca02c",
                        "thursday": "#d62728",
                        "friday": "#9467bd"
                    }
                    color = day_colors.get(day, "#7f7f7f")
                    st.markdown(f"<span style='background-color: {color}; color: white; padding: 3px 10px; border-radius: 5px; font-size: 0.85em;'>{day.title()}</span>", unsafe_allow_html=True)
            
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