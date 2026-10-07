import streamlit as st
import joblib
import os
import re
import plotly.graph_objects as go


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="TruthLens AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

/* =====================================================
   MAIN BACKGROUND
===================================================== */

.stApp {
    background:
        radial-gradient(
            circle at 8% 8%,
            rgba(124, 58, 237, 0.13),
            transparent 30%
        ),
        radial-gradient(
            circle at 92% 12%,
            rgba(34, 197, 94, 0.12),
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #EAF8FF,
            #DDF4FF,
            #F5FBFF
        );

    color: #172033;
}


/* =====================================================
   HIDE STREAMLIT DEFAULT
===================================================== */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}


/* =====================================================
   MAIN CONTAINER
===================================================== */

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}


/* =====================================================
   HERO
===================================================== */

.hero {
    text-align: center;
    padding: 45px 20px 30px;
}

.brand {
    font-size: 18px;
    font-weight: 800;
    letter-spacing: 3px;
    margin-bottom: 15px;

    background: linear-gradient(
        90deg,
        #7C3AED,
        #16A34A
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-title {
    font-size: 58px;
    line-height: 1.05;
    font-weight: 850;
    margin: 0;

    background: linear-gradient(
        90deg,
        #172033,
        #6D28D9,
        #15803D
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    max-width: 720px;
    margin: 20px auto 0;

    color: #526174;

    font-size: 18px;
    line-height: 1.6;
}

.status {
    display: inline-block;

    margin-top: 25px;

    padding: 9px 17px;

    border: 1px solid rgba(22, 163, 74, 0.35);

    border-radius: 999px;

    background: rgba(34, 197, 94, 0.10);

    color: #15803D;

    font-size: 13px;
    font-weight: 700;

    box-shadow:
        0 5px 20px rgba(34, 197, 94, 0.10);
}


/* =====================================================
   SECTION TITLES
===================================================== */

.section-title {
    font-size: 22px;
    font-weight: 750;

    margin-top: 25px;
    margin-bottom: 12px;

    color: #000000 !important;
}


/* =====================================================
   TEXT AREA
===================================================== */

textarea {
    background: #FFFFFF !important;

    color: #172033 !important;

    border: 1px solid rgba(124, 58, 237, 0.25) !important;

    border-radius: 14px !important;

    box-shadow:
        0 5px 20px rgba(50, 100, 150, 0.08);
}

textarea:focus {
    border: 1px solid #7C3AED !important;

    box-shadow:
        0 0 0 1px #7C3AED !important;
}


/* =====================================================
   BUTTON
===================================================== */

.stButton > button {
    width: 100%;

    border: none;

    border-radius: 12px;

    padding: 14px 20px;

    font-size: 16px;

    font-weight: 750;

    color: #FFFFFF !important;

    background: linear-gradient(
        90deg,
        #7C3AED,
        #8B5CF6,
        #16A34A
    );

    transition: all 0.25s ease;

    box-shadow:
        0 8px 25px rgba(124, 58, 237, 0.20);
}

.stButton > button:hover {
    transform: translateY(-2px);

    box-shadow:
        0 12px 30px rgba(124, 58, 237, 0.28);
}


/* =====================================================
   RESULT BOX
===================================================== */

.result-box {
    padding: 27px;

    border-radius: 18px;

    margin-top: 25px;

    background: rgba(255, 255, 255, 0.90);

    border: 1px solid rgba(124, 58, 237, 0.18);

    box-shadow:
        0 10px 35px rgba(50, 100, 150, 0.10);
}

.result-title {
    font-size: 28px;

    font-weight: 850;

    margin-bottom: 8px;

    color: #000000 !important;
}

.confidence {
    font-size: 18px;

    color: #000000 !important;
}

.confidence strong {
    color: #000000 !important;
}


/* =====================================================
   SOURCE CARDS
===================================================== */

.source-card {
    padding: 18px;

    border-radius: 15px;

    background: rgba(255, 255, 255, 0.95);

    border: 1px solid rgba(124, 58, 237, 0.12);

    box-shadow:
        0 7px 22px rgba(50, 100, 150, 0.08);

    text-align: center;

    min-height: 120px;
}


/* ALL SOURCE CARD TEXT BLACK */

.source-card,
.source-card *,
.source-name,
.source-percent,
.source-label {
    color: #000000 !important;
}


/* SOURCE NAME */

.source-name {
    font-size: 17px;

    font-weight: 750;

    margin-bottom: 7px;
}


/* SOURCE PERCENTAGE */

.source-percent {
    font-size: 25px;

    font-weight: 850;
}


/* SOURCE LABEL */

.source-label {
    font-size: 12px;
}


/* =====================================================
   METRICS / ANALYSIS DETAILS
===================================================== */

[data-testid="stMetric"],
[data-testid="stMetric"] *,
[data-testid="stMetricLabel"],
[data-testid="stMetricValue"],
[data-testid="stMetricDelta"] {
    color: #000000 !important;
}

[data-testid="stMetric"] {
    background:
        rgba(255, 255, 255, 0.90);

    padding: 18px;

    border-radius: 14px;

    border: 1px solid
        rgba(124, 58, 237, 0.12);

    box-shadow:
        0 6px 20px
        rgba(50, 100, 150, 0.08);
}


/* =====================================================
   PLOTLY GRAPH TEXT BLACK
===================================================== */

.js-plotly-plot text {
    fill: #000000 !important;
}

.js-plotly-plot .gtitle {
    fill: #000000 !important;
}

.js-plotly-plot .xtick text {
    fill: #000000 !important;
}

.js-plotly-plot .ytick text {
    fill: #000000 !important;
}

.js-plotly-plot .xtitle {
    fill: #000000 !important;
}

.js-plotly-plot .ytitle {
    fill: #000000 !important;
}

.js-plotly-plot .legend text {
    fill: #000000 !important;
}

.js-plotly-plot .textpoint {
    fill: #000000 !important;
}


/* =====================================================
   INFO / WARNING BOX TEXT BLACK
===================================================== */

[data-testid="stAlert"] {
    color: #000000 !important;
}

[data-testid="stAlert"] * {
    color: #000000 !important;
}


/* =====================================================
   FEATURE CARDS
===================================================== */

.feature-card {
    padding: 23px;

    border-radius: 16px;

    background:
        rgba(255, 255, 255, 0.88);

    border:
        1px solid rgba(124, 58, 237, 0.12);

    min-height: 145px;

    transition: 0.25s ease;

    box-shadow:
        0 8px 25px
        rgba(50, 100, 150, 0.08);
}

.feature-card:hover {
    transform: translateY(-3px);

    border-color:
        rgba(124, 58, 237, 0.30);

    box-shadow:
        0 12px 30px
        rgba(124, 58, 237, 0.12);
}

.feature-icon {
    font-size: 26px;

    margin-bottom: 10px;
}

.feature-title {
    font-size: 17px;

    font-weight: 750;

    margin-bottom: 7px;

    color: #6D28D9;
}

.feature-text {
    color: #526174;

    font-size: 14px;

    line-height: 1.5;
}


/* =====================================================
   FOOTER
===================================================== */

.custom-footer {
    text-align: center;

    color: #64748B;

    font-size: 13px;

    padding-top: 45px;
}


/* =====================================================
   MOBILE
===================================================== */

@media(max-width: 768px) {

    .hero-title {
        font-size: 40px;
    }

    .hero-subtitle {
        font-size: 16px;
    }
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# MODEL PATHS
# =========================================================

MODEL_PATH = "model/fake_news_model.pkl"

VECTORIZER_PATH = "model/tfidf_vectorizer.pkl"


# =========================================================
# CHECK MODEL FILES
# =========================================================

if not os.path.exists(MODEL_PATH):

    st.error(
        "❌ Model file not found: "
        "model/fake_news_model.pkl"
    )

    st.stop()


if not os.path.exists(VECTORIZER_PATH):

    st.error(
        "❌ Vectorizer file not found: "
        "model/tfidf_vectorizer.pkl"
    )

    st.stop()


# =========================================================
# LOAD MODEL
# =========================================================

try:

    model = joblib.load(MODEL_PATH)

    vectorizer = joblib.load(
        VECTORIZER_PATH
    )

except Exception as e:

    st.error(
        f"❌ Error loading model: {e}"
    )

    st.stop()


# =========================================================
# CLEAN TEXT
# =========================================================

def clean_text(text):

    text = str(text)

    text = text.lower()

    text = re.sub(
        r"http\S+|www\S+",
        "",
        text
    )

    text = re.sub(
        r"<.*?>",
        "",
        text
    )

    text = re.sub(
        r"[^a-zA-Z0-9\s]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()

    return text


# =========================================================
# HERO SECTION
# =========================================================

st.html("""
<div class="hero">

    <div class="brand">
        🛡️ TRUTHLENS AI
    </div>

    <h1 class="hero-title">
        Separate signal from misinformation.
    </h1>

    <p class="hero-subtitle">
        Analyze news content using machine learning
        and get an instant prediction with confidence scores.
    </p>

    <div class="status">
        ● AI MODEL ONLINE
    </div>

</div>
""")


# =========================================================
# NEWS INPUT
# =========================================================

st.markdown(
    '<div class="section-title">'
    '📰 Enter News Article'
    '</div>',
    unsafe_allow_html=True
)


news_text = st.text_area(
    "News Text",

    placeholder=
    "Paste the news headline or article here...",

    height=220,

    label_visibility="collapsed"
)


analyze = st.button(
    "🔍 Analyze News"
)


# =========================================================
# ANALYZE
# =========================================================

if analyze:

    # -----------------------------------------------------
    # EMPTY INPUT
    # -----------------------------------------------------

    if not news_text.strip():

        st.warning(
            "⚠️ Please enter some news text first."
        )


    # -----------------------------------------------------
    # SHORT INPUT
    # -----------------------------------------------------

    elif len(news_text.strip()) < 10:

        st.warning(
            "⚠️ Please enter a longer news statement "
            "for better prediction."
        )


    else:

        # =================================================
        # MODEL ANALYSIS
        # =================================================

        with st.spinner(
            "🤖 AI is analyzing the news..."
        ):

            cleaned_text = clean_text(
                news_text
            )

            vectorized_text = (
                vectorizer.transform(
                    [cleaned_text]
                )
            )

            prediction = model.predict(
                vectorized_text
            )[0]

            probabilities = (
                model.predict_proba(
                    vectorized_text
                )[0]
            )

            confidence = (
                max(probabilities) * 100
            )


        # =================================================
        # FIND FAKE / REAL PROBABILITY
        # =================================================

        classes = list(
            model.classes_
        )

        fake_probability = 0.0

        real_probability = 0.0


        for i, class_name in enumerate(classes):

            class_name = str(
                class_name
            ).upper()


            if class_name == "FAKE":

                fake_probability = (
                    float(probabilities[i])
                    * 100
                )


            elif class_name == "REAL":

                real_probability = (
                    float(probabilities[i])
                    * 100
                )


        # =================================================
        # RESULT
        # =================================================

        if str(
            prediction
        ).upper() == "FAKE":

            result_icon = "🚨"

            result_text = (
                "LIKELY FAKE NEWS"
            )

        else:

            result_icon = "✅"

            result_text = (
                "LIKELY REAL NEWS"
            )


        # =================================================
        # RESULT BOX
        # =================================================

        st.html(f"""

        <div class="result-box">

            <div class="result-title">

                {result_icon}
                {result_text}

            </div>

            <div class="confidence">

                Model Confidence:

                <strong>
                    {confidence:.2f}%
                </strong>

            </div>

        </div>

        """)


        # =================================================
        # PREDICTION PROBABILITY
        # =================================================

        st.markdown(
            '<div class="section-title">'
            '📊 Prediction Probability'
            '</div>',
            unsafe_allow_html=True
        )


        fig_bar = go.Figure()


        fig_bar.add_trace(
            go.Bar(

                x=[
                    "FAKE NEWS",
                    "REAL NEWS"
                ],

                y=[
                    fake_probability,
                    real_probability
                ],

                text=[
                    f"{fake_probability:.2f}%",
                    f"{real_probability:.2f}%"
                ],

                textposition="auto",

                textfont=dict(
                    color="#000000"
                ),

                marker=dict(
                    color=[
                        "#8B5CF6",
                        "#22C55E"
                    ]
                )
            )
        )


        fig_bar.update_layout(

            title=dict(
                text="Fake vs Real Probability",
                font=dict(
                    color="#000000"
                )
            ),

            yaxis=dict(

                title=dict(
                    text="Probability (%)",
                    font=dict(
                        color="#000000"
                    )
                ),

                range=[0, 100],

                tickfont=dict(
                    color="#000000"
                )
            ),

            xaxis=dict(

                title=dict(
                    text="News Type",
                    font=dict(
                        color="#000000"
                    )
                ),

                tickfont=dict(
                    color="#000000"
                )
            ),

            template="plotly_white",

            paper_bgcolor=
            "rgba(255,255,255,0)",

            plot_bgcolor=
            "rgba(255,255,255,0)",

            font=dict(
                color="#000000"
            ),

            showlegend=False,

            height=420
        )


        st.plotly_chart(
            fig_bar,

            use_container_width=True,

            config={
                "displayModeBar": False
            }
        )


        # =================================================
        # CONFIDENCE DONUT
        # =================================================

        st.markdown(
            '<div class="section-title">'
            '🎯 Confidence Distribution'
            '</div>',
            unsafe_allow_html=True
        )


        fig_donut = go.Figure(

            data=[
                go.Pie(

                    labels=[
                        "Fake News",
                        "Real News"
                    ],

                    values=[
                        fake_probability,
                        real_probability
                    ],

                    hole=0.65,

                    textinfo=
                    "label+percent",

                    textfont=dict(
                        color="#000000"
                    ),

                    marker=dict(
                        colors=[
                            "#8B5CF6",
                            "#22C55E"
                        ]
                    )
                )
            ]
        )


        fig_donut.update_layout(

            title=dict(
                text="Confidence Distribution",
                font=dict(
                    color="#000000"
                )
            ),

            template="plotly_white",

            paper_bgcolor=
            "rgba(255,255,255,0)",

            plot_bgcolor=
            "rgba(255,255,255,0)",

            font=dict(
                color="#000000"
            ),

            height=420,

            showlegend=True,

            legend=dict(
                font=dict(
                    color="#000000"
                )
            )
        )


        st.plotly_chart(
            fig_donut,

            use_container_width=True,

            config={
                "displayModeBar": False
            }
        )


        # =================================================
        # INFORMATION SOURCE COVERAGE
        # =================================================

        st.markdown(
            '<div class="section-title">'
            '🌐 Information Source Coverage'
            '</div>',
            unsafe_allow_html=True
        )


        st.info(
            "ℹ️ These percentages represent the "
            "demo source-coverage distribution of "
            "this application. They are NOT live "
            "verification results from Google, "
            "Instagram, Facebook or Wikipedia."
        )


        # =================================================
        # SOURCE DATA
        # =================================================

        source_names = [

            "Google",
            "Wikipedia",
            "Facebook",
            "Instagram",
            "X / Twitter"

        ]


        source_percentages = [

            35,
            25,
            15,
            10,
            15

        ]


        # =================================================
        # SOURCE GRAPH
        # =================================================

        source_graph = go.Figure()


        source_graph.add_trace(

            go.Bar(

                x=source_names,

                y=source_percentages,

                text=[
                    f"{value}%"
                    for value
                    in source_percentages
                ],

                textposition="auto",

                textfont=dict(
                    color="#000000"
                ),

                marker=dict(

                    color=[

                        "#7C3AED",
                        "#8B5CF6",
                        "#22C55E",
                        "#34D399",
                        "#6D28D9"

                    ]
                )
            )
        )


        source_graph.update_layout(

            title=dict(

                text=
                "Information Source Coverage",

                font=dict(
                    color="#000000"
                )
            ),

            yaxis=dict(

                title=dict(

                    text="Coverage (%)",

                    font=dict(
                        color="#000000"
                    )
                ),

                range=[0, 100],

                tickfont=dict(
                    color="#000000"
                )
            ),

            xaxis=dict(

                title=dict(

                    text="Sources",

                    font=dict(
                        color="#000000"
                    )
                ),

                tickfont=dict(
                    color="#000000"
                )
            ),

            template="plotly_white",

            paper_bgcolor=
            "rgba(255,255,255,0)",

            plot_bgcolor=
            "rgba(255,255,255,0)",

            font=dict(
                color="#000000"
            ),

            showlegend=False,

            height=430
        )


        st.plotly_chart(

            source_graph,

            use_container_width=True,

            config={
                "displayModeBar": False
            }
        )


        # =================================================
        # SOURCE CARDS
        # =================================================

        st.markdown(
            '<div class="section-title">'
            '🔎 Sources'
            '</div>',
            unsafe_allow_html=True
        )


        # -------------------------------------------------
        # GOOGLE / WIKIPEDIA / FACEBOOK
        # -------------------------------------------------

        source_col1, source_col2, source_col3 = (
            st.columns(3)
        )


        with source_col1:

            st.html(f"""

            <div class="source-card">

                <div class="source-name">
                    🔎 Google
                </div>

                <div class="source-percent">
                    {source_percentages[0]}%
                </div>

                <div class="source-label">
                    Demo coverage
                </div>

            </div>

            """)


        with source_col2:

            st.html(f"""

            <div class="source-card">

                <div class="source-name">
                    📚 Wikipedia
                </div>

                <div class="source-percent">
                    {source_percentages[1]}%
                </div>

                <div class="source-label">
                    Demo coverage
                </div>

            </div>

            """)


        with source_col3:

            st.html(f"""

            <div class="source-card">

                <div class="source-name">
                    📘 Facebook
                </div>

                <div class="source-percent">
                    {source_percentages[2]}%
                </div>

                <div class="source-label">
                    Demo coverage
                </div>

            </div>

            """)


        # -------------------------------------------------
        # INSTAGRAM / X
        # -------------------------------------------------

        source_col4, source_col5 = st.columns(2)


        with source_col4:

            st.html(f"""

            <div class="source-card">

                <div class="source-name">
                    📸 Instagram
                </div>

                <div class="source-percent">
                    {source_percentages[3]}%
                </div>

                <div class="source-label">
                    Demo coverage
                </div>

            </div>

            """)


        with source_col5:

            st.html(f"""

            <div class="source-card">

                <div class="source-name">
                    𝕏 X / Twitter
                </div>

                <div class="source-percent">
                    {source_percentages[4]}%
                </div>

                <div class="source-label">
                    Demo coverage
                </div>

            </div>

            """)


        # =================================================
        # ANALYSIS DETAILS
        # =================================================

        st.markdown(
            '<div class="section-title">'
            '📌 Analysis Details'
            '</div>',
            unsafe_allow_html=True
        )


        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(
                "Prediction",
                str(
                    prediction
                ).upper()
            )


        with col2:

            st.metric(
                "Fake Probability",
                f"{fake_probability:.2f}%"
            )


        with col3:

            st.metric(
                "Real Probability",
                f"{real_probability:.2f}%"
            )


        # =================================================
        # WARNING
        # =================================================

        st.warning(
            "⚠️ This is an ML-based prediction, "
            "not a guaranteed fact-check. "
            "The source percentages shown above "
            "are demo coverage values, not live "
            "search results."
        )


# =========================================================
# HOW TRUTHLENS AI WORKS
# =========================================================

st.markdown(
    '<div class="section-title">'
    '✨ How TruthLens AI Works'
    '</div>',
    unsafe_allow_html=True
)


feature1, feature2, feature3 = st.columns(3)


# =========================================================
# FEATURE 1
# =========================================================

with feature1:

    st.html("""
    <div class="feature-card">

        <div class="feature-icon">
            🧹
        </div>

        <div class="feature-title">
            01 — Clean
        </div>

        <div class="feature-text">
            The news text is cleaned and prepared
            before sending it to the machine
            learning model.
        </div>

    </div>
    """)


# =========================================================
# FEATURE 2
# =========================================================

with feature2:

    st.html("""
    <div class="feature-card">

        <div class="feature-icon">
            🧠
        </div>

        <div class="feature-title">
            02 — Analyze
        </div>

        <div class="feature-text">
            TF-IDF converts the text into numerical
            features that the trained ML model
            can understand.
        </div>

    </div>
    """)


# =========================================================
# FEATURE 3
# =========================================================

with feature3:

    st.html("""
    <div class="feature-card">

        <div class="feature-icon">
            🛡️
        </div>

        <div class="feature-title">
            03 — Protect
        </div>

        <div class="feature-text">
            The model predicts whether the news
            is likely REAL or FAKE and displays
            the probability.
        </div>

    </div>
    """)


# =========================================================
# FOOTER
# =========================================================

st.html("""
<div class="custom-footer">

    🛡️ TruthLens AI

    <br><br>

    Built with Python • Scikit-learn • Streamlit • Plotly

</div>
""")