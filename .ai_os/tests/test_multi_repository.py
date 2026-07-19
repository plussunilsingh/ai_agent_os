"""
Multi-Repository Tests
Testing cross-repository intelligence and impact analysis
"""

import pytest

from src.intelligence.knowledge_graph import KnowledgeGraphService
from src.core.data_models import KnowledgeNodeType, KnowledgeEdgeType


class TestMultiRepository:
    """Cross-repository intelligence tests"""
    
    def setup_method(self):
        self.kg = KnowledgeGraphService()
    
    def test_cross_repo_dependencies(self):
        """Test that dependencies across repos can be tracked"""
        # Setup: frontend depends on backend
        frontend = self.kg.add_node("frontend-repo", KnowledgeNodeType.REPOSITORY, {"name": "frontend"})
        backend = self.kg.add_node("backend-repo", KnowledgeNodeType.REPOSITORY, {"name": "backend"})
        
        self.kg.add_edge("frontend-repo", frontend.id, backend.id, KnowledgeEdgeType.DEPENDS_ON)
        
        # Verify dependency chain
        paths = self.kg.traverse("frontend-repo", frontend.id, max_depth=2)
        
        assert len(paths) > 0
    
    def test_cross_repo_impact(self):
        """Test impact analysis across repositories"""
        shared = self.kg.add_node("shared-repo", KnowledgeNodeType.REPOSITORY, {"name": "shared"})
        service_a = self.kg.add_node("service-a", KnowledgeNodeType.REPOSITORY, {"name": "service-a"})
        service_b = self.kg.add_node("service-b", KnowledgeNodeType.REPOSITORY, {"name": "service-b"})
        
        # Both services depend on shared
        self.kg.add_edge("service-a", service_a.id, shared.id, KnowledgeEdgeType.DEPENDS_ON)
        self.kg.add_edge("service-b", service_b.id, shared.id, KnowledgeEdgeType.DEPENDS_ON)
        
        # Find all repos that would be affected by change to shared
        affected = []
        for edge in self.kg._graphs.get("service-a", self.kg.get_or_create_graph("service-a")).edges:
            if edge.target_id == shared.id:
                affected.append("service-a")
        
        assert "service-a" in affected or "service-b" in affected
    
    def test_pattern_detection_across_repos(self):
        """Test pattern detection across repositories"""
        repos = ["repo-a", "repo-b", "repo-c"]
        
        for repo in repos:
            self.kg.add_node(repo, KnowledgeNodeType.REPOSITORY, {"name": repo})
        
        stats = {}
        for repo in repos:
            graph_stats = self.kg.get_graph_stats(repo)
            stats[repo] = graph_stats
        
        # Each repo should have stats
        for repo in repos:
            assert stats[repo]["total_nodes"] >= 1
    
    def test_knowledge_graph_stats_multi_repo(self):
        """Test graph stats across multiple repositories"""
        for i in range(5):
            repo_id = f"repo-{i}"
            self.kg.add_node(repo_id, KnowledgeNodeType.REPOSITORY, {"name": f"Repo {i}"})
        
        # Verify each repo has its own isolated graph
        for i in range(5):
            repo_id = f"repo-{i}"
            stats = self.kg.get_graph_stats(repo_id)
            assert stats["total_nodes"] == 1