"""
AI-SE OS Client - Thin SDK
Communicates with the central AI-SE OS service
"""

from typing import Optional, Dict, Any, List, Iterator
from datetime import datetime
import os
import json
import requests

from .config import Config
from .models import (
    Repository,
    Task,
    Plan,
    Execution,
    ValidationResult,
    Experience,
    GenomeSnapshot,
    SimulationResult,
    EconomicsAnalysis,
    IntelligenceScore,
    TrustExplanation
)
from .exceptions import (
    AISeOSError,
    AuthenticationError,
    NotFoundError,
    ValidationError,
    RateLimitError
)


class AISeOSClient:
    """
    Thin client for AI-SE OS central service.
    
    This client does NOT contain:
    - No planning logic
    - No reasoning
    - No caching
    - No memory
    - No genome building
    - No knowledge graph
    - No model routing
    - No prompt engineering
    
    It ONLY communicates with the central AI-SE OS service.
    """

    def __init__(self, config: Optional[Config] = None):
        """
        Initialize the AI-SE OS client.
        
        Args:
            config: Client configuration. If None, loads from environment.
        """
        self.config = config or Config.from_env()
        self.base_url = self.config.endpoint.rstrip("/")
        self.api_key = self.config.api_key
        self.timeout = self.config.timeout or 60
        
        # Session for connection pooling
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": f"ai-se-os-sdk-python/1.0.0"
        })
    
    # ========================================================================
    # Repository Management
    # ========================================================================
    
    def register_repository(self, repository: Repository) -> Dict[str, Any]:
        """
        Register a repository with AI-SE OS.
        
        Args:
            repository: Repository configuration
        
        Returns:
            Registration response with repository_id
        """
        response = self._post("/repositories/register", repository.to_dict())
        return response
    
    def get_genome(self, repository_id: str, version: Optional[str] = None) -> GenomeSnapshot:
        """
        Get the Genome snapshot for a repository.
        
        Args:
            repository_id: Repository identifier
            version: Optional specific version
        
        Returns:
            GenomeSnapshot
        """
        params = {}
        if version:
            params["version"] = version
        data = self._get(f"/repositories/{repository_id}/genome", params=params)
        return GenomeSnapshot.from_dict(data)
    
    def analyze_repository(self, repository_id: str) -> Dict[str, Any]:
        """
        Trigger repository analysis.
        
        Args:
            repository_id: Repository identifier
        
        Returns:
            Analysis status
        """
        return self._post(f"/repositories/{repository_id}/analyze")
    
    # ========================================================================
    # Planning
    # ========================================================================
    
    def generate_plan(self, requirement: str, repository_id: str, context: Optional[Dict] = None) -> Plan:
        """
        Generate a task plan from a requirement.
        
        Args:
            requirement: Natural language requirement
            repository_id: Repository identifier
            context: Optional context
        
        Returns:
            Plan
        """
        payload = {
            "requirement": requirement,
            "repository_id": repository_id,
            "context": context or {}
        }
        data = self._post("/plans/generate", payload)
        return Plan.from_dict(data)
    
    # ========================================================================
    # Execution
    # ========================================================================
    
    def execute_plan(self, plan_id: str, model: Optional[str] = None, max_tokens: Optional[int] = None) -> Execution:
        """
        Execute a plan.
        
        Args:
            plan_id: Plan identifier
            model: Optional model override
            max_tokens: Optional token limit
        
        Returns:
            Execution
        """
        payload = {}
        if model:
            payload["model"] = model
        if max_tokens:
            payload["max_tokens"] = max_tokens
        
        data = self._post(f"/plans/{plan_id}/execute", payload)
        return Execution.from_dict(data)
    
    def get_execution_status(self, execution_id: str) -> Dict[str, Any]:
        """
        Get execution status.
        
        Args:
            execution_id: Execution identifier
        
        Returns:
            Status information
        """
        return self._get(f"/executions/{execution_id}/status")
    
    # ========================================================================
    # Validation
    # ========================================================================
    
    def run_validation(self, repository_id: str, change_id: Optional[str] = None, layers: Optional[List[str]] = None) -> ValidationResult:
        """
        Run validation on a repository change.
        
        Args:
            repository_id: Repository identifier
            change_id: Optional change identifier
            layers: Optional validation layers
        
        Returns:
            ValidationResult
        """
        payload = {
            "repository_id": repository_id,
            "layers": layers or ["build", "static", "test", "architecture", "security", "policy", "runtime", "acceptance"]
        }
        if change_id:
            payload["change_id"] = change_id
        
        data = self._post("/validation/run", payload)
        return ValidationResult.from_dict(data)
    
    # ========================================================================
    # Experience
    # ========================================================================
    
    def search_experiences(self, query: str, filters: Optional[Dict] = None, limit: int = 10) -> List[Experience]:
        """
        Search engineering experiences.
        
        Args:
            query: Search query
            filters: Optional filters
            limit: Maximum results
        
        Returns:
            List of Experiences
        """
        payload = {
            "query": query,
            "filters": filters or {},
            "limit": limit
        }
        data = self._post("/experiences/search", payload)
        return [Experience.from_dict(item) for item in data.get("experiences", [])]
    
    def recommend_experience(self, problem: str, context: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """
        Get experience recommendations.
        
        Args:
            problem: Problem description
            context: Optional context
        
        Returns:
            List of recommendations
        """
        payload = {
            "problem": problem,
            "context": context or {}
        }
        data = self._post("/experiences/recommend", payload)
        return data.get("recommendations", [])
    
    # ========================================================================
    # Physics
    # ========================================================================
    
    def predict_impact(self, repository_id: str, change: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict impact of a change.
        
        Args:
            repository_id: Repository identifier
            change: Change description
        
        Returns:
            Impact prediction
        """
        payload = {
            "repository_id": repository_id,
            "change": change
        }
        return self._post("/physics/predict", payload)
    
    # ========================================================================
    # Simulation
    # ========================================================================
    
    def run_simulation(self, repository_id: str, change: Dict[str, Any], scenario: Optional[str] = None) -> SimulationResult:
        """
        Run a simulation.
        
        Args:
            repository_id: Repository identifier
            change: Change description
            scenario: Optional scenario name
        
        Returns:
            SimulationResult
        """
        payload = {
            "repository_id": repository_id,
            "change": change
        }
        if scenario:
            payload["scenario"] = scenario
        
        data = self._post("/simulation/run", payload)
        return SimulationResult.from_dict(data)
    
    # ========================================================================
    # Economics
    # ========================================================================
    
    def analyze_economics(self, decision_id: str, alternatives: List[Dict[str, Any]]) -> EconomicsAnalysis:
        """
        Analyze economics of a decision.
        
        Args:
            decision_id: Decision identifier
            alternatives: List of alternatives
        
        Returns:
            EconomicsAnalysis
        """
        payload = {
            "decision_id": decision_id,
            "alternatives": alternatives
        }
        data = self._post("/economics/analyze", payload)
        return EconomicsAnalysis.from_dict(data)
    
    # ========================================================================
    # Intelligence Score
    # ========================================================================
    
    def get_intelligence_score(self, repository_id: str) -> IntelligenceScore:
        """
        Get intelligence score for a repository.
        
        Args:
            repository_id: Repository identifier
        
        Returns:
            IntelligenceScore
        """
        data = self._get("/intelligence/score", params={"repository_id": repository_id})
        return IntelligenceScore.from_dict(data)
    
    # ========================================================================
    # Trust
    # ========================================================================
    
    def explain_decision(self, decision_id: str) -> TrustExplanation:
        """
        Get explanation for a decision.
        
        Args:
            decision_id: Decision identifier
        
        Returns:
            TrustExplanation
        """
        payload = {"decision_id": decision_id}
        data = self._post("/trust/explain", payload)
        return TrustExplanation.from_dict(data)
    
    # ========================================================================
    # Knowledge Graph
    # ========================================================================
    
    def query_knowledge_graph(self, query: str, parameters: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Query the knowledge graph.
        
        Args:
            query: Graph query (Cypher)
            parameters: Query parameters
        
        Returns:
            Query results
        """
        payload = {
            "query": query,
            "parameters": parameters or {}
        }
        return self._post("/knowledge/graph/query", payload)
    
    def trace_intent(self, source_id: str, target_type: str, depth: int = 5) -> Dict[str, Any]:
        """
        Trace intent through the knowledge graph.
        
        Args:
            source_id: Source node ID
            target_type: Target node type
            depth: Maximum depth
        
        Returns:
            Trace results
        """
        payload = {
            "source_id": source_id,
            "target_type": target_type,
            "depth": depth
        }
        return self._post("/knowledge/graph/trace", payload)
    
    # ========================================================================
    # Internal HTTP Methods
    # ========================================================================
    
    def _request(self, method: str, path: str, data: Optional[Dict] = None, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Make HTTP request to AI-SE OS service.
        """
        url = f"{self.base_url}{path}"
        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                params=params,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                raise AuthenticationError("Invalid API key or authentication failed")
            elif response.status_code == 404:
                raise NotFoundError(f"Resource not found: {path}")
            elif response.status_code == 429:
                raise RateLimitError("Rate limit exceeded. Please try again later.")
            elif response.status_code >= 400:
                error_data = response.json() if response.content else {}
                raise AISeOSError(
                    f"Request failed: {response.status_code}",
                    status_code=response.status_code,
                    details=error_data
                )
            
            return response.json()
        
        except requests.exceptions.Timeout:
            raise AISeOSError(f"Request timed out after {self.timeout}s")
        except requests.exceptions.ConnectionError:
            raise AISeOSError(f"Could not connect to AI-SE OS at {self.base_url}")
        except AISeOSError:
            raise
        except Exception as e:
            raise AISeOSError(f"Unexpected error: {str(e)}")
    
    def _get(self, path: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """GET request"""
        return self._request("GET", path, params=params)
    
    def _post(self, path: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """POST request"""
        return self._request("POST", path, data=data)
    
    def _put(self, path: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """PUT request"""
        return self._request("PUT", path, data=data)
    
    def _delete(self, path: str) -> Dict[str, Any]:
        """DELETE request"""
        return self._request("DELETE", path)
    
    def close(self):
        """Close the client session"""
        self.session.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()