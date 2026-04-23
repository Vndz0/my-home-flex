import streamlit as st
import time

# --- APP CONFIG ---
st.set_page_config(page_title="HomeFit - No Equipment", page_icon="💪")

# --- CUSTOM CSS FOR MODERN LOOK ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #007BFF; color: white; }
    .exercise-card { padding: 15px; border-radius: 10px; border: 1px solid #ddd; margin-bottom: 10px; }
    .copy-text { font-size: 0.8em; color: #666; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE (Exercises) ---
WORKOUTS = {
    "Monday: Full Body Intro": [
        {"name": "Standard Push-ups", "desc": "Keep your core tight and back straight.", "reps": "12 Reps"},
        {"name": "Bodyweight Squats", "desc": "Sit back as if into a chair, keep heels down.", "reps": "15 Reps"},
        {"name": "Plank", "desc": "Hold a straight line from head to heels.", "reps": "30 Seconds"},
        {"name": "Lunges", "desc": "Step forward until both knees are at 90 degrees.", "reps": "10 per leg"},
        {"name": "Glute Bridges", "desc": "Lying on back, lift hips toward the ceiling.", "reps": "15 Reps"},
        {"name": "Mountain Climbers", "desc": "Drive knees toward chest rapidly.", "reps": "30 Seconds"},
        {"name": "Bird Dog", "desc": "Opposite arm and leg extension for stability.", "reps": "10 Reps"}
    ],
    "Tuesday: Core & Abs": [
        {"name": "Crunches", "desc": "Lift shoulders off ground using abs.", "reps": "20 Reps"},
        {"name": "Leg Raises", "desc": "Lower legs slowly without touching floor.", "reps": "12 Reps"},
        {"name": "Russian Twists", "desc": "Rotate torso side to side.", "reps": "20 Reps"},
        {"name": "Bicycle Crunches", "desc": "Elbow to opposite knee.", "reps": "20 Reps"},
        {"name": "Flutter Kicks", "desc": "Small, fast leg movements.", "reps": "30 Seconds"},
        {"name": "Side Plank (Left)", "desc": "Balance on one forearm.", "reps": "30 Seconds"},
        {"name": "Side Plank (Right)", "desc": "Balance on the other forearm.", "reps": "30 Seconds"}
    ]
    # Note: You can add more days (Wednesday: Legs, Thursday: Upper Body, etc.)
}

# --- APP HEADER ---
st.title("🏠 HomeFit")
st.subheader("High-Quality Minimalist Training")

# Select Day
day = st.selectbox("Choose your workout day:", list(WORKOUTS.keys()))
exercises = WORKOUTS[day]

# --- PREVIEW SECTION ---
with st.expander("🔍 Preview Exercises (Learn Before Starting)"):
    st.info("Quality > Quantity. Click the name to copy and search on YouTube.")
    for ex in exercises:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{ex['name']}** ({ex['reps']})")
            st.caption(ex['desc'])
        with col2:
            if st.button("Copy Name", key=ex['name']):
                st.code(ex['name']) # Allows easy copy-pasting

st.divider()

# --- WORKOUT SESSION ---
if 'round' not in st.session_state:
    st.session_state.round = 1

st.header(f"Round {st.session_state.round} / 3")
progress = st.progress(0)

# Simulate Workout Flow
if st.button("🏁 Start/Next Exercise"):
    for i, ex in enumerate(exercises):
        # Display Exercise
        st.success(f"**Current: {ex['name']}**")
        st.write(f"Target: {ex['reps']}")
        
        # Progress Bar
        percent_complete = int(((i + 1) / len(exercises)) * 100)
        progress.progress(percent_complete)
        
        # Rest Timer
        with st.empty():
            for seconds in range(15, 0, -1):
                st.write(f"⏳ Rest: {seconds}s before next move...")
                time.sleep(1)
            st.write("🔥 GO!")
    
    if st.session_state.round < 3:
        st.session_state.round += 1
        st.warning(f"Round {st.session_state.round - 1} Complete! Get ready for Round {st.session_state.round}.")
    else:
        st.balloons()
        st.success("Workout Finished! 3 Rounds complete. You are getting stronger!")
        st.session_state.round = 1 # Reset

if st.button("Reset Workout"):
    st.session_state.round = 1
    st.rerun()

# --- FOOTER ---
st.markdown("---")
st.caption("Stay consistent. Movement is medicine.")
