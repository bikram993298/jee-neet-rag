import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load backend .env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))
api_key = os.getenv('GOOGLE_API_KEY') or os.getenv('GEMINI_API_KEY')
if not api_key:
    print('No API key found in backend/.env. Set GOOGLE_API_KEY or GEMINI_API_KEY and try again.')
    raise SystemExit(1)

genai.configure(api_key=api_key)

try:
    models = genai.list_models()
    print('Raw models response:')
    print(models)
    # Try to extract reasonable names
    names = []
    if isinstance(models, dict):
        candidates = models.get('models') or models.get('model') or []
    else:
        candidates = models
    for m in candidates:
        if isinstance(m, str):
            names.append(m)
        else:
            nm = getattr(m, 'name', None) or getattr(m, 'model', None)
            if not nm and isinstance(m, dict):
                nm = m.get('name') or m.get('model')
            if nm:
                names.append(nm)
    print('\nDiscovered model names (first 20):')
    for n in names[:20]:
        print('-', n)
except Exception as e:
    print('Failed to list models:', e)
    raise SystemExit(2)
    
