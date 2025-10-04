#!/usr/bin/env python3
"""
Generate element descriptions from backend domain model.

Reads reaction system architecture and creates JSON for frontend DescBar1 component.
Produces "missing description" for elements without backend implementation.
"""

import json
from pathlib import Path


# Reaction metadata from reactions.py domain model
REACTION_DESCRIPTIONS = {
    'like': 'Express positive sentiment about the speaker',
    'love': 'Express strong positive sentiment about the speaker',
    'dislike': 'Express negative sentiment about the speaker',
    'hate': 'Express strong negative sentiment about the speaker',
    'agree': 'Signal agreement with the speaker\'s point',
    'disagree': 'Signal disagreement with the speaker\'s point',
    'go_on': 'Encourage the speaker to continue',
    'hurry_up': 'Signal the speaker to move faster',
    'boring': 'Indicate the content is uninteresting',
    'interesting': 'Indicate the content is engaging',
    'sympathy': 'Express empathy with the speaker',
    'laugh': 'React with humor to the speaker'
}

# Visibility mode metadata from VisibilityMode enum
VISIBILITY_MODE_DESCRIPTIONS = {
    'anonymous': 'Reactions visible but not attributed by name',
    'accredited': 'Reactions visible and attributed by name',
    'secret': 'Reactions visible only to facilitator'
}


def generate_descriptions():
    """Generate element-descriptions.json from backend domain model."""

    elements = {}

    # Generate reaction1 button descriptions (12 items)
    # Map backend reaction codes to frontend element IDs
    reaction_mapping = {
        'like': 'like1',
        'love': 'love1',
        'dislike': 'dislike1',
        'hate': 'hate1',
        'agree': 'agree1',
        'disagree': 'disagree1',
        'hurryup': 'hurryup1',
        'goon': 'goon1',
        'interest': 'interest1',
        'boring': 'boring1',
        'sympathy': 'sympathy1',
        'laugh': 'laugh1'
    }

    # Backend code to frontend ID mapping
    code_to_frontend = {
        'like': 'like1',
        'love': 'love1',
        'dislike': 'dislike1',
        'hate': 'hate1',
        'agree': 'agree1',
        'disagree': 'disagree1',
        'go_on': 'goon1',
        'hurry_up': 'hurryup1',
        'boring': 'boring1',
        'interesting': 'interest1',
        'sympathy': 'sympathy1',
        'laugh': 'laugh1'
    }

    # Generate reaction1 buttons
    for backend_code, description in REACTION_DESCRIPTIONS.items():
        frontend_id = code_to_frontend[backend_code]
        label = backend_code.replace('_', ' ').title()

        elements[frontend_id] = {
            'label': label,
            'id': frontend_id,
            'description': description
        }

    # Generate reaction2 label descriptions (12 items) - display-only counters
    label_mapping = {
        'like': 'like_l1',
        'love': 'love_l1',
        'dislike': 'dislike_l1',
        'hate': 'hate_l1',
        'agree': 'agreel1',
        'disagree': 'disagree_l1',
        'go_on': 'goon_l1',
        'hurry_up': 'hurryup_l1',
        'boring': 'boring_l1',
        'interesting': 'interest_l1',
        'sympathy': 'sympathy_l1',
        'laugh': 'laugh_l1'
    }

    for backend_code, frontend_id in label_mapping.items():
        label = f"{backend_code.replace('_', ' ').title()} Count"

        elements[frontend_id] = {
            'label': label,
            'id': frontend_id,
            'description': f"Shows total {backend_code.replace('_', ' ')} reactions"
        }

    # Generate reaction option descriptions (ropt1, ropt2, ropt3)
    elements['ropt1'] = {
        'label': 'Public Mode',
        'id': 'ropt1',
        'description': VISIBILITY_MODE_DESCRIPTIONS['accredited']
    }

    elements['ropt2'] = {
        'label': 'Anonymous Mode',
        'id': 'ropt2',
        'description': VISIBILITY_MODE_DESCRIPTIONS['anonymous']
    }

    elements['ropt3'] = {
        'label': 'Secret Mode',
        'id': 'ropt3',
        'description': VISIBILITY_MODE_DESCRIPTIONS['secret']
    }

    # Generate reaction choice descriptions (rch1, rch2, rch3) - current mode indicators
    elements['rch1'] = {
        'label': 'Public Mode Indicator',
        'id': 'rch1',
        'description': 'missing description'
    }

    elements['rch2'] = {
        'label': 'Anonymous Mode Indicator',
        'id': 'rch2',
        'description': 'missing description'
    }

    elements['rch3'] = {
        'label': 'Secret Mode Indicator',
        'id': 'rch3',
        'description': 'missing description'
    }

    output = {
        'defaultMessage': {
            'id': 'descbar-empty-state',
            'text': 'Click an element to see what it does'
        },
        'elements': elements
    }

    return output


if __name__ == '__main__':
    descriptions = generate_descriptions()

    # Output path relative to script location
    script_dir = Path(__file__).parent
    output_path = script_dir.parent.parent / 'frontend' / 'public' / 'data' / 'element-descriptions.json'
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        json.dump(descriptions, f, indent=2)

    print(f"✅ Generated {len(descriptions['elements'])} element descriptions")
    print(f"📁 Output: {output_path}")

    # Print summary by type
    reaction_buttons = [k for k in descriptions['elements'].keys() if k.endswith('1') and not k.startswith('r')]
    reaction_labels = [k for k in descriptions['elements'].keys() if '_l1' in k]
    reaction_options = [k for k in descriptions['elements'].keys() if k.startswith('ropt')]
    reaction_choices = [k for k in descriptions['elements'].keys() if k.startswith('rch')]

    print(f"\n📊 Summary:")
    print(f"  - Reaction buttons: {len(reaction_buttons)}")
    print(f"  - Reaction labels: {len(reaction_labels)}")
    print(f"  - Reaction options: {len(reaction_options)}")
    print(f"  - Reaction choices: {len(reaction_choices)}")
    print(f"  - Total: {len(descriptions['elements'])}")
