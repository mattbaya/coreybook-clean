#!/usr/bin/env python3
"""
Update all page prompts with the new detailed Corey character description.
"""

import re
from pathlib import Path

def get_new_corey_description():
    """Return the updated Corey character description."""
    return """**COREY CHARACTER CONSISTENCY - MUST MATCH EXACTLY:**

Illustrate Corey EXACTLY matching the established reference character.

Corey is a late-middle-aged adult man (late 40s to 50s), bald with a high forehead,
clean-shaven, realistic facial structure.

MANDATORY CHARACTER CONSTRAINTS:
- Smaller, slightly tired eyes (NOT large or cute)
- Longer face, defined jawline
- Subtle age lines around eyes and mouth
- Head-to-body ratio realistic (no chibi, no mascot proportions)
- Neck visible and proportional
- Calm, warm smile (not exaggerated)

DO NOT:
- Do not make Corey look young
- Do not enlarge eyes
- Do not smooth facial features
- Do not shorten torso
- Do not stylize toward "cute" or "friendly mascot"

Style matches prior Corey reference sheets exactly.

- COREY: Completely BALD adult male (no hair), round face, navy blue apron, white shirt"""

def update_corey_references(content):
    """Update all Corey references in the content."""
    new_description = get_new_corey_description()
    
    # Pattern to match existing Corey descriptions in the character consistency section
    patterns = [
        # Match the full character consistency block and replace Corey's part
        r'(\*\*CRITICAL CHARACTER CONSISTENCY - MUST MATCH EXACTLY:\*\*\s*\n)- COREY:[^\n]*',
        # Also match standalone Corey descriptions
        r'- \*\*COREY\*\*:[^\n]*',
        r'- COREY:[^\n]*',
    ]
    
    # First, try to replace within existing character consistency blocks
    for pattern in patterns:
        if re.search(pattern, content, re.IGNORECASE):
            content = re.sub(pattern, f'\\1{new_description}' if '\\1' in pattern else new_description, content, flags=re.IGNORECASE)
            break
    else:
        # If no existing character consistency block, add it before image prompt
        image_prompt_match = re.search(r'## IMAGE PROMPT', content)
        if image_prompt_match:
            insert_pos = image_prompt_match.start()
            content = content[:insert_pos] + f"{new_description}\n\n" + content[insert_pos:]
    
    return content

def update_all_prompts():
    """Update all page prompt files with new Corey description."""
    prompts_dir = Path("page-prompts")
    updated_count = 0
    
    # Get all page prompt files
    page_files = []
    page_files.append(prompts_dir / "page-00-cover.md")
    
    for i in range(1, 52):
        page_files.append(prompts_dir / f"page-{i:02d}.md")
    
    page_files.append(prompts_dir / "page-52.md")  # Back cover
    
    print("🔄 Updating Corey character descriptions in all page prompts...")
    
    for page_file in page_files:
        if not page_file.exists():
            print(f"⏭️  Skipping {page_file.name} (not found)")
            continue
        
        # Read current content
        with open(page_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if this page mentions Corey
        if 'corey' not in content.lower():
            print(f"⏭️  Skipping {page_file.name} (no Corey references)")
            continue
        
        # Update Corey descriptions
        updated_content = update_corey_references(content)
        
        # Write back if changed
        if updated_content != content:
            with open(page_file, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            updated_count += 1
            print(f"✅ Updated {page_file.name}")
        else:
            print(f"➡️  No changes needed for {page_file.name}")
    
    print(f"\n🎉 Update complete!")
    print(f"📊 Updated {updated_count} files")
    print(f"🎨 All Corey descriptions now include:")
    print(f"   - Late-middle-aged appearance (40s-50s)")
    print(f"   - Realistic proportions and facial structure")
    print(f"   - Smaller, tired eyes (not cute/large)")
    print(f"   - Defined jawline with subtle age lines")
    print(f"   - Clear style constraints against mascot look")

if __name__ == "__main__":
    update_all_prompts()