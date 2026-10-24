import json
from pathlib import Path
from measurement import analyze, synthetic_fixture
if __name__=='__main__':
 rows=synthetic_fixture();result=analyze(rows)
 Path('synthetic_data.json').write_text(json.dumps(rows,indent=2)+'\n')
 Path('results.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))
