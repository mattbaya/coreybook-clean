#!/usr/bin/env python3
"""
Renumber all pages after the new page 7 insertion.
Pages 8-52 become pages 9-53, and update page titles.
"""

import os
import re
from pathlib import Path

def renumber_pages():
    """Renumber pages from 8-52 to 9-53."""
    pages_dir = Path("page-prompts")
    
    # Work backwards to avoid conflicts
    pages_to_rename = []
    
    # Add back cover (page-52.md becomes page-53.md)
    if pages_dir.joinpath("page-52.md").exists():
        pages_to_rename.append((52, 53, True))  # True = back cover
    
    # Add regular pages (page-51.md becomes page-52.md, etc.)
    for i in range(51, 7, -1):  # 51 down to 8
        old_file = pages_dir / f"page-{i:02d}.md"
        if old_file.exists():
            pages_to_rename.append((i, i + 1, False))  # False = regular page
    
    print(f"📄 Renumbering {len(pages_to_rename)} pages...")
    
    # Rename files and update titles
    for old_num, new_num, is_back_cover in pages_to_rename:
        old_file = pages_dir / f"page-{old_num:02d}.md"
        new_file = pages_dir / f"page-{new_num:02d}.md"
        
        # Read and update content
        with open(old_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update the title line
        if is_back_cover:
            # Back cover keeps its special title
            updated_content = re.sub(
                r'^# Page \d+ - The Chef at the Store',
                f'# Page {new_num:02d} - Back Cover - The Chef at the Store',
                content
            )
        else:
            # Regular pages get updated numbers
            updated_content = re.sub(
                r'^# Page \d+ - The Chef at the Store',
                f'# Page {new_num:02d} - The Chef at the Store',
                content
            )
        
        # Write to new file
        with open(new_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        # Remove old file
        old_file.unlink()
        
        print(f"✅ Renamed: page-{old_num:02d}.md → page-{new_num:02d}.md")
    
    print(f"\n🎉 Renumbering complete!")
    print(f"📊 Now have pages 00-07, 08-53 (total: 54 pages)")

def update_page_08_title():
    """Update page 08 title since it was copied from page 07."""
    page_08 = Path("page-prompts/page-08.md")
    
    if page_08.exists():
        with open(page_08, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update title
        updated_content = re.sub(
            r'^# Page \d+ - The Chef at the Store',
            '# Page 08 - The Chef at the Store',
            content
        )
        
        with open(page_08, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print("✅ Updated page 08 title")

if __name__ == "__main__":
    print("🔄 Renumbering pages after new page 7 insertion...\n")
    renumber_pages()
    update_page_08_title()
    print("\n📚 Page structure now:")
    print("   Pages 05-07: Review sequence (A Place That Feels Good → What People Are Saying → Greatest Hits)")
    print("   Pages 08-53: Continuing story content")