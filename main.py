import streamlit as st
import time

# إعدادات واجهة التطبيق
st.set_page_config(page_title="HomeFlex 30-Day", page_icon="💪")

# التنسيق الجمالي (CSS)
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #00ffcc; color: black; font-weight: bold; }
    .stProgress > div > div > div > div { background-color: #00ffcc; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏠 HomeFlex")
st.subheader("برنامج الـ 30 يوماً لاستعادة النشاط")

# قاعدة بيانات التمارين (نموذج مبسط للأيام)
workout_plan = {
    "الأسبوع الأول: الإيقاظ": [
        {"name": "Glute Bridges", "target": 12, "type": "Reps", "desc": "الاستلقاء ورفع الحوض لتنشيط العضلات."},
        {"name": "Wall Push-ups", "target": 10, "type": "Reps", "desc": "ضغط خفيف على الحائط."},
        {"name": "Cat-Cow Stretch", "target": 30, "type": "Time", "desc": "إطالة للظهر لتحسين مرونة العمود الفقري."}
    ],
    "الأسبوع الثاني: التنشيط": [
        {"name": "Bird-Dog", "target": 10, "type": "Reps", "desc": "مد اليد والرجل المعاكسة للتوازن."},
        {"name": "Plank", "target": 20, "type": "Time", "desc": "ثبات لشد عضلات البطن."},
        {"name": "Chair Squats", "target": 12, "type": "Reps", "desc": "الوقوف والجلوس على الكرسي لتقوية الأرجل."}
    ]
}

# حفظ التقدم في المتصفح
if 'day' not in st.session_state:
    st.session_state.day = 1
if 'ex_index' not in st.session_state:
    st.session_state.ex_index = 0

# تحديد الأسبوع والتمارين بناءً على اليوم الحالي
current_week = "الأسبوع الأول: الإيقاظ" if st.session_state.day <= 7 else "الأسبوع الثاني: التنشيط"
day_exercises = workout_plan[current_week]

# واجهة التطبيق
st.write(f"📅 **اليوم: {st.session_state.day}** | {current_week}")
progress = (st.session_state.day / 30)
st.progress(progress)

if st.session_state.ex_index < len(day_exercises):
    ex = day_exercises[st.session_state.ex_index]
    
    st.info(f"**التمرين الحالي:** {ex['name']}")
    st.write(ex['desc'])
    st.metric("الهدف", f"{ex['target']} {'ثانية' if ex['type'] == 'Time' else 'تكرار'}")

    if ex['type'] == "Time":
        if st.button("⏱️ ابدأ المؤقت"):
            t_placeholder = st.empty()
            for secs in range(ex['target'], 0, -1):
                t_placeholder.header(f"متبقي: {secs} ثانية")
                time.sleep(1)
            st.success("انتهى التمرين!")
            time.sleep(1)

    if st.button("التالي ➡️"):
        st.session_state.ex_index += 1
        st.rerun()
else:
    st.success("🎊 أحسنت! أنهيت تمارين اليوم!")
    if st.button("حفظ التقدم والانتقال لليوم التالي"):
        st.session_state.day += 1
        st.session_state.ex_index = 0
        st.rerun()

if st.button("🔄 إعادة ضبط البرنامج"):
    st.session_state.day = 1
    st.session_state.ex_index = 0
    st.rerun()
