"""
AI-SE OS Reasoning Engine
Engineering analysis, impact prediction, and risk assessment
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import json
import math


@dataclass
class ImpactPrediction:
    """Predicted impact of a change"""
    scope: str = ""
    risk_level: str = "low"  # low, medium, high, critical
    files_affected: List[str] = field(default_factory=list)
    modules_affected: List[str] = field(default_factory=list)
    tests_affected: List[str] = field(default_factory=list)
    breaking_changes: bool = False
    estimated_effort_hours: float = 0.0
    confidence: float = 0.0
    reasoning: List[str] = field(default_factory=list)


@dataclass
class ComplexityAnalysis:
    """Code complexity analysis"""
    cyclomatic_complexity: float = 0.0
    cognitive_complexity: float = 0.0
    dependency_complexity: float = 0.0
    overall_rating: str = "simple"  # simple, moderate, complex, very_complex
    hotspots: List[Dict[str, Any]] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)


@dataclass
class RiskAssessment:
    """Risk assessment for a change"""
    overall_risk: str = "low"
    risk_factors: List[Dict[str, Any]] = field(default_factory=list)
    mitigation: List[str] = field(default_factory=list)
    confidence: float = 0.0


class ReasoningEngine:
    """
    Engineering reasoning and analysis engine.
    
    Provides:
    - Impact prediction for changes
    - Complexity analysis
    - Risk assessment
    - Architecture compliance checking
    """

    def __init__(self):
        self._analysis_cache: Dict[str, Any] = {}

    def predict_impact(
        self,
        repository_id: str,
        change_description: Dict[str, Any]
    ) -> ImpactPrediction:
        """
        Predict the impact of a change.
        
        Args:
            repository_id: Repository identifier
            change_description: Description of the change
            
        Returns:
            ImpactPrediction with scope and risk
        """
        files_changed = change_description.get("files_changed", [])
        modules_changed = change_description.get("modules_changed", [])
        change_type = change_description.get("type", "modification")

        # Calculate risk based on change type and scope
        risk_scores = {
            "refactoring": 0.7,
            "api_change": 0.8,
            "database_change": 0.9,
            "security_change": 0.9,
            "dependency_update": 0.6,
            "modification": 0.4,
            "addition": 0.3,
            "deletion": 0.5,
            "configuration": 0.3,
            "documentation": 0.1
        }

        base_risk = risk_scores.get(change_type, 0.5)
        file_count_risk = min(len(files_changed) * 0.1, 0.5)
        module_count_risk = min(len(modules_changed) * 0.15, 0.5)

        total_risk = min(base_risk + file_count_risk + module_count_risk, 1.0)

        # Determine risk level
        if total_risk >= 0.8:
            risk_level = "critical"
        elif total_risk >= 0.6:
            risk_level = "high"
        elif total_risk >= 0.3:
            risk_level = "medium"
        else:
            risk_level = "low"

        # Estimate effort
        effort_hours = len(files_changed) * 0.5 + len(modules_changed) * 2.0

        reasoning = [
            f"Change type '{change_type}' has base risk {base_risk:.2f}",
            f"Affects {len(files_changed)} files (risk factor: {file_count_risk:.2f})",
            f"Affects {len(modules_changed)} modules (risk factor: {module_count_risk:.2f})",
            f"Overall risk score: {total_risk:.2f} -> {risk_level.upper()}"
        ]

        return ImpactPrediction(
            scope=change_description.get("scope", "local"),
            risk_level=risk_level,
            files_affected=files_changed,
            modules_affected=modules_changed,
            tests_affected=[],  # Would need test mapping
            breaking_changes=total_risk > 0.7,
            estimated_effort_hours=round(effort_hours, 1),
            confidence=1.0 - (total_risk * 0.3),
            reasoning=reasoning
        )

    def analyze_complexity(
        self,
        code_structure: Dict[str, Any]
    ) -> ComplexityAnalysis:
        """
        Analyze code complexity from structure data.
        
        Args:
            code_structure: Code structure with methods, dependencies etc.
            
        Returns:
            ComplexityAnalysis with metrics
        """
        methods = code_structure.get("methods", [])
        dependencies = code_structure.get("dependencies", [])
        conditional_count = sum(m.get("conditionals", 0) for m in methods)
        nesting_depth = max(m.get("max_nesting", 0) for m in methods) if methods else 0

        # Approximate cyclomatic complexity
        cyclomatic = 1 + conditional_count + len(methods)

        # Cognitive complexity (nesting weighted)
        cognitive = conditional_count * (1 + nesting_depth * 0.5)

        # Dependency complexity
        dep_complexity = len(dependencies) * 0.1

        # Overall score (normalized 0-100)
        overall = min(cyclomatic * 2 + cognitive + dep_complexity * 10, 100)

        if overall < 10:
            rating = "simple"
        elif overall < 25:
            rating = "moderate"
        elif overall < 50:
            rating = "complex"
        else:
            rating = "very_complex"

        hotspots = []
        for method in methods:
            m_cyclo = 1 + method.get("conditionals", 0)
            if m_cyclo > 10:
                hotspots.append({
                    "name": method.get("name", "unknown"),
                    "complexity": m_cyclo,
                    "recommendation": "Extract into smaller methods"
                })

        recommendations = []
        if rating in ["complex", "very_complex"]:
            recommendations.append("Consider breaking down large methods")
        if cyclomatic > 20:
            recommendations.append("High cyclomatic complexity - increase test coverage")
        if nesting_depth > 4:
            recommendations.append("Deep nesting detected - extract helper methods")
        if len(dependencies) > 10:
            recommendations.append("High dependency count - consider dependency injection")

        return ComplexityAnalysis(
            cyclomatic_complexity=round(cyclomatic, 1),
            cognitive_complexity=round(cognitive, 1),
            dependency_complexity=round(dep_complexity, 1),
            overall_rating=rating,
            hotspots=hotspots,
            recommendations=recommendations
        )

    def assess_risk(
        self,
        change: Dict[str, Any],
        impact: ImpactPrediction,
        complexity: ComplexityAnalysis
    ) -> RiskAssessment:
        """
        Assess overall risk combining impact and complexity.
        
        Args:
            change: Change description
            impact: Impact prediction
            complexity: Complexity analysis
            
        Returns:
            RiskAssessment with factors and mitigation
        """
        risk_factors = []

        # Impact-based risk
        risk_factors.append({
            "factor": "impact_scope",
            "value": impact.risk_level,
            "weight": 0.4,
            "detail": f"Risk level: {impact.risk_level}, files: {len(impact.files_affected)}"
        })

        # Complexity-based risk
        complexity_risk_map = {"simple": 0.1, "moderate": 0.3, "complex": 0.6, "very_complex": 0.9}
        comp_risk = complexity_risk_map.get(complexity.overall_rating, 0.5)
        risk_factors.append({
            "factor": "complexity",
            "value": complexity.overall_rating,
            "weight": 0.3,
            "detail": f"Complexity rating: {complexity.overall_rating} (score: {comp_risk:.2f})"
        })

        # Breaking changes risk
        if impact.breaking_changes:
            risk_factors.append({
                "factor": "breaking_changes",
                "value": "yes",
                "weight": 0.2,
                "detail": "Change introduces breaking API changes"
            })

        # Security risk (if applicable)
        if "security" in str(change).lower() or "auth" in str(change).lower():
            risk_factors.append({
                "factor": "security_impact",
                "value": "high",
                "weight": 0.3,
                "detail": "Change affects security-sensitive code"
            })

        # Calculate overall risk score
        risk_score = 0.0
        total_weight = sum(f.get("weight", 0.1) for f in risk_factors)

        for factor in risk_factors:
            weight = factor["weight"]
            value = factor["value"]

            if value in ["critical", "very_complex"]:
                score = 0.9
            elif value in ["high", "complex"]:
                score = 0.7
            elif value in ["medium", "moderate"]:
                score = 0.5
            elif value in ["low", "simple", "yes"]:
                score = 0.3
            else:
                score = 0.1

            risk_score += score * weight

        risk_score = risk_score / total_weight if total_weight > 0 else 0.5

        if risk_score >= 0.7:
            overall_risk = "high"
        elif risk_score >= 0.4:
            overall_risk = "medium"
        else:
            overall_risk = "low"

        # Mitigation strategies
        mitigation = []
        if overall_risk == "high":
            mitigation.append("Require senior developer review")
            mitigation.append("Add comprehensive test coverage")
            mitigation.append("Run full regression test suite")
            mitigation.append("Consider phased rollout")

        if impact.breaking_changes:
            mitigation.append("Document breaking changes in changelog")
            mitigation.append("Create migration guide for consumers")

        if complexity.overall_rating in ["complex", "very_complex"]:
            mitigation.append("Refactor complex code before making changes")
            mitigation.append("Add inline documentation")

        return RiskAssessment(
            overall_risk=overall_risk,
            risk_factors=risk_factors,
            mitigation=mitigation,
            confidence=min(impact.confidence, 1.0 - complexity.cyclomatic_complexity / 100)
        )

    def check_architecture_compliance(
        self,
        change: Dict[str, Any],
        architecture_rules: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Check if a change complies with architecture rules.
        
        Args:
            change: Change description
            architecture_rules: List of architecture rules
            
        Returns:
            List of compliance findings
        """
        findings = []

        for rule in architecture_rules:
            rule_type = rule.get("type", "")
            rule_pattern = rule.get("pattern", "")
            severity = rule.get("severity", "warning")

            # Basic pattern matching
            if rule_type == "layer_violation":
                from_layer = change.get("from_layer", "")
                to_layer = change.get("to_layer", "")
                if from_layer and to_layer:
                    # Check if dependency is allowed
                    allowed = rule.get("allowed_dependencies", [])
                    if to_layer not in allowed and from_layer in rule.get("layers", []):
                        findings.append({
                            "type": "layer_violation",
                            "severity": severity,
                            "message": f"Dependency from '{from_layer}' to '{to_layer}' violates architecture",
                            "rule": rule.get("name", "unnamed")
                        })

            elif rule_type == "naming_convention":
                name = change.get("name", "")
                convention = rule.get("convention", "")
                if name and convention and not name.startswith(convention):
                    findings.append({
                        "type": "naming_violation",
                        "severity": severity,
                        "message": f"'{name}' does not follow naming convention '{convention}'",
                        "rule": rule.get("name", "unnamed")
                    })

        return findings