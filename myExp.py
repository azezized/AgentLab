from agentlab.agents.generic_agent import AGENT_4o_MINI
from agentlab.experiments.study import make_study

study = make_study(
    benchmark="miniwob_tiny_test",  # Remplacez par un autre benchmark si nécessaire : "webarena", "workarena_l1", etc.
    agent_args=[AGENT_4o_MINI],
    comment="My first study",
)

# Exécuter l'étude avec 5 processus parallèles
study.run(n_jobs=1)
