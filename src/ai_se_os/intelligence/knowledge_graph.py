"""
AI-SE OS Knowledge Graph Service
Manages versioned graph projections of repository knowledge
"""

from typing import Dict, Any, Optional, List, Tuple, Set
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4
import json
import threading

from ..core.data_models import (
    KnowledgeNode,
    KnowledgeEdge,
    KnowledgeGraph,
    KnowledgeNodeType,
    KnowledgeEdgeType
)
from ..core.events import Event, EventType, get_event_bus


class KnowledgeGraphService:
    """
    Knowledge Graph Service for AI-SE OS.
    
    A graph is a derived, queryable projection. It never invents or owns source facts.
    All facts originate from Repository Intelligence, the Genome, or validated experiences.
    """

    def __init__(self):
        self._graphs: Dict[str, KnowledgeGraph] = {}  # repository_id -> graph
        self._lock = threading.RLock()
        self._event_bus = get_event_bus()

    def get_or_create_graph(self, repository_id: str) -> KnowledgeGraph:
        """Get or create a knowledge graph for a repository"""
        with self._lock:
            if repository_id not in self._graphs:
                self._graphs[repository_id] = KnowledgeGraph(
                    version="1.0.0"
                )
            return self._graphs[repository_id]

    def add_node(
        self,
        repository_id: str,
        node_type: KnowledgeNodeType,
        properties: Dict[str, Any]
    ) -> KnowledgeNode:
        """Add a node to the knowledge graph"""
        with self._lock:
            graph = self.get_or_create_graph(repository_id)
            node = KnowledgeNode(
                type=node_type,
                properties=properties
            )
            graph.add_node(node)
            return node

    def add_edge(
        self,
        repository_id: str,
        source_id: UUID,
        target_id: UUID,
        edge_type: KnowledgeEdgeType,
        properties: Optional[Dict[str, Any]] = None
    ) -> KnowledgeEdge:
        """Add an edge to the knowledge graph"""
        with self._lock:
            graph = self.get_or_create_graph(repository_id)
            edge = KnowledgeEdge(
                source_id=source_id,
                target_id=target_id,
                type=edge_type,
                properties=properties or {}
            )
            graph.add_edge(edge)

            self._event_bus.publish(Event(
                type=EventType.KNOWLEDGE_GRAPH_UPDATED,
                source="knowledge_graph",
                producer="intelligence",
                payload={
                    "repository_id": repository_id,
                    "edge_type": edge_type.value,
                    "source_id": str(source_id),
                    "target_id": str(target_id)
                }
            ))

            return edge

    def get_node(self, repository_id: str, node_id: UUID) -> Optional[KnowledgeNode]:
        """Get a node by ID"""
        graph = self._graphs.get(repository_id)
        if not graph:
            return None
        if isinstance(graph.nodes, dict):
            return graph.nodes.get(node_id)
        for node in graph.nodes:
            if getattr(node, "id", None) == node_id:
                return node
        return None

    def find_nodes(
        self,
        repository_id: str,
        node_type: Optional[KnowledgeNodeType] = None,
        properties: Optional[Dict[str, Any]] = None
    ) -> List[KnowledgeNode]:
        """Find nodes by type and/or properties"""
        graph = self._graphs.get(repository_id)
        if not graph:
            return []

        results = list(graph.nodes.values()) if isinstance(graph.nodes, dict) else list(graph.nodes)

        if node_type:
            results = [n for n in results if n.type == node_type]

        if properties:
            for key, value in properties.items():
                results = [n for n in results if n.properties.get(key) == value]

        return results

    def traverse(
        self,
        repository_id: str,
        start_node_id: UUID,
        edge_type: Optional[KnowledgeEdgeType] = None,
        max_depth: int = 3,
        direction: str = "both"
    ) -> List[Dict[str, Any]]:
        """
        Traverse the graph from a starting node.
        
        Args:
            repository_id: Repository identifier
            start_node_id: Starting node UUID
            edge_type: Optional edge type filter
            max_depth: Maximum traversal depth
            direction: "forward", "backward", or "both"
            
        Returns:
            List of path dictionaries
        """
        graph = self._graphs.get(repository_id)
        if not graph:
            return []

        visited: Set[UUID] = set()
        paths: List[Dict[str, Any]] = []

        def _dfs(node_id: UUID, depth: int, path: List[Dict]):
            if depth > max_depth or node_id in visited:
                return

            node = self.get_node(repository_id, node_id)
            if not node:
                return

            visited.add(node_id)
            current_path = path + [{"node_id": str(node_id), "type": node.type.value, "properties": node.properties}]

            # Find connected edges
            edges = graph.get_edges_for_node(node_id)
            for edge in edges:
                if edge_type and edge.type != edge_type:
                    continue

                next_id = None
                if direction in ["forward", "both"] and edge.source_id == node_id:
                    next_id = edge.target_id
                elif direction in ["backward", "both"] and edge.target_id == node_id:
                    next_id = edge.source_id

                if next_id and next_id not in visited:
                    paths.append({
                        "path": current_path + [{"edge": edge.type.value, "target_id": str(next_id)}],
                        "depth": depth + 1
                    })
                    _dfs(next_id, depth + 1, current_path)

        _dfs(start_node_id, 0, [])
        return paths

    def find_shortest_path(
        self,
        repository_id: str,
        source_id: UUID,
        target_id: UUID,
        max_depth: int = 10
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Find shortest path between two nodes (BFS).
        
        Args:
            repository_id: Repository identifier
            source_id: Source node UUID
            target_id: Target node UUID
            max_depth: Maximum search depth
            
        Returns:
            Shortest path as list of hops, or None
        """
        graph = self._graphs.get(repository_id)
        if not graph:
            return None

        from collections import deque

        visited: Set[UUID] = {source_id}
        queue: deque = deque()
        queue.append((source_id, [{"node_id": str(source_id), "type": "start"}]))

        while queue:
            current_id, path = queue.popleft()

            if current_id == target_id:
                return path

            if len(path) >= max_depth:
                continue

            edges = graph.get_edges_for_node(current_id)
            for edge in edges:
                neighbor_id = edge.target_id if edge.source_id == current_id else edge.source_id

                if neighbor_id not in visited:
                    visited.add(neighbor_id)
                    node = self.get_node(repository_id, neighbor_id)
                    new_path = path + [{
                        "edge": edge.type.value,
                        "node_id": str(neighbor_id),
                        "node_type": node.type.value if node else "unknown"
                    }]
                    queue.append((neighbor_id, new_path))

        return None

    def query_cypher(self, repository_id: str, query: str) -> List[Dict[str, Any]]:
        """
        Simulate a Cypher-like query against the in-memory graph.
        Supports basic pattern matching.
        
        In production, this would delegate to Neo4j.
        """
        graph = self._graphs.get(repository_id)
        if not graph:
            return []

        results = []

        # Basic pattern: (node1)-[edge]->(node2)
        for edge in graph.edges:
            source_node = self.get_node(repository_id, edge.source_id)
            target_node = self.get_node(repository_id, edge.target_id)

            if source_node and target_node:
                results.append({
                    "source": {
                        "id": str(source_node.id),
                        "type": source_node.type.value,
                        "properties": source_node.properties
                    },
                    "edge": {
                        "id": str(edge.id),
                        "type": edge.type.value,
                        "properties": edge.properties
                    },
                    "target": {
                        "id": str(target_node.id),
                        "type": target_node.type.value,
                        "properties": target_node.properties
                    }
                })

        return results

    def trace_intent(
        self,
        repository_id: str,
        source_id: str,
        target_type: str,
        max_depth: int = 5
    ) -> Dict[str, Any]:
        """
        Trace intent through the knowledge graph.
        
        Args:
            repository_id: Repository identifier
            source_id: Source node UUID as string
            target_type: Target node type to trace to
            max_depth: Maximum trace depth
            
        Returns:
            Trace results with paths
        """
        graph = self._graphs.get(repository_id)
        if not graph:
            return {"error": "Graph not found"}

        try:
            source_uuid = UUID(source_id)
        except ValueError:
            return {"error": "Invalid source_id"}

        source_node = self.get_node(repository_id, source_uuid)
        if not source_node:
            return {"error": "Source node not found"}

        # Find all nodes of target type
        target_nodes = self.find_nodes(repository_id, KnowledgeNodeType(target_type))

        traces = []
        for target in target_nodes:
            path = self.find_shortest_path(repository_id, source_uuid, target.id, max_depth)
            if path:
                traces.append({
                    "source": source_id,
                    "target": str(target.id),
                    "target_properties": target.properties,
                    "path": path,
                    "hops": len(path) - 1
                })

        return {
            "source_id": source_id,
            "source_type": source_node.type.value,
            "target_type": target_type,
            "traces": traces,
            "trace_count": len(traces),
            "completed_in": "in_memory"
        }

    def get_graph_stats(self, repository_id: str) -> Dict[str, Any]:
        """Get graph statistics"""
        graph = self._graphs.get(repository_id)
        if not graph:
            return {"error": "Graph not found"}

        node_types = {}
        edge_types = {}
        nodes_list = graph.nodes.values() if isinstance(graph.nodes, dict) else graph.nodes
        for node in nodes_list:
            node_types[node.type.value] = node_types.get(node.type.value, 0) + 1
        for edge in graph.edges:
            edge_types[edge.type.value] = edge_types.get(edge.type.value, 0) + 1

        return {
            "total_nodes": len(graph.nodes),
            "total_edges": len(graph.edges),
            "node_types": node_types,
            "edge_types": edge_types,
            "version": graph.version,
            "updated_at": graph.updated_at.isoformat()
        }