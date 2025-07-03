#!/usr/bin/env python3
"""
Knowledge Graph Verification Script
Checks what's loaded and what's missing
"""

import json
import os
from pathlib import Path
from typing import Set, Dict, List
from neo4j import GraphDatabase
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

class KnowledgeGraphVerifier:
    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def close(self):
        self.driver.close()
    
    def get_loaded_data(self) -> Dict[str, Set[str]]:
        """Get all currently loaded data from Neo4j"""
        loaded = {
            'intents': set(),
            'entities': set(),
            'responses': set(),
            'intent_data': set()
        }
        
        with self.driver.session() as session:
            # Get loaded intents
            result = session.run("MATCH (i:Intent) RETURN i.name as name")
            loaded['intents'] = {record['name'] for record in result}
            
            # Get loaded entities
            result = session.run("MATCH (e:Entity) RETURN e.name as name")
            loaded['entities'] = {record['name'] for record in result}
            
            # Get loaded responses
            result = session.run("MATCH (r:Response) RETURN r.name as name")
            loaded['responses'] = {record['name'] for record in result}
            
            # Get loaded intent data
            result = session.run("MATCH (id:IntentData) RETURN id.intent_name as name")
            loaded['intent_data'] = {record['name'] for record in result if record['name']}
        
        return loaded
    
    def get_file_data(self, base_path: str) -> Dict[str, Set[str]]:
        """Get all available data from files"""
        base_path = Path(base_path)
        available = {
            'intents': set(),
            'entities': set(),
            'responses': set(),
            'intent_data': set()
        }
        
        # Get intent files
        intents_path = base_path / 'intents'
        if intents_path.exists():
            for file in intents_path.glob('*.json'):
                try:
                    with open(file, 'r') as f:
                        data = json.load(f)
                        name = data.get('name', file.stem)
                        available['intents'].add(name)
                except:
                    available['intents'].add(file.stem)
        
        # Get entity files
        entities_path = base_path / 'entities'
        if entities_path.exists():
            for file in entities_path.glob('*.json'):
                try:
                    with open(file, 'r') as f:
                        data = json.load(f)
                        name = data.get('name', file.stem)
                        available['entities'].add(name)
                except:
                    available['entities'].add(file.stem)
        
        # Get response files
        responses_path = base_path / 'responses'
        if responses_path.exists():
            for file in responses_path.glob('*.json'):
                try:
                    with open(file, 'r') as f:
                        data = json.load(f)
                        name = data.get('name', file.stem)
                        available['responses'].add(name)
                except:
                    available['responses'].add(file.stem)
        
        # Get intent data files
        intent_data_path = base_path / 'intent_data'
        if intent_data_path.exists():
            for file in intent_data_path.glob('intent_data_*.json'):
                intent_name = file.stem.replace('intent_data_', '')
                available['intent_data'].add(intent_name)
        
        return available
    
    def print_verification_report(self, base_path: str):
        """Print comprehensive verification report"""
        loaded = self.get_loaded_data()
        available = self.get_file_data(base_path)
        
        print("\n" + "="*80)
        print("KNOWLEDGE GRAPH VERIFICATION REPORT")
        print("="*80)
        
        # Summary statistics
        print("\n📊 SUMMARY STATISTICS")
        print("-"*40)
        
        with self.driver.session() as session:
            # Node counts
            result = session.run("""
                MATCH (n)
                RETURN labels(n)[0] as Label, count(n) as Count
                ORDER BY Count DESC
            """)
            
            print("\nNode Counts:")
            for record in result:
                print(f"  {record['Label']:20} {record['Count']:>6}")
            
            # Relationship counts
            result = session.run("""
                MATCH ()-[r]->()
                RETURN type(r) as Type, count(r) as Count
                ORDER BY Count DESC
            """)
            
            print("\nRelationship Counts:")
            for record in result:
                print(f"  {record['Type']:20} {record['Count']:>6}")
        
        # Coverage analysis
        print("\n\n📈 COVERAGE ANALYSIS")
        print("-"*40)
        
        for data_type in ['intents', 'entities', 'responses', 'intent_data']:
            loaded_items = loaded[data_type]
            available_items = available[data_type]
            missing_items = available_items - loaded_items
            extra_items = loaded_items - available_items
            
            coverage = len(loaded_items) / len(available_items) * 100 if available_items else 0
            
            print(f"\n{data_type.upper()}:")
            print(f"  Files Available: {len(available_items)}")
            print(f"  Loaded in Neo4j: {len(loaded_items)}")
            print(f"  Coverage: {coverage:.1f}%")
            
            if missing_items:
                print(f"  Missing ({len(missing_items)}): {', '.join(sorted(list(missing_items))[:5])}")
                if len(missing_items) > 5:
                    print(f"    ... and {len(missing_items) - 5} more")
            
            if extra_items:
                print(f"  Extra in DB ({len(extra_items)}): {', '.join(sorted(list(extra_items))[:5])}")
                if len(extra_items) > 5:
                    print(f"    ... and {len(extra_items) - 5} more")
        
        # Sample data verification
        print("\n\n🔍 SAMPLE DATA VERIFICATION")
        print("-"*40)
        
        # Check a few intents for completeness
        sample_intents = list(loaded['intents'])[:3]
        for intent_name in sample_intents:
            print(f"\nIntent: {intent_name}")
            
            with self.driver.session() as session:
                # Check slots
                result = session.run("""
                    MATCH (i:Intent {name: $name})-[:HAS_SLOT]->(s:Slot)
                    RETURN count(s) as slot_count
                """, name=intent_name)
                slot_count = result.single()['slot_count']
                
                # Check responses
                result = session.run("""
                    MATCH (i:Intent {name: $name})-[:USES_RESPONSE]->(r:Response)
                    RETURN collect(r.name) as responses
                """, name=intent_name)
                responses = result.single()['responses']
                
                # Check training data
                result = session.run("""
                    MATCH (i:Intent {name: $name})-[:HAS_TRAINING_DATA]->(id:IntentData)
                    RETURN count(id) as data_count
                """, name=intent_name)
                data_count = result.single()['data_count']
                
                print(f"  ├─ Slots: {slot_count}")
                print(f"  ├─ Responses: {len(responses)} - {', '.join(responses[:3])}")
                print(f"  └─ Training Examples: {data_count}")
        
        # Recommendations
        print("\n\n💡 RECOMMENDATIONS")
        print("-"*40)
        
        total_missing = sum(len(available[dt] - loaded[dt]) for dt in ['intents', 'entities', 'responses'])
        
        if total_missing > 0:
            print(f"\n⚠️  {total_missing} items need to be loaded")
            print("   Run the comprehensive loader script to load missing data")
        else:
            print("\n✅ All available data has been loaded!")
        
        # Check for orphaned nodes
        with self.driver.session() as session:
            # Orphaned responses
            result = session.run("""
                MATCH (r:Response)
                WHERE NOT (r)<-[:USES_RESPONSE]-()
                RETURN count(r) as count
            """)
            orphaned_responses = result.single()['count']
            
            # Orphaned entities
            result = session.run("""
                MATCH (e:Entity)
                WHERE NOT (e)<-[:USES_ENTITY]-()
                RETURN count(e) as count
            """)
            orphaned_entities = result.single()['count']
            
            if orphaned_responses > 0 or orphaned_entities > 0:
                print(f"\n⚠️  Found orphaned nodes:")
                if orphaned_responses > 0:
                    print(f"   - {orphaned_responses} responses not linked to any intent")
                if orphaned_entities > 0:
                    print(f"   - {orphaned_entities} entities not used by any slot")


def main():
    # Neo4j connection details
    NEO4J_URI = "bolt://localhost:7687"
    NEO4J_USER = "neo4j"
    NEO4J_PASSWORD = "neo4j2024!"  # Change this
    
    # Base path for data files
    BASE_PATH = "/Users/jaskew/workspace/Skynet/desktop/domains"
    
    # Create verifier and run report
    verifier = KnowledgeGraphVerifier(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
    
    try:
        verifier.print_verification_report(BASE_PATH)
    finally:
        verifier.close()


if __name__ == "__main__":
    main()
