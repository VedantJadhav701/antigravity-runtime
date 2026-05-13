import os
import re

for root, dirs, files in os.walk('agrt'):
    if '__pycache__' in root: continue
    for file in files:
        if file.endswith('.py'):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace string literals for paths and loggers
            new_content = re.sub(r'"runtime\.', '"agrt.', content)
            new_content = re.sub(r'runtime/artifacts', 'agrt/artifacts', new_content)
            new_content = re.sub(r'"runtime", "artifacts"', '"agrt", "artifacts"', new_content)
            new_content = re.sub(r'"runtime", "generation"', '"agrt", "generation"', new_content)
            new_content = re.sub(r'\.runtime', '.agrt', new_content)
            
            if new_content != content:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f'Updated {path}')
