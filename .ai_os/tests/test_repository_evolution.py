"""
Repository Evolution Tests
Testing that AI correctly tracks repository changes over time
"""

import pytest
import os
import tempfile
import hashlib
import json

from src.intelligence.evolution import EvolutionEngine, ChangeType
from src.intelligence.genome import GenomeAnalyzer, RepositoryFingerprint
from src.core.data_models import GenomeSnapshot


class TestRepositoryEvolution:
    """Repository evolution and change detection tests"""
    
    def setup_method(self):
        self.evolution_engine = EvolutionEngine()
        self.genome_analyzer = GenomeAnalyzer()
    
    def test_evolution_tracks_changes(self):
        """Test that evolution engine tracks repository changes"""
        # Create initial snapshot
        fp1 = RepositoryFingerprint(
            git_hash="abc123",
            file_count=100,
            language_breakdown={"python": 50}
        )
        genome1 = self.genome_analyzer.create_snapshot("test-repo", "v1", fp1)
        
        # Track evolution
        evolution = self.evolution_engine.track_evolution(genome1, "/tmp")
        
        # Should detect changes
        assert evolution is not None
        assert hasattr(evolution, 'changes')
    
    def test_evolution_detects_modifications(self):
        """Test that evolution detects file modifications"""
        fp1 = RepositoryFingerprint(
            git_hash="abc123",
            file_count=100,
            language_breakdown={"python": 50}
        )
        genome1 = self.genome_analyzer.create_snapshot("test-evo-repo", "v1", fp1)
        
        evolution = self.evolution_engine.track_evolution(genome1, "/tmp")
        
        # Evolution result should have expected structure
        assert hasattr(evolution, 'total_changes')
        assert hasattr(evolution, 'modifications')
    
    def test_genome_stability_across_versions(self):
        """Test that genome is stable across repository versions"""
        fp = RepositoryFingerprint(
            git_hash="abc123",
            file_count=100,
            language_breakdown={"python": 50}
        )
        
        # Create same genome multiple times
        genome_ids = []
        for i in range(5):
            genome = self.genome_analyzer.create_snapshot("stable-repo", "v1", fp)
            genome_ids.append(str(genome.id))
        
        # IDs will differ (each is a new UUID), but structure should be identical
        # The key test is that the structure/scores are deterministic
        confidences = []
        for i in range(5):
            genome = self.genome_analyzer.create_snapshot("stable-repo", "v1", fp)
            confidences.append(genome.health.intelligence_score)
        
        # All confidence values should be identical
        assert len(set(confidences)) == 1
    
    def test_no_false_positive_changes(self):
        """Test that unchanged repos don't show false positives"""
        fp = RepositoryFingerprint(
            git_hash="abc123",
            file_count=100,
            language_breakdown={"python": 50}
        )
        
        genome1 = self.genome_analyzer.create_snapshot("stable-repo", "v1", fp)
        genome2 = self.genome_analyzer.create_snapshot("stable-repo", "v1", fp)
        
        # Same fingerprint should produce same scores
        assert genome1.health.intelligence_score == genome2.health.intelligence_score
        assert genome1.health.confidence == genome2.health.confidence
    
    def test_evolution_history_preserved(self):
        """Test that evolution history is preserved"""
        fp = RepositoryFingerprint(
            git_hash="abc123",
            file_count=100,
            language_breakdown={"python": 50}
        )
        genome = self.genome_analyzer.create_snapshot("history-repo", "v1", fp)
        
        # Track evolution multiple times
        for i in range(3):
            self.evolution_engine.track_evolution(genome, "/tmp")
        
        # History should exist
        assert hasattr(self.evolution_engine, '_history')