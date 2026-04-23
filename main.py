import streamlit as st
import time

# إعدادات الصفحة
st.set_page_config(page_title="HomeFlex Pro: Custom Split", page_icon="⚡", layout="wide")

# --- قاعدة بيانات التمارين مع البدائل والإحماء ---
workout_database = {
    "Day 1: Arms (Biceps & Triceps)": {
        "warmup": {"name": "Arm Circles & Wrist Rotations", "target": 45, "type": "Time", "video": "https://www.youtube.com/watch?v=1rP_Y_V-A7W0"},
        "exercises": [
            {"name": "Wall Bicep Curls", "target": 15, "type": "Reps", "video": "https://www.youtube.com/watch?v=iOaT_u6v-s8", "alts": ["Towel Curls", "Door Frame Rows"]},
            {"name": "Tricep Wall Dips", "target": 12, "type": "Reps", "video": "https://www.youtube.com/watch?v=vVfS0vD_Puw", "alts": ["Overhead Arm Extension", "Chair Dips"]},
            {"name": "Diamond Wall Push-ups", "target": 10, "type": "Reps", "video": "https://www.youtube.com/watch?v=33mU_6A8_S0", "alts": ["Close Grip Push-offs", "Plank Shoulder Taps"]}
        ]
    },
    "Day 2: Legs (Quads & Glutes)": {
        "warmup": {"name": "Marching in Place", "target": 60, "type": "Time", "video": "https://www.youtube.com/watch?v=vX_Y_V-A7W0"},
        "exercises": [
            {"name": "Wall Sit", "target": 30, "type": "Time", "video": "https://www.youtube.com/watch?v=y-wV4Venusw", "alts": ["Statue Hold", "Glute Bridge Hold"]},
            {"name": "Chair Squats", "target": 15, "type": "Reps", "video": "https://www.youtube.com/watch?v=1uPrX7tovfM", "alts": ["Sumo Squats", "Step-ups"]},
            {"name": "Forward Lunges", "target": 12, "type": "Reps", "video": "https://www.youtube.com/watch?v=COKYKgQ8KR0", "alts": ["Side Lunges", "Reverse Lunges"]}
        ]
    },
    "Day 3: Back & Neck (Posture)": {
        "warmup": {"name": "Cat-Cow Stretch", "target": 45, "type": "Time", "video": "https://www.youtube.com/watch?v=wiFNA3sqjCb"},
        "exercises": [
            {"name": "Bird-Dog", "target": 12, "type": "Reps", "video": "https://www.youtube.com/watch?v=2SSTInV6C_c", "alts": ["Dead Bug", "Prone Y-Raise"]},
            {"name": "Cobra Stretch", "target": 30, "type": "Time", "video": "https://www.youtube.com/watch?v=z21McHHOpAg", "alts": ["Sphinx Pose", "Wall Angels"]},
            {"name": "Shoulder Squeezes", "target": 15, "type": "Reps", "video": "https://www.youtube.com/watch?v=L_6vE_7U3-4", "alts": ["Scapular Push-ups", "Wall Pull-aparts"]}
        ]
    },
    "Day 4: Chest (Push Power)": {
        "warmup": {"name": "Chest Expansions", "target": 45, "type": "Time", "video": "https://www.youtube.com/watch?v=mGzI60mP_9k"},
        "exercises": [
            {"name": "Standard Wall Push-ups", "target": 15, "type": "Reps", "video": "https://www.youtube.com/watch?v=vVfS0vD_Puw", "alts": ["Incline Bench Push-ups", "Knee Push-ups"]},
            {"name": "Wide Grip Push-ups", "target": 12, "type": "Reps", "video": "https://www.youtube.com/watch?v=33mU_6A8_S0", "alts": ["Staggered Push-ups", "Chest Squeeze Press"]}
        ]
    },
    "Day 5: Abs (Core Stability)": {
        "warmup": {"name": "Torso Twists", "target": 45, "type": "Time", "video": "https://www.youtube.com/watch?v=iSSAk4XCs_4"},
        "exercises": [
            {"name": "High Plank Hold", "target": 40, "type": "Time", "video": "https://www.youtube.com/watch?v=pSHjTRCQxIw", "alts": ["Forearm Plank", "Bear Crawl Hold"]},
            {"name": "Mountain Climbers", "target": 20, "type": "Reps", "video": "https://www.youtube.com/watch?v=zT-9L37Re9Y", "alts": ["Bicycle Crunches", "Knee to Chest"]}
        ]
    }
}

# --- إدارة الحالة ---
if 'status' not in st.session_state: st.session_state.status = "SELECT"
if 'current_day' not in st.session_state: st.session_state.current_day = None
if 'ex_idx' not in st.session_state: st.session_state.ex_idx = 0
if 'current_set' not in st.session_state: st.session_state.current_set = 1
if 'total_sets' not in st.session_state: st.session_state.total_sets = 3
if 'custom_plan' not in st.session_state: st.session_state.custom_plan = []

def play_audio(url):
    st.components.v1.html(f'<audio autoplay><source src="{url}" type="audio/mpeg"></audio>', height=0)

# --- الواجهة ---
st.title("⚡ HomeFlex Elite: Customized Split")

if st.session_state.status == "SELECT":
    st.header("Step 1: Choose Your Training Day")
    for day in workout_database.keys():
        if st.button(f"📅 {day}", use_container_width=True):
            st.session_state.current_day = day
            # تحويل اليوم المختار لخطة قابلة للتعديل
            day_data = workout_database[day]
            st.session_state.custom_plan = [day_data['warmup']] + [ex.copy() for ex in day_data['exercises']]
            st.session_state.status = "PREVIEW"
            st.rerun()

elif st.session_state.status == "PREVIEW":
    st.header(f"Preview: {st.session_state.current_day}")
    st.session_state.total_sets = st.slider("Select Rounds (Sets):", 1, 5, 3)
    
    st.write("---")
    st.subheader("Customize Your Routine:")
    
    for i, ex in enumerate(st.session_state.custom_plan):
        with st.expander(f"{'Warm-up' if i==0 else 'Ex '+str(i)}: {ex['name']}"):
            if 'video' in ex: st.video(ex['video'])
            st.code(ex['name'], language="text")
            
            # خيار تبديل التمرين إذا لم يكن تمرين إحماء وله بدائل
            if i > 0 and 'alts' in ex:
                alt_choice = st.radio(f"Replace {ex['name']} with:", [ex['name']] + ex['alts'], key=f"alt_{i}")
                if alt_choice != ex['name']:
                    ex['name'] = alt_choice
                    # ملاحظة: الفيديو سيبقى للأصلي كمرجع تقني عام، لكن الاسم سيتغير
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚀 Start Personalized Workout", use_container_width=True):
            st.session_state.ex_idx = 0
            st.session_state.current_set = 1
            st.session_state.status = "WORKOUT"
            st.rerun()
    with col2:
        if st.button("⬅️ Back", use_container_width=True):
            st.session_state.status = "SELECT"
            st.rerun()

elif st.session_state.status == "WORKOUT":
    ex = st.session_state.custom_plan[st.session_state.ex_idx]
    
    st.warning(f"⭕ Set: {st.session_state.current_set} / {st.session_state.total_sets}")
    st.title(ex['name'])
    st.code(ex['name'], language="text")
    st.metric("Goal", f"{ex['target']} {ex['type']}")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if ex['type'] == "Time":
            if st.button("⏱️ Start"):
                p = st.empty()
                for s in range(ex['target'], -1, -1):
                    p.header(f"⏳ {s}s")
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
            st.session_state.status = "REST"
            st.rerun()
    with col3:
        if st.button("Stop 🛑"):
            st.session_state.status = "SELECT"
            st.rerun()

elif st.session_state.status == "REST":
    st.subheader("🥤 Rest")
    if st.button("Skip ⏩"):
        # منطق الانتقال
        if st.session_state.ex_idx < len(st.session_state.custom_plan) - 1:
            st.session_state.ex_idx += 1
            st.session_state.status = "WORKOUT"
        else:
            if st.session_state.current_set < st.session_state.total_sets:
                st.session_state.current_set += 1
                st.session_state.ex_idx = 1 # ابدأ من التمرين الأول بعد الإحماء
                st.session_state.status = "WORKOUT"
            else:
                st.session_state.status = "SELECT"
        st.rerun()

    p = st.empty()
    for i in range(30, -1, -1):
        p.metric("Ready?", f"{i}s")
        time.sleep(1)
    
    play_audio("https://www.soundjay.com/misc/sounds/referee-whistle-01.mp3")
    
    if st.session_state.ex_idx < len(st.session_state.custom_plan) - 1:
        st.session_state.ex_idx += 1
        st.session_state.status = "WORKOUT"
    else:
        if st.session_state.current_set < st.session_state.total_sets:
            st.session_state.current_set += 1
            st.session_state.ex_idx = 1 # لا نعيد الإحماء في الجولات التالية
            st.session_state.status = "WORKOUT"
        else:
            st.balloons()
            st.success("Session Finished!")
            time.sleep(2)
            st.session_state.status = "SELECT"
    st.rerun()
