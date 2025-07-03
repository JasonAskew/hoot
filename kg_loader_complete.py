#!/usr/bin/env python3
"""
Comprehensive Knowledge Graph Loader
Loads all intents, responses, segments, and entities into Neo4j
"""

import json
import os
from typing import Dict, List, Any, Set
from neo4j import GraphDatabase
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class KnowledgeGraphLoader:
    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.loaded_intents = set()
        self.loaded_entities = set()
        self.loaded_responses = set()
        self.loaded_intent_data = set()
        
    def close(self):
        self.driver.close()
    
    def clear_database(self):
        """Optional: Clear existing data before loading"""
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
            logger.info("Cleared existing database")
    
    def create_constraints(self):
        """Create uniqueness constraints and indexes"""
        constraints = [
            "CREATE CONSTRAINT IF NOT EXISTS FOR (i:Intent) REQUIRE i.name IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (e:Entity) REQUIRE e.name IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (r:Response) REQUIRE r.name IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (s:Slot) REQUIRE s.id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (eo:EntityOption) REQUIRE eo.id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (id:IntentData) REQUIRE id.id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (seg:Segment) REQUIRE seg.name IS UNIQUE",
            "CREATE INDEX IF NOT EXISTS FOR (i:Intent) ON (i.filename)",
            "CREATE INDEX IF NOT EXISTS FOR (e:Entity) ON (e.filename)",
            "CREATE INDEX IF NOT EXISTS FOR (r:Response) ON (r.filename)",
            "CREATE INDEX IF NOT EXISTS FOR (seg:Segment) ON (seg.name)"
        ]
        
        with self.driver.session() as session:
            for constraint in constraints:
                try:
                    session.run(constraint)
                    logger.info(f"Created constraint/index: {constraint[:50]}...")
                except Exception as e:
                    logger.warning(f"Constraint/index may already exist: {e}")
    
    def load_segment(self, filepath: Path) -> str:
        """Load a single segment definition file"""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            segment_name = data.get('name', filepath.stem)
            
            with self.driver.session() as session:
                # Create or update segment
                session.run(
                    """
                    MERGE (s:Segment {name: $name})
                    SET s.active = $active,
                        s.description = $description,
                        s.filename = $filename,
                        s.disabled_actions = $disabled_actions
                    """,
                    name=segment_name,
                    active=data.get('active', True),
                    description=data.get('description', ''),
                    filename=filepath.name,
                    disabled_actions=data.get('disabled_actions', [])
                )
                
                # Store criteria as JSON string
                criteria = data.get('criteria', [])
                if criteria:
                    import json as json_module
                    criteria_json = json_module.dumps(criteria)
                    session.run(
                        """
                        MATCH (s:Segment {name: $name})
                        SET s.criteria = $criteria
                        """,
                        name=segment_name,
                        criteria=criteria_json
                    )
                
                # Create relationships to disabled intents
                disabled_actions = data.get('disabled_actions', [])
                for action in disabled_actions:
                    session.run(
                        """
                        MATCH (s:Segment {name: $segment_name})
                        MATCH (i:Intent {name: $intent_name})
                        MERGE (s)-[:DISABLES]->(i)
                        """,
                        segment_name=segment_name,
                        intent_name=action
                    )
                
                logger.info(f"Loaded segment: {segment_name} (disables {len(disabled_actions)} intents)")
                
        except Exception as e:
            logger.error(f"Error loading segment {filepath}: {e}")
        
        return segment_name
    
    def load_categories(self):
        """Load intent categories"""
        categories = [
            {"name": "Banking", "description": "Banking related intents"},
            {"name": "Investment", "description": "Investment and trading intents"},
            {"name": "Super", "description": "Superannuation related intents"},
            {"name": "Account", "description": "Account management intents"},
            {"name": "Support", "description": "Customer support intents"},
            {"name": "Information", "description": "Information requests"},
            {"name": "Transaction", "description": "Transaction related intents"},
            {"name": "Security", "description": "Security and authentication"},
            {"name": "General", "description": "General intents"}
        ]
        
        with self.driver.session() as session:
            for cat in categories:
                session.run(
                    "MERGE (c:Category {name: $name}) "
                    "SET c.description = $description",
                    cat
                )
            logger.info(f"Loaded {len(categories)} categories")
    
    def load_entity(self, filepath: Path) -> str:
        """Load a single entity file"""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            entity_name = data.get('name', filepath.stem)
            
            if entity_name in self.loaded_entities:
                return entity_name
            
            with self.driver.session() as session:
                # Create entity
                session.run(
                    """
                    MERGE (e:Entity {name: $name})
                    SET e.filename = $filename,
                        e.type = $type,
                        e.system = $system
                    """,
                    name=entity_name,
                    filename=filepath.name,
                    type=data.get('type', 'custom'),
                    system=data.get('system', False)
                )
                
                # Load entity options
                options = data.get('options', [])
                for idx, option in enumerate(options):
                    option_id = f"{entity_name}_option_{idx}"
                    session.run(
                        """
                        MERGE (eo:EntityOption {id: $id})
                        SET eo.entity_name = $entity_name,
                            eo.value = $value,
                            eo.aliases = $aliases
                        WITH eo
                        MATCH (e:Entity {name: $entity_name})
                        MERGE (e)-[:HAS_OPTION]->(eo)
                        """,
                        id=option_id,
                        entity_name=entity_name,
                        value=option.get('value', ''),
                        aliases=option.get('aliases', [])
                    )
                
                self.loaded_entities.add(entity_name)
                logger.info(f"Loaded entity: {entity_name} with {len(options)} options")
                
        except Exception as e:
            logger.error(f"Error loading entity {filepath}: {e}")
        
        return entity_name
    
    def load_response(self, filepath: Path) -> str:
        """Load a single response file"""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            response_name = data.get('name', filepath.stem)
            
            if response_name in self.loaded_responses:
                return response_name
            
            with self.driver.session() as session:
                session.run(
                    """
                    MERGE (r:Response {name: $name})
                    SET r.filename = $filename,
                        r.searchable = $searchable,
                        r.system = $system
                    """,
                    name=response_name,
                    filename=filepath.name,
                    searchable=data.get('searchable', True),
                    system=data.get('system', False)
                )
                
                # Load segments from this response
                segment_responses = data.get('segment_responses', [])
                for seg_resp in segment_responses:
                    segment_name = seg_resp.get('segment_name')
                    if segment_name:
                        # Create segment and link to response
                        session.run(
                            """
                            MERGE (seg:Segment {name: $segment_name})
                            WITH seg
                            MATCH (r:Response {name: $response_name})
                            MERGE (r)-[:HAS_SEGMENT_VARIANT]->(seg)
                            """,
                            segment_name=segment_name,
                            response_name=response_name
                        )
                
                self.loaded_responses.add(response_name)
                logger.info(f"Loaded response: {response_name} with {len(segment_responses)} segment variants")
                
        except Exception as e:
            logger.error(f"Error loading response {filepath}: {e}")
        
        return response_name
    
    def load_intent(self, filepath: Path):
        """Load a single intent file"""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            intent_name = data.get('name', filepath.stem)
            
            if intent_name in self.loaded_intents:
                return
            
            with self.driver.session() as session:
                # Create intent
                session.run(
                    """
                    MERGE (i:Intent {name: $name})
                    SET i.filename = $filename,
                        i.display_name = $display_name,
                        i.skill = $skill,
                        i.active = $active,
                        i.ml_enabled = $ml_enabled,
                        i.webhook_name = $webhook_name,
                        i.display_sentence = $display_sentence
                    """,
                    name=intent_name,
                    filename=filepath.name,
                    display_name=data.get('displayName', intent_name),
                    skill=data.get('skill', 'default'),
                    active=data.get('active', True),
                    ml_enabled=data.get('mlEnabled', True),
                    webhook_name=data.get('webhookName', ''),
                    display_sentence=data.get('displaySentence', '')
                )
                
                # Assign category based on intent name
                category = self._determine_category(intent_name)
                session.run(
                    """
                    MATCH (i:Intent {name: $intent_name})
                    MATCH (c:Category {name: $category})
                    MERGE (i)-[:BELONGS_TO_CATEGORY]->(c)
                    """,
                    intent_name=intent_name,
                    category=category
                )
                
                # Link to responses - check both 'responses' array and webhook_params
                responses = data.get('responses', [])
                
                # Also check webhook_params for response_name
                webhook_params = data.get('webhook_params', {})
                webhook_response = webhook_params.get('response_name')
                if webhook_response and webhook_response not in responses:
                    responses.append(webhook_response)
                
                for response in responses:
                    session.run(
                        """
                        MATCH (i:Intent {name: $intent_name})
                        MERGE (r:Response {name: $response_name})
                        MERGE (i)-[:USES_RESPONSE]->(r)
                        """,
                        intent_name=intent_name,
                        response_name=response
                    )
                
                # Create slots
                slots = data.get('slots', [])
                for slot in slots:
                    slot_id = f"{intent_name}_{slot.get('name', 'unnamed')}"
                    entity_type = slot.get('entity', '')
                    
                    session.run(
                        """
                        MERGE (s:Slot {id: $id})
                        SET s.name = $name,
                            s.entity_type = $entity_type,
                            s.intent = $intent
                        WITH s
                        MATCH (i:Intent {name: $intent})
                        MERGE (i)-[:HAS_SLOT]->(s)
                        """,
                        id=slot_id,
                        name=slot.get('name', ''),
                        entity_type=entity_type,
                        intent=intent_name
                    )
                    
                    # Link slot to entity if it exists
                    if entity_type:
                        session.run(
                            """
                            MATCH (s:Slot {id: $slot_id})
                            MATCH (e:Entity {name: $entity_name})
                            MERGE (s)-[:USES_ENTITY]->(e)
                            """,
                            slot_id=slot_id,
                            entity_name=entity_type
                        )
                
                self.loaded_intents.add(intent_name)
                logger.info(f"Loaded intent: {intent_name} with {len(responses)} responses and {len(slots)} slots")
                
        except Exception as e:
            logger.error(f"Error loading intent {filepath}: {e}")
    
    def load_intent_data(self, filepath: Path):
        """Load intent training data"""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            # Extract intent name from filename
            intent_name = filepath.stem.replace('intent_data_', '')
            
            with self.driver.session() as session:
                # Load training examples
                examples = data.get('examples', [])
                for idx, example in enumerate(examples):
                    data_id = f"{intent_name}_data_{idx}"
                    
                    if data_id in self.loaded_intent_data:
                        continue
                    
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
                        id=data_id,
                        intent_name=intent_name,
                        trigger_sentence=example.get('text', ''),
                        type=example.get('type', 'training'),
                        scope=example.get('scope', 'general'),
                        source=example.get('source', 'manual'),
                        tags=example.get('tags', []),
                        active=example.get('active', True)
                    )
                    
                    self.loaded_intent_data.add(data_id)
                
                logger.info(f"Loaded {len(examples)} training examples for intent: {intent_name}")
                
        except Exception as e:
            logger.error(f"Error loading intent data {filepath}: {e}")
    
    def _determine_category(self, intent_name: str) -> str:
        """Determine category based on intent name"""
        name_lower = intent_name.lower()
        
        if 'bt_' in name_lower or 'panorama' in name_lower:
            if 'invest' in name_lower or 'trade' in name_lower or 'share' in name_lower:
                return 'Investment'
            elif 'super' in name_lower:
                return 'Super'
            elif 'account' in name_lower or 'balance' in name_lower:
                return 'Account'
            else:
                return 'Banking'
        elif 'transaction' in name_lower or 'transfer' in name_lower or 'payment' in name_lower:
            return 'Transaction'
        elif 'security' in name_lower or 'login' in name_lower or 'password' in name_lower:
            return 'Security'
        elif 'support' in name_lower or 'help' in name_lower or 'feedback' in name_lower:
            return 'Support'
        elif 'info' in name_lower or 'statement' in name_lower or 'report' in name_lower:
            return 'Information'
        else:
            return 'General'
    
    def load_all_data(self, base_path: str):
        """Load all data from the specified base path"""
        base_path = Path(base_path)
        
        # Create constraints first
        self.create_constraints()
        
        # Load categories
        self.load_categories()
        
        # Load entities
        entities_path = base_path / 'entities'
        if entities_path.exists():
            for file in entities_path.glob('*.json'):
                self.load_entity(file)
        
        # Load segments
        segments_path = base_path / 'segments'
        if segments_path.exists():
            for file in segments_path.glob('*.json'):
                self.load_segment(file)
        
        # Load responses
        responses_path = base_path / 'responses'
        if responses_path.exists():
            for file in responses_path.glob('*.json'):
                self.load_response(file)
        
        # Load intents
        intents_path = base_path / 'intents'
        if intents_path.exists():
            for file in intents_path.glob('*.json'):
                self.load_intent(file)
        
        # Load intent data (training examples)
        intent_data_path = base_path / 'intent_data'
        if intent_data_path.exists():
            for file in intent_data_path.glob('intent_data_*.json'):
                self.load_intent_data(file)
        
        # Print summary
        self._print_summary()
    
    def _print_summary(self):
        """Print loading summary"""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (n)
                RETURN labels(n)[0] as Label, count(n) as Count
                ORDER BY Label
            """)
            
            logger.info("\n=== LOADING SUMMARY ===")
            total = 0
            for record in result:
                logger.info(f"{record['Label']}: {record['Count']}")
                total += record['Count']
            logger.info(f"Total nodes: {total}")
            
            # Check relationships
            rel_result = session.run("""
                MATCH ()-[r]->()
                RETURN type(r) as Type, count(r) as Count
                ORDER BY Type
            """)
            
            logger.info("\nRelationships:")
            total_rels = 0
            for record in rel_result:
                logger.info(f"{record['Type']}: {record['Count']}")
                total_rels += record['Count']
            logger.info(f"Total relationships: {total_rels}")


def main():
    # Neo4j connection details
    NEO4J_URI = "bolt://localhost:7687"
    NEO4J_USER = "neo4j"
    NEO4J_PASSWORD = "neo4j2024!"  # Change this
    
    # Base path for data files
    BASE_PATH = "/Users/jaskew/workspace/Skynet/desktop/domains"
    
    # Create loader and load data
    loader = KnowledgeGraphLoader(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
    
    try:
        # Optional: Clear existing data
        # loader.clear_database()
        
        # Load all data
        loader.load_all_data(BASE_PATH)
        
    finally:
        loader.close()


if __name__ == "__main__":
    main()
