"""
Reusable UI components for calendar management
"""
import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL", "http://localhost:8000")

def calendar_editor(calendar_id: int, current_focus: str, current_campaigns: list):
    """
    Editable calendar focus and campaigns component
    
    Args:
        calendar_id: ID of the calendar to edit
        current_focus: Current focus text
        current_campaigns: List of current campaign names
    
    Returns:
        bool: True if changes were saved
    """
    st.markdown("#### Edit Calendar Details")
    
    new_focus = st.text_input(
        "Monthly Focus:",
        value=current_focus or "",
        help="What is the main focus for this month?"
    )
    
    campaigns_text = "\n".join(current_campaigns) if current_campaigns else ""
    new_campaigns = st.text_area(
        "Major Campaigns (one per line):",
        value=campaigns_text,
        help="List major campaigns or initiatives for this month"
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("💾 Save Changes", use_container_width=True):
            campaigns_list = [c.strip() for c in new_campaigns.split("\n") if c.strip()]
            
            try:
                payload = {
                    "focus": new_focus,
                    "major_campaigns": campaigns_list
                }
                response = requests.put(
                    f"{API_URL}/api/marketing-calendar/calendars/{calendar_id}",
                    json=payload
                )
                
                if response.status_code == 200:
                    st.success("✓ Saved successfully!")
                    return True
                else:
                    st.error(f"Error: {response.status_code}")
                    return False
            except Exception as e:
                st.error(f"Error saving: {str(e)}")
                return False
    
    return False


def activity_creator(calendar_id: int, week_number: int):
    """
    Create new activity component
    
    Args:
        calendar_id: ID of the calendar
        week_number: Week number (1-4)
    
    Returns:
        bool: True if activity was created
    """
    with st.form(key=f"create_activity_week{week_number}", clear_on_submit=True):
        st.markdown(f"**Add Activity to Week {week_number}**")
        
        activity_name = st.text_input(
            "Activity Name:",
            placeholder="e.g., LinkedIn: Industry Insights/Trends"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            day_of_week = st.selectbox(
                "Day of Week:",
                options=["monday", "tuesday", "wednesday", "thursday", "friday"],
                format_func=lambda x: x.title()
            )
        
        submitted = st.form_submit_button("➕ Add Activity", use_container_width=True)
        
        if submitted:
            if not activity_name:
                st.error("Please enter an activity name")
                return False
            
            try:
                payload = {
                    "calendar_id": calendar_id,
                    "week_number": week_number,
                    "activity_name": activity_name,
                    "day_of_week": day_of_week,
                    "order_in_week": 0,  # Will be adjusted by backend
                    "is_completed": False
                }
                
                response = requests.post(
                    f"{API_URL}/api/marketing-calendar/activities/",
                    json=payload
                )
                
                if response.status_code == 200:
                    st.success("✓ Activity created!")
                    return True
                else:
                    st.error(f"Error: {response.status_code}")
                    return False
            except Exception as e:
                st.error(f"Error creating activity: {str(e)}")
                return False
    
    return False


def activity_list_item(activity: dict, edit_mode: bool = False):
    """
    Display single activity list item with completion checkbox
    
    Args:
        activity: Activity dict from API
        edit_mode: Whether to show edit/delete controls
    
    Returns:
        str: Action taken ('toggled', 'updated', 'deleted', None)
    """
    action = None
    
    col1, col2, col3, col4 = st.columns([0.5, 3, 1, 0.5])
    
    with col1:
        # Completion checkbox
        is_complete = activity["is_completed"]
        new_state = st.checkbox(
            "Complete",
            value=is_complete,
            key=f"check_{activity['id']}",
            label_visibility="collapsed"
        )
        
        if new_state != is_complete:
            try:
                response = requests.patch(
                    f"{API_URL}/api/marketing-calendar/activities/{activity['id']}/toggle"
                )
                if response.status_code == 200:
                    action = 'toggled'
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    with col2:
        if edit_mode:
            # Editable name
            new_name = st.text_input(
                "Activity",
                value=activity["activity_name"],
                key=f"name_{activity['id']}",
                label_visibility="collapsed"
            )
            
            if new_name != activity["activity_name"] and st.button("💾", key=f"save_{activity['id']}"):
                try:
                    response = requests.put(
                        f"{API_URL}/api/marketing-calendar/activities/{activity['id']}",
                        json={"activity_name": new_name}
                    )
                    if response.status_code == 200:
                        action = 'updated'
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            # Display only
            if is_complete:
                st.markdown(f"~~{activity['activity_name']}~~")
            else:
                st.markdown(f"**{activity['activity_name']}**")
    
    with col3:
        # Day badge
        day_colors = {
            "monday": "#1f77b4",
            "tuesday": "#ff7f0e",
            "wednesday": "#2ca02c",
            "thursday": "#d62728",
            "friday": "#9467bd"
        }
        color = day_colors.get(activity["day_of_week"], "#7f7f7f")
        
        st.markdown(
            f"<span style='background-color: {color}; color: white; padding: 3px 10px; border-radius: 5px; font-size: 0.85em;'>{activity['day_of_week'].title()}</span>",
            unsafe_allow_html=True
        )
    
    with col4:
        if edit_mode:
            if st.button("🗑️", key=f"del_{activity['id']}"):
                try:
                    response = requests.delete(
                        f"{API_URL}/api/marketing-calendar/activities/{activity['id']}"
                    )
                    if response.status_code == 200:
                        action = 'deleted'
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    return action


def calendar_stats_widget(calendar_id: int):
    """
    Display calendar completion statistics
    
    Args:
        calendar_id: ID of the calendar
    """
    try:
        response = requests.get(
            f"{API_URL}/api/marketing-calendar/calendars/{calendar_id}/stats"
        )
        
        if response.status_code == 200:
            stats = response.json()
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Activities", stats["total_activities"])
            with col2:
                st.metric("Completed", stats["completed_activities"], 
                         delta=f"{stats['completion_percentage']}%")
            with col3:
                st.metric("Pending", stats["pending_activities"])
            with col4:
                progress = stats["completion_percentage"] / 100
                st.progress(progress, text=f"{stats['completion_percentage']}% Complete")
    
    except Exception as e:
        st.error(f"Error loading stats: {str(e)}")