import os
import sys
import pandas as pd


# ---------------------------------------------------------
# Make project root available for package imports
# ---------------------------------------------------------

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(
        0,
        PROJECT_ROOT
    )


# ---------------------------------------------------------
# Optional Ollama
# ---------------------------------------------------------

try:
    import ollama

    OLLAMA_AVAILABLE = True

except ImportError:

    ollama = None
    OLLAMA_AVAILABLE = False


# ---------------------------------------------------------
# AI Risk Copilot
# ---------------------------------------------------------

def ask_risk_copilot(
    question,
    risk_projects,
    project_data,
    selected_project=None
):
    """
    Answers project risk questions using the available
    project risk analysis.

    Ollama is used for natural-language explanations.
    A deterministic fallback is used if Ollama is unavailable.
    """

    question_lower = question.lower().strip()

    # -----------------------------------------------------
    # Find selected project
    # -----------------------------------------------------

    selected_row = None

    if selected_project is not None:

        matches = risk_projects[
            risk_projects["Project_ID"]
            == selected_project
        ]

        if not matches.empty:
            selected_row = matches.iloc[0]

    # -----------------------------------------------------
    # Why is this project risky?
    # -----------------------------------------------------

    if (
        "why" in question_lower
        and selected_row is not None
    ):

        project_id = selected_row["Project_ID"]

        return (
            f"{project_id} is classified as "
            f"{selected_row['Overall_Risk_Level']} risk "
            f"with an overall risk score of "
            f"{selected_row['Overall_Risk_Score']:.2f}. "
            f"The primary risk driver is "
            f"{selected_row['Primary_Risk_Driver']}. "
            f"Cost risk is "
            f"{selected_row['Cost_Risk_Score']:.0f}, "
            f"schedule risk is "
            f"{selected_row['Schedule_Risk_Score']:.0f}, "
            f"and resource risk is "
            f"{selected_row['Resource_Risk_Score']:.0f}. "
            f"The recommended action is: "
            f"{selected_row['Recommended_Action']}."
        )

    # -----------------------------------------------------
    # Highest overall risk
    # -----------------------------------------------------

    if (
        "highest risk" in question_lower
        or "most risky" in question_lower
    ):

        row = risk_projects.iloc[0]

        return (
            f"The highest-ranked project is "
            f"{row['Project_ID']} with an overall "
            f"risk score of "
            f"{row['Overall_Risk_Score']:.2f}. "
            f"It is classified as "
            f"{row['Overall_Risk_Level']} risk, "
            f"with {row['Primary_Risk_Driver']} "
            f"as the primary risk driver."
        )

    # -----------------------------------------------------
    # Highest cost risk
    # -----------------------------------------------------

    if (
        "cost risk" in question_lower
        or "budget risk" in question_lower
    ):

        row = risk_projects.sort_values(
            "Cost_Risk_Score",
            ascending=False
        ).iloc[0]

        return (
            f"{row['Project_ID']} has the highest "
            f"cost risk score of "
            f"{row['Cost_Risk_Score']:.0f}. "
            f"Its budget overrun is "
            f"{row['Budget_Overrun_Percent']:.2f}%."
        )

    # -----------------------------------------------------
    # Highest schedule risk
    # -----------------------------------------------------

    if (
        "schedule risk" in question_lower
        or "delay" in question_lower
    ):

        row = risk_projects.sort_values(
            "Schedule_Risk_Score",
            ascending=False
        ).iloc[0]

        return (
            f"{row['Project_ID']} has the highest "
            f"schedule risk score of "
            f"{row['Schedule_Risk_Score']:.0f}. "
            f"It has a delay of "
            f"{row['Delay_Days']} days and a schedule "
            f"variance of "
            f"{row['Schedule_Variance_Percent']:.2f}%."
        )

    # -----------------------------------------------------
    # Highest resource risk
    # -----------------------------------------------------

    if (
        "resource risk" in question_lower
        or "resource utilization" in question_lower
    ):

        row = risk_projects.sort_values(
            "Resource_Risk_Score",
            ascending=False
        ).iloc[0]

        return (
            f"{row['Project_ID']} has the highest "
            f"resource risk score of "
            f"{row['Resource_Risk_Score']:.0f}. "
            f"Resource utilization is "
            f"{row['Resource_Utilization_Percent']:.2f}% "
            f"and task completion is "
            f"{row['Task_Completion_Percent']:.2f}%."
        )

    # -----------------------------------------------------
    # Recommended action
    # -----------------------------------------------------

    if (
        (
            "action" in question_lower
            or "recommend" in question_lower
            or "should we do" in question_lower
        )
        and selected_row is not None
    ):

        return (
            f"For {selected_row['Project_ID']}, "
            f"the recommended action is: "
            f"{selected_row['Recommended_Action']}. "
            f"The project has an overall risk score of "
            f"{selected_row['Overall_Risk_Score']:.2f} "
            f"and is classified as "
            f"{selected_row['Overall_Risk_Level']} risk."
        )

    # -----------------------------------------------------
    # Build context for Ollama
    # -----------------------------------------------------

    top_projects = risk_projects[
        [
            "Project_ID",
            "Overall_Risk_Score",
            "Overall_Risk_Level",
            "Primary_Risk_Driver",
            "Cost_Risk_Score",
            "Schedule_Risk_Score",
            "Resource_Risk_Score",
            "Recommended_Action"
        ]
    ].head(15)

    context = top_projects.to_string(
        index=False
    )

    selected_context = ""

    if selected_row is not None:

        selected_context = f"""
Selected Project:
Project ID: {selected_row['Project_ID']}
Overall Risk Score: {selected_row['Overall_Risk_Score']}
Overall Risk Level: {selected_row['Overall_Risk_Level']}
Primary Risk Driver: {selected_row['Primary_Risk_Driver']}
Cost Risk Score: {selected_row['Cost_Risk_Score']}
Schedule Risk Score: {selected_row['Schedule_Risk_Score']}
Resource Risk Score: {selected_row['Resource_Risk_Score']}
Budget Overrun: {selected_row['Budget_Overrun_Percent']:.2f}%
Delay: {selected_row['Delay_Days']} days
Resource Utilization: {selected_row['Resource_Utilization_Percent']:.2f}%
Task Completion: {selected_row['Task_Completion_Percent']:.2f}%
Recommended Action: {selected_row['Recommended_Action']}
"""

    prompt = f"""
You are an AI Project Risk Management Copilot.

Answer the user's question using ONLY the project
risk information provided below.

Do not invent project numbers, causes, percentages,
or recommendations.

Keep the answer concise and suitable for a project manager.

Project Risk Data:
{context}

{selected_context}

User Question:
{question}
"""

    # -----------------------------------------------------
    # Try Ollama
    # -----------------------------------------------------

    if OLLAMA_AVAILABLE:

        try:

            response = ollama.chat(
                model="llama3.2:3b",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            return response[
                "message"
            ][
                "content"
            ].strip()

        except Exception:

            pass

    # -----------------------------------------------------
    # Generic fallback
    # -----------------------------------------------------

    if selected_row is not None:

        return (
            f"{selected_row['Project_ID']} is "
            f"{selected_row['Overall_Risk_Level']} risk "
            f"with an overall score of "
            f"{selected_row['Overall_Risk_Score']:.2f}. "
            f"The main risk driver is "
            f"{selected_row['Primary_Risk_Driver']}. "
            f"Recommended action: "
            f"{selected_row['Recommended_Action']}."
        )

    return (
        "I can answer questions about project risk, "
        "cost risk, schedule risk, resource risk, "
        "highest-risk projects, and recommended actions."
    )


# ---------------------------------------------------------
# Test the Copilot independently
# ---------------------------------------------------------

if __name__ == "__main__":

    from agents.cost_risk_agent import (
        calculate_cost_risk
    )

    from agents.schedule_risk_agent import (
        calculate_schedule_risk
    )

    from agents.resource_risk_agent import (
        calculate_resource_risk
    )

    from agents.risk_strategist import (
        calculate_overall_risk
    )

    # -----------------------------------------------------
    # Load dataset
    # -----------------------------------------------------

    data = pd.read_csv(
        os.path.join(
            PROJECT_ROOT,
            "data",
            "project_data.csv"
        )
    )

    # -----------------------------------------------------
    # Run domain agents
    # -----------------------------------------------------

    cost_result = calculate_cost_risk(
        data
    )

    schedule_result = calculate_schedule_risk(
        data
    )

    resource_result = calculate_resource_risk(
        data
    )

    # -----------------------------------------------------
    # Run Risk Strategist
    # -----------------------------------------------------

    risk_result = calculate_overall_risk(
        cost_result,
        schedule_result,
        resource_result
    )

    risk_projects = risk_result[
        "project_scores"
    ]

    # -----------------------------------------------------
    # Test question
    # -----------------------------------------------------

    question = (
        "Why is this project critical?"
    )

    answer = ask_risk_copilot(
        question,
        risk_projects,
        data,
        selected_project="P212"
    )

    # -----------------------------------------------------
    # Display result
    # -----------------------------------------------------

    print("\n" + "=" * 60)
    print("AI RISK COPILOT")
    print("=" * 60)

    print("\nQuestion:")
    print(question)

    print("\nAnswer:")
    print(answer)

    print("\n" + "=" * 60)
    print("COPILOT TEST COMPLETED")
    print("=" * 60)
