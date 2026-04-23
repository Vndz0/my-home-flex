import streamlit as st
import time

# إعدادات الصفحة
st.set_page_config(page_title="HomeFlex: Circuit Trainer", page_icon="🔁", layout="wide")

# --- قاعدة بيانات التمارين (6 تمارين أساسية قوية) ---
full_body_circuit = [
    {"name": "Warm-up: Jumping Jacks", "target": 45, "type": "Time", "video": "https://www.youtube.com/watch?v=iSSAk4XCs_4"},
    {"name": "Wall Push-ups", "target": 12, "type": "Reps", "video": "https://www.youtube.com/watch?v=vVfS0vD_Puw"},
    {"name": "Air Squats", "target": 15, "type": "Reps", "video": "https://www.youtube.com/watch?v=1uPrX7tovfM"},
    {"name": "Bird-Dog Reach", "target": 12, "type": "Reps", "video": "https://www.youtube.com/watch?v=2SSTInV6C_c"},
    {"name": "Glute Bridges", "target": 15, "type": "Reps", "video": "https://www.youtube.com/watch?v=8bbE6adQTpM"},
    {"name": "Plank Hold", "target": 30, "type": "Time", "video": "https://www.youtube.com/watch?v=pSHjTRCQxIw"}
]

workout_database = {
    "Day 1: Full Body Circuit": full_body_circuit,
    "Day 2: Upper Body & Core": full_body_circuit,
    "Day 3: Lower Body Focus": full_body_circuit,
    "Day 4: Mobility & Strength": full_body_circuit,
    "Day 5: Fat Burner": full_body_circuit
}

# --- إدارة الحالة ---
if 'status' not in st.session_state: st.session_state.status = "SELECT"
if 'current_day' not in st.session_state: st.session_state.current_day = None
if 'ex_idx' not in st.session_state: st.session_state.ex_idx = 0
if 'current_set' not in st.session_state: st.session_state.current_set = 1
if 'total_sets' not in st.session_state: st.session_state.total_sets = 3

def play_audio(url):
    st.components.v1.html(f'<audio autoplay><source src="{url}" type="audio/mpeg"></audio>', height=0)

# --- الواجهة الرئيسية ---
st.title("🔁 HomeFlex Circuit Trainer")

# 1. شاشة اختيار اليوم وعدد الجولات
if st.session_state.status == "SELECT":
    st.header("Step 1: Select Your Day")
    for day in workout_database.keys():
        if st.button(f"📅 {day}", use_container_width=True):
            st.session_state.current_day = day
            st.session_state.status = "PREVIEW"
            st.rerun()

# 2. شاشة المعاينة وتحديد الجولات
elif st.session_state.status == "PREVIEW":
    st.header(f"Preview: {st.session_state.current_day}")
    
    # اختيار عدد الجولات قبل البدء
    st.session_state.total_sets = st.slider("Select number of Rounds (Sets):", 1, 5, 3)
    
    st.write("Review exercises below:")
    day_exercises = workout_database[st.session_state.current_day]
    for idx, ex in enumerate(day_exercises):
        with st.expander(f"{idx+1}. {ex['name']}"):
            st.video(ex['video'])
            st.code(ex['name'], language="text")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚀 Start Circuit Training", use_container_width=True):
            st.session_state.ex_idx = 0
            st.session_state.current_set = 1
            st.session_state.status = "WORKOUT"
            st.rerun()
    with col2:
        if st.button("⬅️ Back to Menu", use_container_width=True):
            st.session_state.status = "SELECT"
            st.rerun()

# 3. شاشة التمرين (التركيز)
elif st.session_state.status == "WORKOUT":
    day_exercises = workout_database[st.session_state.current_day]
    ex = day_exercises[st.session_state.ex_idx]
    
    st.info(f"⭕ Round: {st.session_state.current_set} / {st.session_state.total_sets}")
    st.markdown(f"### Exercise {st.session_state.ex_idx + 1} of {len(day_exercises)}")
    st.title(ex['name'])
    st.code(ex['name'], language="text")
    
    st.metric(label="Target", value=f"{ex['target']} {ex['type']}")
    
    col1, col2 = st.columns(2)
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
            st.session_state.status = "REST"
            st.rerun()

# 4. شاشة الراحة مع منطق التكرار الذكي
elif st.session_state.status == "REST":
    st.subheader("🥤 Rest Interval")
    
    if st.button("Skip Rest ⏩"):
        # منطق الانتقال للتمرين التالي أو الجولة التالية
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
            st.success("All Rounds Complete!")
            time.sleep(3)
            st.session_state.status = "SELECT"
    st.rerun()
