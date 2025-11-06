# Restaurant Management System

## Deployment on Render

### Configuration
1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Use these settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Python Version: 3.13

### Environment Variables
Add these environment variables in Render dashboard:
- `SECRET_KEY`: Set a secure random string
- `FLASK_ENV`: Set to `production`

### Database
The application uses SQLite which will be automatically initialized on first run.
Default admin credentials:
- Username: admin
- Password: admin123

## Local Development
1. Create virtual environment:
```bash
python -m venv venv
```

2. Activate virtual environment:
- Windows:
```powershell
.\venv\Scripts\activate
```
- Unix/MacOS:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

Visit http://127.0.0.1:5000/ in your browser.