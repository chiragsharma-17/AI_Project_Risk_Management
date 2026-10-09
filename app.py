import streamlit as st
import pandas as pd
import plotly.express as px

from agents.orchestrator import run_project_risk_analysis
from agents.copilot_agent import ask_risk_copilot


# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="AI Project Risk Management System",
    page_icon="📊",
    layout="wide"
)


# ---------------------------------------------------------
# Title
# ---------------------------------------------------------

st.title("AI Project Risk Management System")

st.markdown(
    """
    **Multi-Agent System for Project Risk Detection and Mitigation**

    The system analyses project cost, schedule and resource
    conditions to identify high-risk projects and recommend
    management actions.
    """
)


# ---------------------------------------------------------
# Load Dataset
# ---------------------------------------------------------

@st.cache_data
def load_data():

    return pd.read_csv(
        "data/project_data.csv"
    )


df = load_data()


# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------

st.sidebar.header("Analysis Settings")

st.sidebar.write(
    f"Projects Loaded: **{len(df)}**"
)

selected_department = st.sidebar.selectbox(
    "Department",
    ["All Departments"]
    + sorted(
        df["Department"].unique().tolist()
    )
)


# ---------------------------------------------------------
# Filter Data
# ---------------------------------------------------------

if selected_department == "All Departments":

    filtered_df = df.copy()

else:

    filtered_df = df[
        df["Department"]
        == selected_department
    ].copy()


# ---------------------------------------------------------
# Architecture
# ---------------------------------------------------------

st.subheader("System Architecture")

st.info(
    """
    Project Data → Orchestrator → Cost Risk Agent +
    Schedule Risk Agent + Resource Risk Agent →
    Risk Strategist → Management Action
    """
)


# ---------------------------------------------------------
# Run Analysis
# ---------------------------------------------------------

if st.button(
    "Run Project Risk Analysis",
    type="primary"
):

    with st.spinner(
        "Running multi-agent risk analysis..."
    ):

        result = run_project_risk_analysis(
            filtered_df
        )

    st.session_state["analysis_result"] = result

    st.success(
        "Project risk analysis completed successfully."
    )


# ---------------------------------------------------------
# Check if analysis exists
# ---------------------------------------------------------

if "analysis_result" not in st.session_state:

    st.info(
        "Click **Run Project Risk Analysis** "
        "to start the multi-agent analysis."
    )

    st.stop()


# ---------------------------------------------------------
# Extract Results
# ---------------------------------------------------------

result = st.session_state[
    "analysis_result"
]

risk_result = result[
    "risk_analysis"
]

risk_summary = risk_result[
    "summary"
]

risk_projects = risk_result[
    "project_scores"
].copy()


# ---------------------------------------------------------
# KPI Cards
# ---------------------------------------------------------

st.subheader("Project Risk Overview")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:

    st.metric(
        "Total Projects",
        risk_summary[
            "Total_Projects"
        ]
    )

with col2:

    st.metric(
        "Critical",
        risk_summary[
            "Critical_Projects"
        ]
    )

with col3:

    st.metric(
        "High Risk",
        risk_summary[
            "High_Risk_Projects"
        ]
    )

with col4:

    st.metric(
        "Medium Risk",
        risk_summary[
            "Medium_Risk_Projects"
        ]
    )

with col5:

    st.metric(
        "Low Risk",
        risk_summary[
            "Low_Risk_Projects"
        ]
    )


# ---------------------------------------------------------
# Risk Distribution
# ---------------------------------------------------------

st.subheader("Risk Distribution")

risk_distribution = pd.DataFrame({

    "Risk Level": [
        "Critical",
        "High",
        "Medium",
        "Low"
    ],

    "Projects": [
        risk_summary[
            "Critical_Projects"
        ],

        risk_summary[
            "High_Risk_Projects"
        ],

        risk_summary[
            "Medium_Risk_Projects"
        ],

        risk_summary[
            "Low_Risk_Projects"
        ]
    ]
})


fig = px.bar(
    risk_distribution,
    x="Risk Level",
    y="Projects",
    text="Projects",
    title="Project Risk Distribution"
)

fig.update_traces(
    textposition="outside"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ---------------------------------------------------------
# Top Risk Projects
# ---------------------------------------------------------

st.subheader(
    "Highest-Risk Projects"
)

top_projects = risk_projects[
    [
        "Risk_Rank",
        "Project_ID",
        "Overall_Risk_Score",
        "Overall_Risk_Level",
        "Primary_Risk_Driver",
        "Cost_Risk_Score",
        "Schedule_Risk_Score",
        "Resource_Risk_Score",
        "Recommended_Action"
    ]
].head(10)


st.dataframe(
    top_projects,
    use_container_width=True,
    hide_index=True
)


# ---------------------------------------------------------
# Project Selection
# ---------------------------------------------------------

st.subheader(
    "Project Risk Details"
)

project_options = (
    risk_projects[
        "Project_ID"
    ]
    .tolist()
)

selected_project = st.selectbox(
    "Select a project",
    project_options
)


project = risk_projects[
    risk_projects["Project_ID"]
    == selected_project
].iloc[0]


# ---------------------------------------------------------
# Project Details
# ---------------------------------------------------------

st.markdown(
    f"### Project {selected_project}"
)

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Overall Risk",
        f"{project['Overall_Risk_Score']:.0f}"
    )

with col2:

    st.metric(
        "Cost Risk",
        f"{project['Cost_Risk_Score']:.0f}"
    )

with col3:

    st.metric(
        "Schedule Risk",
        f"{project['Schedule_Risk_Score']:.0f}"
    )

with col4:

    st.metric(
        "Resource Risk",
        f"{project['Resource_Risk_Score']:.0f}"
    )


# ---------------------------------------------------------
# Risk Information
# ---------------------------------------------------------

st.write(
    f"**Risk Level:** "
    f"{project['Overall_Risk_Level']}"
)

st.write(
    f"**Primary Risk Driver:** "
    f"{project['Primary_Risk_Driver']}"
)

st.write(
    f"**High-Risk Dimensions:** "
    f"{project['High_Risk_Dimensions']} / 3"
)

st.write(
    f"**Recommended Action:** "
    f"{project['Recommended_Action']}"
)


# ---------------------------------------------------------
# Domain Analysis
# ---------------------------------------------------------

st.subheader(
    "Domain Risk Analysis"
)

tab1, tab2, tab3 = st.tabs(
    [
        "Cost Risk",
        "Schedule Risk",
        "Resource Risk"
    ]
)


with tab1:

    st.write(
        f"**Budget Overrun:** "
        f"{project['Budget_Overrun_Percent']:.2f}%"
    )

    st.write(
        f"**Cost Risk Score:** "
        f"{project['Cost_Risk_Score']:.0f}"
    )

    st.write(
        f"**Cost Risk Level:** "
        f"{project['Cost_Risk_Level']}"
    )


with tab2:

    st.write(
        f"**Delay:** "
        f"{project['Delay_Days']} days"
    )

    st.write(
        f"**Schedule Variance:** "
        f"{project['Schedule_Variance_Percent']:.2f}%"
    )

    st.write(
        f"**Schedule Risk Score:** "
        f"{project['Schedule_Risk_Score']:.0f}"
    )

    st.write(
        f"**Schedule Risk Level:** "
        f"{project['Schedule_Risk_Level']}"
    )


with tab3:

    st.write(
        f"**Resource Utilization:** "
        f"{project['Resource_Utilization_Percent']:.2f}%"
    )

    st.write(
        f"**Task Completion:** "
        f"{project['Task_Completion_Percent']:.2f}%"
    )

    st.write(
        f"**Resource Risk Score:** "
        f"{project['Resource_Risk_Score']:.0f}"
    )

    st.write(
        f"**Resource Risk Level:** "
        f"{project['Resource_Risk_Level']}"
    )

# ---------------------------------------------------------
# What-If Risk Simulator
# ---------------------------------------------------------

st.subheader("What-If Risk Simulator")

st.write(
    """
    Test how the overall project risk changes when management
    gives different importance to Cost, Schedule, and Resource risk.
    """
)

# ---------------------------------------------------------
# Scenario Selection
# ---------------------------------------------------------

scenario = st.selectbox(
    "Select Risk Scenario",
    [
        "Balanced",
        "Cost Focused",
        "Schedule Focused",
        "Resource Focused",
        "Custom"
    ]
)


# ---------------------------------------------------------
# Default Scenario Weights
# ---------------------------------------------------------

if scenario == "Balanced":

    cost_weight = 0.35
    schedule_weight = 0.40
    resource_weight = 0.25


elif scenario == "Cost Focused":

    cost_weight = 0.50
    schedule_weight = 0.30
    resource_weight = 0.20


elif scenario == "Schedule Focused":

    cost_weight = 0.25
    schedule_weight = 0.50
    resource_weight = 0.25


elif scenario == "Resource Focused":

    cost_weight = 0.25
    schedule_weight = 0.25
    resource_weight = 0.50


else:

    st.write("Set your own risk weights.")

    cost_weight = st.slider(
        "Cost Risk Weight",
        min_value=0,
        max_value=100,
        value=35,
        step=5
    ) / 100

    schedule_weight = st.slider(
        "Schedule Risk Weight",
        min_value=0,
        max_value=100,
        value=40,
        step=5
    ) / 100

    resource_weight = st.slider(
        "Resource Risk Weight",
        min_value=0,
        max_value=100,
        value=25,
        step=5
    ) / 100


# ---------------------------------------------------------
# Display Weights
# ---------------------------------------------------------

st.write(
    f"**Cost:** {cost_weight * 100:.0f}%  |  "
    f"**Schedule:** {schedule_weight * 100:.0f}%  |  "
    f"**Resource:** {resource_weight * 100:.0f}%"
)


# ---------------------------------------------------------
# Validate Custom Weights
# ---------------------------------------------------------

total_weight = (
    cost_weight
    + schedule_weight
    + resource_weight
)


if abs(total_weight - 1.0) > 0.001:

    st.warning(
        "Custom risk weights must add up to 100%."
    )

else:

    # -----------------------------------------------------
    # Calculate Scenario Risk Score
    # -----------------------------------------------------

    scenario_projects = risk_projects.copy()

    scenario_projects[
        "Scenario_Risk_Score"
    ] = (

        scenario_projects[
            "Cost_Risk_Score"
        ] * cost_weight

        +

        scenario_projects[
            "Schedule_Risk_Score"
        ] * schedule_weight

        +

        scenario_projects[
            "Resource_Risk_Score"
        ] * resource_weight
    )

    scenario_projects[
        "Scenario_Risk_Score"
    ] = (
        scenario_projects[
            "Scenario_Risk_Score"
        ].round(2)
    )


    # -----------------------------------------------------
    # Determine Scenario Risk Level
    # -----------------------------------------------------

    def scenario_risk_level(score):

        if score <= 24:
            return "Low"

        elif score <= 49:
            return "Medium"

        elif score <= 74:
            return "High"

        else:
            return "Critical"


    scenario_projects[
        "Scenario_Risk_Level"
    ] = (
        scenario_projects[
            "Scenario_Risk_Score"
        ].apply(
            scenario_risk_level
        )
    )


    # -----------------------------------------------------
    # Scenario Ranking
    # -----------------------------------------------------

    scenario_projects = (
        scenario_projects
        .sort_values(
            "Scenario_Risk_Score",
            ascending=False
        )
        .reset_index(drop=True)
    )

    scenario_projects[
        "Scenario_Rank"
    ] = (
        scenario_projects.index + 1
    )


    # -----------------------------------------------------
    # Selected Project Scenario
    # -----------------------------------------------------

    selected_scenario_project = (
        scenario_projects[
            scenario_projects["Project_ID"]
            == selected_project
        ].iloc[0]
    )


    # -----------------------------------------------------
    # Display Selected Project Result
    # -----------------------------------------------------

    st.markdown(
        f"### Scenario Result for {selected_project}"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Scenario Risk Score",
            f"{selected_scenario_project['Scenario_Risk_Score']:.2f}"
        )

    with col2:

        st.metric(
            "Scenario Risk Level",
            selected_scenario_project[
                "Scenario_Risk_Level"
            ]
        )

    with col3:

        original_rank = int(
            project["Risk_Rank"]
        )

        scenario_rank = int(
            selected_scenario_project[
                "Scenario_Rank"
            ]
        )

        st.metric(
            "Scenario Rank",
            scenario_rank,
            delta=(
                original_rank
                - scenario_rank
            )
        )


    # -----------------------------------------------------
    # Scenario Ranking Table
    # -----------------------------------------------------

    st.markdown(
        "### Scenario Risk Ranking"
    )

    scenario_display = scenario_projects[
        [
            "Scenario_Rank",
            "Project_ID",
            "Scenario_Risk_Score",
            "Scenario_Risk_Level",
            "Primary_Risk_Driver"
        ]
    ].head(10)


    st.dataframe(
        scenario_display,
        use_container_width=True,
        hide_index=True
    )

    # ---------------------------------------------------------
# AI Risk Copilot
# ---------------------------------------------------------

st.subheader("AI Risk Copilot")

st.write(
    """
    Ask questions about project risk, cost, schedule,
    resources, and recommended actions.
    """
)

question = st.chat_input(
    "Ask the Risk Copilot..."
)

if question:

    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):

        with st.spinner(
            "Analysing project risk..."
        ):

            answer = ask_risk_copilot(
                question=question,
                risk_projects=risk_projects,
                project_data=filtered_df,
                selected_project=selected_project
            )

        st.write(answer)

# ---------------------------------------------------------
# Raw Project Data
# ---------------------------------------------------------

with st.expander(
    "View Project Dataset"
):

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )