import streamlit as st
import time

# إعدادات الصفحة
st.set_page_config(page_title="HomeFlex: 20-Min Split", page_icon="⚡", layout="wide")

# --- قاعدة بيانات التمارين (تقسيم عضلي احترافي) ---
workout_database = {
    "Day 1: Arms (Biceps & Triceps)": [
        {"name": "Wall Bicep Curls (No weights)", "target": 15, "type": "Reps", "video": "https://www.youtube.com/watch?v=iOaT_u6v-s8"},
        {"name": "Tricep Wall Dips", "target": 12, "type": "Reps", "video": "https://www.youtube.com/watch?v=vVfS0vD_Puw"},
        {"name": "Diamond Wall Push-ups", "target": 10, "type": "Reps", "video": "https://www.youtube.com/watch?v=33mU_6A8_S0"},
        {"name": "Arm Circles (Clockwise)", "target": 30, "type": "Time", "video": "https://www.youtube.com/watch?v=1rP_Y_V-A7W0"},
        {"name": "Forearm Plank Pulse", "target": 20, "type": "Reps", "video": "https://www.youtube.com/watch?v=pSHjTRCQxIw"}
    ],
    "Day 2: Legs (Quads & Glutes)": [
        {"name": "Wall Sit", "target": 30, "type": "Time", "video": "https://www.youtube.com/watch?v=y-wV4Venusw"},
        {"name": "Chair Squats", "target": 15, "type": "Reps", "video": "https://www.youtube.com/watch?v=1uPrX7tovfM"},
        {"name": "Glute Bridges", "target": 15, "type": "Reps", "video": "https://www.youtube.com/watch?v=8bbE6adQTpM"},
        {"name": "Alternating Forward Lunges", "target": 12, "type": "Reps", "video": "https://www.youtube.com/watch?v=COKYKgQ8KR0"},
        {"name": "Calf Raises", "target": 20, "type": "Reps", "video": "https://www.youtube.com/watch?v=gwLzBJYoWlU"}
    ],
    "Day 3: Back & Neck (Posture)": [
        {"name": "Bird-Dog (Back focus)", "target": 12, "type": "Reps", "video": "https://www.youtube.com/watch?v=2SSTInV6C_c"},
        {"name": "Cobra Stretch Hold", "target": 30, "type": "Time", "video": "https://www.youtube.com/watch?v=z21McHHOpAg"},
        {"name": "Shoulder Blade Squeezes", "target": 15, "type": "Reps", "video": "https://www.youtube.com/watch?v=L_6vE_7U3-4"},
        {"name": "Superman Hold", "target": 10, "type": "Reps", "video": "https://www.youtube.com/watch?v=z6jBReW_SdU"},
        {"name": "Neck Range Motion Stretch", "target": 40, "type": "Time", "video": "https://www.youtube.com/watch?v=wiFNA3sqjCb"}
    ],
    "Day 4: Chest (Push Power)": [
        {"name": "Standard Wall Push-ups", "target": 15, "type": "Reps", "video": "https://www.youtube.com/watch?v=vVfS0vD_Puw"},
        {"name": "Wide Grip Wall Push-ups", "target": 12, "type": "Reps", "video": "https://www.youtube.com/watch?v=33mU_6A8_S0"},
        {"name": "Chest Expansion Stretch", "target": 30, "type": "Time", "video": "https://www.youtube.com/watch?v=mGzI60mP_9k"},
        {"name": "Slow Dynamic Push-offs", "target": 10, "type": "Reps", "video": "https://www.youtube.com/watch?v=pSHjTRCQxIw"},
        {"name": "Isometric Chest Press", "target": 30, "type": "Time", "video": "https://www.youtube.com/watch?v=wiFNA3sqjCb"}
    ],
    "Day 5: Abs (Core Stability)": [
        {"name": "High Plank Hold", "target": 40, "type": "Time", "video": "https://www.youtube.com/watch?v=pSHjTRCQxIw"},
        {"name": "Mountain Climbers (Slow)", "target": 20, "type": "Reps", "video": "https://www.youtube.com/watch?v=zT-9L37Re9Y"},
        {"name": "Standing Knee to Elbow", "target": 16, "type": "Reps", "video": "https://www.youtube.com/watch?v=iSSAk4XCs_4"},
        {"name": "Dead Bug Hold", "target": 12, "type": "Reps", "video": "https://www.youtube.com/watch?v=2SSTInV6C_c"},
        {"name": "Child's Pose Recovery", "target": 45, "type": "Time", "video": "https://www.youtube.com/watch?v=2vLY7J_V0ps"}
    ]
}

# --- إدارة الحالة (Session State) ---
if 'status' not in st.session_state: st.session_state.status = "SELECT"
if 'current_day' not in st.session_state: st.session_state.current_day = None
if 'ex_idx' not in st.session_state: st.session_state.ex_idx = 0
if 'current_set' not in st.session_state: st.session_state.current_set = 1
if 'total_sets' not in st.session_state: st.session_state.total_sets = 3

def play_audio(url):
    st.components.v1.html(f'<audio autoplay><source src="{url}" type="audio/mpeg"></audio>', height=0)

# --- واجهة التطبيق ---
st.title("⚡ HomeFlex: 20-Min Daily Trainer")

# 1. شاشة اختيار اليوم
if st.session_state.status == "SELECT":
    st.header("Step 1: Select Today's Workout")
    for day in workout_database.keys():
        if st.button(f"📅 {day}", use_container_width=True):
            st.session_state.current_day = day
            st.session_state.status = "PREVIEW"
            st.rerun()

# 2. شاشة المعاينة (Preview)
elif st.session_state.status == "PREVIEW":
    st.header(f"Preview: {st.session_state.current_day}")
    st.session_state.total_sets = st.slider("Select Rounds (Default 3 is recommended for 20 mins):", 1, 5, 3)
    
    st.write("Click to learn the technique:")
    day_exercises = workout_database[st.session_state.current_day]
    for idx, ex in enumerate(day_exercises):
        with st.expander(f"{idx+1}. {ex['name']}"):
            st.video(ex['video'])
            st.code(ex['name'], language="text")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚀 Start Workout", use_container_width=True):
            st.session_state.ex_idx = 0
            st.session_state.current_set = 1
            st.session_state.status = "WORKOUT"
            st.rerun()
    with col2:
        if st.button("⬅️ Menu", use_container_width=True):
            st.session_state.status = "SELECT"
            st.rerun()

# 3. شاشة التمرين (Workout Mode)
elif st.session_state.status == "WORKOUT":
    day_exercises = workout_database[st.session_state.current_day]
    ex = day_exercises[st.session_state.ex_idx]
    
    st.warning(f"⭕ Round: {st.session_state.current_set} / {st.session_state.total_sets}")
    st.markdown(f"### Exercise {st.session_state.ex_idx + 1} of {len(day_exercises)}")
    st.title(ex['name'])
    st.code(ex['name'], language="text") # لسهولة النسخ
    
    st.metric(label="Target Goal", value=f"{ex['target']} {ex['type']}")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if ex['type'] == "Time":
            if st.button("⏱️ Start Timer"):
                t_place = st.empty()
                for s in range(ex['target'], -1, -1):
                    t_place.header(f"⏳ {s}s")
                    time.sleep(1)
                play_audio("https://www.soundjay.com/misc/sounds/bell-ringing-05.mp3")
                st.session_state.status = "REST"
                st.rerun()
        else:
            if st.button("Next (Done) ✅", use_container_width=True):
                play_audio("https://www.soundjay.com/misc/sounds/bell-ringing-05.mp3")
                st.session_state.status = "REST"
                st.rerun()

    with col2:
        if st.button("Skip ⏭️"):
            st.session_state.status = "REST"
            st.rerun()
    
    with col3:
        if st.button("Stop 🛑"):
            st.session_state.status = "SELECT"
            st.rerun()

# 4. شاشة الراحة (Rest Interval)
elif st.session_state.status == "REST":
    st.subheader("🥤 Rest Interval (30s)")
    if st.button("Skip Rest ⏩"):
        day_exercises = workout_database[st.session_state.current_day]
        if st.session_state.ex_idx < len(day_exercises) - 1:
            st.session_state.ex_idx += 1
            st.session_state.status = "WORKOUT"
        else:
            if st.session_state.current_set < st.session_state.total_sets:
                st.session_state.current_set += 1
                st.session_state.ex_idx = 0
                st.session_state.status = "WORKOUT"
            else:
                st.session_state.status = "SELECT"
        st.rerun()

    p = st.empty()
    for i in range(30, -1, -1):
        p.metric("Get Ready...", f"{i}s")
        time.sleep(1)
    
    play_audio("https://www.soundjay.com/misc/sounds/referee-whistle-01.mp3")
    
    day_exercises = workout_database[st.session_state.current_day]
    if st.session_state.ex_idx < len(day_exercises) - 1:
        st.session_state.ex_idx += 1
        st.session_state.status = "WORKOUT"
    else:
        if st.session_state.current_set < st.session_state.total_sets:
            st.session_state.current_set += 1
            st.session_state.ex_idx = 0
            st.session_state.status = "WORKOUT"
        else:
            st.balloons()
            st.success("20-Minute Session Complete!")
            time.sleep(3)
            st.session_state.status = "SELECT"
    st.rerun()
