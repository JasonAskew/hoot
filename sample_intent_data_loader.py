#!/usr/bin/env python3
"""
Sample Intent Data Loader
Loads a sample of training data for each intent
"""

import json
import random
from typing import List, Dict
from neo4j import GraphDatabase
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

class SampleIntentDataLoader:
    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        
    def close(self):
        self.driver.close()
    
    def generate_sample_training_data(self, intent_name: str) -> List[Dict]:
        """Generate sample training data for an intent"""
        # Sample templates based on intent type
        templates = self._get_templates_for_intent(intent_name)
        
        training_data = []
        for i, template in enumerate(templates[:5]):  # Max 5 samples per intent
            training_data.append({
                'id': f"{intent_name}_sample_{i}",
                'text': template,
                'type': 'training',
                'scope': 'general',
                'source': 'sample_generator',
                'tags': self._get_tags_for_intent(intent_name),
                'active': True
            })
        
        return training_data
    
    def _get_templates_for_intent(self, intent_name: str) -> List[str]:
        """Get relevant training templates based on intent name"""
        intent_lower = intent_name.lower()
        
        # Define templates for different intent types
        if 'balance' in intent_lower:
            return [
                "What's my account balance?",
                "Show me my balance",
                "How much money do I have?",
                "Check my balance please",
                "I want to see my current balance"
            ]
        elif 'transfer' in intent_lower or 'asset_transfer' in intent_lower:
            return [
                "I want to transfer money",
                "How do I transfer funds?",
                "Transfer assets to another account",
                "Move money between accounts",
                "I need to do an asset transfer"
            ]
        elif 'withdraw' in intent_lower:
            return [
                "I want to withdraw money",
                "How can I make a withdrawal?",
                "Request a withdrawal",
                "Take money out of my account",
                "Process a withdrawal please"
            ]
        elif 'deposit' in intent_lower:
            return [
                "How do I deposit funds?",
                "I want to add money to my account",
                "Make a deposit",
                "Put money in my account",
                "Add funds to my balance"
            ]
        elif 'login' in intent_lower or 'password' in intent_lower:
            return [
                "I forgot my password",
                "Can't log in",
                "Reset my password",
                "Login issues",
                "Help me access my account"
            ]
        elif 'statement' in intent_lower or 'report' in intent_lower:
            return [
                "I need my statement",
                "Show me my transaction history",
                "Download my report",
                "Get my account statement",
                "View my annual statement"
            ]
        elif 'insurance' in intent_lower:
            return [
                "Check my insurance",
                "What's my insurance coverage?",
                "Insurance details please",
                "Show me my insurance policy",
                "I want to review my insurance"
            ]
        elif 'trade' in intent_lower or 'share' in intent_lower:
            return [
                "I want to buy shares",
                "Trade stocks",
                "Execute a trade",
                "Buy or sell shares",
                "Make a stock trade"
            ]
        elif 'feedback' in intent_lower:
            return [
                "I want to give feedback",
                "Submit feedback",
                "Rate my experience",
                "Provide feedback",
                "Leave a review"
            ]
        else:
            # Generic templates
            return [
                f"I need help with {intent_name.replace('_', ' ')}",
                f"Tell me about {intent_name.replace('_', ' ')}",
                f"How does {intent_name.replace('_', ' ')} work?",
                f"Information on {intent_name.replace('_', ' ')}",
                f"Help with {intent_name.replace('_', ' ')}"
            ]
    
    def _get_tags_for_intent(self, intent_name: str) -> List[str]:
        """Get relevant tags based on intent name"""
        tags = []
        intent_lower = intent_name.lower()
        
        # Add general tags
        if 'bt_' in intent_lower:
            tags.append('bt_platform')
        if 'kcb_' in intent_lower:
            tags.append('kcb_platform')
        
        # Add specific tags
        if 'account' in intent_lower:
            tags.append('account_management')
        if 'transaction' in intent_lower or 'transfer' in intent_lower:
            tags.append('transactions')
        if 'security' in intent_lower or 'login' in intent_lower:
            tags.append('security')
        if 'invest' in intent_lower or 'trade' in intent_lower:
            tags.append('investment')
        if 'super' in intent_lower:
            tags.append('superannuation')
        
        return tags
    
    def load_sample_data_for_all_intents(self):
        """Load sample training data for all intents"""
        with self.driver.session() as session:
            # Get all intents
            result = session.run("MATCH (i:Intent) RETURN i.name as name")
            intent_names = [record['name'] for record in result]
            
            logger.info(f"Found {len(intent_names)} intents to process")
            
            # Load sample data for each intent
            total_loaded = 0
            for intent_name in intent_names:
                training_data = self.generate_sample_training_data(intent_name)
                
                for data in training_data:
                    session.run(
                        """
                        MERGE (id:IntentData {id: $id})
                        SET id.intent_name = $intent_name,
                            id.trigger_sentence = $trigger_sentence,
                            id.type = $type,
                            id.scope = $scope,
                            id.source = $source,
                            id.tags = $tags,
                            id.active = $active
                        WITH id
                        MATCH (i:Intent {name: $intent_name})
                        MERGE (i)-[:HAS_TRAINING_DATA]->(id)
                        """,
                        id=data['id'],
                        intent_name=intent_name,
                        trigger_sentence=data['text'],
                        type=data['type'],
                        scope=data['scope'],
                        source=data['source'],
                        tags=data['tags'],
                        active=data['active']
                    )
                    total_loaded += 1
                
                logger.info(f"  ✓ Loaded {len(training_data)} samples for {intent_name}")
            
            logger.info(f"\n✅ Total training samples loaded: {total_loaded}")
    
    def verify_loaded_data(self):
        """Verify the loaded training data"""
        with self.driver.session() as session:
            # Check intents with training data
            result = session.run("""
                MATCH (i:Intent)
                OPTIONAL MATCH (i)-[:HAS_TRAINING_DATA]->(id:IntentData)
                RETURN i.name as intent_name, count(id) as training_count
                ORDER BY training_count DESC
            """)
            
            print("\n📊 TRAINING DATA SUMMARY")
            print("-"*50)
            print(f"{'Intent Name':<40} {'Training Examples':>10}")
            print("-"*50)
            
            total_intents = 0
            intents_with_data = 0
            total_examples = 0
            
            for record in result:
                total_intents += 1
                count = record['training_count']
                total_examples += count
                if count > 0:
                    intents_with_data += 1
                
                print(f"{record['intent_name']:<40} {count:>10}")
            
            print("-"*50)
            print(f"Total intents: {total_intents}")
            print(f"Intents with training data: {intents_with_data}")
            print(f"Total training examples: {total_examples}")
            print(f"Average examples per intent: {total_examples/total_intents:.1f}")


def main():
    # Neo4j connection details
    NEO4J_URI = "bolt://localhost:7687"
    NEO4J_USER = "neo4j"
    NEO4J_PASSWORD = "neo4j2024!"  # Change this
    
    # Create loader
    loader = SampleIntentDataLoader(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
    
    try:
        # Load sample data
        loader.load_sample_data_for_all_intents()
        
        # Verify what was loaded
        loader.verify_loaded_data()
        
    finally:
        loader.close()


if __name__ == "__main__":
    main()
