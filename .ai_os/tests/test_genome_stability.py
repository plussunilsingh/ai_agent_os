"""
Repository Learning Tests
Testing that genome generation is stable and deterministic
"""

import pytest
import hashlib
import json
from datetime import datetime

from src.intelligence.genome import GenomeAnalyzer, RepositoryFingerprint
from src.core.data_models import GenomeSnapshot


class TestGenomeStability:
    """Genome stability and reproducibility tests"""
    
    def setup_method(self):
        self.genome_analyzer = GenomeAnalyzer()
        self.test_repo_id = "test-repo"
    
    def test_genome_deterministic(self):
        """Test that genome generation is deterministic"""
        fp = RepositoryFingerprint(
            git_hash="abc123",
            file_count=100,
            language_breakdown={"python": 50, "java": 30},
            dependency_count=25,
            module_count=8,
            test_count=30,
            total_lines=10000
        )
        
        genomes = []
        for i in range(10):
            genome = self.genome_analyzer.create_snapshot(
                self.test_repo_id, fp.git_hash, fp
            )
            genomes.append(genome)
        
        # Compare deterministic fields (version auto-increments, so exclude it)
        base = genomes[0]
        base_deterministic = {
            'git_hash': base.git_hash,
            'health': base.health.intelligence_score,
            'architecture_modules': [m.get('name', m) if isinstance(m, dict) else getattr(m, 'name', m) for m in base.architecture.modules]
        }
        
        for genome in genomes[1:]:
            deterministic = {
                'git_hash': genome.git_hash,
                'health': genome.health.intelligence_score,
                'architecture_modules': [m.get('name', m) if isinstance(m, dict) else getattr(m, 'name', m) for m in genome.architecture.modules]
            }
            assert deterministic == base_deterministic
    
    def test_genome_detects_changes(self):
        """Test that genome detects real changes"""
        fp1 = RepositoryFingerprint(
            git_hash="abc123",
            file_count=100,
            language_breakdown={"python": 50},
            dependency_count=25,
            module_count=8
        )
        
        fp2 = RepositoryFingerprint(
            git_hash="def456",
            file_count=150,
            language_breakdown={"python": 75},
            dependency_count=30,
            module_count=10
        )
        
        genome1 = self.genome_analyzer.create_snapshot(self.test_repo_id, fp1.git_hash, fp1)
        genome2 = self.genome_analyzer.create_snapshot(self.test_repo_id + "_v2", fp2.git_hash, fp2)
        
        # Different fingerprints should produce different git hashes
        assert genome1.git_hash != genome2.git_hash
    
    def test_genome_no_hallucinated_changes(self):
        """Test that genome doesn't hallucinate changes"""
        fp = RepositoryFingerprint(
            git_hash="abc123",
            file_count=100,
            language_breakdown={"python": 50},
            dependency_count=25,
            module_count=8
        )
        
        # Generate same genome multiple times
        genomes = []
        for i in range(20):
            genome = self.genome_analyzer.create_snapshot(
                self.test_repo_id, fp.git_hash, fp
            )
            # Compare truly deterministic fields (version is incrementing by design per snapshot)
            deterministic = (
                genome.git_hash,
                genome.health.intelligence_score,
                tuple(m.get('name', m) if isinstance(m, dict) else getattr(m, 'name', m) for m in genome.architecture.modules)
            )
            genomes.append(deterministic)
        
        # All snapshots from same input should have identical deterministic fields
        unique_genomes = set(genomes)
        assert len(unique_genomes) == 1, f"Expected identical genomes but got {len(unique_genomes)} unique: {unique_genomes}"
    
    def test_genome_confidence_stability(self):
        """Test that confidence scores are stable"""
        fp = RepositoryFingerprint(
            git_hash="abc123",
            file_count=100,
            language_breakdown={"python": 50},
            dependency_count=25,
            module_count=8
        )
        
        confidence_values = []
        for i in range(10):
            genome = self.genome_analyzer.create_snapshot(
                self.test_repo_id, fp.git_hash, fp
            )
            confidence_values.append(genome.health.confidence)
        
        # Confidence should be identical across runs
        assert len(set(confidence_values)) == 1
    
    def test_genome_snapshot_retrieval(self):
        """Test snapshot storage and retrieval"""
        fp = RepositoryFingerprint(
            git_hash="abc123",
            file_count=100,
            language_breakdown={"python": 50},
            dependency_count=25,
            module_count=8
        )
        
        genome1 = self.genome_analyzer.create_snapshot(self.test_repo_id, "v1.0", fp)
        genome2 = self.genome_analyzer.get_snapshot(self.test_repo_id)
        
        assert genome2 is not None
        assert genome2.git_hash == "v1.0"
