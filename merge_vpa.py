import re
from collections import defaultdict

# Read files
with open('VPA.md', 'r', encoding='utf-8') as f:
    vpa_content = f.read()
with open('VPA_NEW.md', 'r', encoding='utf-8') as f:
    vpa_new_content = f.read()

def extract_ticker_blocks(md_text):
    # Find all ticker headers (e.g. # TICKER) and their content
    pattern = re.compile(r'(^# ([A-Z0-9]+)\n)(.*?)(?=^# [A-Z0-9]+\n|\Z)', re.DOTALL | re.MULTILINE)
    blocks = {}
    for m in pattern.finditer(md_text):
        header, ticker, body = m.groups()
        blocks[ticker] = header + body.strip() + '\n'
    return blocks

def extract_new_lines(md_text):
    # For each ticker, extract the lines (excluding the header)
    pattern = re.compile(r'^# ([A-Z0-9]+)\n(.*?)(?=^# [A-Z0-9]+\n|\Z)', re.DOTALL | re.MULTILINE)
    ticker_lines = defaultdict(list)
    for m in pattern.finditer(md_text):
        ticker = m.group(1)
        body = m.group(2).strip()
        if body:
            # Split by ---
            parts = re.split(r'\n---+\n', body)
            for part in parts:
                part = part.strip()
                if part:
                    ticker_lines[ticker].append(part)
    return ticker_lines

# Extract ticker blocks from VPA.md
vpa_blocks = extract_ticker_blocks(vpa_content)
# Extract new lines from VPA_NEW.md
vpa_new_lines = extract_new_lines(vpa_new_content)

# Merge: for each ticker in vpa_new_lines, if exists in vpa_blocks, append new lines after old content, else create new block
for ticker, new_parts in vpa_new_lines.items():
    if ticker in vpa_blocks:
        old_block = vpa_blocks[ticker].rstrip('\n')
        for part in new_parts:
            old_block += '\n---\n' + part.strip()
        vpa_blocks[ticker] = old_block + '\n'
    else:
        block = f'# {ticker}\n'
        for i, part in enumerate(new_parts):
            if i > 0:
                block += '\n---\n'
            block += part.strip()
        vpa_blocks[ticker] = block + '\n'

# Sort tickers by name
sorted_tickers = sorted(vpa_blocks.keys())

# Write to new VPA.md
with open('VPA.md', 'w', encoding='utf-8') as f:
    for ticker in sorted_tickers:
        f.write('\n' + vpa_blocks[ticker].strip() + '\n')

# Post-process: Ensure blank lines before and after each # TICKER header
with open('VPA.md', 'r', encoding='utf-8') as f:
    merged = f.read()

# Ensure a blank line before each # TICKER (except at start)
merged = re.sub(r'([^\n])\n# ([A-Z0-9]+)', r'\1\n\n# \2', merged)
# Ensure a blank line after each # TICKER
merged = re.sub(r'# ([A-Z0-9]+)\n([^\n])', r'# \1\n\n\2', merged)
# Normalize extra blank lines to just two
merged = re.sub(r'\n{3,}', r'\n\n', merged)

with open('VPA.md', 'w', encoding='utf-8') as f:
    f.write(merged)
