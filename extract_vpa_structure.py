#!/usr/bin/env python3
"""
One-time script to extract headings and subheadings from VPA_METHOD.md
and create structured content in docs/methods/ folder
"""

import os
import re
from pathlib import Path

def extract_headings(file_path):
    """Extract all headings and subheadings from markdown file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match markdown headings
    heading_pattern = r'^(#{1,6})\s+(.+)$'
    headings = []
    
    for match in re.finditer(heading_pattern, content, re.MULTILINE):
        level = len(match.group(1))
        title = match.group(2).strip()
        headings.append({
            'level': level,
            'title': title,
            'anchor': title.lower().replace(' ', '-').replace(':', '').replace('(', '').replace(')', '').replace('–', '').replace(',', '').replace('.', '')
        })
    
    return headings

def create_methods_structure(headings, output_dir):
    """Create structured files in methods directory based on headings"""
    
    # Create methods directory if it doesn't exist
    methods_dir = Path(output_dir)
    methods_dir.mkdir(exist_ok=True)
    
    current_section = None
    current_subsection = None
    current_content = []
    
    # Structure to hold all sections
    sections = {}
    
    for heading in headings:
        if heading['level'] == 2:  # Main sections (##)
            # Save previous section if exists
            if current_section and current_content:
                sections[current_section] = '\n'.join(current_content)
            
            current_section = heading['title']
            current_content = [f"# {heading['title']}\n"]
            current_subsection = None
            
        elif heading['level'] == 3:  # Subsections (###)
            if current_section:
                current_content.append(f"\n## {heading['title']}\n")
                current_subsection = heading['title']
                
        elif heading['level'] == 4:  # Sub-subsections (####)
            if current_section:
                current_content.append(f"\n### {heading['title']}\n")
    
    # Save the last section
    if current_section and current_content:
        sections[current_section] = '\n'.join(current_content)
    
    # Create files for each main section
    section_files = []
    for section_name, content in sections.items():
        # Create safe filename
        filename = re.sub(r'[^\w\s-]', '', section_name).strip()
        filename = re.sub(r'[-\s]+', '-', filename).lower()
        filename = f"{filename}.md"
        
        file_path = methods_dir / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        section_files.append({
            'filename': filename,
            'title': section_name,
            'path': str(file_path)
        })
    
    return section_files

def create_methods_readme(section_files, readme_path):
    """Create README.md for methods directory with table of contents"""
    
    readme_content = """# Phương Pháp VPA và Wyckoff - Tài Liệu Tham Khảo

Thư mục này chứa các phần được trích xuất từ tài liệu gốc "PHƯƠNG PHÁP GIAO DỊCH VPA (VOLUME PRICE ANALYSIS) THEO ANNA COULLING VÀ NỀN TẢNG WYCKOFF" để hỗ trợ việc viết lại các tutorial.

## Cấu Trúc Tài Liệu

"""
    
    for i, section in enumerate(section_files, 1):
        readme_content += f"{i}. **[{section['title']}](./{section['filename']})** - {section['filename']}\n"
    
    readme_content += """

## Cách Sử Dụng

Mỗi file trong thư mục này tương ứng với một phần chính trong tài liệu gốc VPA. Khi viết lại các tutorial, hãy tham khảo:

1. **Terminology** - Thuật ngữ tiếng Việt chính xác
2. **Educational Style** - Phong cách giảng dạy
3. **Structure** - Cấu trúc nội dung
4. **Examples** - Ví dụ thực tế

## Mapping với Tutorial Files

- **Nền tảng VPA & Wyckoff** → chapters 1.1, 1.2, 1.3
- **Giai đoạn Wyckoff** → chapters 2.1, 2.2
- **Tín hiệu VPA** → chapters 3.1, 3.2
- **Hệ thống Giao dịch** → chapter 4.1
- **Case Studies** → case-studies/ folder

Sử dụng `gemini -p` để truy cập nội dung với context window lớn khi cần thiết.
"""
    
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)

def main():
    # File paths
    vpa_file = "/Volumes/data/workspace/aipriceaction/docs/VPA_METHOD.md"
    methods_dir = "/Volumes/data/workspace/aipriceaction/docs/methods"
    
    # Check if VPA file exists
    if not os.path.exists(vpa_file):
        print(f"Error: {vpa_file} not found")
        return
    
    print("Extracting headings from VPA_METHOD.md...")
    headings = extract_headings(vpa_file)
    
    print(f"Found {len(headings)} headings")
    
    # Create methods structure
    print("Creating methods directory structure...")
    section_files = create_methods_structure(headings, methods_dir)
    
    # Create README
    readme_path = os.path.join(methods_dir, "README.md")
    create_methods_readme(section_files, readme_path)
    
    print(f"Created {len(section_files)} method files:")
    for section in section_files:
        print(f"  - {section['filename']}")
    
    print(f"\nMethods README created at: {readme_path}")
    print("\nNext: Use 'gemini -p' to create comprehensive Map of Content")

if __name__ == "__main__":
    main()