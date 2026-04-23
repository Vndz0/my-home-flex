import streamlit as st
import time

# إعدادات واجهة التطبيق
st.set_page_config(page_title="HomeFlex Pro", page_icon="💪", layout="centered")

# قاعدة بيانات التمارين (3 تمارين كمثال، يمكنك تكرار النمط لإضافة المزيد)
workout_data = [
    {
        "name": "Glute Bridges (جسر الحوض)",
        "target": 12,
        "type": "Reps",
        "desc": "استلقِ على ظهرك وارفع حوضك للأعلى. هذا التمرين يوقظ عضلاتك بعد جلوس طويل.",
        "gif": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExOHpueGZ4bmZ4bmZ4bmZ4bmZ4bmZ4bmZ4bmZ4bmZ4bmZ4bmZ4bmZ4JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZ力をZWFyY2hfZnVsbCZjdD1n/3o7TKMGpxVMEKExD9u/giphy.gif"
    },
    {
        "name": "Wall Push-ups (الضغط على الحائط)",
        "target": 10,
        "type": "Reps",
        "desc": "قف أمام الحائط وادفع بجسمك. ممتاز لتقوية الصدر دون إجهاد المفاصل.",
        "gif": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbnRwaGZxeXJ4bmZ4bmZ4bmZ4bmZ4bmZ4bmZ4bmZ4bmZ4bmZ4bmZ4bmZ4JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZ力をZWFyY2hfZnVsbCZjdD1n/l3vR7CSfS69uSIn9S/giphy.gif"
    },
    {
        "name": "Bird-Dog (وضعية الكلب الطائر)",
        "target": 10,
        "type": "Reps",
        "desc": "مد يدك اليمنى ورجلك اليسرى معاً وأنت على أطرافك الأربعة. رائع لاستقرار الظهر.",
        "gif": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbmZ4bmZ4bmZ4bmZ4bmZ4bmZ4bmZ4bmZ4bmZ4bmZ4bmZ4bmZ4bmZ4JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZ力をZWFyY2hfZnVsbCZjdD1n/3o7TKpxO7XzO5Jp8Ry/giphy.gif"
    },
    {
        "name": "Plank (تمرين البلانك)",
        "target": 30,
        "type": "Time",
        "desc": "ثبات كامل للجسم. تنفس بعمق وحافظ على استقامة ظهرك.",
        "gif": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExYnJ4bmZ4bmZ4bmZ4bmZ4bmZ4bmZ4bmZ4bmZ4bmZ4bmZ4bmZ4bmZ4JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZ力をZWFyY2hfZnVsbCZjdD1n/3o7TKSj0S1i/giphy.gif"
    }
]

# إدارة الحالة (State Management)
if 'step' not in st.session_state:
    st.session_state.step = 0  # index للتمرين
if 'is_resting' not in st.session_state:
    st.session_state.is_resting = False

# شاشة الراحة
def show_rest():
    st.warning("🥤 وقت الراحة (30 ثانية)")
    st.write("تنفس بعمق، استعد للتمرين التالي...")
    placeholder = st.empty()
    for i in range(30, 0, -1):
        placeholder.subheader(f"متبقي: {i} ثانية")
        time.sleep(1)
    st.session_state.is_resting = False
    st.session_state.step += 1
    st.rerun()

# واجهة التطبيق الرئيسية
st.title("💪 HomeFlex: مستشارك الرياضي")

if st.session_state.is_resting:
    show_rest()
else:
    if st.session_state.step < len(workout_data):
        current_ex = workout_data[st.session_state.step]
        
        # 1. عرض الصورة المتحركة
        st.image(current_ex['gif'], use_container_width=True)
        
        # 2. معلومات التمرين
        st.header(current_ex['name'])
        st.info(current_ex['desc'])
        st.subheader(f"الهدف: {current_ex['target']} {'ثانية' if current_ex['type'] == 'Time' else 'عدات'}")
        
        # 3. شريط التقدم العام
        progress = (st.session_state.step) / len(workout_data)
        st.progress(progress)
        
        # 4. أزرار التحكم
        col1, col2 = st.columns(2)
        
        with col1:
            if current_ex['type'] == 'Time':
                if st.button("⏱️ ابدأ المؤقت"):
                    t_place = st.empty()
                    for s in range(current_ex['target'], 0, -1):
                        t_place.header(f"🔥 {s} ثانية")
                        time.sleep(1)
                    st.success("تم الإنجاز!")
        
        with col2:
            if st.button("التالي (راحة) ➡️"):
                st.session_state.is_resting = True
                st.rerun()
                
    else:
        st.balloons()
        st.success("🏆 بطل! أنهيت تمرين اليوم بنجاح.")
        if st.button("البدء من جديد"):
            st.session_state.step = 0
            st.rerun()

# تذييل بسيط
st.markdown("---")
st.caption("تذكر: الاستمرارية أهم من القوة. ابدأ اليوم!")
