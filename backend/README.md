```bash
## start venv
py -m venv env

## activate bat
.\env\Scripts\activate.bat

## install pip dependencies in requirements.txt
pip install -r requirements.txt

## run fastapi
uvicorn app.main:app --reload
```