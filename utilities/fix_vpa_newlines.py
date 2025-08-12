#!/usr/bin/env python3
"""
Script to remove newlines before "**Phân tích VPA/Wyckoff:**" 
to merge it with the previous line across all .md files in vpa_data folder.
"""

import os
import re
from pathlib import Path

def fix_vpa_newlines(file_path):
    """Fix newlines before VPA analysis blocks in a single file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Pattern to match standalone "**Phân tích VPA/Wyckoff:**" lines and merge with previous line
        #    - **Phân tích VPA/Wyckoff:**
        pattern = r'(\S)\n+    - \*\*Phân tích VPA/Wyckoff:\*\*'
        replacement = r'\1 **Phân tích VPA/Wyckoff:**'
        
        fixed_content = re.sub(pattern, replacement, content)
        
        if content != fixed_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            return True
        return False
    
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    vpa_data_dir = Path("/home/quan/workspace/aipriceaction/vpa_data_week")
    
    if not vpa_data_dir.exists():
        print(f"Directory {vpa_data_dir} does not exist")
        return
    
    fixed_files = []
    total_files = 0
    
    # Process all .md files in the directory
    for md_file in vpa_data_dir.glob("*.md"):
        total_files += 1
        print(f"Processing: {md_file.name}")
        
        if fix_vpa_newlines(md_file):
            fixed_files.append(md_file.name)
            print(f"  ✓ Fixed")
        else:
            print(f"  - No changes needed")
    
    print(f"\nSummary:")
    print(f"Total files processed: {total_files}")
    print(f"Files fixed: {len(fixed_files)}")
    
    if fixed_files:
        print(f"Fixed files: {', '.join(fixed_files)}")

if __name__ == "__main__":
    main()