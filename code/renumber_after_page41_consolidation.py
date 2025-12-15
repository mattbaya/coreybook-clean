#!/usr/bin/env python3
"""
Renumber pages after consolidating page 41+42 into just page 41.
All pages 43-48 need to be renumbered down by 1.
"""

import os
import shutil

def renumber_pages():
    """Renumber pages after page 41-42 consolidation."""
    
    # Define the renumbering mapping: (old_page_num, new_page_num)
    renumber_map = [
        (43, 42),  # Page 43 becomes 42
        (44, 43),  # Page 44 becomes 43  
        (45, 44),  # Page 45 becomes 44
        (46, 45),  # Page 46 becomes 45
        (47, 46),  # Page 47 becomes 46
    ]
    
    print("🔄 Renumbering pages after page 41-42 consolidation...")
    
    # Renumber remaining pages
    print("\n🔢 Renumbering pages...")
    for old_num, new_num in renumber_map:
        # Handle main prompts
        old_main = f"page-prompts/page-{old_num:02d}.md"
        new_main = f"page-prompts/page-{new_num:02d}.md"
        
        if os.path.exists(old_main):
            shutil.move(old_main, new_main)
            print(f"   Renamed: page-{old_num:02d}.md → page-{new_num:02d}.md")
            
            # Update the page title in the content
            update_page_title(new_main, new_num)
        
        # Handle Leonardo prompts
        old_leonardo = f"leonardo/page-{old_num:02d}-leonardo.txt"
        new_leonardo = f"leonardo/page-{new_num:02d}-leonardo.txt"
        
        if os.path.exists(old_leonardo):
            shutil.move(old_leonardo, new_leonardo)
            print(f"   Renamed: page-{old_num:02d}-leonardo.txt → page-{new_num:02d}-leonardo.txt")
    
    # Handle back cover
    if os.path.exists("page-prompts/page-48-back-cover.md"):
        shutil.move("page-prompts/page-48-back-cover.md", "page-prompts/page-47-back-cover.md")
        print(f"   Renamed: page-48-back-cover.md → page-47-back-cover.md")
        
        # Update title
        update_back_cover_title("page-prompts/page-47-back-cover.md", 47)
    
    if os.path.exists("leonardo/page-48-back-cover-leonardo.txt"):
        shutil.move("leonardo/page-48-back-cover-leonardo.txt", "leonardo/page-47-back-cover-leonardo.txt")
        print(f"   Renamed: page-48-back-cover-leonardo.txt → page-47-back-cover-leonardo.txt")

def update_page_title(file_path, new_page_num):
    """Update the page title in the markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update the title line
        lines = content.split('\n')
        if lines and lines[0].startswith('# Page'):
            # Extract the title part after the page number
            parts = lines[0].split(' - ', 1)
            if len(parts) == 2:
                title_part = parts[1]
                lines[0] = f"# Page {new_page_num} - {title_part}"
            else:
                lines[0] = f"# Page {new_page_num} - The Chef at the Store"
        
        # Write back the updated content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
            
    except Exception as e:
        print(f"   Warning: Could not update title in {file_path}: {e}")

def update_back_cover_title(file_path, new_page_num):
    """Update the back cover page title."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update the title line
        lines = content.split('\n')
        if lines and lines[0].startswith('# Page'):
            lines[0] = f"# Page {new_page_num} - BACK COVER"
        
        # Write back the updated content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
            
    except Exception as e:
        print(f"   Warning: Could not update back cover title in {file_path}: {e}")

def main():
    """Main function to handle the renumbering."""
    print("📚 CoreyBook Page Renumbering After 41-42 Consolidation")
    print("=" * 55)
    print("Consolidating page 41+42 and renumbering remaining pages")
    
    try:
        renumber_pages()
        
        print("\n🎉 Renumbering completed successfully!")
        print(f"📊 New book structure:")
        print(f"   - Pages 1-40: Unchanged")
        print(f"   - Page 41: Combined transformation page (was 41+42)")
        print(f"   - Pages 42-46: Final story pages (renumbered from 43-47)")
        print(f"   - Page 47: Back cover (renumbered from 48)")
        print(f"   - Total pages: 47 (reduced from 48)")
        
    except Exception as e:
        print(f"❌ Error during renumbering: {e}")

if __name__ == "__main__":
    main()