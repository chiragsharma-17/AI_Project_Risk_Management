import pandas as pd


def calculate_cost_risk(df):
    """
    Calculates cost overrun and cost risk for each project.
    """

    result = df.copy()

    # ---------------------------------------------------------
    # Calculate budget variance
    # ---------------------------------------------------------

    result["Budget_Variance"] = (
        result["Actual_Spend"] - result["Budget"]
    )

    # ---------------------------------------------------------
    # Calculate budget overrun percentage
    # ---------------------------------------------------------

    result["Budget_Overrun_Percent"] = (
        result["Budget_Variance"]
        / result["Budget"]
    ) * 100

    # ---------------------------------------------------------
    # Calculate cost risk score
    # ---------------------------------------------------------

    def cost_risk_score(overrun):

        if overrun <= 0:
            return 0

        elif overrun <= 5:
            return 20

        elif overrun <= 10:
            return 40

        elif overrun <= 20:
            return 60

        elif overrun <= 30:
            return 80

        else:
            return 100

    result["Cost_Risk_Score"] = (
        result["Budget_Overrun_Percent"]
        .apply(cost_risk_score)
    )

    # ---------------------------------------------------------
    # Determine cost risk level
    # ---------------------------------------------------------

    def cost_risk_level(score):

        if score <= 24:
            return "Low"

        elif score <= 49:
            return "Medium"

        elif score <= 74:
            return "High"

        else:
            return "Critical"

    result["Cost_Risk_Level"] = (
        result["Cost_Risk_Score"]
        .apply(cost_risk_level)
    )

    # ---------------------------------------------------------
    # Sort by highest cost risk
    # ---------------------------------------------------------

    result = result.sort_values(
        by="Cost_Risk_Score",
        ascending=False
    )

    # ---------------------------------------------------------
    # Summary
    # ---------------------------------------------------------

    summary = {
        "Average_Budget_Overrun_Percent":
            round(
                result["Budget_Overrun_Percent"].mean(),
                2
            ),

        "High_Risk_Projects":
            int(
                (result["Cost_Risk_Level"] == "High")
                .sum()
            ),

        "Critical_Risk_Projects":
            int(
                (result["Cost_Risk_Level"] == "Critical")
                .sum()
            ),

        "Highest_Cost_Risk_Project":
            result.iloc[0]["Project_ID"],

        "Highest_Cost_Risk_Score":
            result.iloc[0]["Cost_Risk_Score"]
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

    result = calculate_cost_risk(data)

    print("\n" + "=" * 60)
    print("COST RISK AGENT")
    print("=" * 60)

    print("\nSummary:")
    for key, value in result["summary"].items():
        print(f"{key}: {value}")

    print("\nTop 10 Projects by Cost Risk:")

    display_columns = [
        "Project_ID",
        "Project_Name",
        "Budget",
        "Actual_Spend",
        "Budget_Overrun_Percent",
        "Cost_Risk_Score",
        "Cost_Risk_Level"
    ]

    print(
        result["project_scores"]
        [display_columns]
        .head(10)
        .to_string(index=False)
    )
