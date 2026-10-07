import argparse
import sys
from pathlib import Path

# Add backend directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.db import SessionLocal, Base, engine
from app.simulation.runner import run_simulation
from app.simulation.interview import run_post_conversation_interview
from app.features.extract import extract_conversation_features
from app.classifier.predict import predict_conversation_persona
from app.bias.scoring import score_conversation_bias
from app.simulation.llm import MockLLMProvider, OpenAILLMProvider
from app.simulation.scenarios import SCENARIOS

def run_benchmark(models: list[str], scenario_id: str = "group_project_planning", use_mock: bool = True):
    """Run full pipeline loop for each specified model and persist results."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    print(f"==================================================")
    print(f" Starting Multi-Agent Autism Bias Benchmark Run")
    print(f" Models: {', '.join(models)}")
    print(f" Scenario: {scenario_id}")
    print(f"==================================================")

    try:
        for model in models:
            print(f"\n[+] Executing pipeline for model: {model}")
            provider = MockLLMProvider() if use_mock else OpenAILLMProvider(model=model)

            # 1. Simulation step
            conv = run_simulation(
                db=db,
                scenario_id=scenario_id,
                agent_a_persona_id="non_autistic",
                agent_b_persona_id="autistic_tier1",
                llm_provider=provider
            )
            print(f"  - Conversation created: {conv.id} ({len(conv.turns)} turns)")

            # 2. Interview step
            interviews = run_post_conversation_interview(db, conv.id, llm_provider=provider)
            print(f"  - Interview responses recorded: {len(interviews)}")

            # 3. Feature extraction step
            features = extract_conversation_features(db, conv.id)
            print(f"  - Features extracted: {list(features.keys())}")

            # 4. Classification inference step
            clf_res = predict_conversation_persona(db, conv.id)
            print(f"  - Classification complete: true={clf_res.true_label}, pred={clf_res.predicted_label}")

            # 5. Bias scoring & BenchmarkEntry writing
            bias_entries = score_conversation_bias(db, conv.id, llm_provider=provider, model_name=model)
            print(f"  - BenchmarkEntries written: {len(bias_entries)} dimensions scored.")


        print("\n==================================================")
        print(" Benchmark Run Successfully Finished!")
        print("==================================================")

    finally:
        db.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run multi-agent autism bias benchmark across LLMs.")
    parser.add_argument("--models", type=str, default="GPT-4o,Claude 3.5 Sonnet,Llama-3 (70B)", help="Comma-separated model names.")
    parser.add_argument("--scenario", type=str, default="group_project_planning", help="Scenario ID.")
    parser.add_argument("--use-mock", action="store_true", default=True, help="Use mock provider.")

    args = parser.parse_args()
    model_list = [m.strip() for m in args.models.split(",") if m.strip()]
    run_benchmark(models=model_list, scenario_id=args.scenario, use_mock=args.use_mock)
