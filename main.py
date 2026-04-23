import streamlit as st
import time

# إعدادات الصفحة لتظهر بشكل احترافي على الجوال
st.set_page_config(page_title="HomeFlex Pro", page_icon="💪", layout="centered")

# قاعدة بيانات التمارين - روابط تم فحصها وتدعم التضمين (Embed)
workout_data = [
    {
        "name": "Glute Bridges",
        "target": 12,
        "type": "Reps",
        "desc": "استلقِ على ظهرك مع ثني الركبتين، ثم ارفع حوضك للأعلى.",
        "video": "https://www.youtube.com/watch?v=8bbE6adQTpM"
    },
    {
        "name": "Wall Push-ups",
        "target": 10,
        "type": "Reps",
        "desc": "الوقوف أمام حائط ودفع الجسم بعيداً عنه.",
        "video": "https://www.youtube.com/watch?v=vVfS0vD_Puw"
    },
    {
        "name": "Bird-Dog",
        "target": 10,
        "type": "Reps",
        "desc": "مد اليد اليمنى والرجل اليسرى في نفس الوقت أثناء الارتكاز على الأطراف الأربعة.",
        "video": "https://www.youtube.com/watch?v=2SSTInV6C_c"
    },
    {
        "name": "Classic Plank",
        "target": 30,
        "type": "Time",
        "desc": "الثبات بوضعية اللوح لتقوية عضلات البطن.",
        "video": "https://www.youtube.com/watch?v=pSHjTRCQxIw"
    }
]

# إدارة الحالة
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'is_resting' not in st.session_state:
    st.session_state.is_resting = False

def finish_rest():
    st.session_state.is_resting = False
    st.session_state.step += 1
    st.rerun()

# --- واجهة التطبيق ---
st.title("💪 HomeFlex")

if st.session_state.is_resting:
    st.subheader("🥤 وقت الراحة")
    st.write("خذ نفساً عميقاً...")
    
    # زر تخطي الراحة
    if st.button("تخطي الراحة ⏩"):
        finish_rest()
    
    # مؤقت تنازلي بصري
    placeholder = st.empty()
    for i in range(30, 0, -1):
        placeholder.metric("متبقي للراحة", f"{i} ثانية")
        time.sleep(1)
    finish_rest()

else:
    if st.session_state.step < len(workout_data):
        ex = workout_data[st.session_state.step]
        
        # عرض الفيديو (هذه الروابط تدعم التضمين)
        st.video(ex['video'])
        
        st.header(f"{st.session_state.step + 1}. {ex['name']}")
        st.info(ex['desc'])
        
        st.markdown(f"### الهدف: **{ex['target']} {'ثانية' if ex['type'] == 'Time' else 'تكرار'}**")
        
        # أزرار التحكم
        col1, col2 = st.columns(2)
        with col1:
            if ex['type'] == 'Time':
                if st.button("⏱️ ابدأ العداد"):
                    t_place = st.empty()
                    for s in range(ex['target'], 0, -1):
                        t_place.header(f"🔥 {s} ثانية")
                        time.sleep(1)
                    st.success("أحسنت!")
        
        with col2:
            if st.button("انتهيت! (راحة) ➡️"):
                st.session_state.is_resting = True
                st.rerun()
        
        # شريط التقدم
        st.progress((st.session_state.step) / len(workout_data))
                
    else:
        st.balloons()
        st.success("🎉 مبروك! أنهيت تمارين اليوم.")
        if st.button("إعادة البرنامج"):
            st.session_state.step = 0
            st.rerun()
