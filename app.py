import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date
from supabase import create_client, Client

st.set_page_config(
    page_title="Mood Tracker",
    page_icon="😊",
    layout="wide"
)

@st.cache_resource
def get_supabase_client():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

def save_mood_entry(mood_data):
    try:
        supabase = get_supabase_client()
        today = datetime.now().date().isoformat()
        
        # Check if an entry already exists for today
        existing_entry = get_existing_entry_for_date(today)
        
        if existing_entry:
            # Update existing entry
            result = supabase.schema('moodlogs').table('mood_entries').update(mood_data).eq('id', existing_entry['id']).execute()
            return existing_entry['id'] if result.data else None
        else:
            # Create new entry
            mood_data['created_at'] = datetime.now().isoformat()
            result = supabase.schema('moodlogs').table('mood_entries').insert(mood_data).execute()
            return result.data[0]['id'] if result.data else None
    except Exception as e:
        st.error(f"Database error: {e}")
        return None

def get_mood_history():
    try:
        supabase = get_supabase_client()
        result = supabase.schema('moodlogs').table('mood_entries').select("*").order('created_at', desc=True).execute()
        return result.data
    except Exception as e:
        st.error(f"Error fetching history: {e}")
        return []

def update_mood_entry(entry_id, updated_data):
    try:
        supabase = get_supabase_client()
        result = supabase.schema('moodlogs').table('mood_entries').update(updated_data).eq('id', entry_id).execute()
        return result.data
    except Exception as e:
        st.error(f"Error updating entry: {e}")
        return None

def delete_mood_entry(entry_id):
    try:
        supabase = get_supabase_client()
        result = supabase.schema('moodlogs').table('mood_entries').delete().eq('id', entry_id).execute()
        return result.data
    except Exception as e:
        st.error(f"Error deleting entry: {e}")
        return None

def get_existing_entry_for_date(target_date):
    try:
        supabase = get_supabase_client()
        # Get entries for the target date (comparing just the date part)
        result = supabase.schema('moodlogs').table('mood_entries').select("*").gte('created_at', f"{target_date}T00:00:00").lt('created_at', f"{target_date}T23:59:59").execute()
        return result.data[0] if result.data else None
    except Exception as e:
        st.error(f"Error checking for existing entry: {e}")
        return None


st.title("Mood Diary Tracker")

def is_authorized_user(submitted_password):
    expected_password = st.secrets.get('SUPABASE_PASSWORD', '')
    return submitted_password == expected_password

# Check if user has entered password
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    tab1, tab2, tab3, tab4 = st.tabs(["🔐 Login", "📝 Enter Mood", "📊 Historic Entries", "📈 Dashboard"])
    
    with tab1:
        st.header("Welcome to Mood Diary Tracker")
        st.write("Please enter your password to access your mood tracking features.")
        st.write("This app helps you track and analyze your daily mood variables including:")
        st.markdown("""
        - Emotional states (loneliness, fulfillment, excitement, anger, depression)
        - Energy levels (tiredness, energy, sleepiness)
        - Mental states (mania, creativity)
        - Creative inspiration (song ideas, essay ideas)
        """)
        
        password = st.text_input("Password:", type="password", key="password_input")
        
        if st.button("Log in", type="primary"):
            if is_authorized_user(password):
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("🚫 Access Denied - Incorrect password")
    
    with tab2:
        st.info("🔒 Please log in to access mood entry features")
    
    with tab3:
        st.info("🔒 Please log in to view your historic entries")
    
    with tab4:
        st.info("🔒 Please log in to access your dashboard")

else:
    st.write("Welcome! You are authenticated.")
    
    # User is verified, show full app
    tab1, tab2, tab3 = st.tabs(["📝 Enter Mood", "📊 Historic Entries", "📈 Dashboard"])

    with tab1:
        st.header("Enter Your Mood Variables")
        
        col1, col2 = st.columns(2)
        
        with col1:
            loneliness = st.number_input("Loneliness", min_value=0, value=3, step=1)
            fulfillment = st.number_input("Fulfillment", min_value=0, value=3, step=1)
            tiredness = st.number_input("Tiredness", min_value=0, value=3, step=1)
            energy_levels = st.number_input("Energy Levels", min_value=0, value=3, step=1)
            excitement = st.number_input("Excitement", min_value=0, value=3, step=1)
            sleepiness = st.number_input("Sleepiness", min_value=0, value=3, step=1)
        
        with col2:
            anger = st.number_input("Anger", min_value=0, value=3, step=1)
            depression = st.number_input("Depression", min_value=0, value=3, step=1)
            mania = st.number_input("Mania", min_value=0, value=3, step=1)
            creativity = st.number_input("Creativity", min_value=0, value=3, step=1)
            song_ideas = st.number_input("Song Ideas", min_value=0, value=0, step=1)
            essay_ideas = st.number_input("Essay Ideas", min_value=0, value=0, step=1)
        
        if st.button("Save Entry", type="primary"):
            mood_data = {
                "loneliness": int(loneliness),
                "fulfillment": int(fulfillment),
                "tiredness": int(tiredness),
                "energy_levels": int(energy_levels),
                "excitement": int(excitement),
                "sleepiness": int(sleepiness),
                "anger": int(anger),
                "depression": int(depression),
                "mania": int(mania),
                "creativity": int(creativity),
                "song_ideas": int(song_ideas),
                "essay_ideas": int(essay_ideas)
            }
            
            today = datetime.now().date().isoformat()
            existing_entry = get_existing_entry_for_date(today)
            entry_id = save_mood_entry(mood_data)
            if entry_id:
                if existing_entry:
                    st.success(f"Entry updated successfully! ID: {entry_id}")
                else:
                    st.success(f"Entry saved successfully! ID: {entry_id}")
            else:
                st.error("Failed to save entry")

    with tab2:
        st.header("Historic Entries")
        
        mood_history = get_mood_history()
        
        if mood_history:
            # Convert to DataFrame for display
            df = pd.DataFrame(mood_history)
            if 'created_at' in df.columns:
                df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%Y-%m-%d %H:%M')
            
            # Make dataframe editable
            edited_df = st.data_editor(
                df, 
                key="mood_history_editor",
                use_container_width=True,
                disabled=["id", "created_at"]  # Don't allow editing ID or timestamp
            )
            
            col_stats, col_delete = st.columns([3, 1])
            
            with col_stats:
                st.write(f"Total entries: {len(mood_history)}")
            
            with col_delete:
                # Delete functionality
                if len(df) > 0:
                    delete_options = [f"ID {row['id']} - {row['created_at']}" for _, row in df.iterrows()]
                    selected_delete = st.selectbox(
                        "Select entry to delete:",
                        ["Select an entry..."] + delete_options,
                        key="delete_selector"
                    )
                    
                    if selected_delete != "Select an entry..." and st.button("🗑️ Delete Entry", type="secondary"):
                        # Extract ID from selection
                        entry_id = int(selected_delete.split(" ")[1])
                        
                        if delete_mood_entry(entry_id):
                            st.success("Entry deleted successfully!")
                            st.rerun()
                        else:
                            st.error("Failed to delete entry")
            
            # Check for changes and update database
            if "mood_history_editor" in st.session_state:
                changes = st.session_state["mood_history_editor"]
                
                if changes.get("edited_rows"):
                    st.write("**Changes detected:**")
                    
                    if st.button("Save Changes", type="primary"):
                        success_count = 0
                        for row_index, row_changes in changes["edited_rows"].items():
                            entry_id = df.iloc[row_index]['id']
                            
                            # Only include mood variable fields for update
                            mood_fields = ['loneliness', 'fulfillment', 'tiredness', 'energy_levels', 
                                          'excitement', 'sleepiness', 'anger', 'depression', 
                                          'mania', 'creativity', 'song_ideas', 'essay_ideas']
                            
                            update_data = {field: value for field, value in row_changes.items() 
                                         if field in mood_fields}
                            
                            if update_data and update_mood_entry(entry_id, update_data):
                                success_count += 1
                        
                        if success_count > 0:
                            st.success(f"Successfully updated {success_count} entries!")
                            st.rerun()  # Refresh to show updated data
                        else:
                            st.error("Failed to update entries")
        else:
            st.info("No mood entries found. Add your first entry in the Enter Mood tab!")
    
    with tab3:
        st.header("Mood Analytics Dashboard")
        
        # Time period selector
        period_options = {
            "Last 7 days": 7,
            "Last 30 days": 30,
            "Last 90 days": 90
        }
        
        selected_period = st.selectbox(
            "Select time period:",
            options=list(period_options.keys()),
            index=0  # Default to 7 days
        )
        
        days_back = period_options[selected_period]
        
        mood_history = get_mood_history()
        
        if mood_history and len(mood_history) > 0:
            # Convert to DataFrame for analysis
            df = pd.DataFrame(mood_history)
            df['created_at'] = pd.to_datetime(df['created_at'])
            df['date'] = df['created_at'].dt.date
            
            # Filter data based on selected period
            cutoff_date = pd.Timestamp.now(tz='UTC') - pd.Timedelta(days=days_back)
            # Ensure created_at is timezone-aware
            if df['created_at'].dt.tz is None:
                df['created_at'] = df['created_at'].dt.tz_localize('UTC')
            df = df[df['created_at'] >= cutoff_date]
            
            # Sort by date for proper time series
            df = df.sort_values('created_at')
            
            # Define mood categories
            emotional_vars = ['loneliness', 'fulfillment', 'excitement', 'anger', 'depression']
            energy_vars = ['tiredness', 'energy_levels', 'sleepiness']
            mental_vars = ['mania', 'creativity']
            creative_vars = ['song_ideas', 'essay_ideas']
            
            # Summary Statistics - Individual Averages
            st.subheader(f"📊 Average Mood Variables ({selected_period})")
            
            if len(df) > 0:
                # Create columns for all 12 measurements
                col1, col2, col3, col4 = st.columns(4)
                
                all_vars = emotional_vars + energy_vars + mental_vars + creative_vars
                
                for i, var in enumerate(all_vars):
                    col = [col1, col2, col3, col4][i % 4]
                    with col:
                        avg_val = df[var].mean()
                        # Format variable name for display
                        display_name = var.replace('_', ' ').title()
                        st.metric(display_name, f"{avg_val:.1f}")
            else:
                st.info(f"No entries found for {selected_period.lower()}")
            
            # Time Series Charts
            st.subheader("📈 Mood Trends Over Time")
            
            if len(df) > 0:
                # Emotional states over time
                fig_emotional = px.line(
                    df, 
                    x='date', 
                    y=emotional_vars,
                    title="Emotional States Over Time",
                    labels={'value': 'Mood Level', 'date': 'Date'}
                )
                fig_emotional.update_layout(height=400)
                fig_emotional.update_xaxes(tickformat='%Y-%m-%d')
                st.plotly_chart(fig_emotional, use_container_width=True)
                
                # Creative output over time
                if df[creative_vars].sum().sum() > 0:
                    fig_creative = px.bar(
                        df, 
                        x='date', 
                        y=creative_vars,
                        title="Creative Ideas Over Time",
                        labels={'value': 'Number of Ideas', 'date': 'Date'}
                    )
                    fig_creative.update_layout(height=400)
                    fig_creative.update_xaxes(tickformat='%Y-%m-%d')
                    st.plotly_chart(fig_creative, use_container_width=True)
            
                # Correlation Analysis
                st.subheader("🔗 Mood Correlations")
                
                # Calculate correlations for mood variables only (exclude timestamps and IDs)
                mood_cols = emotional_vars + energy_vars + mental_vars + creative_vars
                corr_matrix = df[mood_cols].corr()
                
                # Create correlation heatmap
                fig_corr = px.imshow(
                    corr_matrix,
                    title="Mood Variable Correlations",
                    color_continuous_scale="RdBu",
                    aspect="auto"
                )
                fig_corr.update_layout(height=600)
                st.plotly_chart(fig_corr, use_container_width=True)
                
        else:
            st.info("No data available for dashboard. Add some mood entries first!")
