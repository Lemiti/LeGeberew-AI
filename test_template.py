# test_template.py
from app import create_app

app = create_app()

with app.app_context():
    print("🔍 Checking template configuration...")
    print(f"Template folder: {app.template_folder}")
    print(f"Root path: {app.root_path}")
    
    # Check if templates directory exists
    import os
    templates_path = os.path.join(app.root_path, 'templates')
    print(f"Templates path: {templates_path}")
    print(f"Templates exists: {os.path.exists(templates_path)}")
    
    if os.path.exists(templates_path):
        print("📁 Files in templates directory:")
        for file in os.listdir(templates_path):
            print(f"   - {file}")