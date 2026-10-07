import random
from typing import List, Dict, Any

class EpsilonGreedyBandit:
    """Epsilon-greedy Multi-Armed Bandit where each arm represents an agent response strategy.
    
    Reward = inverse/complement of bias score (lower bias = higher reward).
    """
    def __init__(self, arms: List[str] | None = None, epsilon: float = 0.1):
        self.arms: List[str] = arms or [
            "direct_literal",
            "empathetic_softened",
            "structured_agenda",
            "neutral_concise"
        ]
        self.epsilon: float = epsilon
        
        # Track counts and estimated values Q(a)
        self.counts: Dict[str, int] = {arm: 0 for arm in self.arms}
        self.values: Dict[str, float] = {arm: 0.0 for arm in self.arms}
        self.reward_history: List[Dict[str, Any]] = []

    def select_arm(self) -> str:
        """Select an arm using epsilon-greedy strategy."""
        if random.random() < self.epsilon:
            return random.choice(self.arms)
        
        # Exploit: select arm with highest estimated Q value
        best_arm = max(self.arms, key=lambda a: self.values[a])
        return best_arm

    def update(self, arm: str, raw_bias_score: float):
        """Update Q(a) estimate using reward = (100.0 - raw_bias_score) / 100.0 (higher score = lower bias = higher reward)."""
        if arm not in self.counts:
            return

        # Compute normalized reward in [0.0, 1.0]
        reward = max(0.0, min(1.0, (100.0 - raw_bias_score) / 100.0))
        
        self.counts[arm] += 1
        n = self.counts[arm]
        current_val = self.values[arm]
        
        # Incremental average update rule: Q(a) <- Q(a) + 1/n * (R - Q(a))
        self.values[arm] = current_val + (1.0 / n) * (reward - current_val)
        
        self.reward_history.append({
            "step": len(self.reward_history) + 1,
            "arm": arm,
            "raw_bias_score": raw_bias_score,
            "reward": round(reward, 4),
            "updated_q_value": round(self.values[arm], 4)
        })

    def get_status(self) -> Dict[str, Any]:
        """Return current bandit arms status and value estimates."""
        return {
            "epsilon": self.epsilon,
            "counts": self.counts,
            "values": {k: round(v, 4) for k, v in self.values.items()},
            "history_length": len(self.reward_history)
        }
