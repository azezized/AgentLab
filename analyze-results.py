from agentlab.analyze import inspect_results

result_df = inspect_results.load_result_df(
    "C:/Users/LENOVO/Desktop/AI courses/servicenow/AgentLab/result-dir"
)

print(result_df.head())

from bgym import ExpResult

exp_result = ExpResult(result_df["exp_dir"][0])
step_0_screenshot = exp_result.screenshots[0]
step_0_action = exp_result.steps_info[0].action
