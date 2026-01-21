import streamlit as st
import requests
import pandas as pd
from datetime import date, datetime, timedelta
import plotly.graph_objects as go
import os

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

def api_get(endpoint):
    try:
        response = requests.get(f"{API_BASE_URL}{endpoint}")
        return response.json() if response.status_code == 200 else []
    except:
        return []

def api_post(endpoint, data):
    try:
        response = requests.post(f"{API_BASE_URL}{endpoint}", json=data)
        return response.json() if response.status_code == 200 else None
    except:
        return None

def get_color_for_performance(current, target, threshold_high, threshold_low):
    """Returns color based on performance against target"""
    if current is None or target is None or target == 0:
        return "#7f7f7f"  # Gray for no data
    
    ratio = current / target
    
    if ratio >= threshold_high:
        return "#2ca02c"  # Green
    elif ratio >= threshold_low:
        return "#ff7f0e"  # Yellow/Orange
    else:
        return "#d62728"  # Red

def get_status_emoji(current, target, threshold_high, threshold_low):
    """Returns emoji based on performance"""
    if current is None or target is None or target == 0:
        return "⚪"
    
    ratio = current / target
    
    if ratio >= threshold_high:
        return "🟢"
    elif ratio >= threshold_low:
        return "🟡"
    else:
        return "🔴"

def create_sparkline(data_points, color="#1f77b4"):
    """Creates a small sparkline chart"""
    if not data_points or len(data_points) == 0:
        return None
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        y=[d['value'] for d in data_points],
        mode='lines',
        line=dict(color=color, width=2),
        showlegend=False
    ))
    
    fig.update_layout(
        height=60,
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
        yaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def format_metric_value(value, unit):
    """Format large numbers with K/M suffix"""
    if value is None:
        return "No data"
    
    # For percentages, keep as-is
    if unit == '%':
        return f"{value:.1f}%"
    
    # For large numbers, use K/M notation with space before unit
    if value >= 1000000:
        return f"{value/1000000:.1f}M {unit}" if unit else f"{value/1000000:.1f}M"
    elif value >= 1000:
        return f"{value/1000:.1f}K {unit}" if unit else f"{value/1000:.1f}K"
    else:
        return f"{value:.0f} {unit}" if unit else f"{value:.0f}"

def show():
    st.title("📊 KPI Dashboard")
    
    # Main tabs
    tab1, tab2, tab3 = st.tabs(["📈 Dashboard", "📝 Log Data", "⚙️ Manage Metrics"])
    
    # Get all dashboard data
    dashboard_data = api_get("/api/kpi/dashboard/summary")
    
   # ==========================================
    # TAB 1: DASHBOARD VIEW
    # ==========================================
    with tab1:
        # Custom CSS to make metrics smaller
        st.markdown("""
        <style>
        [data-testid="stMetricValue"] {
            font-size: 1.5rem !important;
        }
        [data-testid="stMetricLabel"] {
            font-size: 0.9rem !important;
        }
        [data-testid="stMetricDelta"] {
            font-size: 0.8rem !important;
        }
        </style>
        """, unsafe_allow_html=True)

        if not dashboard_data:
            st.info("No metrics configured yet. Go to 'Manage Metrics' tab to add your first KPI.")
        else:
            # Active Red Flags Alert Box
            st.markdown("### 🚨 Active Alerts")
            
            # Check for actual red flag conditions
            alerts = []
            for item in dashboard_data:
                metric = item['metric']
                latest_weekly = item['latest_weekly']
                latest_monthly = item['latest_monthly']
                
                current_value = None
                if latest_monthly:
                    current_value = latest_monthly['actual_value']
                elif latest_weekly:
                    current_value = latest_weekly['actual_value']
                
                # Check conditions
                if metric['name'] == 'Website Conversion Rate' and current_value:
                    baseline = metric.get('baseline_value')
                    if baseline and current_value < baseline * 0.7:
                        alerts.append("🔴 Conversion rate dropped 30%+ from baseline - Investigate immediately")
                
                if metric['name'] == 'Email Open Rate' and current_value:
                    if current_value < 15:
                        alerts.append("🟡 Email open rate below 15% - Review subject lines and send times")
                
                if metric['name'] == 'Website Traffic' and current_value:
                    # Check if we have at least 3 months of data to detect decline
                    monthly_hist = item['monthly_history']
                    if len(monthly_hist) >= 3:
                        recent_values = [h['actual_value'] for h in monthly_hist[:3]]
                        if all(recent_values[i] > recent_values[i+1] for i in range(len(recent_values)-1)):
                            alerts.append("🟢 Traffic declining for 2-3 months - Review SEO and content")
            
            if alerts:
                for alert in alerts:
                    if "🔴" in alert:
                        st.error(alert)
                    elif "🟡" in alert:
                        st.warning(alert)
                    else:
                        st.info(alert)
            else:
                st.success("✅ All metrics healthy - No alerts")
            
            st.divider()

            st.markdown("### 📊 Performance Overview")
            
            # Filter by category
            categories = list(set([item['metric']['category'] for item in dashboard_data]))
            
            for category in categories:
                st.markdown(f"#### {category}")
                
                category_metrics = [item for item in dashboard_data if item['metric']['category'] == category]
                
                # Create columns for cards (2 per row)
                cols = st.columns(2)
                
                for idx, item in enumerate(category_metrics):
                    metric = item['metric']
                    latest_weekly = item['latest_weekly']
                    latest_monthly = item['latest_monthly']
                    weekly_history = item['weekly_history']
                    monthly_history = item['monthly_history']
                    
                    with cols[idx % 2]:
                        # Determine which data to show (prefer monthly if available)
                        current_value = None
                        current_date = None
                        history_data = []
                        
                        if metric['tracking_frequency'] in ['monthly', 'both'] and latest_monthly:
                            current_value = latest_monthly['actual_value']
                            current_date = latest_monthly['snapshot_date']
                            history_data = [{'date': h['snapshot_date'], 'value': h['actual_value']} 
                                          for h in reversed(monthly_history)]
                        elif metric['tracking_frequency'] in ['weekly', 'both'] and latest_weekly:
                            current_value = latest_weekly['actual_value']
                            current_date = latest_weekly['snapshot_date']
                            history_data = [{'date': h['snapshot_date'], 'value': h['actual_value']} 
                                          for h in reversed(weekly_history)]
                        
                        # Calculate progress
                        target = metric['target_value']
                        baseline = metric['baseline_value'] if metric['baseline_value'] else 0
                        
                        color = get_color_for_performance(
                            current_value, 
                            target, 
                            metric['target_threshold_high'], 
                            metric['target_threshold_low']
                        )
                        
                        status_emoji = get_status_emoji(
                            current_value,
                            target,
                            metric['target_threshold_high'],
                            metric['target_threshold_low']
                        )
                        
                        # Create card
                        st.markdown(f"""
                        <div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px; 
                                    border-left: 5px solid {color}; margin-bottom: 20px;'>
                            <h4 style='margin: 0 0 10px 0; color: #2c3e50;'>{status_emoji} {metric['name']}</h4>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Metrics row
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            current_display = format_metric_value(current_value, metric['unit'])
                            st.metric(
                                "Current", 
                                current_display,
                                delta=f"as of {current_date}" if current_date else None
                            )

                        with col2:
                            target_display = format_metric_value(target, metric['unit'])
                            st.metric("Target", target_display)

                        with col3:
                            if current_value and target:
                                pct_of_target = (current_value / target * 100)
                                st.metric("Progress", f"{pct_of_target:.0f}%")
                        
                        # Progress bar
                        if current_value and target:
                            progress_pct = min(current_value / target, 1.0)
                            st.progress(progress_pct)
                        
                        # Sparkline
                        if history_data and len(history_data) > 1:
                            sparkline = create_sparkline(history_data, color)
                            if sparkline:
                                st.plotly_chart(sparkline, use_container_width=True, config={'displayModeBar': False})
                        
                        # Details expander
                        with st.expander("View Details"):
                            st.caption(f"**Baseline:** {metric['baseline_label']}")
                            st.caption(f"**Target:** {metric['target_label']}")
                            st.caption(f"**Measurement:** {metric['measurement_method']}")
                            st.caption(f"**Tracking:** {metric['tracking_frequency']}")
                            
                            if metric['description']:
                                st.caption(f"**Notes:** {metric['description']}")
                            
                            # Historical data
                            if history_data:
                                st.markdown("**Recent History:**")
                                history_df = pd.DataFrame(history_data)
                                history_df['date'] = pd.to_datetime(history_df['date'])
                                history_df = history_df.sort_values('date', ascending=False)
                                st.dataframe(history_df.head(5), use_container_width=True)
                
                st.divider()
        
        st.dataframe(use_container_width=True, hide_index=True)
    
    # ==========================================
    # TAB 2: LOG DATA
    # ==========================================
    with tab2:
        st.markdown("### 📝 Log KPI Data")
        
        metrics = api_get("/api/kpi/metrics/")
        
        if not metrics:
            st.info("No metrics configured yet. Go to 'Manage Metrics' tab to add metrics first.")
        else:
            st.markdown("#### Quick Log")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                selected_metric = st.selectbox(
                    "Select Metric",
                    metrics,
                    format_func=lambda x: f"{x['name']} ({x['category']})"
                )
            
            with col2:
                snapshot_type = st.selectbox(
                    "Type",
                    ["weekly", "monthly"] if selected_metric['tracking_frequency'] == 'both' 
                    else [selected_metric['tracking_frequency']]
                )
            
            with st.form("log_kpi_data"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    snapshot_date = st.date_input("Date", value=date.today())
                
                with col2:
                    actual_value = st.number_input(
                        f"Value ({selected_metric['unit'] or ''})",
                        min_value=0.0,
                        value=0.0,
                        format="%.2f"
                    )
                
                with col3:
                    st.write("")  # Spacing
                
                notes = st.text_area("Notes (optional)", placeholder="Any context for this data point...")
                
                col_submit, col_clear = st.columns(2)
                
                with col_submit:
                    if st.form_submit_button("📊 Log Data", type="primary", use_container_width=True):
                        if actual_value <= 0:
                            st.error("Value must be greater than 0")
                        else:
                            data = {
                                "metric_id": selected_metric['id'],
                                "snapshot_date": snapshot_date.isoformat(),
                                "snapshot_type": snapshot_type,
                                "actual_value": float(actual_value),
                                "notes": notes if notes else None
                            }
                            
                            result = api_post("/api/kpi/snapshots/", data)
                            
                            if result:
                                st.success(f"✅ Logged {actual_value}{selected_metric['unit'] or ''} for {selected_metric['name']}")
                                st.rerun()
                            else:
                                st.error("Failed to log data")
                
                with col_clear:
                    if st.form_submit_button("Clear", use_container_width=True):
                        st.rerun()
            
            st.divider()
            
            # Recent entries
            st.markdown("#### Recent Entries")
            
            if selected_metric:
                recent_snapshots = api_get(f"/api/kpi/snapshots/metric/{selected_metric['id']}?limit=10")
                
                if recent_snapshots:
                    df = pd.DataFrame(recent_snapshots)
                    df['snapshot_date'] = pd.to_datetime(df['snapshot_date']).dt.strftime('%Y-%m-%d')
                    df = df[['snapshot_date', 'snapshot_type', 'actual_value', 'notes']]
                    df.columns = ['Date', 'Type', 'Value', 'Notes']
                    
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info("No data logged yet for this metric.")
    
    # ==========================================
    # TAB 3: MANAGE METRICS
    # ==========================================
    with tab3:
        st.markdown("### ⚙️ Manage KPI Metrics")
        
        sub_tab1, sub_tab2 = st.tabs(["View Metrics", "Add New Metric"])
        
        with sub_tab1:
            metrics = api_get("/api/kpi/metrics/")
            
            if not metrics:
                st.info("No metrics configured yet. Use 'Add New Metric' tab to create your first KPI.")
            else:
                for metric in metrics:
                    with st.expander(f"{metric['name']} ({metric['category']})"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write(f"**Baseline:** {metric['baseline_label']}")
                            st.write(f"**Target:** {metric['target_label']}")
                            st.write(f"**Measurement:** {metric['measurement_method']}")
                        
                        with col2:
                            st.write(f"**Category:** {metric['category']}")
                            st.write(f"**Tracking:** {metric['tracking_frequency']}")
                            st.write(f"**Unit:** {metric['unit'] or 'N/A'}")
                        
                        if metric['description']:
                            st.write(f"**Description:** {metric['description']}")
                        
                        # Count snapshots
                        snapshots = api_get(f"/api/kpi/snapshots/metric/{metric['id']}")
                        st.caption(f"📊 {len(snapshots)} data points logged")
        
        with sub_tab2:
            st.markdown("#### Add New KPI Metric")
            
            with st.form("add_metric"):
                col1, col2 = st.columns(2)
                
                with col1:
                    name = st.text_input("Metric Name*", placeholder="e.g., Website Traffic")
                    category = st.selectbox("Category*", 
                                           ["Website", "Email", "LinkedIn", "Leads", "Conventions", "Revenue", "Other"])
                    baseline_label = st.text_input("Baseline Label", placeholder="e.g., ~4,000 users/month")
                    baseline_value = st.number_input("Baseline Value (for calculations)", value=0.0, format="%.2f")
                
                with col2:
                    target_label = st.text_input("Target Label*", placeholder="e.g., 4,500-5,000 users/month")
                    target_value = st.number_input("Target Value*", value=0.0, format="%.2f")
                    unit = st.text_input("Unit", placeholder="e.g., users, %, $")
                    tracking_frequency = st.selectbox("Tracking Frequency*", ["weekly", "monthly", "both"])
                
                measurement_method = st.text_input("Measurement Method*", 
                                                  placeholder="e.g., GA4 - Weekly review")
                description = st.text_area("Description (optional)")
                
                st.markdown("**Performance Thresholds**")
                col1, col2 = st.columns(2)
                with col1:
                    threshold_high = st.slider("Green threshold (% of target)", 0, 100, 95) / 100
                with col2:
                    threshold_low = st.slider("Yellow threshold (% of target)", 0, 100, 70) / 100
                
                if st.form_submit_button("Create Metric", type="primary"):
                    if not name or not target_label or target_value <= 0 or not measurement_method:
                        st.error("Please fill in all required fields")
                    else:
                        data = {
                            "name": name,
                            "description": description if description else None,
                            "category": category,
                            "baseline_value": float(baseline_value) if baseline_value > 0 else None,
                            "baseline_label": baseline_label if baseline_label else None,
                            "target_value": float(target_value),
                            "target_label": target_label,
                            "measurement_method": measurement_method,
                            "tracking_frequency": tracking_frequency,
                            "unit": unit if unit else None,
                            "target_threshold_high": threshold_high,
                            "target_threshold_low": threshold_low
                        }
                        
                        result = api_post("/api/kpi/metrics/", data)
                        
                        if result:
                            st.success(f"✅ Created metric: {name}")
                            st.rerun()
                        else:
                            st.error("Failed to create metric")
            
            st.divider()
            
            st.markdown("#### Quick Setup: 2026 UTAK Metrics")
            
            if st.button("Load Standard UTAK KPIs"):
                standard_metrics = [
                    {
                        "name": "Website Traffic",
                        "category": "Website",
                        "baseline_value": 4000,
                        "baseline_label": "~4,000 users/month",
                        "target_value": 4750,
                        "target_label": "4,500-5,000 users/month",
                        "measurement_method": "GA4 - Weekly review",
                        "tracking_frequency": "both",
                        "unit": "users",
                        "target_threshold_high": 0.95,
                        "target_threshold_low": 0.70
                    },
                    {
                        "name": "Website Conversion Rate",
                        "category": "Website",
                        "baseline_value": 0.6,
                        "baseline_label": "0.6% (26 forms/month)",
                        "target_value": 2.0,
                        "target_label": "2% (80+ forms/month)",
                        "measurement_method": "GA4 - Weekly review",
                        "tracking_frequency": "both",
                        "unit": "%",
                        "target_threshold_high": 0.95,
                        "target_threshold_low": 0.70
                    },
                    {
                        "name": "Monthly New Leads",
                        "category": "Leads",
                        "baseline_value": 50,
                        "baseline_label": "~50 contacts",
                        "target_value": 70,
                        "target_label": "60-80 contacts",
                        "measurement_method": "HubSpot - Weekly tracking",
                        "tracking_frequency": "both",
                        "unit": "contacts",
                        "target_threshold_high": 0.95,
                        "target_threshold_low": 0.70
                    },
                    {
                        "name": "Email Open Rate",
                        "category": "Email",
                        "baseline_value": 26.5,
                        "baseline_label": "20-33%",
                        "target_value": 26.5,
                        "target_label": "Maintain 20-33%",
                        "measurement_method": "HubSpot - Campaign reports",
                        "tracking_frequency": "monthly",
                        "unit": "%",
                        "target_threshold_high": 0.95,
                        "target_threshold_low": 0.70
                    },
                    {
                        "name": "Email Click Rate",
                        "category": "Email",
                        "baseline_value": 4.0,
                        "baseline_label": "~3-5%",
                        "target_value": 4.0,
                        "target_label": "3-5%",
                        "measurement_method": "HubSpot - Campaign reports",
                        "tracking_frequency": "monthly",
                        "unit": "%",
                        "target_threshold_high": 0.95,
                        "target_threshold_low": 0.70
                    },
                    {
                        "name": "LinkedIn Followers",
                        "category": "LinkedIn",
                        "baseline_value": None,
                        "baseline_label": "TBD",
                        "target_value": 500,
                        "target_label": "+500 followers",
                        "measurement_method": "LinkedIn Analytics",
                        "tracking_frequency": "monthly",
                        "unit": "followers",
                        "target_threshold_high": 0.95,
                        "target_threshold_low": 0.70
                    },
                    {
                        "name": "LinkedIn Engagement Rate",
                        "category": "LinkedIn",
                        "baseline_value": None,
                        "baseline_label": "TBD",
                        "target_value": 2.5,
                        "target_label": "2-3% engagement rate",
                        "measurement_method": "LinkedIn Analytics",
                        "tracking_frequency": "weekly",
                        "unit": "%",
                        "target_threshold_high": 0.95,
                        "target_threshold_low": 0.70
                    },
                    {
                        "name": "SOFT Convention Leads",
                        "category": "Conventions",
                        "baseline_value": None,
                        "baseline_label": "Historical data",
                        "target_value": 50,
                        "target_label": "50+ qualified leads",
                        "measurement_method": "Convention tracking",
                        "tracking_frequency": "monthly",
                        "unit": "leads",
                        "target_threshold_high": 0.95,
                        "target_threshold_low": 0.70
                    },
                    {
                        "name": "R&D Partnerships",
                        "category": "Revenue",
                        "baseline_value": 0,
                        "baseline_label": "0",
                        "target_value": 3,
                        "target_label": "3 by mid-year",
                        "measurement_method": "Sales tracking",
                        "tracking_frequency": "monthly",
                        "unit": "partnerships",
                        "target_threshold_high": 0.95,
                        "target_threshold_low": 0.70
                    },
                    {
                        "name": "Marketing ROI",
                        "category": "Revenue",
                        "baseline_value": None,
                        "baseline_label": "N/A",
                        "target_value": 3.0,
                        "target_label": "3:1 ($600k pipeline)",
                        "measurement_method": "Revenue attribution",
                        "tracking_frequency": "monthly",
                        "unit": ":1",
                        "target_threshold_high": 0.95,
                        "target_threshold_low": 0.70
                    }
                ]
                
                success_count = 0
                for metric_data in standard_metrics:
                    result = api_post("/api/kpi/metrics/", metric_data)
                    if result:
                        success_count += 1
                
                if success_count > 0:
                    st.success(f"✅ Loaded {success_count} standard UTAK KPIs")
                    st.rerun()
                else:
                    st.error("Failed to load metrics")

if __name__ == "__main__":
    show()