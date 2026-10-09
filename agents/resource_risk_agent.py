import pandas as pd


def calculate_resource_risk(df):
    """
    Calculates resource utilisation risk and
    resource pressure for each project.
    """

    result = df.copy()

    # ---------------------------------------------------------
    # Calculate base resource risk score
    # ---------------------------------------------------------

    def resource_risk_score(utilization):

        if utilization <= 70:
            return 0

        elif utilization <= 80:
            return 20

        elif utilization <= 90:
            return 40

        elif utilization <= 95:
            return 60

        elif utilization <= 98:
            return 80

        else:
            return 100

    result["Resource_Risk_Score"] = (
        result["Resource_Utilization_Percent"]
        .apply(resource_risk_score)
    )

    # ---------------------------------------------------------
    # Additional resource pressure
    # ---------------------------------------------------------
    # High utilisation combined with delay or low completion
    # indicates stronger resource pressure.

    result["Resource_Pressure_Flag"] = (
        (
            result["Resource_Utilization_Percent"] >= 90
        )
        &
        (
            (
                result["Delay_Days"] >= 15
            )
            |
            (
                result["Task_Completion_Percent"] < 70
            )
        )
    )

    # ---------------------------------------------------------
    # Add pressure adjustment
    # ---------------------------------------------------------

    result.loc[
        result["Resource_Pressure_Flag"],
        "Resource_Risk_Score"
    ] += 10

    # Keep score between 0 and 100

    result["Resource_Risk_Score"] = (
        result["Resource_Risk_Score"]
        .clip(0, 100)
    )

    # ---------------------------------------------------------
    # Determine resource risk level
    # ---------------------------------------------------------

    def resource_risk_level(score):

        if score <= 24:
            return "Low"

        elif score <= 49:
            return "Medium"

        elif score <= 74:
            return "High"

        else:
            return "Critical"

    result["Resource_Risk_Level"] = (
        result["Resource_Risk_Score"]
        .apply(resource_risk_level)
    )

    # ---------------------------------------------------------
    # Sort by highest resource risk
    # ---------------------------------------------------------

    result = result.sort_values(
        by="Resource_Risk_Score",
        ascending=False
    )

    # ---------------------------------------------------------
    # Summary
    # ---------------------------------------------------------

    summary = {
        "Average_Resource_Utilization":
            round(
                result[
                    "Resource_Utilization_Percent"
                ].mean(),
                2
            ),

        "High_Risk_Projects":
            int(
                (
                    result["Resource_Risk_Level"]
                    == "High"
                ).sum()
            ),

        "Critical_Risk_Projects":
            int(
                (
                    result["Resource_Risk_Level"]
                    == "Critical"
                ).sum()
            ),

        "Resource_Pressure_Projects":
            int(
                result["Resource_Pressure_Flag"]
                .sum()
            ),

        "Highest_Resource_Risk_Project":
            result.iloc[0]["Project_ID"],

        "Highest_Resource_Risk_Score":
            result.iloc[0]["Resource_Risk_Score"]
    }

    return {
        "project_scores": result,
        "summary": summary
    }


# ---------------------------------------------------------
# Test the agent independently
# ---------------------------------------------------------

if __name__ == "__main__":

    data = pd.read_csv(
        "data/project_data.csv"
    )

    result = calculate_resource_risk(data)

    print("\n" + "=" * 60)
    print("RESOURCE RISK AGENT")
    print("=" * 60)

    print("\nSummary:")

    for key, value in result["summary"].items():
        print(f"{key}: {value}")

    print("\nTop 10 Projects by Resource Risk:")

    display_columns = [
        "Project_ID",
        "Project_Name",
        "Resource_Utilization_Percent",
        "Team_Size",
        "Task_Completion_Percent",
        "Delay_Days",
        "Resource_Risk_Score",
        "Resource_Risk_Level",
        "Resource_Pressure_Flag"
    ]

    print(
        result["project_scores"]
        [display_columns]
        .head(10)
        .to_string(index=False)
    )
