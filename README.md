# Mood Diary Tracker 😊

A comprehensive Streamlit-based mood tracking application with Supabase backend integration for personal mental health monitoring and analysis.

## Features

### 🔐 **Authentication**
- Simple password-based authentication system
- Secure access to personal mood data

### 📝 **Mood Entry**
- Track 12 mood variables with numeric inputs:
  - **Emotional States**: Loneliness, Fulfillment, Excitement, Anger, Depression
  - **Energy Levels**: Tiredness, Energy Levels, Sleepiness
  - **Mental States**: Mania, Creativity
  - **Creative Inspiration**: Song Ideas, Essay Ideas
- Default values set to 3 (neutral) for mood variables, 0 for creative ideas
- Real-time data saving to Supabase database

### 📊 **Historic Entries**
- View all past mood entries in an interactive table
- **Editable Records**: Directly edit mood values in the table
- **Delete Functionality**: Remove unwanted entries with dropdown selection
- **Auto-sync**: Changes immediately saved to database
- Formatted timestamps for easy reference

### 💾 **Data Storage**
- **Supabase Integration**: PostgreSQL backend with real-time sync
- **Secure Schema**: Data stored in `moodlogs.mood_entries` table
- **User Tracking**: Entries include timestamps and user identification
- **Data Persistence**: All changes instantly reflected in database

## Tech Stack

- **Frontend**: Streamlit
- **Backend**: Supabase (PostgreSQL)
- **Data Visualization**: Pandas, Plotly
- **Authentication**: Custom password-based system
- **Database**: PostgreSQL with Supabase REST API

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd mood-diary
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Supabase**:
   - Create a Supabase project
   - Set up the database schema:
   ```sql
   CREATE SCHEMA IF NOT EXISTS moodlogs;
   
   CREATE TABLE moodlogs.mood_entries (
       id BIGSERIAL PRIMARY KEY,
       loneliness INTEGER NOT NULL DEFAULT 0,
       fulfillment INTEGER NOT NULL DEFAULT 0,
       tiredness INTEGER NOT NULL DEFAULT 0,
       energy_levels INTEGER NOT NULL DEFAULT 0,
       excitement INTEGER NOT NULL DEFAULT 0,
       sleepiness INTEGER NOT NULL DEFAULT 0,
       anger INTEGER NOT NULL DEFAULT 0,
       depression INTEGER NOT NULL DEFAULT 0,
       mania INTEGER NOT NULL DEFAULT 0,
       creativity INTEGER NOT NULL DEFAULT 0,
       song_ideas INTEGER NOT NULL DEFAULT 0,
       essay_ideas INTEGER NOT NULL DEFAULT 0,
       created_at TIMESTAMPTZ DEFAULT NOW()
   );
   ```

4. **Create secrets configuration**:
   ```bash
   mkdir -p .streamlit
   ```
   
   Create `.streamlit/secrets.toml`:
   ```toml
   SUPABASE_PASSWORD = "your-app-password"
   SUPABASE_URL = "https://your-project.supabase.co"
   SUPABASE_KEY = "your-supabase-anon-key"
   ```

5. **Run the application**:
   ```bash
   streamlit run app.py
   ```

## Usage

1. **Login**: Enter your configured password to access the app
2. **Track Mood**: Use the "Enter Mood" tab to log daily mood variables
3. **Review History**: View and edit past entries in "Historic Entries" tab
4. **Delete Records**: Use the dropdown to remove unwanted entries

## Configuration

The app uses Streamlit's secrets management for configuration:
- `SUPABASE_PASSWORD`: App authentication password
- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_KEY`: Your Supabase anon/public key

## Database Schema

The mood entries are stored with the following structure:
- `id`: Auto-incrementing primary key
- `loneliness` through `essay_ideas`: Integer mood variables
- `created_at`: Timestamp of entry creation

## Contributing

This is a personal mood tracking application. Feel free to fork and adapt for your own use.

## License

This project is for personal use.