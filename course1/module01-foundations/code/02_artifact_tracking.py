"""
Module 01: Artifact Tracking

This script demonstrates tracking artifacts manually.
In later modules, we'll use MLflow to do this automatically!

Key concepts:
- What are artifacts?
- Why track them?
- How to track lineage
- How to query artifact history
"""

import json
import hashlib
from datetime import datetime
from pathlib import Path


class ArtifactTracker:
    """
    Simple artifact tracking system.
    
    This demonstrates the concept of tracking artifacts.
    In production, we use MLflow for this!
    """
    
    def __init__(self, tracking_dir='artifacts'):
        self.tracking_dir = Path(tracking_dir)
        self.tracking_dir.mkdir(exist_ok=True)
        self.manifest_file = self.tracking_dir / 'manifest.json'
        self.artifacts = self.load_manifest()
    
    def load_manifest(self):
        """Load existing artifact manifest."""
        if self.manifest_file.exists():
            with open(self.manifest_file, 'r') as f:
                return json.load(f)
        return []
    
    def save_manifest(self):
        """Save artifact manifest."""
        with open(self.manifest_file, 'w') as f:
            json.dump(self.artifacts, f, indent=2)
    
    def compute_hash(self, file_path):
        """Compute SHA256 hash of a file."""
        sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                sha256.update(chunk)
        return sha256.hexdigest()
    
    def track_artifact(self, artifact_path, artifact_type, metadata=None):
        """
        Track an artifact.
        
        Args:
            artifact_path: Path to the artifact file
            artifact_type: Type (data, model, config, metric)
            metadata: Additional information about the artifact
        """
        artifact_path = Path(artifact_path)
        
        if not artifact_path.exists():
            print(f"❌ File not found: {artifact_path}")
            return None
        
        # Create artifact record
        artifact_id = len(self.artifacts) + 1
        artifact_hash = self.compute_hash(artifact_path)
        
        artifact_record = {
            'id': artifact_id,
            'path': str(artifact_path),
            'type': artifact_type,
            'hash': artifact_hash,
            'size_bytes': artifact_path.stat().st_size,
            'created_at': datetime.now().isoformat(),
            'metadata': metadata or {}
        }
        
        self.artifacts.append(artifact_record)
        self.save_manifest()
        
        print(f"✅ Tracked {artifact_type}: {artifact_path.name}")
        print(f"   ID: {artifact_id}")
        print(f"   Hash: {artifact_hash[:16]}...")
        
        return artifact_id
    
    def link_artifacts(self, source_id, target_id, relationship):
        """
        Link two artifacts to track lineage.
        
        Args:
            source_id: ID of source artifact
            target_id: ID of target artifact
            relationship: Description of relationship
        """
        # Find artifacts
        source = next((a for a in self.artifacts if a['id'] == source_id), None)
        target = next((a for a in self.artifacts if a['id'] == target_id), None)
        
        if not source or not target:
            print("❌ Artifact not found")
            return
        
        # Add lineage information
        if 'lineage' not in target:
            target['lineage'] = []
        
        target['lineage'].append({
            'source_id': source_id,
            'source_path': source['path'],
            'relationship': relationship,
            'linked_at': datetime.now().isoformat()
        })
        
        self.save_manifest()
        print(f"✅ Linked: {source['path']} → {target['path']}")
        print(f"   Relationship: {relationship}")
    
    def query_artifacts(self, artifact_type=None):
        """Query artifacts by type."""
        if artifact_type:
            results = [a for a in self.artifacts if a['type'] == artifact_type]
        else:
            results = self.artifacts
        return results
    
    def show_lineage(self, artifact_id):
        """Show lineage of an artifact."""
        artifact = next((a for a in self.artifacts if a['id'] == artifact_id), None)
        
        if not artifact:
            print(f"❌ Artifact {artifact_id} not found")
            return
        
        print(f"\n📊 Lineage for: {artifact['path']}")
        print("="*60)
        
        if 'lineage' not in artifact or not artifact['lineage']:
            print("  No lineage recorded")
            return
        
        for i, link in enumerate(artifact['lineage'], 1):
            print(f"\n{i}. Source: {link['source_path']}")
            print(f"   Relationship: {link['relationship']}")
            print(f"   Linked at: {link['linked_at']}")


def demonstrate_tracking():
    """Demonstrate artifact tracking with a real workflow."""
    print("="*60)
    print(" " * 10 + "📦 ARTIFACT TRACKING DEMONSTRATION")
    print("="*60)
    
    # Initialize tracker
    print("\n🔧 Initializing artifact tracker...")
    tracker = ArtifactTracker()
    print("✅ Tracker initialized")
    
    # Step 1: Track data artifact
    print("\n" + "-"*60)
    print("STEP 1: Tracking raw data")
    print("-"*60)
    data_id = tracker.track_artifact(
        artifact_path='data/customers.csv',
        artifact_type='data',
        metadata={
            'description': 'Raw customer data',
            'source': 'generated',
            'records': 1000
        }
    )
    
    # Step 2: Track model artifact
    print("\n" + "-"*60)
    print("STEP 2: Tracking trained model")
    print("-"*60)
    model_id = tracker.track_artifact(
        artifact_path='models/churn_model.pkl',
        artifact_type='model',
        metadata={
            'description': 'Random Forest churn predictor',
            'algorithm': 'RandomForestClassifier',
            'hyperparameters': {
                'n_estimators': 100,
                'max_depth': 10
            }
        }
    )
    
    # Step 3: Track metrics artifact
    print("\n" + "-"*60)
    print("STEP 3: Tracking metrics")
    print("-"*60)
    metrics_id = tracker.track_artifact(
        artifact_path='metrics/run_metrics.json',
        artifact_type='metrics',
        metadata={
            'description': 'Model performance metrics',
            'metrics': ['accuracy', 'precision', 'recall']
        }
    )
    
    # Step 4: Link artifacts (establish lineage)
    print("\n" + "-"*60)
    print("STEP 4: Establishing lineage")
    print("-"*60)
    
    # Data was used to train model
    tracker.link_artifacts(
        source_id=data_id,
        target_id=model_id,
        relationship='trained_on'
    )
    
    # Model was evaluated to produce metrics
    tracker.link_artifacts(
        source_id=model_id,
        target_id=metrics_id,
        relationship='evaluated_to'
    )
    
    # Step 5: Query artifacts
    print("\n" + "-"*60)
    print("STEP 5: Querying artifacts")
    print("-"*60)
    
    all_artifacts = tracker.query_artifacts()
    print(f"\n📊 Total artifacts tracked: {len(all_artifacts)}")
    
    for artifact in all_artifacts:
        print(f"\n  {artifact['id']}. {artifact['path']}")
        print(f"     Type: {artifact['type']}")
        print(f"     Size: {artifact['size_bytes']} bytes")
        print(f"     Created: {artifact['created_at']}")
    
    # Step 6: Show lineage
    print("\n" + "-"*60)
    print("STEP 6: Viewing lineage")
    print("-"*60)
    
    if model_id:
        tracker.show_lineage(model_id)
    
    if metrics_id:
        tracker.show_lineage(metrics_id)
    
    # Summary
    print("\n" + "="*60)
    print("✅ TRACKING DEMONSTRATION COMPLETE!")
    print("="*60)
    
    print("\n📚 Key Concepts:")
    print("  1. Artifacts = Files produced/used by ML pipeline")
    print("  2. Tracking = Recording what artifacts exist")
    print("  3. Lineage = Recording relationships between artifacts")
    print("  4. Hashing = Detecting if artifacts changed")
    
    print("\n💡 In Real MLOps:")
    print("  - We use MLflow for automatic tracking")
    print("  - We use DVC for data version control")
    print("  - We use Git for code version control")
    print("  - All work together for complete lineage")
    
    print("\n🔍 Check artifacts/manifest.json to see what was tracked")
    print("="*60)


def main():
    """Main function."""
    # First, ensure we have artifacts from previous script
    if not Path('data/customers.csv').exists():
        print("⚠️  Run 01_ml_workflow.py first to generate artifacts!")
        print("   python 01_ml_workflow.py")
        return
    
    demonstrate_tracking()


if __name__ == "__main__":
    main()
