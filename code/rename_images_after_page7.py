#!/usr/bin/env python3
"""
Rename all generated images in the leonardo folder to match the new page numbering.
Pages 7+ become pages 8+, so:
- page7.jpg becomes page8.jpg  
- page8.jpg becomes page9.jpg
- etc.
"""

import os
import shutil
from pathlib import Path

def rename_leonardo_images():
    """Rename images in cartoon-characters/leonardo/ folder."""
    leonardo_dir = Path("cartoon-characters/leonardo")
    
    if not leonardo_dir.exists():
        print(f"❌ Directory not found: {leonardo_dir}")
        return
    
    # Find all page images that need renaming (pages 7 and up)
    images_to_rename = []
    
    for ext in ['.jpg', '.png']:
        # Check for pages 7-52 (which will become 8-53)
        for page_num in range(7, 53):  # 7 to 52
            old_file = leonardo_dir / f"page{page_num}{ext}"
            if old_file.exists():
                new_page_num = page_num + 1
                new_file = leonardo_dir / f"page{new_page_num}{ext}"
                images_to_rename.append((old_file, new_file, page_num, new_page_num))
    
    if not images_to_rename:
        print("📸 No images found that need renaming")
        return
    
    print(f"🔄 Found {len(images_to_rename)} images to rename...")
    
    # Sort by page number in reverse order to avoid conflicts
    images_to_rename.sort(key=lambda x: x[2], reverse=True)
    
    # Rename files
    renamed_count = 0
    for old_file, new_file, old_num, new_num in images_to_rename:
        try:
            # Check if target file already exists
            if new_file.exists():
                print(f"⚠️  Target exists: {new_file.name} - skipping {old_file.name}")
                continue
            
            # Rename the file
            shutil.move(str(old_file), str(new_file))
            print(f"✅ Renamed: page{old_num}{old_file.suffix} → page{new_num}{new_file.suffix}")
            renamed_count += 1
            
        except Exception as e:
            print(f"❌ Error renaming {old_file.name}: {e}")
    
    print(f"\n🎉 Renaming complete!")
    print(f"📊 Successfully renamed {renamed_count} images")
    
    # Show what images we now have
    print(f"\n📸 Current leonardo folder structure:")
    all_pages = []
    for ext in ['.jpg', '.png']:
        for page_file in sorted(leonardo_dir.glob(f"page*{ext}")):
            if page_file.name.startswith('page') and page_file.name[4].isdigit():
                all_pages.append(page_file.name)
    
    if all_pages:
        all_pages.sort(key=lambda x: int(''.join(filter(str.isdigit, x.split('.')[0]))))
        for i, page in enumerate(all_pages[:10]):  # Show first 10
            print(f"   {page}")
        if len(all_pages) > 10:
            print(f"   ... and {len(all_pages) - 10} more")
    else:
        print("   No page images found")

def rename_backup_images():
    """Also rename any backup images that might exist."""
    leonardo_dir = Path("cartoon-characters/leonardo")
    
    backup_patterns = [
        "page*.backup.*",
        "page*.square_backup.*", 
        "page*_phil_foglio.*",
        "page*_unique.*"
    ]
    
    renamed_backups = 0
    
    for pattern in backup_patterns:
        for backup_file in leonardo_dir.glob(pattern):
            # Extract the page number
            name = backup_file.name
            if 'page' in name:
                # Find the number after 'page'
                try:
                    start = name.find('page') + 4
                    end = start
                    while end < len(name) and name[end].isdigit():
                        end += 1
                    
                    if end > start:
                        page_num = int(name[start:end])
                        if page_num >= 7:  # Only rename pages 7+
                            new_page_num = page_num + 1
                            new_name = name.replace(f'page{page_num}', f'page{new_page_num}')
                            new_file = leonardo_dir / new_name
                            
                            if not new_file.exists():
                                shutil.move(str(backup_file), str(new_file))
                                print(f"✅ Renamed backup: {name} → {new_name}")
                                renamed_backups += 1
                                
                except (ValueError, IndexError):
                    continue
    
    if renamed_backups > 0:
        print(f"📦 Also renamed {renamed_backups} backup files")

if __name__ == "__main__":
    print("🖼️  Renaming generated images to match new page numbering...\n")
    rename_leonardo_images()
    print()
    rename_backup_images()
    print("\n✅ All image renaming complete!")
    print("📋 Next: Generate new page 7 image and update page mapping in automation scripts")