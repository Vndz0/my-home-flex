import streamlit as st
import time

# إعدادات الصفحة
st.set_page_config(page_title="HomeFlex: Auto-Trainer", page_icon="🏋️‍♂️")

# --- محرك التطور (Progressive Overload) ---
week_num = st.sidebar.number_input("الأسبوع الحالي", min_value=1, max_value=4, value=1)
difficulty_factor = 1 + (week_num - 1) * 0.1  # زيادة 10% كل أسبوع

# --- قاعدة بيانات التمارين (شاملة للجسم) ---
# ملاحظة: الروابط تم اختيارها لدعم التشغيل التلقائي والتضمين
workout_db = [
    {"name": "التسخين: إطالة القطة", "target": 30, "type": "Time", "video": "https://www.youtube.com/watch?v=wiFNA3sqjCb"},
    {"name": "صدر: ضغط الحائط", "target": int(10 * difficulty_factor), "type": "Reps", "video": "https://www.youtube.com/watch?v=vVfS0vD_Puw"},
    {"name": "أرجل: سكوات الكرسي", "target": int(12 * difficulty_factor), "type": "Reps", "video": "https://www.youtube.com/watch?v=1uPrX7tovfM"},
    {"name": "ظهر: الكلب الطائر", "target": int(10 * difficulty_factor), "type": "Reps", "video": "https://www.youtube.com/watch?v=2SSTInV6C_c"},
    {"name": "بطن: بلانك ثابت", "target": int(30 * difficulty_factor), "type": "Time", "video": "https://www.youtube.com/watch?v=pSHjTRCQxIw"}
]

# --- إدارة الحالة الصوتية والآلية ---
if 'ex_idx' not in st.session_state: st.session_state.ex_idx = 0
if 'status' not in st.session_state: st.session_state.status = "START" # START, WORKOUT, REST, FINISHED
if 'day' not in st.session_state: st.session_state.day = 1

def play_sound(type="bell"):
    # استخدام أكواد HTML لتشغيل أصوات تنبيهية بسيطة
    if type == "bell":
        st.components.v1.html('<audio autoplay><source src="https://www.soundjay.com/misc/sounds/bell-ringing-05.mp3" type="audio/mpeg"></audio>', height=0)
    elif type == "whistle":
        st.components.v1.html('<audio autoplay><source src="https://www.soundjay.com/misc/sounds/referee-whistle-01.mp3" type="audio/mpeg"></audio>', height=0)

# --- واجهة التطبيق ---
st.title("🏋️‍♂️ مدرب HomeFlex الذكي")
st.sidebar.header(f"📅 اليوم {st.session_state.day} من 5")
st.sidebar.progress(st.session_state.day / 5)

if st.session_state.status == "START":
    st.info("مرحباً بك! برنامج اليوم مصمم ليشمل كامل الجسم مع زيادة تدريجية.")
    if st.button("🚀 ابدأ التمرين الآن (تشغيل تلقائي)", use_container_width=True):
        st.session_state.status = "WORKOUT"
        st.rerun()

elif st.session_state.status == "WORKOUT":
    ex = workout_db[st.session_state.ex_idx]
    
    # مسمى التمرين في خانة مستقلة للنسخ
    st.code(ex['name'], language="text")
    st.video(ex['video'])
    
    st.subheader(f"الهدف: {ex['target']} {'ثانية' if ex['type'] == 'Time' else 'تكرار'}")
    
    if ex['type'] == "Time":
        if st.button("🔄 إعادة التعداد"): st.rerun()
        
        t_place = st.empty()
        for s in range(ex['target'], -1, -1):
            t_place.header(f"⏳ {s} ثانية")
            time.sleep(1)
        play_sound("bell")
        st.session_state.status = "REST"
        st.rerun()
    else:
        if st.button("تم الإنجاز! (انتقل للراحة) ✅", use_container_width=True):
            play_sound("bell")
            st.session_state.status = "REST"
            st.rerun()

elif st.session_state.status == "REST":
    st.subheader("🥤 وقت راحة (30 ثانية)")
    if st.button("تخطي الراحة ⏩"):
        if st.session_state.ex_idx < len(workout_db) - 1:
            st.session_state.ex_idx += 1
            st.session_state.status = "WORKOUT"
        else:
            st.session_state.status = "FINISHED"
        st.rerun()
        
    p = st.empty()
    for i in range(30, -1, -1):
        p.metric("استعد للتالي...", f"{i} ثانية")
        time.sleep(1)
    
    play_sound("whistle") # صفارة نهاية الراحة
    
    if st.session_state.ex_idx < len(workout_db) - 1:
        st.session_state.ex_idx += 1
        st.session_state.status = "WORKOUT"
        st.rerun()
    else:
        st.session_state.status = "FINISHED"
        st.rerun()

elif st.session_state.status == "FINISHED":
    st.balloons()
    st.success(f"أحسنت! أكملت اليوم {st.session_state.day}")
    if st.button("حفظ التقدم لليوم التالي 💾"):
        if st.session_state.day < 5:
            st.session_state.day += 1
            st.session_state.ex_idx = 0
            st.session_state.status = "START"
        else:
            st.write("تهانينا! أكملت أسبوعاً كاملاً. زد رقم الأسبوع من القائمة الجانبية.")
            st.session_state.day = 1
            st.session_state.ex_idx = 0
            st.session_state.status = "START"
        st.rerun()
