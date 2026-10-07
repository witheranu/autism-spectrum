from dataclasses import dataclass
from typing import List

@dataclass
class Scenario:
    id: str
    title: str
    context_description: str
    num_turns: int

SCENARIOS: List[Scenario] = [
    Scenario(
        id="group_project_planning",
        title="Planning a Group Project",
        context_description="Two students are discussing workload distribution, task deadlines, and presentation formats for an upcoming computer science capstone project.",
        num_turns=6
    ),
    Scenario(
        id="scheduling_conflict",
        title="Resolving a Scheduling Conflict",
        context_description="Two team members are negotiating a reschedule for a mandatory study session due to overlapping personal commitments and library room bookings.",
        num_turns=6
    ),
    Scenario(
        id="casual_small_talk",
        title="Casual Small Talk Before Class",
        context_description="Two peers arrive early to a lecture hall and engage in informal conversation about weekend activities, upcoming exams, and coffee preferences.",
        num_turns=4
    ),
    Scenario(
        id="peer_code_review",
        title="Conducting a Peer Code Review",
        context_description="Two lab partners are reviewing code logic and refactoring suggestions for a shared repository assignment before submitting.",
        num_turns=6
    ),
    Scenario(
        id="organizing_social_event",
        title="Organizing a Club Event",
        context_description="Two student club officers discuss venue choices, budget allocations, and itinerary timing for an end-of-semester social gathering.",
        num_turns=8
    )
]

def get_scenario(scenario_id: str) -> Scenario | None:
    return next((s for s in SCENARIOS if s.id == scenario_id), None)
