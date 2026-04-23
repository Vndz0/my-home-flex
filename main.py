import streamlit as st
import time

# إعدادات الصفحة
st.set_page_config(page_title="HomeFlex Pro: YouTube Edition", page_icon="📺")

# التنسيق الجمالي
st.markdown("""
    <style>
    .stVideo { border-radius: 15px; overflow: hidden; box-shadow: 0px 4px 15px rgba(0,255,204,0.3); }
    </style>
    """, unsafe_allow_html=True)

# قاعدة بيانات التمارين مع روابط يوتيوب
workout_data = [
    {
        "name": "Glute Bridges (جسر الحوض)",
        "target": 12,
        "type": "Reps",
        "desc": "تمرين أساسي لتنشيط العضلات الخاملة وتقوية أسفل الظهر.",
        "video": "https://www.youtube.com/watch?v=wPM8icPu6H8"
    },
    {
        "name": "Wall Push-ups (الضغط على الحائط)",
        "target": 10,
        "type": "Reps",
        "desc": "بديل آمن وسهل للضغط العادي، يقوي الصدر والأكتاف.",
        "video": "https://www.youtube.com/watch?v=a6YHbXbeZ3M"
    },
    {
        "name": "Bird-Dog (تمرين الكلب الطائر)",
        "target": 10,
        "type": "Reps",
        "desc": "يركز على التوازن وتقوية عضلات الكور والظهر.",
        "video": "https://www.youtube.com/watch?v=wiFNA3sqjCb"
    },
    {
        "name": "Plank (تمرين البلانك)",
        "target": 30,
        "type": "Time",
        "desc": "أفضل تمرين لشد الجسم بالكامل وزيادة التحمل.",
        "video": "https://www.youtube.com/watch?v=pSHjTRCQxIw"
    }
]

# إدارة الحالة
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'is_resting' not in st.session_state:
    st.session_state.is_resting = False

# شاشة الراحة
def show_rest():
    st.warning("🥤 وقت الراحة (30 ثانية)")
    st.write("خذ نفساً عميقاً واستعد للتمرين التالي...")
    placeholder = st.empty()
    for i in range(30, 0, -1):
        placeholder.subheader(f"متبقي: {i} ثانية")
        time.sleep(1)
    st.session_state.is_resting = False
    st.session_state.step += 1
    st.rerun()

# واجهة التطبيق
st.title("📺 HomeFlex YouTube Edition")

if st.session_state.is_resting:
    show_rest()
else:
    if st.session_state.step < len(workout_data):
        current_ex = workout_data[st.session_state.step]
        
        # 1. عرض فيديو يوتيوب
        st.video(current_ex['video'])
        
        # 2. معلومات التمرين
        st.header(current_ex['name'])
        st.info(current_ex['desc'])
        st.subheader(f"الهدف المطلوب: {current_ex['target']} {'ثانية' if current_ex['type'] == 'Time' else 'عدات'}")
        
        # 3. التحكم والعداد
        col1, col2 = st.columns(2)
        with col1:
            if current_ex['type'] == 'Time':
                if st.button("⏱️ ابدأ العداد"):
                    t_place = st.empty()
                    for s in range(current_ex['target'], 0, -1):
                        t_place.header(f"🔥 {s} ثانية")
                        time.sleep(1)
                    st.success("تم!")
        
        with col2:
            if st.button("انتهيت! (بدء الراحة) ➡️"):
                st.session_state.is_resting = True
                st.rerun()
        
        # شريط التقدم
        st.progress((st.session_state.step) / len(workout_data))
                
    else:
        st.balloons()
        st.success("🏆 بطل! أنهيت جدول اليوم بنجاح.")
        if st.button("البدء من جديد (يوم 1)"):
            st.session_state.step = 0
            st.rerun()
