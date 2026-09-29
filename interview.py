import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="Interview Arena",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.html("""
<style>

body {
    overflow-x: hidden;
}

.stApp {
    background:
        radial-gradient(circle at 15% 20%, rgba(124,92,255,0.35), transparent 25%),
        radial-gradient(circle at 85% 20%, rgba(0,217,255,0.25), transparent 25%),
        radial-gradient(circle at 50% 90%, rgba(255,0,150,0.20), transparent 30%),
        linear-gradient(135deg, #05060b, #0a0d18, #090817);

    background-size: 200% 200%;
    animation: glowMove 8s ease-in-out infinite;
}

@keyframes glowMove {
    0% {
        background-position: 0% 50%;
    }

    50% {
        background-position: 100% 50%;
    }

    100% {
        background-position: 0% 50%;
    }
}

</style>
""")



# =========================================================
# DATABASE CONNECTION
# =========================================================

conn = sqlite3.connect(
    "interview_evaluation.db",
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT NOT NULL,
    confidence INTEGER DEFAULT 0,
    communication INTEGER DEFAULT 0,
    knowledge INTEGER DEFAULT 0,
    CV INTEGER DEFAULT 0,
    total_marks INTEGER DEFAULT 0,
    percentage REAL DEFAULT 0,
    remarks TEXT DEFAULT ''
)
""")

conn.commit()

# =========================================================
# PRELOAD 10 STUDENTS
# Only when database is completely empty
# =========================================================

cursor.execute("SELECT COUNT(*) FROM students")
student_count = cursor.fetchone()[0]

if student_count == 0:

    initial_students = [
        "Khushi",
        "Trusha",
        "Manasavi",
        "Yashvi",
        "Kajal",
        "Pritam",
        "Krish",
        "Paresh",
        "Meet",
        "Deepak"
    ]

    for name in initial_students:

        cursor.execute("""
        INSERT INTO students
        (
            student_name,
            confidence,
            communication,
            knowledge,
            CV,
            total_marks,
            percentage,
            remarks
        )
        VALUES (?, 0, 0, 0, 0, 0, 0, '')
        """, (name,))

    conn.commit()

# =========================================================
# CUSTOM UI
# =========================================================

st.html("""
<style>
.particles {
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 0;
    opacity: 0.35;
    background-image:
        radial-gradient(circle, rgba(255,255,255,0.35) 1px, transparent 1px),
        radial-gradient(circle, rgba(0,217,255,0.25) 1px, transparent 1px);
    background-size: 70px 70px, 120px 120px;
    animation: particlesMove 18s linear infinite;
}

@keyframes particlesMove {
    from {
        background-position: 0 0, 0 0;
    }
    to {
        background-position: 70px 100px, -120px 80px;
    }
}

.stApp {
    background:
        radial-gradient(
            circle at 10% 10%,
            rgba(120, 80, 255, 0.22),
            transparent 28%
        ),
        radial-gradient(
            circle at 90% 15%,
            rgba(0, 220, 255, 0.14),
            transparent 25%
        ),
        radial-gradient(
            circle at 50% 100%,
            rgba(255, 0, 150, 0.10),
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #05060b 0%,
            #0a0d18 50%,
            #090817 100%
        );

    color: white;
}

[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #080a12,
            #11142b
        );

    border-right: 1px solid rgba(255,255,255,0.08);
}

[data-testid="stSidebar"] * {
    color: #eeeeff;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

/* HERO */

.hero {
    padding: 30px;
    border-radius: 25px;
    margin-bottom: 25px;

    background:
        linear-gradient(
            135deg,
            rgba(124,92,255,0.20),
            rgba(0,214,255,0.08),
            rgba(255,0,128,0.08)
        );

    border: 1px solid rgba(255,255,255,0.10);

    box-shadow:
        0 20px 70px rgba(0,0,0,0.35);
}

.hero-title {
    font-size: 42px;
    font-weight: 900;
    letter-spacing: 2px;
}

.hero-subtitle {
    color: #aeb7d9;
    font-size: 16px;
}

/* KPI */

.kpi {
    background: rgba(255,255,255,0.055);

    border: 1px solid rgba(255,255,255,0.09);

    border-radius: 20px;

    padding: 20px;

    min-height: 125px;

    box-shadow:
        0 15px 40px rgba(0,0,0,0.25);
}

.kpi-label {
    color: #9fa9cc;

    font-size: 13px;

    text-transform: uppercase;

    letter-spacing: 1.2px;
}

.kpi-value {
    font-size: 30px;

    font-weight: 900;

    margin-top: 8px;
}

.kpi-small {
    color: #aeb7d9;

    font-size: 12px;

    margin-top: 4px;
}

/* PODIUM */

/* PODIUM */

.podium {
    text-align: center;
    padding: 25px 10px;
    border-radius: 22px;
    border: 1px solid rgba(255,255,255,0.10);
    background: rgba(255,255,255,0.045);
    box-shadow: 0 20px 50px rgba(0,0,0,0.28);
    transition: 0.3s ease;
}

.podium:hover {
    transform: translateY(-8px);
    box-shadow: 0 25px 60px rgba(0,217,255,0.18);
}

.podium-first {
    min-height: 270px;
    padding-top: 35px;
    background: linear-gradient(
        145deg,
        rgba(255,193,7,0.16),
        rgba(124,92,255,0.10)
    );
}

.podium-second {
    min-height: 220px;
    margin-top: 50px;
    background: linear-gradient(
        145deg,
        rgba(192,192,192,0.12),
        rgba(124,92,255,0.08)
    );
}

.podium-third {
    min-height: 190px;
    margin-top: 80px;
    background: linear-gradient(
        145deg,
        rgba(205,127,50,0.14),
        rgba(0,217,255,0.06)
    );
}

.rank-number {
    font-size: 45px;
    font-weight: 900;
}

.rank-name {
    font-size: 19px;
    font-weight: 800;
    margin-top: 5px;
}

.rank-score {
    font-size: 27px;
    font-weight: 900;
    margin-top: 8px;
}

.rank-label {
    color: #aeb7d9;
    font-size: 12px;
}

/* LEADERBOARD */

.leader-card {

    padding: 16px 18px;

    margin: 8px 0;

    border-radius: 16px;

    background:
        rgba(255,255,255,0.045);

    border:
        1px solid rgba(255,255,255,0.07);

    box-shadow:
        0 10px 30px rgba(0,0,0,0.20);
}

.leader-name {

    font-weight: 800;

    font-size: 16px;
}

.score {

    font-weight: 900;

    font-size: 18px;
}

.progress-bg {

    background:
        rgba(255,255,255,0.08);

    border-radius: 20px;

    height: 8px;

    margin-top: 8px;

    overflow: hidden;
}

.progress-fill {

    height: 8px;

    border-radius: 20px;

    background:
        linear-gradient(
            90deg,
            #7c5cff,
            #00d9ff
        );
}

.section-title {

    font-size: 25px;

    font-weight: 850;

    margin: 25px 0 15px 0;
}

/* BUTTON */

div.stButton > button {

    border-radius: 12px;

    border:
        1px solid rgba(124,92,255,0.45);

    background:
        rgba(124,92,255,0.14);

    color: white;

    font-weight: 700;
}

div.stButton > button:hover {

    border-color: #00d9ff;

    color: white;

    box-shadow:
        0 0 22px rgba(0,217,255,0.18);
}

/* INPUT */

.stTextInput input,
.stNumberInput input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"] > div {

    background:
        rgba(255,255,255,0.055) !important;

    color: white !important;

    border-radius: 10px !important;
}

</style>
""")

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.html("""
<div style="
text-align:center;
padding:10px 0 20px 0;
">

<div style="font-size:42px;">
🏆
</div>

<div style="
font-size:23px;
font-weight:900;
">
INTERVIEW ARENA
</div>

<div style="
font-size:12px;
color:#9fa9cc;
">
STUDENT EVALUATION SYSTEM
</div>

</div>
""")

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "🏠 Command Center",
        "➕ Add Student",
        "📋 All Students",
        "✏️ Update Evaluation",
        "🗑️ Delete Student",
        "🏆 Top 10 Leaderboard",
        "📊 Analytics"
    ]
)

st.sidebar.markdown("---")

st.sidebar.markdown("### 🎯 Evaluation")

st.sidebar.write("Confidence — 10")
st.sidebar.write("Communication — 10")
st.sidebar.write("Knowledge — 10")
st.sidebar.write("CV — 10")

st.sidebar.markdown("---")

st.sidebar.html(
    "<b>Maximum Score: 40</b>"
)

# =========================================================
# GET DATA
# =========================================================

df = pd.read_sql_query(
    """
    SELECT *
    FROM students
    ORDER BY
        total_marks DESC,
        percentage DESC,
        student_name ASC
    """,
    conn
)

# =========================================================
# COMMAND CENTER
# =========================================================

if page == "🏠 Command Center":

    st.html("""
    <div class="hero">

        <div class="hero-title">
            🏆 INTERVIEW ARENA
        </div>

        <div class="hero-subtitle">
            Smart Student Interview Evaluation &
            Ranking Dashboard
        </div>

    </div>
    """)

    total_students = len(df)

    if total_students > 0:

        average_marks = df["total_marks"].mean()

        highest_marks = df["total_marks"].max()

        top_student = df.iloc[0]["student_name"]

    else:

        average_marks = 0

        highest_marks = 0

        top_student = "-"

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.html(f"""
        <div class="kpi">

            <div class="kpi-label">
                Total Students
            </div>

            <div class="kpi-value">
                {total_students}
            </div>

            <div class="kpi-small">
                Candidates in database
            </div>

        </div>
        """)

    with c2:

        st.html(f"""
        <div class="kpi">

            <div class="kpi-label">
                Average Score
            </div>

            <div class="kpi-value">
                {average_marks:.1f}/40
            </div>

            <div class="kpi-small">
                Overall batch average
            </div>

        </div>
        """)

    with c3:

        st.html(f"""
        <div class="kpi">

            <div class="kpi-label">
                Highest Score
            </div>

            <div class="kpi-value">
                {highest_marks}/40
            </div>

            <div class="kpi-small">
                Current highest performance
            </div>

        </div>
        """)

    with c4:

        st.html(f"""
        <div class="kpi">

            <div class="kpi-label">
                Top Candidate
            </div>

            <div class="kpi-value"
                 style="font-size:20px;">

                {top_student}

            </div>

            <div class="kpi-small">
                Rank #1
            </div>

        </div>
        """)

    # -----------------------------------------------------
    # TOP 3
    # -----------------------------------------------------

    st.html(
        '<div class="section-title">🥇 TOP 3 PERFORMERS</div>'
    )

    top3 = df.head(3)

    if len(top3) >= 3:

        p1, p2, p3 = st.columns([1, 1.25, 1])

        # SECOND

        with p1:

            row = top3.iloc[1]

            st.html(f"""
            <div class="podium podium-second"
                 style="margin-top:35px;">

                <div class="rank-number">
                    🥈
                </div>

                <div class="rank-name">
                    {row['student_name']}
                </div>

                <div class="rank-score">
                    {row['total_marks']} / 40
                </div>

                <div class="rank-label">
                    2ND PLACE
                </div>

            </div>
            """)

        # FIRST

        with p2:

            row = top3.iloc[0]

            st.html(f"""
            <div class="podium podium-first"
                 style="transform:scale(1.04);">

                <div class="rank-number">
                    👑
                </div>

                <div class="rank-name">
                    {row['student_name']}
                </div>

                <div class="rank-score">
                    {row['total_marks']} / 40
                </div>

                <div class="rank-label">
                    🥇 CHAMPION
                </div>

            </div>
            """)

        # THIRD

        with p3:

            row = top3.iloc[2]

            st.html(f"""
            <div class="podium podium-third"
                 style="margin-top:35px;">

                <div class="rank-number">
                    🥉
                </div>

                <div class="rank-name">
                    {row['student_name']}
                </div>

                <div class="rank-score">
                    {row['total_marks']} / 40
                </div>

                <div class="rank-label">
                    3RD PLACE
                </div>

            </div>
            """)

    # -----------------------------------------------------
    # TOP 10
    # -----------------------------------------------------

    st.html(
        '<div class="section-title">🔥 CURRENT TOP 10</div>'
    )

    leaderboard = df.head(10)

    for index, row in leaderboard.iterrows():

        rank = leaderboard.index.get_loc(index) + 1

        percentage = float(row["percentage"])

        width = min(max(percentage, 0), 100)

        if rank == 1:

            badge = "🥇"

        elif rank == 2:

            badge = "🥈"

        elif rank == 3:

            badge = "🥉"

        else:

            badge = f"#{rank}"

        st.html(f"""
        <div class="leader-card">

            <div style="
                display:flex;
                justify-content:space-between;
                align-items:center;
            ">

                <div>

                    <span style="font-size:20px;">
                        {badge}
                    </span>

                    <span class="leader-name">
                        &nbsp; {row['student_name']}
                    </span>

                </div>

                <div class="score">
                    {row['total_marks']} / 40
                </div>

            </div>

            <div class="progress-bg">

                <div class="progress-fill"
                     style="width:{width}%;">
                </div>

            </div>

            <div style="
                font-size:11px;
                color:#9fa9cc;
                margin-top:5px;
            ">

                {percentage:.1f}%

                &nbsp; • &nbsp;

                {row['remarks']
                if row['remarks']
                else 'No remarks yet'}

            </div>

        </div>
        """)

# =========================================================
# ADD STUDENT
# =========================================================

elif page == "➕ Add Student":

    st.html("""
    <div class="hero">

        <div class="hero-title">
            ➕ ADD STUDENT
        </div>

        <div class="hero-subtitle">
            Add a new candidate to the database
        </div>

    </div>
    """)

    with st.form("add_student_form"):

        name = st.text_input(
            "Student Name"
        )

        st.markdown("### 🎯 Interview Evaluation")

        c1, c2 = st.columns(2)

        with c1:

            confidence = st.number_input(
                "Confidence / 10",
                min_value=0,
                max_value=10,
                value=0
            )

            communication = st.number_input(
                "Communication / 10",
                min_value=0,
                max_value=10,
                value=0
            )

        with c2:

            knowledge = st.number_input(
                "Knowledge / 10",
                min_value=0,
                max_value=10,
                value=0
            )

            CV = st.number_input(
                "CV / 10",
                min_value=0,
                max_value=10,
                value=0
            )

        remarks = st.text_area(
            "Remarks"
        )

        submitted = st.form_submit_button(
            "🚀 Add Student"
        )

        if submitted:

            if name.strip() == "":

                st.error(
                    "Please enter student name."
                )

            else:

                cursor.execute(
                    """
                    SELECT COUNT(*)
                    FROM students
                    WHERE LOWER(student_name)
                    = LOWER(?)
                    """,
                    (name.strip(),)
                )

                duplicate = cursor.fetchone()[0]

                if duplicate > 0:

                    st.warning(
                        "Student with this name already exists."
                    )

                else:

                    total = (
                        confidence
                        + communication
                        + knowledge
                        + CV
                    )

                    percentage = (
                        total / 40
                    ) * 100

                    cursor.execute("""
                    INSERT INTO students
                    (
                        student_name,
                        confidence,
                        communication,
                        knowledge,
                        CV,
                        total_marks,
                        percentage,
                        remarks
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        name.strip(),
                        confidence,
                        communication,
                        knowledge,
                        CV,
                        total,
                        percentage,
                        remarks
                    ))

                    conn.commit()

                    st.success(
                        f"✅ {name} added successfully!"
                    )

                    st.rerun()

# =========================================================
# ALL STUDENTS
# =========================================================

elif page == "📋 All Students":

    st.html("""
    <div class="hero">

        <div class="hero-title">
            📋 ALL STUDENTS
        </div>

        <div class="hero-subtitle">
            Complete interview evaluation records
        </div>

    </div>
    """)

    search = st.text_input(
        "🔎 Search Student"
    )

    display_df = df.copy()

    if search.strip():

        display_df = display_df[
            display_df["student_name"].str.contains(
                search.strip(),
                case=False,
                na=False
            )
        ]

    display_df = display_df[
        [
            "id",
            "student_name",
            "confidence",
            "communication",
            "knowledge",
            "CV",
            "total_marks",
            "percentage",
            "remarks"
        ]
    ].copy()

    display_df.columns = [
        "ID",
        "Student",
        "Confidence",
        "Communication",
        "Knowledge",
        "CV",
        "Total / 40",
        "Percentage",
        "Remarks"
    ]

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

# =========================================================
# UPDATE EVALUATION
# =========================================================

elif page == "✏️ Update Evaluation":

    st.html("""
    <div class="hero">

        <div class="hero-title">
            ✏️ UPDATE EVALUATION
        </div>

        <div class="hero-subtitle">
            Edit marks and remarks of any student
        </div>

    </div>
    """)

    student_options = df["student_name"].tolist()

    if student_options:

        selected_name = st.selectbox(
            "Select Student",
            student_options
        )

        cursor.execute("""
        SELECT
            confidence,
            communication,
            knowledge,
            CV,
            remarks
        FROM students
        WHERE student_name = ?
        """, (selected_name,))

        current = cursor.fetchone()

        current_confidence = current[0]
        current_communication = current[1]
        current_knowledge = current[2]
        current_CV = current[3]
        current_remarks = current[4]

        c1, c2 = st.columns(2)

        with c1:

            confidence = st.number_input(
                "Confidence / 10",
                min_value=0,
                max_value=10,
                value=int(current_confidence),
                key="update_confidence"
            )

            communication = st.number_input(
                "Communication / 10",
                min_value=0,
                max_value=10,
                value=int(current_communication),
                key="update_communication"
            )

        with c2:

            knowledge = st.number_input(
                "Knowledge / 10",
                min_value=0,
                max_value=10,
                value=int(current_knowledge),
                key="update_knowledge"
            )

            CV = st.number_input(
                "CV / 10",
                min_value=0,
                max_value=10,
                value=int(current_CV),
                key="update_CV"
            )

        remarks = st.text_area(
            "Remarks",
            value=current_remarks or "",
            key="update_remarks"
        )

        total = (
            confidence
            + communication
            + knowledge
            + CV
        )

        percentage = (
            total / 40
        ) * 100

        ring_degree = percentage * 3.6

        st.html(f"""
                <div style="
                    text-align:center;
                    margin:25px 0;
                ">

                    <div style="
                        width:155px;
                        height:155px;
                        border-radius:50%;
                        margin:auto;
                        display:flex;
                        align-items:center;
                        justify-content:center;

                        background:conic-gradient(
                            #7c5cff 0deg,
                            #00d9ff {ring_degree}deg,
                            rgba(255,255,255,0.08) {ring_degree}deg,
                            rgba(255,255,255,0.08) 360deg
                        );

                        box-shadow:
                            0 0 25px rgba(0,217,255,0.25),
                            0 0 50px rgba(124,92,255,0.15);
                    ">

                        <div style="
                            width:118px;
                            height:118px;
                            border-radius:50%;
                            background:#090d1d;

                            display:flex;
                            flex-direction:column;
                            align-items:center;
                            justify-content:center;
                        ">

                            <div style="
                                font-size:32px;
                                font-weight:900;
                                color:white;
                            ">
                                {total}/40
                            </div>

                            <div style="
                                font-size:13px;
                                color:#aeb7d9;
                            ">
                                {percentage:.1f}%
                            </div>

                        </div>
                    </div>

                    <div style="
                        margin-top:12px;
                        color:#9fa9cc;
                        font-size:13px;
                        letter-spacing:1px;
                    ">
                        🎯 LIVE SCORE
                    </div>

                </div>
                """)

        if st.button(
            "💾 Save Evaluation",
            use_container_width=True
        ):

            cursor.execute("""
            UPDATE students
            SET
                confidence = ?,
                communication = ?,
                knowledge = ?,
                CV = ?,
                total_marks = ?,
                percentage = ?,
                remarks = ?
            WHERE student_name = ?
            """, (
                confidence,
                communication,
                knowledge,
                CV,
                total,
                percentage,
                remarks,
                selected_name
            ))

            conn.commit()

            st.success(
                "✅ Evaluation updated successfully!"
            )

            st.rerun()

# =========================================================
# DELETE STUDENT
# =========================================================

elif page == "🗑️ Delete Student":

    st.html("""
    <div class="hero">

        <div class="hero-title">
            🗑️ DELETE STUDENT
        </div>

        <div class="hero-subtitle">
            Remove a candidate from the database
        </div>

    </div>
    """)

    student_options = df["student_name"].tolist()

    if student_options:

        selected_name = st.selectbox(
            "Select Student to Delete",
            student_options
        )

        selected_row = df[
            df["student_name"] == selected_name
        ].iloc[0]

        st.warning(
            f"⚠️ You are about to delete "
            f"**{selected_name}** "
            f"with score "
            f"**{selected_row['total_marks']}/40**."
        )

        confirm = st.checkbox(
            "I confirm that I want to delete this student."
        )

        if st.button(
            "🗑️ Delete Student",
            use_container_width=True
        ):

            if confirm:

                cursor.execute(
                    """
                    DELETE FROM students
                    WHERE student_name = ?
                    """,
                    (selected_name,)
                )

                conn.commit()

                st.success(
                    f"✅ {selected_name} deleted successfully!"
                )

                st.rerun()

            else:

                st.error(
                    "Please confirm deletion first."
                )

# =========================================================
# TOP 10 LEADERBOARD
# =========================================================

elif page == "🏆 Top 10 Leaderboard":

    st.html("""
    <div class="hero">

        <div class="hero-title">
            🏆 TOP 10 LEADERBOARD
        </div>

        <div class="hero-subtitle">
            Students ranked automatically by total marks
        </div>

    </div>
    """)

    top10 = df.sort_values(
        by=[
            "total_marks",
            "percentage",
            "student_name"
        ],
        ascending=[
            False,
            False,
            True
        ]
    ).head(10).reset_index(drop=True)

    for i, row in top10.iterrows():

        rank = i + 1

        percentage = float(
            row["percentage"]
        )

        width = min(
            max(percentage, 0),
            100
        )

        if rank == 1:

            badge = "🥇"

        elif rank == 2:

            badge = "🥈"

        elif rank == 3:

            badge = "🥉"

        else:

            badge = f"#{rank}"

        st.html(f"""
        <div class="leader-card">

            <div style="
                display:flex;
                justify-content:space-between;
            ">

                <div>

                    <span style="font-size:23px;">
                        {badge}
                    </span>

                    <span class="leader-name">
                        &nbsp; {row['student_name']}
                    </span>

                </div>

                <div class="score">
                    {row['total_marks']} / 40
                </div>

            </div>

            <div class="progress-bg">

                <div class="progress-fill"
                     style="width:{width}%;">
                </div>

            </div>

            <div style="
                display:flex;
                justify-content:space-between;
                color:#9fa9cc;
                font-size:12px;
                margin-top:7px;
            ">

                <span>
                    {percentage:.1f}%
                </span>

                <span>
                    C: {row['confidence']}
                    |
                    Com: {row['communication']}
                    |
                    K: {row['knowledge']}
                    |
                    CV: {row['CV']}
                </span>

            </div>

            <div style="
                color:#aeb7d9;
                font-size:12px;
                margin-top:5px;
            ">

                📝
                {row['remarks']
                if row['remarks']
                else 'No remarks'}

            </div>

        </div>
        """)

# =========================================================
# ANALYTICS
# =========================================================

elif page == "📊 Analytics":

    st.html("""
    <div class="hero">

        <div class="hero-title">
            📊 PERFORMANCE ANALYTICS
        </div>

        <div class="hero-subtitle">
            Visual analysis of interview performance
        </div>

    </div>
    """)

    category_data = pd.DataFrame({

        "Category": [
            "Confidence",
            "Communication",
            "Knowledge",
            "CV"
        ],

        "Average Marks": [
            df["confidence"].mean(),
            df["communication"].mean(),
            df["knowledge"].mean(),
            df["CV"].mean()
        ]
    })

    fig1 = px.bar(
        category_data,
        x="Category",
        y="Average Marks",
        range_y=[0, 10],
        text_auto=".1f",
        title="Average Marks by Category"
    )

    fig1.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#EAF0FF"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    score_data = df.sort_values(
        "total_marks",
        ascending=False
    ).head(10)

    fig2 = px.bar(
        score_data,
        x="student_name",
        y="total_marks",
        range_y=[0, 40],
        text="total_marks",
        title="Top 10 Student Scores"
    )

    fig2.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#EAF0FF",
        xaxis_title="Student",
        yaxis_title="Total Marks"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    st.html(
        '<div class="section-title">'
        '📌 SCORE SUMMARY'
        '</div>'
    )

    score_summary = pd.DataFrame({

        "Student":
            df["student_name"],

        "Total Score":
            df["total_marks"],

        "Percentage":
            df["percentage"]
    })

    st.dataframe(
        score_summary,
        use_container_width=True,
        hide_index=True
    )

# =========================================================
# END
# =========================================================

conn.close()