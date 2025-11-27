import json
from app import app

with app.test_client() as c:
    resp = c.get('/api/all/options')
    try:
        data = resp.get_json()
    except Exception:
        data = resp.get_data(as_text=True)
    print(json.dumps(data, indent=2, ensure_ascii=False))
