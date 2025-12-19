#!/usr/bin/env python3
"""
Rename all generated images in the generated_images folder to match the new page numbering.
Pages 7+ become pages 8+, so:
- page-07-text.png becomes page-08-text.png  
- page-08-text.png becomes page-09-text.png
- etc.
"""

import os
import shutil
from pathlib import Path

def rename_generated_images():
    """Rename images in generated_images/ folder."""
    images_dir = Path("generated_images")
    
    if not images_dir.exists():
        print(f"❌ Directory not found: {images_dir}")
        return
    
    # Find all page images that need renaming (pages 7 and up)
    images_to_rename = []
    
    # Check for pages 7-52 (which will become 8-53)
    for page_num in range(7, 53):  # 7 to 52
        old_file = images_dir / f"page-{page_num:02d}-text.png"
        if old_file.exists():
            new_page_num = page_num + 1
            new_file = images_dir / f"page-{new_page_num:02d}-text.png"
            images_to_rename.append((old_file, new_file, page_num, new_page_num))
    
    # Also check for any .png files without -text suffix
    for page_num in range(7, 53):  # 7 to 52
        old_file = images_dir / f"page-{page_num:02d}.png"
        if old_file.exists():
            new_page_num = page_num + 1
            new_file = images_dir / f"page-{new_page_num:02d}.png"
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
            print(f"✅ Renamed: {old_file.name} → {new_file.name}")
            renamed_count += 1
            
        except Exception as e:
            print(f"❌ Error renaming {old_file.name}: {e}")
    
    print(f"\n🎉 Renaming complete!")
    print(f"📊 Successfully renamed {renamed_count} images")
    
    # Show what images we now have
    print(f"\n📸 Current generated_images folder structure:")
    all_pages = []
    for page_file in sorted(images_dir.glob("page-*-text.png")):
        all_pages.append(page_file.name)
    
    if all_pages:
        for i, page in enumerate(all_pages[:15]):  # Show first 15
            print(f"   {page}")
        if len(all_pages) > 15:
            print(f"   ... and {len(all_pages) - 15} more")
    else:
        print("   No page images found")

if __name__ == "__main__":
    print("🖼️  Renaming generated images to match new page numbering...\n")
    rename_generated_images()
    print("\n✅ All image renaming complete!")
    print("📋 Next: Generate new page 7 image")