import streamlit as st
import time

# إعدادات الصفحة
st.set_page_config(page_title="HomeFlex: Progress Tracker", page_icon="📈")

# --- قاعدة بيانات التمارين ---
workout_plan = {
    "Day 1: Full Body Awakening": [
        {"name": "Cat-Cow Stretch", "target": 30, "type": "Time", "video": "https://www.youtube.com/watch?v=wiFNA3sqjCb"},
        {"name": "Wall Push-ups", "target": 12, "type": "Reps", "video": "https://www.youtube.com/watch?v=vVfS0vD_Puw"},
        {"name": "Bodyweight Squats", "target": 15, "type": "Reps", "video": "https://www.youtube.com/watch?v=1uPrX7tovfM"},
        {"name": "Classic Plank", "target": 30, "type": "Time", "video": "https://www.youtube.com/watch?v=pSHjTRCQxIw"}
    ],
    "Day 2: Upper Body & Core": [
        {"name": "Dynamic Chest Stretch", "target": 30, "type": "Time", "video": "https://www.youtube.com/watch?v=mGzI60mP_9k"},
        {"name": "Incline Push-ups", "target": 10, "type": "Reps", "video": "https://www.youtube.com/watch?v=33mU_6A8_S0"},
        {"name": "Bird-Dog", "target": 12, "type": "Reps", "video": "https://www.youtube.com/watch?v=2SSTInV6C_c"},
        {"name": "Side Plank", "target": 20, "type": "Time", "video": "https://www.youtube.com/watch?v=N_fJ4Y6v0lE"}
    ],
    "Day 3: Lower Body & Stability": [
        {"name": "Leg Swings", "target": 30, "type": "Time", "video": "https://www.youtube.com/watch?v=vX_Y_V-A7W0"},
        {"name": "Glute Bridges", "target": 15, "type": "Reps", "video": "https://www.youtube.com/watch?v=8bbE6adQTpM"},
        {"name": "Lunges", "target": 10, "type": "Reps", "video": "https://www.youtube.com/watch?v=COKYKgQ8KR0"},
        {"name": "Wall Sit", "target": 30, "type": "Time", "video": "https://www.youtube.com/watch?v=y-wV4Venusw"}
    ],
    "Day 4: Mobility & Posture": [
        {"name": "Shoulder Circles", "target": 30, "type": "Time", "video": "https://www.youtube.com/watch?v=L_6vE_7U3-4"},
        {"name": "Cobra Stretch", "target": 30, "type": "Time", "video": "https://www.youtube.com/watch?v=z21McHHOpAg"},
        {"name": "Child's Pose", "target": 40, "type": "Time", "video": "https://www.youtube.com/watch?v=2vLY7J_V0ps"},
        {"name": "Superman Hold", "target": 10, "type": "Reps", "video": "https://www.youtube.com/watch?v=z6jBReW_SdU"}
    ],
    "Day 5: High Intensity Finish": [
        {"name": "Jumping Jacks", "target": 30, "type": "Time", "video": "https://www.youtube.com/watch?v=iSSAk4XCs_4"},
        {"name": "Mountain Climbers", "target": 20, "type": "Reps", "video": "https://www.youtube.com/watch?v=zT-9L37Re9Y"},
        {"name": "Burpees (Slow)", "target": 8, "type": "Reps", "video": "https://www.youtube.com/watch?v=auQLre_6v0M"},
        {"name": "Final Plank", "target": 45, "type": "Time", "video": "https://www.youtube.com/watch?v=pSHjTRCQxIw"}
    ]
}

if 'current_day' not in st.session_state: st.session_state.current_day = None
if 'ex_idx' not in st.session_state: st.session_state.ex_idx = 0
if 'status' not in st.session_state: st.session_state.status = "SELECT"

def play_audio(url):
    st.components.v1.html(f'<audio autoplay><source src="{url}" type="audio/mpeg"></audio>', height=0)

# --- الواجهة الرئيسية ---
st.title("🏋️‍♂️ HomeFlex Pro Trainer")

# 1. شاشة اختيار اليوم
if st.session_state.status == "SELECT":
    st.subheader("Select your workout day:")
    for day_name, exercises in workout_plan.items():
        # عرض عدد التمارين في كل زر
        btn_label = f"{day_name} ({len(exercises)} Exercises)"
        if st.button(btn_label, use_container_width=True):
            st.session_state.current_day = day_name
            st.session_state.ex_idx = 0
            st.session_state.status = "WORKOUT"
            st.rerun()

# 2. شاشة التمرين
elif st.session_state.status == "WORKOUT":
    day_data = workout_plan[st.session_state.current_day]
    total_ex = len(day_data)
    current_num = st.session_state.ex_idx + 1
    remaining = total_ex - current_num
    ex = day_data[st.session_state.ex_idx]
    
    # فيديو التمرين
    st.video(ex['video'])
    
    # اسم التمرين (English Only)
    st.code(ex['name'], language="text")
    
    # عداد التمارين الرقمي
    st.markdown(f"**Exercise {current_num} of {total_ex}** | `{remaining} remaining`")
    
    st.subheader(f"Target: {ex['target']} {'Seconds' if ex['type'] == 'Time' else 'Reps'}")
    
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
            if st.button("Done ✅"):
                play_audio("https://www.soundjay.com/misc/sounds/bell-ringing-05.mp3")
                st.session_state.status = "REST"
                st.rerun()
                
    with col2:
        if st.button("Skip ⏭️"):
            if st.session_state.ex_idx < total_ex - 1:
                st.session_state.ex_idx += 1
                st.rerun()
            else:
                st.session_state.status = "SELECT"
                st.rerun()

    with col3:
        if st.button("Menu 🏠"):
            st.session_state.status = "SELECT"
            st.rerun()

# 3. شاشة الراحة
elif st.session_state.status == "REST":
    st.subheader("🥤 Rest Time (30s)")
    if st.button("Skip Rest ⏩"):
        day_data = workout_plan[st.session_state.current_day]
        if st.session_state.ex_idx < len(day_data) - 1:
            st.session_state.ex_idx += 1
            st.session_state.status = "WORKOUT"
        else:
            st.session_state.status = "SELECT"
        st.rerun()
        
    p = st.empty()
    for i in range(30, -1, -1):
        p.metric("Get ready...", f"{i}s")
        time.sleep(1)
    
    play_audio("https://www.soundjay.com/misc/sounds/referee-whistle-01.mp3")
    
    day_data = workout_plan[st.session_state.current_day]
    if st.session_state.ex_idx < len(day_data) - 1:
        st.session_state.ex_idx += 1
        st.session_state.status = "WORKOUT"
        st.rerun()
    else:
        st.balloons()
        st.success("Great job! Workout Finished.")
        time.sleep(3)
        st.session_state.status = "SELECT"
        st.rerun()
