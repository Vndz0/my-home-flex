import streamlit as st
import time

# إعدادات الصفحة
st.set_page_config(page_title="HomeFlex Elite", page_icon="💪", layout="wide")

# --- قاعدة بيانات التمارين المكثفة (مثال ليوم واحد، يمكنك تكرار النمط لبقية الأيام) ---
# قمت بوضع 10 تمارين كمثال لهذا اليوم
full_body_plan = [
    {"name": "Dynamic Neck & Shoulder Warm-up", "target": 45, "type": "Time", "video": "https://www.youtube.com/watch?v=L_6vE_7U3-4"},
    {"name": "Arm Circles", "target": 30, "type": "Time", "video": "https://www.youtube.com/watch?v=1rP_Y_V-A7W0"},
    {"name": "Wall Push-ups", "target": 15, "type": "Reps", "video": "https://www.youtube.com/watch?v=vVfS0vD_Puw"},
    {"name": "Incline Push-ups", "target": 12, "type": "Reps", "video": "https://www.youtube.com/watch?v=33mU_6A8_S0"},
    {"name": "Bodyweight Squats", "target": 20, "type": "Reps", "video": "https://www.youtube.com/watch?v=1uPrX7tovfM"},
    {"name": "Lunges (Alternating)", "target": 16, "type": "Reps", "video": "https://www.youtube.com/watch?v=COKYKgQ8KR0"},
    {"name": "Glute Bridges", "target": 20, "type": "Reps", "video": "https://www.youtube.com/watch?v=8bbE6adQTpM"},
    {"name": "Bird-Dog Hold", "target": 12, "type": "Reps", "video": "https://www.youtube.com/watch?v=2SSTInV6C_c"},
    {"name": "Classic Plank", "target": 45, "type": "Time", "video": "https://www.youtube.com/watch?v=pSHjTRCQxIw"},
    {"name": "Cobra Stretch (Cool Down)", "target": 40, "type": "Time", "video": "https://www.youtube.com/watch?v=z21McHHOpAg"}
]

# محاكاة لـ 5 أيام (يمكنك ملء كل يوم بـ 15 تمرين بنفس الطريقة)
workout_database = {
    "Day 1: Full Body Power": full_body_plan,
    "Day 2: Upper Body Focus": full_body_plan, # كرر نفس الهيكل مع تغيير التمارين
    "Day 3: Lower Body Blast": full_body_plan,
    "Day 4: Core & Stability": full_body_plan,
    "Day 5: Total Shred": full_body_plan
}

# --- إدارة الحالة ---
if 'status' not in st.session_state: st.session_state.status = "SELECT"
if 'current_day' not in st.session_state: st.session_state.current_day = None
if 'ex_idx' not in st.session_state: st.session_state.ex_idx = 0

def play_audio(url):
    st.components.v1.html(f'<audio autoplay><source src="{url}" type="audio/mpeg"></audio>', height=0)

# --- الواجهة ---
st.title("🏋️‍♂️ HomeFlex Elite Trainer")

# 1. شاشة اختيار اليوم
if st.session_state.status == "SELECT":
    st.header("Select Your Training Day")
    cols = st.columns(1)
    for day in workout_database.keys():
        if st.button(f"📅 {day}", use_container_width=True):
            st.session_state.current_day = day
            st.session_state.status = "PREVIEW"
            st.rerun()

# 2. شاشة المعاينة (Preview)
elif st.session_state.status == "PREVIEW":
    st.header(f"Preview: {st.session_state.current_day}")
    st.write("Click on any exercise to watch the tutorial video:")
    
    day_exercises = workout_database[st.session_state.current_day]
    
    for idx, ex in enumerate(day_exercises):
        with st.expander(f"{idx+1}. {ex['name']} ({ex['target']} {ex['type']})"):
            st.video(ex['video'])
            st.code(ex['name'], language="text")
            st.write("Tutorial Mode: Watch carefully before you start.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚀 Start Workout Now", use_container_width=True):
            st.session_state.ex_idx = 0
            st.session_state.status = "WORKOUT"
            st.rerun()
    with col2:
        if st.button("⬅️ Back to Menu", use_container_width=True):
            st.session_state.status = "SELECT"
            st.rerun()

# 3. شاشة التمرين الفعلي (Focus Mode - لا فيديوهات هنا)
elif st.session_state.status == "WORKOUT":
    day_exercises = workout_database[st.session_state.current_day]
    ex = day_exercises[st.session_state.ex_idx]
    
    st.markdown(f"### Exercise {st.session_state.ex_idx + 1} of {len(day_exercises)}")
    st.title(ex['name'])
    st.code(ex['name'], language="text") # لسهولة النسخ
    
    st.metric(label="Target", value=f"{ex['target']} {ex['type']}")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if ex['type'] == "Time":
            if st.button("⏱️ Start/Restart"):
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
            if st.session_state.ex_idx < len(day_exercises) - 1:
                st.session_state.ex_idx += 1
                st.rerun()
            else:
                st.session_state.status = "SELECT"
                st.rerun()
    
    with col3:
        if st.button("Stop 🛑"):
            st.session_state.status = "SELECT"
            st.rerun()

    st.progress((st.session_state.ex_idx + 1) / len(day_exercises))

# 4. شاشة الراحة
elif st.session_state.status == "REST":
    st.subheader("🥤 Rest Interval")
    if st.button("Skip Rest ⏩"):
        day_exercises = workout_database[st.session_state.current_day]
        if st.session_state.ex_idx < len(day_exercises) - 1:
            st.session_state.ex_idx += 1
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
        st.rerun()
    else:
        st.balloons()
        st.success("Workout Complete!")
        time.sleep(3)
        st.session_state.status = "SELECT"
        st.rerun()
