from agentlab.experiments.study import Study

study = Study.load("C:/Users/LENOVO/Desktop/AI courses/servicenow/AgentLab/result-dir")

incomplete_tasks = study.find_incomplete(include_errors=True)

if incomplete_tasks:
    print(f"Relancement de {len(incomplete_tasks)} tâches incomplètes...")
    study.run()
else:
    print("Aucune tâche incomplète trouvée.")
