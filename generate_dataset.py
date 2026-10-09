import pandas as pd
import numpy as np
import os

# ---------------------------------------------------------
# AI PROJECT RISK MANAGEMENT SYSTEM
# Dataset Generator
# ---------------------------------------------------------

# Reproducible results
np.random.seed(42)

# Number of projects
NUM_PROJECTS = 300

# ---------------------------------------------------------
# Basic project information
# ---------------------------------------------------------

departments = [
    "IT",
    "Marketing",
    "Operations",
    "Finance",
    "HR",
    "Product",
    "Sales"
]

manager_names = [
    "Manager A",
    "Manager B",
    "Manager C",
    "Manager D",
    "Manager E",
    "Manager F",
    "Manager G",
    "Manager H"
]

project_types = [
    "Digital Transformation",
    "Product Launch",
    "System Upgrade",
    "Marketing Campaign",
    "Process Improvement",
    "Data Analytics",
    "Infrastructure Upgrade"
]

projects = []

# ---------------------------------------------------------
# Generate projects
# ---------------------------------------------------------

for i in range(1, NUM_PROJECTS + 1):

    project_id = f"P{i:03d}"

    department = np.random.choice(departments)

    manager = np.random.choice(manager_names)

    project_type = np.random.choice(project_types)

    project_name = f"{project_type} {i:03d}"

    # -----------------------------------------------------
    # Budget and duration
    # -----------------------------------------------------

    budget = np.random.randint(500000, 5000001)

    planned_duration = np.random.randint(60, 241)

    # -----------------------------------------------------
    # Select project scenario
    # -----------------------------------------------------

    scenario = np.random.choice(
        [
            "Healthy",
            "Cost Risk",
            "Schedule Risk",
            "Resource Risk",
            "Critical Risk"
        ],
        p=[
            0.50,
            0.15,
            0.15,
            0.10,
            0.10
        ]
    )

    # -----------------------------------------------------
    # Default project values
    # -----------------------------------------------------

    actual_spend_ratio = np.random.uniform(
        0.85,
        1.05
    )

    delay_days = np.random.randint(
        0,
        11
    )

    resource_utilization = np.random.uniform(
        60,
        85
    )

    task_completion = np.random.uniform(
        65,
        100
    )

    # -----------------------------------------------------
    # Cost Risk scenario
    # -----------------------------------------------------

    if scenario == "Cost Risk":

        actual_spend_ratio = np.random.uniform(
            1.15,
            1.35
        )

        delay_days = np.random.randint(
            5,
            21
        )

        resource_utilization = np.random.uniform(
            75,
            90
        )

        task_completion = np.random.uniform(
            55,
            85
        )

    # -----------------------------------------------------
    # Schedule Risk scenario
    # -----------------------------------------------------

    elif scenario == "Schedule Risk":

        actual_spend_ratio = np.random.uniform(
            0.95,
            1.15
        )

        delay_days = np.random.randint(
            25,
            61
        )

        resource_utilization = np.random.uniform(
            75,
            92
        )

        task_completion = np.random.uniform(
            45,
            75
        )

    # -----------------------------------------------------
    # Resource Risk scenario
    # -----------------------------------------------------

    elif scenario == "Resource Risk":

        actual_spend_ratio = np.random.uniform(
            1.00,
            1.15
        )

        delay_days = np.random.randint(
            10,
            31
        )

        resource_utilization = np.random.uniform(
            93,
            100
        )

        task_completion = np.random.uniform(
            55,
            80
        )

    # -----------------------------------------------------
    # Critical Risk scenario
    # -----------------------------------------------------

    elif scenario == "Critical Risk":

        actual_spend_ratio = np.random.uniform(
            1.20,
            1.50
        )

        delay_days = np.random.randint(
            35,
            91
        )

        resource_utilization = np.random.uniform(
            94,
            100
        )

        task_completion = np.random.uniform(
            35,
            65
        )

    # -----------------------------------------------------
    # Calculate actual spend
    # -----------------------------------------------------

    actual_spend = budget * actual_spend_ratio

    # -----------------------------------------------------
    # Calculate actual duration
    # -----------------------------------------------------

    actual_duration = (
        planned_duration +
        delay_days
    )

    # -----------------------------------------------------
    # Team size
    # -----------------------------------------------------

    team_size = np.random.randint(
        5,
        31
    )

    # -----------------------------------------------------
    # Client satisfaction
    # -----------------------------------------------------

    if scenario == "Healthy":

        client_satisfaction = np.random.uniform(
            75,
            100
        )

    elif scenario == "Cost Risk":

        client_satisfaction = np.random.uniform(
            60,
            85
        )

    elif scenario == "Schedule Risk":

        client_satisfaction = np.random.uniform(
            45,
            75
        )

    elif scenario == "Resource Risk":

        client_satisfaction = np.random.uniform(
            50,
            80
        )

    else:

        client_satisfaction = np.random.uniform(
            30,
            60
        )

    # -----------------------------------------------------
    # Calculate cost overrun
    # -----------------------------------------------------

    cost_overrun = (
        (actual_spend - budget)
        / budget
    ) * 100

    # -----------------------------------------------------
    # Determine project risk level
    # -----------------------------------------------------

    if (
        cost_overrun > 20
        and delay_days > 30
        and resource_utilization > 93
    ):

        risk_level = "Critical"

    elif (
        cost_overrun > 15
        or delay_days > 25
        or resource_utilization > 92
    ):

        risk_level = "High"

    elif (
        cost_overrun > 8
        or delay_days > 10
        or resource_utilization > 85
    ):

        risk_level = "Medium"

    else:

        risk_level = "Low"

    # -----------------------------------------------------
    # Add project to dataset
    # -----------------------------------------------------

    projects.append({

        "Project_ID":
            project_id,

        "Project_Name":
            project_name,

        "Department":
            department,

        "Project_Manager":
            manager,

        "Budget":
            round(budget, 2),

        "Actual_Spend":
            round(actual_spend, 2),

        "Planned_Duration_Days":
            planned_duration,

        "Actual_Duration_Days":
            actual_duration,

        "Task_Completion_Percent":
            round(task_completion, 2),

        "Resource_Utilization_Percent":
            round(resource_utilization, 2),

        "Team_Size":
            team_size,

        "Delay_Days":
            delay_days,

        "Risk_Level":
            risk_level,

        "Client_Satisfaction":
            round(client_satisfaction, 2)
    })


# ---------------------------------------------------------
# Create DataFrame
# ---------------------------------------------------------

df = pd.DataFrame(projects)


# ---------------------------------------------------------
# Make sure data folder exists
# ---------------------------------------------------------

os.makedirs(
    "data",
    exist_ok=True
)


# ---------------------------------------------------------
# Save CSV
# ---------------------------------------------------------

output_path = "data/project_data.csv"

df.to_csv(
    output_path,
    index=False
)


# ---------------------------------------------------------
# Display results
# ---------------------------------------------------------

print("=" * 60)
print("PROJECT RISK DATASET GENERATED SUCCESSFULLY")
print("=" * 60)

print(f"\nNumber of projects: {len(df)}")

print(f"Number of columns: {len(df.columns)}")

print("\nColumns:")
print(list(df.columns))

print("\nRisk Distribution:")
print(
    df["Risk_Level"]
    .value_counts()
    .sort_index()
)

print("\nFirst 5 projects:")
print(
    df.head().to_string(index=False)
)

print("\nDataset statistics:")

print(
    f"Average Budget: "
    f"₹{df['Budget'].mean():,.2f}"
)

print(
    f"Average Actual Spend: "
    f"₹{df['Actual_Spend'].mean():,.2f}"
)

print(
    f"Average Delay: "
    f"{df['Delay_Days'].mean():.2f} days"
)

print(
    f"Average Resource Utilization: "
    f"{df['Resource_Utilization_Percent'].mean():.2f}%"
)

print(
    f"\nDataset saved to: "
    f"{output_path}"
)

print("=" * 60)