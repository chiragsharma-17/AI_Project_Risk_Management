import pandas as pd


def calculate_overall_risk(
    cost_result,
    schedule_result,
    resource_result
):
    """
    Combines Cost, Schedule and Resource Risk
    into an overall project risk assessment.
    """

    # ---------------------------------------------------------
    # Extract project-level results
    # ---------------------------------------------------------

    cost_df = cost_result["project_scores"][
        [
            "Project_ID",
            "Budget_Overrun_Percent",
            "Cost_Risk_Score",
            "Cost_Risk_Level"
        ]
    ].copy()

    schedule_df = schedule_result["project_scores"][
        [
            "Project_ID",
            "Delay_Days",
            "Schedule_Variance_Percent",
            "Schedule_Risk_Score",
            "Schedule_Risk_Level"
        ]
    ].copy()

    resource_df = resource_result["project_scores"][
        [
            "Project_ID",
            "Resource_Utilization_Percent",
            "Task_Completion_Percent",
            "Resource_Risk_Score",
            "Resource_Risk_Level"
        ]
    ].copy()

    # ---------------------------------------------------------
    # Merge all three risk dimensions
    # ---------------------------------------------------------

    result = cost_df.merge(
        schedule_df,
        on="Project_ID",
        how="inner"
    )

    result = result.merge(
        resource_df,
        on="Project_ID",
        how="inner"
    )

    # ---------------------------------------------------------
    # Calculate weighted overall risk
    # ---------------------------------------------------------

    result["Overall_Risk_Score"] = (
        result["Cost_Risk_Score"] * 0.35
        +
        result["Schedule_Risk_Score"] * 0.40
        +
        result["Resource_Risk_Score"] * 0.25
    )

    result["Overall_Risk_Score"] = (
        result["Overall_Risk_Score"]
        .round(2)
    )

    # ---------------------------------------------------------
    # Determine overall risk level
    # ---------------------------------------------------------

    def overall_risk_level(score):

        if score <= 24:
            return "Low"

        elif score <= 49:
            return "Medium"

        elif score <= 74:
            return "High"

        else:
            return "Critical"

    result["Overall_Risk_Level"] = (
        result["Overall_Risk_Score"]
        .apply(overall_risk_level)
    )

    # ---------------------------------------------------------
    # Identify primary risk driver
    # ---------------------------------------------------------

    def identify_primary_driver(row):

        risks = {
            "Cost": row["Cost_Risk_Score"],
            "Schedule": row["Schedule_Risk_Score"],
            "Resource": row["Resource_Risk_Score"]
        }

        return max(
            risks,
            key=risks.get
        )

    result["Primary_Risk_Driver"] = (
        result.apply(
            identify_primary_driver,
            axis=1
        )
    )

    # ---------------------------------------------------------
    # Identify number of high-risk dimensions
    # ---------------------------------------------------------

    result["High_Risk_Dimensions"] = (
        (
            result["Cost_Risk_Score"] >= 50
        ).astype(int)
        +
        (
            result["Schedule_Risk_Score"] >= 50
        ).astype(int)
        +
        (
            result["Resource_Risk_Score"] >= 50
        ).astype(int)
    )

    # ---------------------------------------------------------
    # Create recommended action
    # ---------------------------------------------------------

    def recommended_action(row):

        level = row["Overall_Risk_Level"]

        driver = row["Primary_Risk_Driver"]

        if level == "Critical":

            if driver == "Cost":
                return (
                    "Immediate budget review and "
                    "cost-control intervention"
                )

            elif driver == "Schedule":
                return (
                    "Immediate schedule recovery plan "
                    "and task prioritization"
                )

            else:
                return (
                    "Immediate resource reallocation "
                    "and workload review"
                )

        elif level == "High":

            if driver == "Cost":
                return (
                    "Review spending and implement "
                    "cost controls"
                )

            elif driver == "Schedule":
                return (
                    "Review delayed tasks and "
                    "accelerate critical activities"
                )

            else:
                return (
                    "Review resource allocation and "
                    "team workload"
                )

        elif level == "Medium":

            return (
                "Monitor project closely and "
                "address emerging risk"
            )

        else:

            return (
                "Continue normal monitoring"
            )

    result["Recommended_Action"] = (
        result.apply(
            recommended_action,
            axis=1
        )
    )

    # ---------------------------------------------------------
    # Sort by overall risk
    # ---------------------------------------------------------

    result = result.sort_values(
        by="Overall_Risk_Score",
        ascending=False
    ).reset_index(drop=True)

    # ---------------------------------------------------------
    # Add risk rank
    # ---------------------------------------------------------

    result["Risk_Rank"] = (
        result.index + 1
    )

    # ---------------------------------------------------------
    # Summary
    # ---------------------------------------------------------

    summary = {
        "Total_Projects":
            len(result),

        "Critical_Projects":
            int(
                (
                    result["Overall_Risk_Level"]
                    == "Critical"
                ).sum()
            ),

        "High_Risk_Projects":
            int(
                (
                    result["Overall_Risk_Level"]
                    == "High"
                ).sum()
            ),

        "Medium_Risk_Projects":
            int(
                (
                    result["Overall_Risk_Level"]
                    == "Medium"
                ).sum()
            ),

        "Low_Risk_Projects":
            int(
                (
                    result["Overall_Risk_Level"]
                    == "Low"
                ).sum()
            ),

        "Highest_Risk_Project":
            result.iloc[0]["Project_ID"],

        "Highest_Risk_Score":
            result.iloc[0]["Overall_Risk_Score"],

        "Most_Common_Risk_Driver":
            result["Primary_Risk_Driver"]
            .value_counts()
            .idxmax()
    }

    return {
        "project_scores": result,
        "summary": summary
    }


# ---------------------------------------------------------
# Test the Risk Strategist
# ---------------------------------------------------------

if __name__ == "__main__":

    from cost_risk_agent import calculate_cost_risk
    from schedule_risk_agent import calculate_schedule_risk
    from resource_risk_agent import calculate_resource_risk

    # -----------------------------------------------------
    # Load dataset
    # -----------------------------------------------------

    data = pd.read_csv(
        "data/project_data.csv"
    )

    # -----------------------------------------------------
    # Run all three domain agents
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

    result = calculate_overall_risk(
        cost_result,
        schedule_result,
        resource_result
    )

    # -----------------------------------------------------
    # Display results
    # -----------------------------------------------------

    print("\n" + "=" * 60)
    print("RISK STRATEGIST")
    print("=" * 60)

    print("\nOverall Risk Summary:")

    for key, value in result["summary"].items():
        print(f"{key}: {value}")

    print("\nTop 10 Highest-Risk Projects:")

    display_columns = [
        "Risk_Rank",
        "Project_ID",
        "Overall_Risk_Score",
        "Overall_Risk_Level",
        "Primary_Risk_Driver",
        "Cost_Risk_Score",
        "Schedule_Risk_Score",
        "Resource_Risk_Score",
        "High_Risk_Dimensions",
        "Recommended_Action"
    ]

    print(
        result["project_scores"]
        [display_columns]
        .head(10)
        .to_string(index=False)
    )
