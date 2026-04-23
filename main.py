import streamlit as st
import time

# إعدادات الصفحة
st.set_page_config(page_title="HomeFlex Pro: Verified Edition", page_icon="💪")

# قاعدة بيانات التمارين مع روابط يوتيوب تعمل (Verified Embeds)
workout_data = [
    {
        "name": "Glute Bridges (جسر الحوض)",
        "target": 12,
        "type": "Reps",
        "desc": "استلقِ على ظهرك وارفع حوضك. يركز هذا التمرين على تنشيط عضلات المقعدة وأسفل الظهر.",
        "video": "https://www.youtube.com/watch?v=8bbE6adQTpM"
    },
    {
        "name": "Wall Push-ups (الضغط على الحائط)",
        "target": 10,
        "type": "Reps",
        "desc": "تمرين رائع لتقوية الصدر والذراعين بدون ضغط كبير على المفاصل.",
        "video": "https://www.youtube.com/watch?v=vVfS0vD_Puw"
    },
    {
        "name": "Bird-Dog (الكلب الطائر)",
        "target": 10,
        "type": "Reps",
        "desc": "يركز على تقوية عضلات الكور (Core) وزيادة توازن العمود الفقري.",
        "video": "https://www.youtube.com/watch?v=2SSTInV6C_c"
    },
    {
        "name": "Plank (البلانك التقليدي)",
        "target": 30,
        "type": "Time",
        "desc": "حافظ على استقامة جسمك كلوح خشبي. تمرين جبار لشد كامل الجسم.",
        "video": "https://www.youtube.com/watch?v=pSHjTRCQxIw"
    }
]

# إدارة الحالة
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'is_resting' not in st.session_state:
    st.session_state.is_resting = False

# دالة الانتقال للتمرين التالي
def go_to_next():
    st.session_state.is_resting = False
    st.session_state.step += 1
    st.rerun()

# واجهة التطبيق
st.title("💪 HomeFlex: النسخة المطورة")

if st.session_state.is_resting:
    st.subheader("🥤 وقت الراحة")
    st.info("استرخِ قليلاً، خذ شهيقاً وعميقاً...")
    
    # زر التخطي
    if st.button("تخطي الراحة ⏩"):
        go_to_next()
    
    # عداد الراحة
    placeholder = st.empty()
    for i in range(30, 0, -1):
        placeholder.metric("الوقت المتبقي للراحة", f"{i} ثانية")
        time.sleep(1)
    
    go_to_next()

else:
    if st.session_state.step < len(workout_data):
        current_ex = workout_data[st.session_state.step]
        
        # عرض الفيديو
        st.video(current_ex['video'])
        
        # معلومات التمرين
        st.header(f"{st.session_state.step + 1}. {current_ex['name']}")
        st.write(current_ex['desc'])
        
        # الهدف والعداد
        st.markdown(f"### الهدف: **{current_ex['target']} {'ثانية' if current_ex['type'] == 'Time' else 'تكرار'}**")
        
        col1, col2 = st.columns(2)
        with col1:
            if current_ex['type'] == 'Time':
                if st.button("⏱️ ابدأ العداد"):
                    timer_place = st.empty()
                    for s in range(current_ex['target'], 0, -1):
                        timer_place.subheader(f"🔥 {s} ثانية متبقية")
                        time.sleep(1)
                    st.success("انتهى الوقت! عمل رائع.")
        
        with col2:
            if st.button("انتهيت! (بدء الراحة) ➡️"):
                st.session_state.is_resting = True
                st.rerun()
        
        # شريط التقدم
        st.progress((st.session_state.step) / len(workout_data))
                
    else:
        st.balloons()
        st.success("🎊 مذهل! لقد أكملت تمارين اليوم.")
        if st.button("إعادة البرنامج من اليوم الأول"):
            st.session_state.step = 0
            st.rerun()

st.markdown("---")
st.caption("تطبيق HomeFlex - رفيقك لاستعادة نشاطك البدني")
