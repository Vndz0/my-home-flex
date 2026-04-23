import streamlit as st
import time
import json
import os
import random

st.set_page_config(page_title="HomeFlex Elite", page_icon="💪", layout="wide")

# ================== STORAGE ==================
DATA_FILE = "user_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"history": [], "points": 0, "streak": 0}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

user_data = load_data()

# ================== DATABASE ==================
workout_database = {
    "Arms (Biceps & Triceps)": [
        {
            "name": "Wall Bicep Curls",
            "desc": "Controlled curl motion focusing on tension.",
            "target": 15,
            "type": "Reps",
            "video": "https://www.youtube.com/watch?v=iOaT_u6v-s8",
            "alts": [
                {"name": "Towel Bicep Curls", "desc": "Use towel resistance.", "video": "https://www.youtube.com/watch?v=av7-8igSXTs"},
                {"name": "Door Frame Rows", "desc": "Pull using door frame.", "video": "https://www.youtube.com/watch?v=GZbfZ033f74"}
            ]
        },
        {
            "name": "Chair Tricep Dips",
            "desc": "Lower body using chair.",
            "target": 12,
            "type": "Reps",
            "video": "https://www.youtube.com/watch?v=0326dy_-CzM",
            "alts": [
                {"name": "Bench Dips", "desc": "Same movement on bench.", "video": "https://www.youtube.com/watch?v=0326dy_-CzM"},
                {"name": "Overhead Extension", "desc": "Bodyweight extension.", "video": "https://www.youtube.com/watch?v=_gsUck-7M74"}
            ]
        }
    ],

    "Legs (Quads & Glutes)": [
        {
            "name": "Chair Squats",
            "desc": "Sit and stand with control.",
            "target": 15,
            "type": "Reps",
            "video": "https://www.youtube.com/watch?v=1uPrX7tovfM",
            "alts": [
                {"name": "Sumo Squats", "desc": "Wide stance squat.", "video": "https://www.youtube.com/watch?v=aclHkVaku9U"},
                {"name": "Step Ups", "desc": "Step onto chair.", "video": "https://www.youtube.com/watch?v=dQqApCGd5Ss"}
            ]
        }
    ]
}

# ================== SESSION ==================
if "page" not in st.session_state: st.session_state.page = "menu"
if "plan" not in st.session_state: st.session_state.plan = []
if "selected" not in st.session_state: st.session_state.selected = {}
if "ex_idx" not in st.session_state: st.session_state.ex_idx = 0
if "set" not in st.session_state: st.session_state.set = 1
if "sets" not in st.session_state: st.session_state.sets = 3

# ================== HEADER ==================
st.title("🔥 HomeFlex Elite")

col1, col2, col3 = st.columns(3)
col1.metric("🔥 Streak", user_data["streak"])
col2.metric("🏆 Points", user_data["points"])
col3.metric("📈 Level", user_data["points"] // 100)

st.divider()

# ================== MENU ==================
if st.session_state.page == "menu":

    st.subheader("Choose Workout")

    for day in workout_database:
        if st.button(day, use_container_width=True):
            st.session_state.current_day = day
            st.session_state.page = "preview"
            st.session_state.selected = {}
            st.rerun()

    if st.button("⚡ Quick Start"):
        st.session_state.current_day = random.choice(list(workout_database.keys()))
        st.session_state.page = "preview"
        st.rerun()

# ================== PREVIEW ==================
elif st.session_state.page == "preview":

    st.header(st.session_state.current_day)

    exercises = workout_database[st.session_state.current_day]

    for i, ex in enumerate(exercises):

        selected = st.session_state.selected.get(i, ex)

        st.subheader(f"Exercise {i+1}")

        st.video(selected["video"])

        c1, c2 = st.columns([4,1])
        with c1:
            st.markdown(f"### {selected['name']}")
        with c2:
            st.code(selected["name"])

        st.info(selected["desc"])
        st.metric("Target", f"{selected['target']} {selected['type']}")

        st.write("Alternatives:")

        cols = st.columns(2)

        for j, alt in enumerate(ex["alts"]):
            with cols[j]:
                if st.button(alt["name"], key=f"{i}_{j}"):
                    st.session_state.selected[i] = {
                        "name": alt["name"],
                        "video": alt["video"],
                        "desc": alt["desc"],
                        "target": ex["target"],
                        "type": ex["type"]
                    }
                    st.rerun()

        if i in st.session_state.selected:
            if st.button("Use Original", key=f"reset_{i}"):
                del st.session_state.selected[i]
                st.rerun()

        st.divider()

    # build plan
    plan = []
    for i, ex in enumerate(exercises):
        plan.append(st.session_state.selected.get(i, ex))

    st.session_state.plan = plan

    st.session_state.sets = st.slider("Sets", 1, 5, 3)

    if st.button("🚀 Start"):
        st.session_state.ex_idx = 0
        st.session_state.set = 1
        st.session_state.page = "workout"
        st.rerun()

    if st.button("⬅️ Back"):
        st.session_state.page = "menu"
        st.rerun()

# ================== WORKOUT ==================
elif st.session_state.page == "workout":

    ex = st.session_state.plan[st.session_state.ex_idx]

    st.warning(f"Set {st.session_state.set}/{st.session_state.sets}")
    st.title(ex["name"])
    st.metric("Target", f"{ex['target']} {ex['type']}")

    progress = (st.session_state.ex_idx + 1) / len(st.session_state.plan)
    st.progress(progress)

    if ex["type"] == "Time":
        if st.button("Start Timer"):
            for i in range(ex["target"], -1, -1):
                st.write(f"{i}s")
                time.sleep(1)
            st.session_state.page = "rest"
            st.rerun()
    else:
        if st.button("Done"):
            st.session_state.page = "rest"
            st.rerun()

    if st.button("Skip"):
        st.session_state.page = "rest"
        st.rerun()

# ================== REST ==================
elif st.session_state.page == "rest":

    st.subheader("Rest Time")

    rest_time = 20 if st.session_state.plan[st.session_state.ex_idx]["type"] == "Time" else 30

    for i in range(rest_time, -1, -1):
        st.metric("Rest", f"{i}s")
        time.sleep(1)

    if st.session_state.ex_idx < len(st.session_state.plan) - 1:
        st.session_state.ex_idx += 1
        st.session_state.page = "workout"
    else:
        if st.session_state.set < st.session_state.sets:
            st.session_state.set += 1
            st.session_state.ex_idx = 0
            st.session_state.page = "workout"
        else:
            st.success("Workout Finished 🎉")

            # تحديث البيانات
            user_data["points"] += 20
            user_data["streak"] += 1
            user_data["history"].append({
                "day": st.session_state.current_day,
                "time": time.time()
            })
            save_data(user_data)

            time.sleep(2)
            st.session_state.page = "menu"

    st.rerun()
