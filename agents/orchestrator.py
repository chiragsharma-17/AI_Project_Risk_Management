import pandas as pd

from agents.cost_risk_agent import calculate_cost_risk
from agents.schedule_risk_agent import calculate_schedule_risk
from agents.resource_risk_agent import calculate_resource_risk
from agents.risk_strategist import calculate_overall_risk


def run_project_risk_analysis(df):
    """
    Main orchestrator for the AI Project Risk Management System.

    Runs all domain expert agents and combines their
    outputs into a final project risk assessment.
    """

    # ---------------------------------------------------------
    # Step 1: Cost Risk Analysis
    # ---------------------------------------------------------

    print("\nRunning Cost Risk Agent...")

    cost_result = calculate_cost_risk(df)

    print("Cost Risk Agent completed.")

    # ---------------------------------------------------------
    # Step 2: Schedule Risk Analysis
    # ---------------------------------------------------------

    print("\nRunning Schedule Risk Agent...")

    schedule_result = calculate_schedule_risk(df)

    print("Schedule Risk Agent completed.")

    # ---------------------------------------------------------
    # Step 3: Resource Risk Analysis
    # ---------------------------------------------------------

    print("\nRunning Resource Risk Agent...")

    resource_result = calculate_resource_risk(df)

    print("Resource Risk Agent completed.")

    # ---------------------------------------------------------
    # Step 4: Overall Risk Strategy
    # ---------------------------------------------------------

    print("\nRunning Risk Strategist...")

    risk_result = calculate_overall_risk(
        cost_result,
        schedule_result,
        resource_result
    )

    print("Risk Strategist completed.")

    # ---------------------------------------------------------
    # Return complete analysis
    # ---------------------------------------------------------

    return {
        "cost_analysis": cost_result,
        "schedule_analysis": schedule_result,
        "resource_analysis": resource_result,
        "risk_analysis": risk_result
    }


# ---------------------------------------------------------
# Test the complete orchestrator
# ---------------------------------------------------------

if __name__ == "__main__":

    print("\n" + "=" * 60)
    print("AI PROJECT RISK MANAGEMENT SYSTEM")
    print("MULTI-AGENT ORCHESTRATOR")
    print("=" * 60)

    # -----------------------------------------------------
    # Load project data
    # -----------------------------------------------------

    data = pd.read_csv(
        "data/project_data.csv"
    )

    print(
        f"\nLoaded {len(data)} projects."
    )

    # -----------------------------------------------------
    # Run complete analysis
    # -----------------------------------------------------

    result = run_project_risk_analysis(
        data
    )

    # -----------------------------------------------------
    # Extract final risk results
    # -----------------------------------------------------

    risk_result = result[
        "risk_analysis"
    ]

    risk_summary = risk_result[
        "summary"
    ]

    risk_projects = risk_result[
        "project_scores"
    ]

    # -----------------------------------------------------
    # Display final summary
    # -----------------------------------------------------

    print("\n" + "=" * 60)
    print("FINAL PROJECT RISK SUMMARY")
    print("=" * 60)

    for key, value in risk_summary.items():

        print(
            f"{key}: {value}"
        )

    # -----------------------------------------------------
    # Display top projects
    # -----------------------------------------------------

    print("\nTop 10 Highest-Risk Projects:")

    display_columns = [
        "Risk_Rank",
        "Project_ID",
        "Overall_Risk_Score",
        "Overall_Risk_Level",
        "Primary_Risk_Driver",
        "Recommended_Action"
    ]

    print(
        risk_projects[
            display_columns
        ]
        .head(10)
        .to_string(index=False)
    )

    print("\n" + "=" * 60)
    print("ORCHESTRATOR TEST COMPLETED")
    print("=" * 60)
