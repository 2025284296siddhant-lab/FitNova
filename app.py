import streamlit as st
import pandas as pd


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Smart Fitness Assistant",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# LOAD EXERCISE DATABASE
# ============================================================

try:
    exercises = pd.read_csv("exercises.csv")

except FileNotFoundError:
    st.error(
        "exercises.csv was not found. "
        "Make sure exercises.csv is in the same folder as app.py."
    )
    st.stop()


# ============================================================
# CLEAN DATABASE
# ============================================================

exercises.columns = exercises.columns.str.strip()

text_columns = [
    "Exercise",
    "Muscle",
    "Goal",
    "Level",
    "Equipment",
    "Workout_Type",
    "Instructions"
]

for column in text_columns:

    if column in exercises.columns:

        exercises[column] = (
            exercises[column]
            .astype(str)
            .str.strip()
        )


# ============================================================
# SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "fitness_result" not in st.session_state:
    st.session_state.fitness_result = None

if "workout_plan" not in st.session_state:
    st.session_state.workout_plan = None

if "user_name" not in st.session_state:
    st.session_state.user_name = ""


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       MAIN APPLICATION
       ======================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 85% 8%,
                rgba(0, 191, 255, 0.055),
                transparent 28%
            ),
            radial-gradient(
                circle at 10% 90%,
                rgba(0, 191, 255, 0.025),
                transparent 30%
            ),
            #080a0c;

        color: #e8edf0;
    }


    .block-container {
        max-width: 1380px;
        padding-top: 1.8rem;
        padding-bottom: 5rem;
    }


    /* ========================================================
       TEXT
       ======================================================== */

    h1 {
        color: #f1f5f7 !important;
        font-size: 48px !important;
        font-weight: 800 !important;
        letter-spacing: -1.8px !important;
        line-height: 1.08 !important;
    }


    h2 {
        color: #edf2f4 !important;
        font-size: 30px !important;
        font-weight: 750 !important;
        letter-spacing: -0.5px !important;
    }


    h3 {
        color: #e9eef1 !important;
        font-size: 20px !important;
        font-weight: 700 !important;
    }


    p {
        color: #8f9aa2;
        line-height: 1.75;
    }


    .main-brand {
        color: #00bfff !important;

        font-size: 13px !important;

        font-weight: 850 !important;

        letter-spacing: 3px !important;

        text-shadow:
            0 0 8px rgba(0, 191, 255, 0.65),
            0 0 20px rgba(0, 191, 255, 0.18);

        margin-bottom: 22px !important;
    }


    .section-label {
        color: #00bfff !important;

        font-size: 11px !important;

        font-weight: 800 !important;

        letter-spacing: 2px !important;

        text-transform: uppercase;

        margin-bottom: 5px !important;
    }


    /* ========================================================
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] {

        background:
            linear-gradient(
                180deg,
                #101316 0%,
                #0a0c0e 100%
            );

        border-right: 1px solid #252b30;
    }


    section[data-testid="stSidebar"] > div {
        padding: 1.4rem 1rem;
    }


    section[data-testid="stSidebar"] h2 {

        color: #00bfff !important;

        font-size: 20px !important;

        line-height: 1.55 !important;

        font-weight: 850 !important;

        letter-spacing: 2px !important;

        text-shadow:
            0 0 8px rgba(0, 191, 255, 0.65),
            0 0 20px rgba(0, 191, 255, 0.18);
    }


    section[data-testid="stSidebar"] p {
        color: #69757d !important;
    }


    section[data-testid="stSidebar"] hr {
        border-color: #252b30 !important;
    }


    section[data-testid="stSidebar"] label {
        color: #657078 !important;
        font-size: 10px !important;
        font-weight: 750 !important;
        letter-spacing: 1.7px !important;
    }


    section[data-testid="stSidebar"]
    div[role="radiogroup"] label {

        background: transparent;

        border-radius: 9px;

        padding: 9px 10px;

        margin: 4px 0;

        border-left: 2px solid transparent;
    }


    section[data-testid="stSidebar"]
    div[role="radiogroup"] label:hover {

        background: #171b1f;
    }


    section[data-testid="stSidebar"]
    div[role="radiogroup"] label p {

        color: #a8b2b8 !important;

        font-size: 14px !important;

        font-weight: 500 !important;
    }


    section[data-testid="stSidebar"]
    div[role="radiogroup"] label:has(
        input:checked
    ) {

        background:
            linear-gradient(
                90deg,
                rgba(0, 191, 255, 0.13),
                rgba(0, 191, 255, 0.02)
            );

        border-left-color: #00bfff;
    }


    section[data-testid="stSidebar"]
    div[role="radiogroup"] label:has(
        input:checked
    ) p {

        color: #00bfff !important;

        font-weight: 700 !important;
    }


    /* ========================================================
       BUTTONS
       ======================================================== */

    .stButton > button {

        background:
            linear-gradient(
                135deg,
                #00bfff,
                #009bd7
            ) !important;

        color: #071116 !important;

        border: none !important;

        border-radius: 10px !important;

        min-height: 50px;

        padding: 0 25px;

        font-size: 15px !important;

        font-weight: 800 !important;

        box-shadow:
            0 8px 25px rgba(0, 191, 255, 0.20);
    }


    .stButton > button p,
    .stButton > button span {

        color: #071116 !important;

        font-weight: 800 !important;
    }


    .stButton > button:hover {

        background:
            linear-gradient(
                135deg,
                #19c9ff,
                #00a8e8
            ) !important;

        transform: translateY(-2px);

        box-shadow:
            0 12px 32px rgba(0, 191, 255, 0.35);
    }


    /* ========================================================
       CONTAINERS / CARDS
       ======================================================== */

    [data-testid="stVerticalBlockBorderWrapper"] {

        background:
            linear-gradient(
                145deg,
                #15191d,
                #111416
            ) !important;

        border: 1px solid #292f35 !important;

        border-radius: 15px !important;

        box-shadow:
            0 12px 30px rgba(0, 0, 0, 0.20) !important;
    }


    /* ========================================================
       IMAGES
       ======================================================== */

    [data-testid="stImage"] img {

        border-radius: 14px !important;

        border: 1px solid #293138 !important;
    }


    /* ========================================================
       METRICS
       ======================================================== */

    [data-testid="stMetric"] {

        background:
            linear-gradient(
                145deg,
                #171b1f,
                #121517
            );

        border: 1px solid #292f34;

        border-radius: 14px;

        padding: 17px;
    }


    [data-testid="stMetricLabel"] {

        color: #707c84 !important;

        font-size: 10px !important;

        text-transform: uppercase;

        letter-spacing: 1px;
    }


    [data-testid="stMetricValue"] {

        color: #00bfff !important;

        font-weight: 750 !important;
    }


    /* ========================================================
       INPUTS
       ======================================================== */

    .stTextInput input,
    .stNumberInput input {

        background: #15191c !important;

        color: #e9eef1 !important;

        border: 1px solid #30383e !important;

        border-radius: 9px !important;
    }


    .stSelectbox div[data-baseweb="select"] > div {

        background: #15191c !important;

        color: #e9eef1 !important;

        border: 1px solid #30383e !important;

        border-radius: 9px !important;
    }


    /* ========================================================
       DIVIDERS
       ======================================================== */

    hr {

        border-color: #242a2f !important;

        margin: 30px 0 !important;
    }


    /* ========================================================
       ALERTS
       ======================================================== */

    .stAlert {

        background: #15191c !important;

        border: 1px solid #2c343a !important;
    }


    /* ========================================================
       MOBILE
       ======================================================== */

    @media (max-width: 900px) {

        .block-container {

            padding-left: 1rem;

            padding-right: 1rem;
        }

        h1 {

            font-size: 36px !important;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# WORKOUT GENERATOR
# ============================================================

def generate_workout(
    goal,
    level,
    equipment,
    workout_days
):

    # --------------------------------------------------------
    # 1. FILTER BY GOAL
    # --------------------------------------------------------

    filtered = exercises[
        exercises["Goal"] == goal
    ].copy()


    # --------------------------------------------------------
    # 2. FILTER BY EXPERIENCE LEVEL
    # --------------------------------------------------------

    filtered = filtered[
        filtered["Level"] == level
    ].copy()


    # --------------------------------------------------------
    # 3. FILTER BY EQUIPMENT
    # --------------------------------------------------------

    if equipment == "No Equipment":

        filtered = filtered[
            filtered["Equipment"] == "No Equipment"
        ]


    elif equipment == "Dumbbells":

        filtered = filtered[
            filtered["Equipment"].isin(
                [
                    "No Equipment",
                    "Dumbbells"
                ]
            )
        ]


    elif equipment == "Barbell":

        filtered = filtered[
            filtered["Equipment"].isin(
                [
                    "No Equipment",
                    "Barbell"
                ]
            )
        ]


    elif equipment == "Full Gym":

        filtered = filtered[
            filtered["Equipment"].isin(
                [
                    "No Equipment",
                    "Dumbbells",
                    "Barbell",
                    "Full Gym"
                ]
            )
        ]


    # --------------------------------------------------------
    # 4. CHECK FOR NO RESULTS
    # --------------------------------------------------------

    if filtered.empty:

        return {
            "error":
            "No suitable exercises were found for "
            "your selected goal, level and equipment."
        }


    # --------------------------------------------------------
    # 5. CLEAN EXERCISE NAMES
    # --------------------------------------------------------

    filtered["Exercise"] = (
        filtered["Exercise"]
        .astype(str)
        .str.strip()
    )


    # --------------------------------------------------------
    # 6. REMOVE DUPLICATE EXERCISES
    # --------------------------------------------------------

    filtered = filtered.drop_duplicates(
        subset=["Exercise"],
        keep="first"
    ).reset_index(drop=True)


    # --------------------------------------------------------
    # 7. FOUR EXERCISES PER DAY
    # --------------------------------------------------------

    exercises_per_day = 4

    total_required = (
        workout_days *
        exercises_per_day
    )


    # --------------------------------------------------------
    # 8. CHECK WHETHER DATABASE HAS ENOUGH VARIETY
    # --------------------------------------------------------

    if len(filtered) < exercises_per_day:

        return {
            "error":
            f"Only {len(filtered)} suitable exercise(s) "
            f"are available. At least 4 different exercises "
            f"are needed for each workout day."
        }


    # --------------------------------------------------------
    # 9. RANDOMIZE EXERCISE DATABASE
    # --------------------------------------------------------

    shuffled = filtered.sample(
        frac=1
    ).reset_index(drop=True)


    # --------------------------------------------------------
    # 10. WEEKLY PLAN
    # --------------------------------------------------------

    day_names = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday"
    ]


    plan = {}


    # ========================================================
    # CASE 1
    #
    # Enough exercises exist for the WHOLE WEEK.
    #
    # Example:
    #
    # 3 days × 4 exercises = 12 exercises
    #
    # If database has 16 exercises,
    # we can use 12 different exercises.
    # ========================================================

    if len(shuffled) >= total_required:

        selected = shuffled.head(
            total_required
        ).copy()


        for day_index in range(workout_days):

            start = (
                day_index *
                exercises_per_day
            )

            end = (
                start +
                exercises_per_day
            )


            daily_workout = selected.iloc[
                start:end
            ].copy()


            daily_workout = (
                daily_workout
                .drop_duplicates(
                    subset=["Exercise"]
                )
                .reset_index(drop=True)
            )


            plan[
                day_names[day_index]
            ] = daily_workout


    # ========================================================
    # CASE 2
    #
    # Not enough exercises for the entire week.
    #
    # We still guarantee:
    #
    # - 4 different exercises per day
    # - no duplicate exercise within a day
    #
    # Some exercises may appear again on another day.
    # ========================================================

    else:

        used_names = set()


        for day_index in range(workout_days):

            # First choose exercises not recently used.

            fresh = shuffled[
                ~shuffled["Exercise"].isin(
                    used_names
                )
            ].copy()


            # If fewer than 4 fresh exercises remain,
            # start with the complete pool again.

            if len(fresh) < exercises_per_day:

                fresh = shuffled.copy()


            # Shuffle again.

            fresh = fresh.sample(
                frac=1
            ).reset_index(drop=True)


            # Select four.

            daily_workout = fresh.head(
                exercises_per_day
            ).copy()


            # Final duplicate protection.

            daily_workout = (
                daily_workout
                .drop_duplicates(
                    subset=["Exercise"],
                    keep="first"
                )
                .reset_index(drop=True)
            )


            # Safety check.

            if len(daily_workout) < exercises_per_day:

                return {
                    "error":
                    "There are not enough unique exercises "
                    "in the database to build this workout."
                }


            # Add names to used list.

            for exercise_name in daily_workout[
                "Exercise"
            ]:

                used_names.add(
                    exercise_name
                )


            plan[
                day_names[day_index]
            ] = daily_workout


    # --------------------------------------------------------
    # RETURN PLAN
    # --------------------------------------------------------

    return plan


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        "## SMART FITNESS ASSISTANT"
    )

    st.caption(
        "PERSONAL FITNESS INTELLIGENCE"
    )

    st.divider()


    navigation = [
        "Home",
        "Create Workout",
        "My Workout",
        "Progress",
        "About"
    ]


    current_index = navigation.index(
        st.session_state.page
    )


    selected_page = st.radio(
        "NAVIGATION",
        navigation,
        index=current_index
    )


    if selected_page != st.session_state.page:

        st.session_state.page = selected_page

        st.rerun()


    st.divider()


    st.caption(
        "SMART FITNESS ASSISTANT"
    )

    st.caption(
        "Python • Streamlit • Pandas"
    )


# ============================================================
# HOME
# ============================================================

if st.session_state.page == "Home":

    st.markdown(
        '<p class="main-brand">'
        'SMART FITNESS ASSISTANT'
        '</p>',
        unsafe_allow_html=True
    )


    left, right = st.columns(
        [1.1, 1],
        gap="large"
    )


    with left:

        with st.container(
            border=True
        ):

            st.markdown(
                '<p class="section-label">'
                'PERSONALIZED FITNESS PLANNING'
                '</p>',
                unsafe_allow_html=True
            )


            st.title(
                "Train smarter."
            )


            st.subheader(
                "Build your plan."
            )


            st.write(
                "Create a personalized workout plan "
                "based on your goals, experience level "
                "and available equipment."
            )


            st.write("")


            if st.button(
                "Create My Workout",
                type="primary",
                key="home_create"
            ):

                st.session_state.page = (
                    "Create Workout"
                )

                st.rerun()


    with right:

        st.image(
            "https://images.unsplash.com/"
            "photo-1534438327276-14e5300c3a48"
            "?auto=format&fit=crop&w=1200&q=90",
            use_container_width=True
        )


        image_left, image_right = st.columns(
            2,
            gap="medium"
        )


        with image_left:

            st.image(
                "https://images.unsplash.com/"
                "photo-1581009146145-b5ef050c2e1e"
                "?auto=format&fit=crop&w=700&q=85",
                use_container_width=True
            )


        with image_right:

            st.image(
                "https://images.unsplash.com/"
                "photo-1583454110551-21f2fa2afe61"
                "?auto=format&fit=crop&w=700&q=85",
                use_container_width=True
            )


    st.divider()


    st.markdown(
        '<p class="section-label">'
        'THE PLATFORM'
        '</p>',
        unsafe_allow_html=True
    )


    stat1, stat2, stat3, stat4 = st.columns(
        4
    )


    with stat1:

        st.metric(
            "Personalized",
            "100%"
        )


    with stat2:

        st.metric(
            "Exercise Library",
            f"{len(exercises)}+"
        )


    with stat3:

        st.metric(
            "Training Goals",
            "4"
        )


    with stat4:

        st.metric(
            "Workout Builder",
            "Active"
        )


    st.divider()


    st.markdown(
        '<p class="section-label">'
        'THE SMARTER WAY TO TRAIN'
        '</p>',
        unsafe_allow_html=True
    )


    st.header(
        "Everything organized around your goals."
    )


    feature1, feature2, feature3 = st.columns(
        3,
        gap="large"
    )


    with feature1:

        with st.container(border=True):

            st.image(
                "https://images.unsplash.com/"
                "photo-1538805060514-97d9cc17730c"
                "?auto=format&fit=crop&w=700&q=85",
                use_container_width=True
            )

            st.subheader(
                "Personalized Planning"
            )

            st.write(
                "The system considers your goal, "
                "experience level, equipment and "
                "training frequency."
            )


    with feature2:

        with st.container(border=True):

            st.image(
                "https://images.unsplash.com/"
                "photo-1517836357463-d25dfeac3438"
                "?auto=format&fit=crop&w=700&q=85",
                use_container_width=True
            )

            st.subheader(
                "Smart Recommendations"
            )

            st.write(
                "Python filters the exercise database "
                "and selects exercises that match "
                "your training preferences."
            )


    with feature3:

        with st.container(border=True):

            st.image(
                "https://images.unsplash.com/"
                "photo-1461896836934-ffe607ba8211"
                "?auto=format&fit=crop&w=700&q=85",
                use_container_width=True
            )

            st.subheader(
                "Progress Ready"
            )

            st.write(
                "The project is prepared for workout "
                "history and progress tracking."
            )


    st.divider()


    st.markdown(
        '<p class="section-label">'
        'HOW IT WORKS'
        '</p>',
        unsafe_allow_html=True
    )


    st.header(
        "From your inputs to a structured plan."
    )


    step1, step2, step3 = st.columns(
        3,
        gap="large"
    )


    with step1:

        with st.container(border=True):

            st.caption("01")

            st.subheader(
                "Tell us about you"
            )

            st.write(
                "Enter your basic information, "
                "fitness goal, experience level, "
                "available equipment and training "
                "frequency."
            )


    with step2:

        with st.container(border=True):

            st.caption("02")

            st.subheader(
                "Smart filtering"
            )

            st.write(
                "The recommendation engine filters "
                "the exercise database according "
                "to your selections."
            )


    with step3:

        with st.container(border=True):

            st.caption("03")

            st.subheader(
                "Your plan"
            )

            st.write(
                "The selected exercises are organized "
                "into a weekly workout plan."
            )


# ============================================================
# CREATE WORKOUT
# ============================================================

elif st.session_state.page == "Create Workout":

    st.markdown(
        '<p class="main-brand">'
        'WORKOUT BUILDER'
        '</p>',
        unsafe_allow_html=True
    )


    st.title(
        "Create your personalized workout."
    )


    st.write(
        "Enter your information and training "
        "preferences. The recommendation engine "
        "will generate a structured workout plan."
    )


    st.divider()


    st.markdown(
        '<p class="section-label">'
        'PERSONAL INFORMATION'
        '</p>',
        unsafe_allow_html=True
    )


    st.header(
        "Tell us about yourself."
    )


    col1, col2 = st.columns(
        2,
        gap="large"
    )


    with col1:

        name = st.text_input(
            "Name",
            value=st.session_state.user_name
        )


        age = st.number_input(
            "Age",
            min_value=10,
            max_value=100,
            value=20
        )


        sex = st.selectbox(
            "Sex",
            [
                "Male",
                "Female"
            ]
        )


    with col2:

        height = st.number_input(
            "Height (cm)",
            min_value=50.0,
            max_value=250.0,
            value=170.0
        )


        weight = st.number_input(
            "Weight (kg)",
            min_value=20.0,
            max_value=250.0,
            value=65.0
        )


        activity = st.selectbox(
            "Activity Level",
            [
                "Sedentary",
                "Lightly Active",
                "Moderately Active",
                "Very Active",
                "Extra Active"
            ]
        )


    st.divider()


    st.markdown(
        '<p class="section-label">'
        'TRAINING PREFERENCES'
        '</p>',
        unsafe_allow_html=True
    )


    st.header(
        "Define your training."
    )


    col1, col2 = st.columns(
        2,
        gap="large"
    )


    with col1:

        goal = st.selectbox(
            "Fitness Goal",
            [
                "General Fitness",
                "Muscle Gain",
                "Strength",
                "Weight Loss"
            ]
        )


        level = st.selectbox(
            "Experience Level",
            [
                "Beginner",
                "Intermediate"
            ]
        )


    with col2:

        equipment = st.selectbox(
            "Available Equipment",
            [
                "No Equipment",
                "Dumbbells",
                "Barbell",
                "Full Gym"
            ]
        )


        workout_days = st.selectbox(
            "Workout Days Per Week",
            [
                2,
                3,
                4,
                5,
                6
            ]
        )


    st.write("")


    if st.button(
        "Generate Personalized Workout",
        type="primary",
        key="generate_workout"
    ):

        # ====================================================
        # BMI
        # ====================================================

        height_m = height / 100

        bmi = weight / (
            height_m ** 2
        )


        if bmi < 18.5:

            bmi_category = "Underweight"

        elif bmi < 25:

            bmi_category = "Normal"

        elif bmi < 30:

            bmi_category = "Overweight"

        else:

            bmi_category = "Obese"


        # ====================================================
        # BMR
        # ====================================================

        if sex == "Male":

            bmr = (
                (10 * weight)
                + (6.25 * height)
                - (5 * age)
                + 5
            )

        else:

            bmr = (
                (10 * weight)
                + (6.25 * height)
                - (5 * age)
                - 161
            )


        # ====================================================
        # CALORIE ESTIMATE
        # ====================================================

        activity_factor = {

            "Sedentary": 1.2,

            "Lightly Active": 1.375,

            "Moderately Active": 1.55,

            "Very Active": 1.725,

            "Extra Active": 1.9
        }


        calories = (
            bmr *
            activity_factor[activity]
        )


        # ====================================================
        # GENERATE WORKOUT
        # ====================================================

        workout_plan = generate_workout(
            goal,
            level,
            equipment,
            workout_days
        )


        # ====================================================
        # HANDLE ERROR
        # ====================================================

        if (
            isinstance(workout_plan, dict)
            and "error" in workout_plan
        ):

            st.error(
                workout_plan["error"]
            )


            st.info(
                "Try another equipment option or "
                "add more suitable exercises to "
                "exercises.csv."
            )


        else:

            st.session_state.user_name = name


            st.session_state.fitness_result = {

                "bmi": bmi,

                "bmi_category": bmi_category,

                "calories": calories,

                "age": age,

                "height": height,

                "weight": weight,

                "activity": activity,

                "goal": goal,

                "level": level,

                "equipment": equipment,

                "workout_days": workout_days
            }


            st.session_state.workout_plan = (
                workout_plan
            )


            st.success(
                "Your personalized workout has been generated."
            )


            st.info(
                "Open My Workout to view your complete plan."
            )


# ============================================================
# MY WORKOUT
# ============================================================

elif st.session_state.page == "My Workout":

    st.markdown(
        '<p class="main-brand">'
        'PERSONAL WORKOUT'
        '</p>',
        unsafe_allow_html=True
    )


    st.title(
        "Your training plan."
    )


    result = st.session_state.fitness_result

    plan = st.session_state.workout_plan


    if result is None:

        with st.container(border=True):

            st.subheader(
                "No workout generated yet."
            )

            st.write(
                "Open Create Workout and generate "
                "your personalized plan first."
            )


    else:

        if st.session_state.user_name:

            st.write(
                f"Personalized plan for "
                f"**{st.session_state.user_name}**."
            )


        # ----------------------------------------------------
        # SUMMARY
        # ----------------------------------------------------

        c1, c2, c3, c4 = st.columns(4)


        with c1:

            st.metric(
                "BMI",
                f'{result["bmi"]:.1f}'
            )


        with c2:

            st.metric(
                "Goal",
                result["goal"]
            )


        with c3:

            st.metric(
                "Training Days",
                result["workout_days"]
            )


        with c4:

            st.metric(
                "Estimated Calories",
                f'{result["calories"]:.0f}'
            )


        st.divider()


        # ----------------------------------------------------
        # WORKOUT DAYS
        # ----------------------------------------------------

        for day, workout in plan.items():

            st.header(
                day
            )


            # ------------------------------------------------
            # EXERCISES
            # ------------------------------------------------

            for _, exercise in workout.iterrows():

                with st.container(
                    border=True
                ):

                    st.subheader(
                        exercise["Exercise"]
                    )


                    st.caption(
                        f'Target muscle: '
                        f'{exercise["Muscle"]}'
                    )


                    c1, c2, c3 = st.columns(3)


                    with c1:

                        st.metric(
                            "Sets",
                            exercise["Sets"]
                        )


                    with c2:

                        st.metric(
                            "Repetitions",
                            exercise["Reps"]
                        )


                    with c3:

                        st.metric(
                            "Rest",
                            f'{exercise["Rest"]} sec'
                        )


                    st.write(
                        f'**Instructions:** '
                        f'{exercise["Instructions"]}'
                    )


            st.divider()


# ============================================================
# PROGRESS
# ============================================================

elif st.session_state.page == "Progress":

    st.markdown(
        '<p class="main-brand">'
        'PERFORMANCE'
        '</p>',
        unsafe_allow_html=True
    )


    st.title(
        "Progress dashboard."
    )


    st.write(
        "Your future workout history and performance "
        "tracking dashboard."
    )


    st.divider()


    c1, c2, c3 = st.columns(3)


    with c1:

        st.metric(
            "Workouts Completed",
            "0"
        )


    with c2:

        st.metric(
            "Current Streak",
            "0"
        )


    with c3:

        st.metric(
            "Weekly Activity",
            "0"
        )


    st.write("")


    with st.container(border=True):

        st.markdown(
            '<p class="section-label">'
            'COMING NEXT'
            '</p>',
            unsafe_allow_html=True
        )


        st.subheader(
            "Progress tracking"
        )


        st.write(
            "SQLite can be added in the next phase "
            "to store workout history and user progress. "
            "Matplotlib can then be used to visualize "
            "progress over time."
        )


# ============================================================
# ABOUT
# ============================================================

elif st.session_state.page == "About":

    st.markdown(
        '<p class="main-brand">'
        'SYSTEM INFORMATION'
        '</p>',
        unsafe_allow_html=True
    )


    st.title(
        "Smart Fitness Assistant."
    )


    st.write(
        "A Python-based personalized workout "
        "recommendation system."
    )


    st.divider()


    col1, col2 = st.columns(
        2,
        gap="large"
    )


    with col1:

        with st.container(border=True):

            st.markdown(
                '<p class="section-label">'
                'PROJECT OBJECTIVE'
                '</p>',
                unsafe_allow_html=True
            )


            st.header(
                "Personalized fitness planning."
            )


            st.write(
                "The application uses user preferences, "
                "training experience and available "
                "equipment to generate a structured "
                "workout recommendation."
            )


    with col2:

        with st.container(border=True):

            st.markdown(
                '<p class="section-label">'
                'TECHNOLOGY'
                '</p>',
                unsafe_allow_html=True
            )


            st.header(
                "Technology stack."
            )


            st.write(
                "Python"
            )


            st.write(
                "Streamlit"
            )


            st.write(
                "Pandas"
            )


            st.write(
                "CSV Exercise Database"
            )


    st.divider()


    st.markdown(
        '<p class="section-label">'
        'SYSTEM ARCHITECTURE'
        '</p>',
        unsafe_allow_html=True
    )


    st.header(
        "From input to recommendation."
    )


    architecture1, architecture2 = st.columns(
        2,
        gap="large"
    )


    with architecture1:

        with st.container(border=True):

            st.subheader(
                "Input Layer"
            )


            st.write(
                "User information, fitness goal, "
                "experience level, equipment and "
                "training frequency."
            )


            st.subheader(
                "Analysis Layer"
            )


            st.write(
                "BMI and estimated daily energy "
                "requirements are calculated."
            )


    with architecture2:

        with st.container(border=True):

            st.subheader(
                "Recommendation Layer"
            )


            st.write(
                "The exercise database is filtered "
                "according to the selected preferences."
            )


            st.subheader(
                "Output Layer"
            )


            st.write(
                "A structured weekly workout plan "
                "is generated and displayed."
            )