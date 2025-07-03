#!/usr/bin/env python3
"""
Automated Profile Generator from Segment Definitions
Generates test profiles and updates CAPI requests based on segment criteria
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


class ProfileGenerator:
    """Generate test profiles from segment definitions with proper CAPI context mapping"""
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.segments_dir = self.base_path / 'segments'
        self.profiles_dir = self.base_path / 'profiles'
        self.segments = {}
        
        # Ensure profiles directory exists
        self.profiles_dir.mkdir(exist_ok=True)
    
    def load_segment_definitions(self):
        """Load all segment definition files"""
        logger.info("Loading segment definitions...")
        
        if not self.segments_dir.exists():
            logger.error(f"Segments directory not found: {self.segments_dir}")
            return
        
        for file in self.segments_dir.glob('*.json'):
            try:
                with open(file, 'r') as f:
                    data = json.load(f)
                    segment_name = data.get('name', file.stem)
                    self.segments[segment_name] = data
            except Exception as e:
                logger.error(f"Error loading segment {file}: {e}")
        
        logger.info(f"Loaded {len(self.segments)} segment definitions")
    
    def extract_criteria_from_segment(self, segment_data: Dict) -> List[Dict]:
        """Extract all criteria combinations from a segment definition"""
        criteria_list = segment_data.get('criteria', [])
        if not criteria_list:
            return []
        
        extracted_criteria = []
        
        for criteria in criteria_list:
            # Extract platform-level criteria
            platform_criteria = {}
            meta_fields = []
            
            # Handle platform_type (affects both platform.name and meta_fields)
            if 'platform_type' in criteria:
                platform_criteria['platform_type'] = criteria['platform_type']
                # Also add to meta_fields for segment matching
                meta_fields.append({
                    "key": "platform_type",
                    "value": criteria['platform_type']
                })
            
            # Handle user_id (affects platform.user_id)
            if 'userId' in criteria:
                platform_criteria['userId'] = criteria['userId']
                meta_fields.append({
                    "key": "userId",
                    "value": criteria['userId']
                })
            
            # Handle zone (affects user context)
            if 'zone' in criteria:
                platform_criteria['zone'] = criteria['zone']
                meta_fields.append({
                    "key": "zone",
                    "value": criteria['zone']
                })
            
            # Handle customer_data (becomes meta_fields)
            if 'customer_data' in criteria:
                for field in criteria['customer_data']:
                    meta_fields.append({
                        "key": field['name'],
                        "value": field['value']
                    })
            
            # Handle direct key-value pairs (not in customer_data)
            for key, value in criteria.items():
                if key not in ['customer_data', 'platform_type', 'userId', 'zone']:
                    meta_fields.append({
                        "key": key,
                        "value": value
                    })
            
            extracted_criteria.append({
                'platform_criteria': platform_criteria,
                'meta_fields': meta_fields
            })
        
        return extracted_criteria
    
    def determine_platform_name(self, platform_type: str) -> str:
        """Map platform_type to platform.name in CAPI request"""
        platform_mapping = {
            'mobile': 'mobile',
            'web': 'web',
            'web-emul': 'web-emul'
        }
        return platform_mapping.get(platform_type, 'web')
    
    def determine_device_type(self, platform_type: str) -> str:
        """Map platform_type to device.type in CAPI request"""
        device_mapping = {
            'mobile': 'mobile',
            'web': 'web',
            'web-emul': 'web'
        }
        return device_mapping.get(platform_type, 'web')
    
    def generate_profile_file(self, segment_name: str, criteria_index: int, criteria: Dict) -> str:
        """Generate a profile file for a specific criteria combination"""
        # Create profile filename
        if criteria_index == 0:
            profile_name = segment_name
        else:
            profile_name = f"{segment_name}_variant_{criteria_index + 1}"
        
        # Create profile data
        profile_data = {
            "meta_fields": criteria['meta_fields']
        }
        
        # Write profile file
        profile_file = self.profiles_dir / f"{profile_name}.json"
        with open(profile_file, 'w') as f:
            json.dump(profile_data, f, indent=2)
        
        return profile_name
    
    def generate_capi_context_mapping(self) -> Dict:
        """Generate mapping of profiles to CAPI context requirements"""
        context_mapping = {}
        
        for segment_name, segment_data in self.segments.items():
            if not segment_data.get('active', True):
                continue
            
            criteria_list = self.extract_criteria_from_segment(segment_data)
            
            for idx, criteria in enumerate(criteria_list):
                # Determine profile name
                if idx == 0:
                    profile_name = segment_name
                else:
                    profile_name = f"{segment_name}_variant_{idx + 1}"
                
                platform_criteria = criteria['platform_criteria']
                
                # Build CAPI context modifications
                context_mods = {
                    'device': {},
                    'platform': {},
                    'user': {}
                }
                
                # Handle platform_type
                if 'platform_type' in platform_criteria:
                    platform_type = platform_criteria['platform_type']
                    context_mods['platform']['name'] = self.determine_platform_name(platform_type)
                    context_mods['device']['type'] = self.determine_device_type(platform_type)
                
                # Handle userId
                if 'userId' in platform_criteria:
                    context_mods['platform']['user_id'] = platform_criteria['userId']
                
                # Handle zone
                if 'zone' in platform_criteria:
                    context_mods['user']['zone'] = platform_criteria['zone']
                
                # Always include meta_fields
                context_mods['user']['meta_fields'] = criteria['meta_fields']
                
                context_mapping[profile_name] = context_mods
        
        return context_mapping
    
    def generate_all_profiles(self):
        """Generate all profile files from segment definitions"""
        logger.info("Generating profile files...")
        
        generated_profiles = []
        skipped_segments = []
        
        for segment_name, segment_data in self.segments.items():
            if not segment_data.get('active', True):
                skipped_segments.append(segment_name)
                continue
            
            criteria_list = self.extract_criteria_from_segment(segment_data)
            
            if not criteria_list:
                logger.warning(f"No criteria found for segment: {segment_name}")
                continue
            
            for idx, criteria in enumerate(criteria_list):
                profile_name = self.generate_profile_file(segment_name, idx, criteria)
                generated_profiles.append(profile_name)
                
                # Log what was generated
                platform_info = criteria['platform_criteria']
                meta_count = len(criteria['meta_fields'])
                logger.info(f"Generated {profile_name}: {meta_count} meta_fields, platform: {platform_info}")
        
        logger.info(f"\\n✅ Generated {len(generated_profiles)} profile files")
        if skipped_segments:
            logger.info(f"⏭️  Skipped {len(skipped_segments)} inactive segments: {', '.join(skipped_segments)}")
        
        return generated_profiles
    
    def save_context_mapping(self, context_mapping: Dict):
        """Save CAPI context mapping to a JSON file for the test runner"""
        mapping_file = self.base_path / 'capi_context_mapping.json'
        
        with open(mapping_file, 'w') as f:
            json.dump(context_mapping, f, indent=2)
        
        logger.info(f"✅ Saved CAPI context mapping to: {mapping_file}")
        return mapping_file
    
    def generate_updated_test_runner_context(self):
        """Generate code snippet for updating the CAPI test runner"""
        context_code = '''
    def load_capi_context_mapping(self) -> Dict:
        """Load CAPI context mapping for profile-specific requests"""
        mapping_file = "capi_context_mapping.json"
        if os.path.exists(mapping_file):
            try:
                with open(mapping_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load CAPI context mapping: {e}")
        return {}
    
    def apply_profile_context(self, base_payload: Dict, segment: str) -> Dict:
        """Apply profile-specific context modifications to CAPI payload"""
        if not hasattr(self, 'context_mapping'):
            self.context_mapping = self.load_capi_context_mapping()
        
        if segment not in self.context_mapping:
            return base_payload
        
        # Deep copy the payload
        import copy
        payload = copy.deepcopy(base_payload)
        context_mods = self.context_mapping[segment]
        
        # Apply device modifications
        if 'device' in context_mods:
            for key, value in context_mods['device'].items():
                if value:  # Only set non-empty values
                    payload['context']['device'][key] = value
        
        # Apply platform modifications  
        if 'platform' in context_mods:
            for key, value in context_mods['platform'].items():
                if value:  # Only set non-empty values
                    payload['context']['platform'][key] = value
        
        # Apply user modifications
        if 'user' in context_mods:
            for key, value in context_mods['user'].items():
                if key == 'meta_fields':
                    payload['context']['user']['meta_fields'] = value
                elif value:  # Only set non-empty values
                    payload['context']['user'][key] = value
        
        return payload
'''
        
        code_file = self.base_path / 'capi_context_integration_code.py'
        with open(code_file, 'w') as f:
            f.write(context_code)
        
        logger.info(f"✅ Generated integration code: {code_file}")
        return code_file
    
    def print_summary(self, generated_profiles: List[str], context_mapping: Dict):
        """Print a summary of generated profiles and their requirements"""
        print("\\n" + "="*80)
        print("PROFILE GENERATION SUMMARY")
        print("="*80)
        
        print(f"\\n📁 Generated Profiles: {len(generated_profiles)}")
        print(f"🔧 Context Mappings: {len(context_mapping)}")
        
        # Group by platform type
        platform_groups = {}
        for profile_name, context_mods in context_mapping.items():
            platform_name = context_mods.get('platform', {}).get('name', 'web')
            if platform_name not in platform_groups:
                platform_groups[platform_name] = []
            platform_groups[platform_name].append(profile_name)
        
        print("\\n📱 Platform Distribution:")
        for platform, profiles in platform_groups.items():
            print(f"  {platform}: {len(profiles)} profiles")
        
        # Show special requirements
        special_requirements = {}
        for profile_name, context_mods in context_mapping.items():
            requirements = []
            
            device_mods = context_mods.get('device', {})
            platform_mods = context_mods.get('platform', {})
            user_mods = context_mods.get('user', {})
            
            if device_mods.get('type') != 'web':
                requirements.append(f"device.type={device_mods['type']}")
            if platform_mods.get('name') != 'web':
                requirements.append(f"platform.name={platform_mods['name']}")
            if 'user_id' in platform_mods:
                requirements.append(f"platform.user_id={platform_mods['user_id']}")
            if 'zone' in user_mods:
                requirements.append(f"user.zone={user_mods['zone']}")
            
            if requirements:
                special_requirements[profile_name] = requirements
        
        if special_requirements:
            print(f"\\n⚙️  Special CAPI Requirements ({len(special_requirements)} profiles):")
            for profile_name, requirements in sorted(special_requirements.items()):
                print(f"  {profile_name}: {', '.join(requirements)}")
        
        print("\\n" + "="*80)


def main():
    """Main function to generate profiles from segment definitions"""
    BASE_PATH = "/Users/jaskew/workspace/Skynet/desktop/claude/test"
    
    generator = ProfileGenerator(BASE_PATH)
    
    # Load segment definitions
    generator.load_segment_definitions()
    
    if not generator.segments:
        logger.error("No segment definitions found!")
        return
    
    # Generate profile files
    generated_profiles = generator.generate_all_profiles()
    
    # Generate CAPI context mapping
    context_mapping = generator.generate_capi_context_mapping()
    
    # Save context mapping
    generator.save_context_mapping(context_mapping)
    
    # Generate integration code
    generator.generate_updated_test_runner_context()
    
    # Print summary
    generator.print_summary(generated_profiles, context_mapping)
    
    print("\\n🎯 Next Steps:")
    print("1. Review generated profiles in the 'profiles/' directory")
    print("2. Integrate capi_context_integration_code.py into capi_test_runner.py")
    print("3. Update test runner to call apply_profile_context() before API requests")
    print("4. Test with different platform types to verify correct CAPI context")


if __name__ == "__main__":
    main()