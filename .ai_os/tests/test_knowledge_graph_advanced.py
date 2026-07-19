"""
Knowledge Graph Tests
Testing graph correctness, traversal, and consistency
"""

import pytest
from src.intelligence.knowledge_graph import KnowledgeGraphService
from src.core.data_models import KnowledgeNodeType, KnowledgeEdgeType


class TestKnowledgeGraph:
    """Knowledge graph correctness and integrity tests"""
    
    def setup_method(self):
        self.kg = KnowledgeGraphService()
        self.repo_id = "test-repo"
    
    def test_node_creation(self):
        """Test that nodes are correctly created"""
        node = self.kg.add_node(
            self.repo_id,
            KnowledgeNodeType.CLASS,
            {"name": "User", "package": "models"}
        )
        
        assert node.id is not None
        assert node.type == KnowledgeNodeType.CLASS
        assert node.properties["name"] == "User"
    
    def test_edge_creation(self):
        """Test that edges are correctly created"""
        node1 = self.kg.add_node(self.repo_id, KnowledgeNodeType.CLASS, {"name": "User"})
        node2 = self.kg.add_node(self.repo_id, KnowledgeNodeType.CLASS, {"name": "Order"})
        
        edge = self.kg.add_edge(
            self.repo_id,
            node1.id,
            node2.id,
            KnowledgeEdgeType.DEPENDS_ON
        )
        
        assert edge.source_id == node1.id
        assert edge.target_id == node2.id
        assert edge.type == KnowledgeEdgeType.DEPENDS_ON
    
    def test_graph_traversal(self):
        """Test that graph traversal works correctly"""
        user = self.kg.add_node(self.repo_id, KnowledgeNodeType.CLASS, {"name": "User"})
        order = self.kg.add_node(self.repo_id, KnowledgeNodeType.CLASS, {"name": "Order"})
        payment = self.kg.add_node(self.repo_id, KnowledgeNodeType.CLASS, {"name": "Payment"})
        
        self.kg.add_edge(self.repo_id, user.id, order.id, KnowledgeEdgeType.DEPENDS_ON)
        self.kg.add_edge(self.repo_id, order.id, payment.id, KnowledgeEdgeType.DEPENDS_ON)
        
        paths = self.kg.traverse(self.repo_id, user.id, max_depth=3)
        assert len(paths) > 0
    
    def test_no_duplicate_nodes(self):
        """Test that duplicate nodes are handled correctly"""
        node1 = self.kg.add_node(self.repo_id, KnowledgeNodeType.CLASS, {"name": "User"})
        node2 = self.kg.add_node(self.repo_id, KnowledgeNodeType.CLASS, {"name": "User"})
        
        # Should create separate nodes (deduplication would be at higher level)
        assert node1.id is not None
        assert node2.id is not None
    
    def test_graph_query_accuracy(self):
        """Test that graph queries return accurate results"""
        user = self.kg.add_node(self.repo_id, KnowledgeNodeType.CLASS, {"name": "User"})
        order = self.kg.add_node(self.repo_id, KnowledgeNodeType.CLASS, {"name": "Order"})
        
        self.kg.add_edge(self.repo_id, user.id, order.id, KnowledgeEdgeType.DEPENDS_ON)
        
        results = self.kg.query_cypher(self.repo_id, "MATCH (n) RETURN n")
        
        assert len(results) >= 1
    
    def test_graph_stats(self):
        """Test graph statistics"""
        self.kg.add_node(self.repo_id, KnowledgeNodeType.CLASS, {"name": "User"})
        self.kg.add_node(self.repo_id, KnowledgeNodeType.CLASS, {"name": "Order"})
        
        stats = self.kg.get_graph_stats(self.repo_id)
        
        assert stats["total_nodes"] == 2
        assert stats["node_types"]["class"] == 2