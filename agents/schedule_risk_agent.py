import pandas as pd


def calculate_schedule_risk(df):
    """
    Calculates schedule variance, delay risk,
    and schedule risk level for each project.
    """

    result = df.copy()

    # ---------------------------------------------------------
    # Calculate schedule variance
    # ---------------------------------------------------------

    result["Schedule_Variance_Days"] = (
        result["Actual_Duration_Days"]
        - result["Planned_Duration_Days"]
    )

    # ---------------------------------------------------------
    # Calculate schedule variance percentage
    # ---------------------------------------------------------

    result["Schedule_Variance_Percent"] = (
        result["Schedule_Variance_Days"]
        / result["Planned_Duration_Days"]
    ) * 100

    # ---------------------------------------------------------
    # Calculate schedule risk score
    # ---------------------------------------------------------

    def schedule_risk_score(delay):

        if delay <= 5:
            return 0

        elif delay <= 10:
            return 20

        elif delay <= 20:
            return 40

        elif delay <= 30:
            return 60

        elif delay <= 45:
            return 80

        else:
            return 100

    result["Schedule_Risk_Score"] = (
        result["Delay_Days"]
        .apply(schedule_risk_score)
    )

    # ---------------------------------------------------------
    # Determine schedule risk level
    # ---------------------------------------------------------

    def schedule_risk_level(score):

        if score <= 24:
            return "Low"

        elif score <= 49:
            return "Medium"

        elif score <= 74:
            return "High"

        else:
            return "Critical"

    result["Schedule_Risk_Level"] = (
        result["Schedule_Risk_Score"]
        .apply(schedule_risk_level)
    )

    # ---------------------------------------------------------
    # Sort by highest schedule risk
    # ---------------------------------------------------------

    result = result.sort_values(
        by="Schedule_Risk_Score",
        ascending=False
    )

    # ---------------------------------------------------------
    # Summary
    # ---------------------------------------------------------

    summary = {
        "Average_Delay_Days":
            round(
                result["Delay_Days"].mean(),
                2
            ),

        "Average_Schedule_Variance_Percent":
            round(
                result["Schedule_Variance_Percent"].mean(),
                2
            ),

        "High_Risk_Projects":
            int(
                (
                    result["Schedule_Risk_Level"]
                    == "High"
                ).sum()
            ),

        "Critical_Risk_Projects":
            int(
                (
                    result["Schedule_Risk_Level"]
                    == "Critical"
                ).sum()
            ),

        "Highest_Schedule_Risk_Project":
            result.iloc[0]["Project_ID"],

        "Highest_Schedule_Risk_Score":
            result.iloc[0]["Schedule_Risk_Score"]
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

    result = calculate_schedule_risk(data)

    print("\n" + "=" * 60)
    print("SCHEDULE RISK AGENT")
    print("=" * 60)

    print("\nSummary:")

    for key, value in result["summary"].items():
        print(f"{key}: {value}")

    print("\nTop 10 Projects by Schedule Risk:")

    display_columns = [
        "Project_ID",
        "Project_Name",
        "Planned_Duration_Days",
        "Actual_Duration_Days",
        "Delay_Days",
        "Schedule_Variance_Percent",
        "Schedule_Risk_Score",
        "Schedule_Risk_Level"
    ]

    print(
        result["project_scores"]
        [display_columns]
        .head(10)
        .to_string(index=False)
    )
