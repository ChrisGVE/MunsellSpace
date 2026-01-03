#!/usr/bin/env python3
"""
Experiment Registry and Logging System

Provides structured tracking for all transformation research experiments.
Supports registration, logging, searching, and comparison of experiments.

Usage:
    from experiment_logger import ExperimentLogger

    logger = ExperimentLogger()

    # Register a new experiment
    exp_id = logger.register_experiment(
        name="Translation+Scaling Munsell",
        method="translation_scaling",
        domain="munsell_cartesian",
        loss_function="combined",
        parameters={"w_centroid": 0.4, "w_volume": 0.3, "w_shape": 0.3}
    )

    # Log results
    logger.log_result(exp_id, {
        "mean_loss": 0.0535,
        "std_loss": 0.0123,
        "families_analyzed": 21,
        "per_family_losses": {...}
    })

    # Log observations
    logger.log_observation(exp_id, "Best performing method so far")

    # Search experiments
    results = logger.search("munsell domain translation")
"""

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict, field
import uuid


BASE_DIR = Path(__file__).parent.parent
REGISTRY_DIR = BASE_DIR / "datasets" / "transformation_analysis"
REGISTRY_FILE = REGISTRY_DIR / "experiment_registry.json"
OBSERVATIONS_FILE = REGISTRY_DIR / "research_observations.md"


@dataclass
class Experiment:
    """Represents a single experiment in the registry."""
    id: str
    name: str
    method: str
    domain: str
    loss_function: str
    parameters: Dict[str, Any]
    status: str = "registered"  # registered, running, completed, failed
    date_created: str = ""
    date_completed: str = ""
    results: Dict[str, Any] = field(default_factory=dict)
    artifacts: List[str] = field(default_factory=list)
    observations: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    parent_experiment: Optional[str] = None  # For follow-up experiments

    def __post_init__(self):
        if not self.date_created:
            self.date_created = datetime.now(timezone.utc).isoformat() + "Z"


class ExperimentLogger:
    """Main class for managing the experiment registry."""

    def __init__(self, registry_path: Optional[Path] = None):
        """Initialize the experiment logger.

        Args:
            registry_path: Optional custom path to registry file.
        """
        self.registry_path = registry_path or REGISTRY_FILE
        self.observations_path = OBSERVATIONS_FILE
        self._ensure_registry_exists()

    def _ensure_registry_exists(self):
        """Create registry file if it doesn't exist."""
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.registry_path.exists():
            self._save_registry({"experiments": [], "metadata": {
                "created": datetime.now(timezone.utc).isoformat() + "Z",
                "version": "1.0.0",
                "project": "MunsellSpace Transformation Research"
            }})

    def _load_registry(self) -> Dict:
        """Load the registry from disk."""
        with open(self.registry_path) as f:
            return json.load(f)

    def _save_registry(self, registry: Dict):
        """Save the registry to disk."""
        with open(self.registry_path, "w") as f:
            json.dump(registry, f, indent=2, default=str)

    def _generate_id(self) -> str:
        """Generate a unique experiment ID."""
        registry = self._load_registry()
        existing_ids = {exp["id"] for exp in registry["experiments"]}

        # Find next sequential ID
        max_num = 0
        for exp_id in existing_ids:
            match = re.match(r"EXP-(\d+)", exp_id)
            if match:
                max_num = max(max_num, int(match.group(1)))

        return f"EXP-{max_num + 1:03d}"

    def register_experiment(
        self,
        name: str,
        method: str,
        domain: str,
        loss_function: str = "combined",
        parameters: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None,
        parent_experiment: Optional[str] = None
    ) -> str:
        """Register a new experiment.

        Args:
            name: Human-readable experiment name
            method: Transformation method (e.g., "translation_scaling", "affine")
            domain: Color space domain (e.g., "munsell_cartesian", "rgb")
            loss_function: Loss function used (e.g., "combined", "centroid_only")
            parameters: Dictionary of hyperparameters
            tags: List of tags for categorization
            parent_experiment: ID of parent experiment if this is a follow-up

        Returns:
            Experiment ID
        """
        exp_id = self._generate_id()

        experiment = Experiment(
            id=exp_id,
            name=name,
            method=method,
            domain=domain,
            loss_function=loss_function,
            parameters=parameters or {},
            tags=tags or [],
            parent_experiment=parent_experiment
        )

        registry = self._load_registry()
        registry["experiments"].append(asdict(experiment))
        self._save_registry(registry)

        print(f"Registered experiment: {exp_id} - {name}")
        return exp_id

    def update_status(self, exp_id: str, status: str):
        """Update experiment status.

        Args:
            exp_id: Experiment ID
            status: New status (registered, running, completed, failed)
        """
        registry = self._load_registry()
        for exp in registry["experiments"]:
            if exp["id"] == exp_id:
                exp["status"] = status
                if status == "completed":
                    exp["date_completed"] = datetime.now(timezone.utc).isoformat() + "Z"
                break
        self._save_registry(registry)

    def log_result(self, exp_id: str, results: Dict[str, Any]):
        """Log results for an experiment.

        Args:
            exp_id: Experiment ID
            results: Dictionary of results (mean_loss, std_loss, per_family, etc.)
        """
        registry = self._load_registry()
        for exp in registry["experiments"]:
            if exp["id"] == exp_id:
                exp["results"] = results
                exp["status"] = "completed"
                exp["date_completed"] = datetime.now(timezone.utc).isoformat() + "Z"
                break
        self._save_registry(registry)
        print(f"Logged results for {exp_id}")

    def log_observation(self, exp_id: str, observation: str):
        """Log an observation for an experiment.

        Args:
            exp_id: Experiment ID
            observation: Text observation
        """
        registry = self._load_registry()
        for exp in registry["experiments"]:
            if exp["id"] == exp_id:
                timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
                exp["observations"].append(f"[{timestamp}] {observation}")
                break
        self._save_registry(registry)

        # Also append to observations markdown
        self._append_to_observations(exp_id, observation)

    def _append_to_observations(self, exp_id: str, observation: str):
        """Append observation to the markdown log."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

        entry = f"\n### [{exp_id}] {timestamp}\n{observation}\n"

        if self.observations_path.exists():
            with open(self.observations_path, "a") as f:
                f.write(entry)
        else:
            with open(self.observations_path, "w") as f:
                f.write("# Research Observations Log\n\n")
                f.write("Automatically generated observations from experiments.\n")
                f.write(f"\n---\n{entry}")

    def add_artifact(self, exp_id: str, artifact_path: str):
        """Add an artifact reference to an experiment.

        Args:
            exp_id: Experiment ID
            artifact_path: Path to artifact file (relative to project)
        """
        registry = self._load_registry()
        for exp in registry["experiments"]:
            if exp["id"] == exp_id:
                if artifact_path not in exp["artifacts"]:
                    exp["artifacts"].append(artifact_path)
                break
        self._save_registry(registry)

    def add_tag(self, exp_id: str, tag: str):
        """Add a tag to an experiment.

        Args:
            exp_id: Experiment ID
            tag: Tag to add
        """
        registry = self._load_registry()
        for exp in registry["experiments"]:
            if exp["id"] == exp_id:
                if tag not in exp["tags"]:
                    exp["tags"].append(tag)
                break
        self._save_registry(registry)

    def get_experiment(self, exp_id: str) -> Optional[Dict]:
        """Get a single experiment by ID.

        Args:
            exp_id: Experiment ID

        Returns:
            Experiment dictionary or None
        """
        registry = self._load_registry()
        for exp in registry["experiments"]:
            if exp["id"] == exp_id:
                return exp
        return None

    def list_experiments(
        self,
        method: Optional[str] = None,
        domain: Optional[str] = None,
        status: Optional[str] = None,
        tags: Optional[List[str]] = None,
        limit: int = 100
    ) -> List[Dict]:
        """List experiments with optional filters.

        Args:
            method: Filter by method
            domain: Filter by domain
            status: Filter by status
            tags: Filter by tags (experiment must have all specified tags)
            limit: Maximum number of results

        Returns:
            List of matching experiments
        """
        registry = self._load_registry()
        results = []

        for exp in registry["experiments"]:
            # Apply filters
            if method and exp["method"] != method:
                continue
            if domain and exp["domain"] != domain:
                continue
            if status and exp["status"] != status:
                continue
            if tags and not all(t in exp.get("tags", []) for t in tags):
                continue

            results.append(exp)

            if len(results) >= limit:
                break

        return results

    def search(self, query: str, limit: int = 20) -> List[Dict]:
        """Full-text search across experiments.

        Searches in: name, observations, method, domain, loss_function

        Args:
            query: Search query (space-separated terms, all must match)
            limit: Maximum results

        Returns:
            List of matching experiments with relevance scores
        """
        registry = self._load_registry()
        query_terms = query.lower().split()
        results = []

        for exp in registry["experiments"]:
            # Build searchable text
            searchable = " ".join([
                exp["name"].lower(),
                exp["method"].lower(),
                exp["domain"].lower(),
                exp["loss_function"].lower(),
                " ".join(exp.get("tags", [])).lower(),
                " ".join(exp.get("observations", [])).lower(),
                json.dumps(exp.get("parameters", {})).lower(),
                json.dumps(exp.get("results", {})).lower()
            ])

            # Count matching terms
            matches = sum(1 for term in query_terms if term in searchable)

            if matches == len(query_terms):  # All terms must match
                results.append({
                    "experiment": exp,
                    "relevance": matches / len(query_terms)
                })

        # Sort by relevance
        results.sort(key=lambda x: x["relevance"], reverse=True)

        return [r["experiment"] for r in results[:limit]]

    def compare_experiments(self, exp_ids: List[str]) -> Dict:
        """Compare multiple experiments side by side.

        Args:
            exp_ids: List of experiment IDs to compare

        Returns:
            Comparison dictionary with aligned metrics
        """
        experiments = []
        for exp_id in exp_ids:
            exp = self.get_experiment(exp_id)
            if exp:
                experiments.append(exp)

        if not experiments:
            return {"error": "No experiments found"}

        comparison = {
            "experiments": exp_ids,
            "comparison_date": datetime.now(timezone.utc).isoformat() + "Z",
            "summary": []
        }

        # Build comparison table
        for exp in experiments:
            summary = {
                "id": exp["id"],
                "name": exp["name"],
                "method": exp["method"],
                "domain": exp["domain"],
                "status": exp["status"],
                "mean_loss": exp.get("results", {}).get("mean_loss"),
                "std_loss": exp.get("results", {}).get("std_loss"),
                "families_analyzed": exp.get("results", {}).get("families_analyzed")
            }
            comparison["summary"].append(summary)

        # Find best performer
        valid = [s for s in comparison["summary"] if s["mean_loss"] is not None]
        if valid:
            best = min(valid, key=lambda x: x["mean_loss"])
            comparison["best_performer"] = best["id"]
            comparison["best_loss"] = best["mean_loss"]

        return comparison

    def export_summary(
        self,
        format: str = "markdown",
        output_path: Optional[Path] = None
    ) -> str:
        """Export registry summary in various formats.

        Args:
            format: Output format ("markdown", "csv", "html")
            output_path: Optional path to save output

        Returns:
            Formatted summary string
        """
        registry = self._load_registry()
        experiments = registry["experiments"]

        if format == "markdown":
            lines = ["# Experiment Registry Summary\n"]
            lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            lines.append(f"Total experiments: {len(experiments)}\n\n")

            # Status counts
            status_counts = {}
            for exp in experiments:
                status = exp["status"]
                status_counts[status] = status_counts.get(status, 0) + 1

            lines.append("## Status Overview\n")
            for status, count in sorted(status_counts.items()):
                lines.append(f"- {status}: {count}\n")

            lines.append("\n## All Experiments\n\n")
            lines.append("| ID | Name | Method | Domain | Mean Loss | Status |\n")
            lines.append("|-----|------|--------|--------|-----------|--------|\n")

            for exp in sorted(experiments, key=lambda x: x["id"]):
                mean_loss = exp.get("results", {}).get("mean_loss", "N/A")
                if isinstance(mean_loss, float):
                    mean_loss = f"{mean_loss:.4f}"
                lines.append(
                    f"| {exp['id']} | {exp['name'][:30]} | {exp['method']} | "
                    f"{exp['domain']} | {mean_loss} | {exp['status']} |\n"
                )

            # Best performers section
            completed = [e for e in experiments if e.get("results", {}).get("mean_loss")]
            if completed:
                lines.append("\n## Best Performers\n\n")
                sorted_by_loss = sorted(
                    completed,
                    key=lambda x: x["results"]["mean_loss"]
                )[:5]
                for i, exp in enumerate(sorted_by_loss, 1):
                    lines.append(
                        f"{i}. **{exp['id']}** - {exp['name']}: "
                        f"{exp['results']['mean_loss']:.4f}\n"
                    )

            output = "".join(lines)

        elif format == "csv":
            lines = ["id,name,method,domain,loss_function,mean_loss,std_loss,status,date_created\n"]
            for exp in experiments:
                mean_loss = exp.get("results", {}).get("mean_loss", "")
                std_loss = exp.get("results", {}).get("std_loss", "")
                lines.append(
                    f"{exp['id']},{exp['name']},{exp['method']},{exp['domain']},"
                    f"{exp['loss_function']},{mean_loss},{std_loss},"
                    f"{exp['status']},{exp['date_created']}\n"
                )
            output = "".join(lines)

        elif format == "html":
            output = "<html><body><h1>Experiment Registry</h1><table border='1'>"
            output += "<tr><th>ID</th><th>Name</th><th>Method</th><th>Mean Loss</th><th>Status</th></tr>"
            for exp in experiments:
                mean_loss = exp.get("results", {}).get("mean_loss", "N/A")
                if isinstance(mean_loss, float):
                    mean_loss = f"{mean_loss:.4f}"
                output += f"<tr><td>{exp['id']}</td><td>{exp['name']}</td>"
                output += f"<td>{exp['method']}</td><td>{mean_loss}</td><td>{exp['status']}</td></tr>"
            output += "</table></body></html>"
        else:
            raise ValueError(f"Unknown format: {format}")

        if output_path:
            with open(output_path, "w") as f:
                f.write(output)
            print(f"Exported to {output_path}")

        return output

    def get_statistics(self) -> Dict:
        """Get registry statistics.

        Returns:
            Dictionary with counts and aggregates
        """
        registry = self._load_registry()
        experiments = registry["experiments"]

        stats = {
            "total_experiments": len(experiments),
            "by_status": {},
            "by_method": {},
            "by_domain": {},
            "completed_with_results": 0,
            "best_experiment": None,
            "best_loss": float("inf")
        }

        for exp in experiments:
            # Count by status
            status = exp["status"]
            stats["by_status"][status] = stats["by_status"].get(status, 0) + 1

            # Count by method
            method = exp["method"]
            stats["by_method"][method] = stats["by_method"].get(method, 0) + 1

            # Count by domain
            domain = exp["domain"]
            stats["by_domain"][domain] = stats["by_domain"].get(domain, 0) + 1

            # Track best
            if exp.get("results", {}).get("mean_loss") is not None:
                stats["completed_with_results"] += 1
                loss = exp["results"]["mean_loss"]
                if loss < stats["best_loss"]:
                    stats["best_loss"] = loss
                    stats["best_experiment"] = exp["id"]

        if stats["best_loss"] == float("inf"):
            stats["best_loss"] = None

        return stats


def migrate_existing_results():
    """Migrate existing Phase 4 results into the experiment registry."""
    logger = ExperimentLogger()

    # Load existing results files
    analysis_dir = REGISTRY_DIR

    # 1. Migrate linear comparison (Translation+Scaling baseline)
    linear_file = analysis_dir / "baseline_losses.json"
    if linear_file.exists():
        with open(linear_file) as f:
            data = json.load(f)

        exp_id = logger.register_experiment(
            name="Translation+Scaling Baseline",
            method="translation_scaling",
            domain="munsell_cartesian",
            loss_function="combined_0.4_0.3_0.3",
            parameters={
                "w_centroid": 0.4,
                "w_volume": 0.3,
                "w_shape": 0.3,
                "n_params": 6
            },
            tags=["baseline", "linear", "phase4"]
        )

        # Calculate summary from data
        if isinstance(data, dict):
            losses = [v for v in data.values() if isinstance(v, (int, float))]
            if losses:
                logger.log_result(exp_id, {
                    "mean_loss": sum(losses) / len(losses),
                    "std_loss": (sum((x - sum(losses)/len(losses))**2 for x in losses) / len(losses))**0.5,
                    "families_analyzed": len(losses),
                    "per_family_losses": data
                })

        logger.add_artifact(exp_id, "datasets/transformation_analysis/baseline_losses.json")
        logger.log_observation(exp_id, "Baseline linear transformation. Best performer in Phase 4.")

    # 2. Migrate nonlinear comparison
    nonlinear_file = analysis_dir / "nonlinear_comparison.json"
    if nonlinear_file.exists():
        with open(nonlinear_file) as f:
            data = json.load(f)

        methods = data.get("results", {})
        for method_name, results in methods.items():
            exp_id = logger.register_experiment(
                name=f"Nonlinear: {method_name}",
                method=method_name,
                domain="munsell_cartesian",
                loss_function="combined",
                parameters={"type": "nonlinear"},
                tags=["nonlinear", "phase4"]
            )

            # Calculate mean from results
            if results:
                losses = [r["final_loss"] for r in results if "final_loss" in r]
                if losses:
                    logger.log_result(exp_id, {
                        "mean_loss": sum(losses) / len(losses),
                        "std_loss": (sum((x - sum(losses)/len(losses))**2 for x in losses) / len(losses))**0.5,
                        "families_analyzed": len(losses),
                        "per_family_results": results
                    })

            logger.add_artifact(exp_id, "datasets/transformation_analysis/nonlinear_comparison.json")

    # 3. Migrate domain comparison
    domain_file = analysis_dir / "domain_comparison.json"
    if domain_file.exists():
        with open(domain_file) as f:
            data = json.load(f)

        for domain_key, domain_data in data.items():
            if domain_key == "analysis":
                continue

            exp_id = logger.register_experiment(
                name=f"Domain: {domain_data.get('domain', domain_key)}",
                method="translation_scaling",
                domain=domain_key,
                loss_function="combined",
                parameters={},
                tags=["domain_comparison", "phase4"]
            )

            logger.log_result(exp_id, {
                "mean_loss": domain_data.get("mean_loss"),
                "std_loss": domain_data.get("std_loss"),
                "description": domain_data.get("description")
            })

            logger.add_artifact(exp_id, "datasets/transformation_analysis/domain_comparison.json")

    # 4. Migrate extended domain comparison
    extended_file = analysis_dir / "extended_domain_comparison.json"
    if extended_file.exists():
        with open(extended_file) as f:
            data = json.load(f)

        for entry in data:
            exp_id = logger.register_experiment(
                name=f"{entry['method']} in {entry['domain']}",
                method=entry["method"].lower().replace("+", "_").replace(" ", "_"),
                domain=entry["domain"].lower(),
                loss_function="combined_0.4_0.3_0.3",
                parameters={},
                tags=["extended_domain", "phase4"]
            )

            logger.log_result(exp_id, {
                "mean_loss": entry.get("mean_loss"),
                "std_loss": entry.get("std_loss"),
                "per_family_losses": entry.get("per_family_losses", {})
            })

            logger.add_artifact(exp_id, "datasets/transformation_analysis/extended_domain_comparison.json")

    print("\nMigration complete!")
    stats = logger.get_statistics()
    print(f"Total experiments in registry: {stats['total_experiments']}")
    print(f"Best performer: {stats['best_experiment']} with loss {stats['best_loss']:.4f}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "migrate":
            migrate_existing_results()
        elif command == "summary":
            logger = ExperimentLogger()
            print(logger.export_summary("markdown"))
        elif command == "stats":
            logger = ExperimentLogger()
            stats = logger.get_statistics()
            print(json.dumps(stats, indent=2))
        elif command == "search":
            if len(sys.argv) > 2:
                query = " ".join(sys.argv[2:])
                logger = ExperimentLogger()
                results = logger.search(query)
                for exp in results:
                    loss = exp.get("results", {}).get("mean_loss", "N/A")
                    if isinstance(loss, float):
                        loss = f"{loss:.4f}"
                    print(f"{exp['id']}: {exp['name']} - {loss}")
            else:
                print("Usage: python experiment_logger.py search <query>")
        else:
            print("Commands: migrate, summary, stats, search <query>")
    else:
        print("Experiment Logger - Research Documentation Framework")
        print("\nCommands:")
        print("  migrate  - Migrate Phase 4 results to registry")
        print("  summary  - Export registry summary")
        print("  stats    - Show registry statistics")
        print("  search   - Search experiments")
