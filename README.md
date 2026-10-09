# AI Project Risk Management System

An AI-powered multi-agent system that evaluates project risks across cost, schedule, and resource utilization to support better project planning and decision-making.

## Features

- **Cost Risk Agent:** Identifies budget overruns and evaluates cost-related risks.
- **Schedule Risk Agent:** Analyses project delays and schedule variance.
- **Resource Risk Agent:** Evaluates resource utilization and resource pressure.
- **Risk Strategist:** Combines individual risk scores to calculate overall project risk and recommend actions.
- **What-If Risk Simulator:** Compares project risk under different risk-weighting scenarios.
- **AI Risk Copilot:** Answers questions about project risks and recommended mitigation actions.
- **Interactive Dashboard:** Displays risk summaries, project rankings, and detailed analysis.

## Tech Stack

- Python
- Streamlit
- Pandas and NumPy
- Plotly
- Ollama with Llama 3.2
- Multi-agent architecture

## Project Structure

```text
AI_Project_Risk_Management/
├── agents/
├── data/
│   └── project_data.csv
├── app.py
├── config.py
├── generate_dataset.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Run Locally

1. Clone the repository.
2. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Start the application:

   ```bash
   streamlit run app.py
   ```

4. Open the local URL displayed in the terminal.

The AI Risk Copilot includes a fallback response mechanism when the local Ollama model is unavailable.

## Objective

To demonstrate how multi-agent AI systems can analyse project risks, prioritize critical issues, simulate alternative scenarios, and provide actionable recommendations.

**Note:** The included project dataset is intended for demonstration and analytical purposes.
