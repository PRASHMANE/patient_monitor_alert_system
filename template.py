
import os
from pathlib import Path

# Define the folder structure


# Define files with optional boilerplate content
list_of_files = [


    "data/__init__.py",
    "data/raw/__init__.py",
    "data/processed/__init__.py",
    "data/external/__init__.py",



    "src/__init__.py",
    "src/data/__init__.py",
    "src/data/load_data.py",
    "src/data/preprocess.py",
    "src/data/feature_engineering.py",
    
    "src/models/__init__.py",
    "src/models/model.py",
    "src/models/train.py",
    "src/models/evaluate.py",
    
    "src/pipelines/__init__.py",
    "src/pipelines/training_pipeline.py",
    "src/pipelines/prediction_pipeline.py",
    
    "src/utils/__init__.py",
    "src/utils/logger.py",
    "src/utils/helpers.py",
    
    "src/config/__init__.py",
    "src/config/config.yaml",
    
    "tests/__init__.py",
    "tests/test_data.py",
    "tests/test_model.py",
    "tests/test_pipeline.py",
    
    "deployment/__init__.py",
    "deployment/api/__init__.py",
    "deployment/api/main.py",
    "deployment/api/routes.py",
    "deployment/api/schema.py",
    
    "deployment/docker/Dockerfile",
    
    "deployment/kubernetes/deployment.yaml",
    "deployment/cloud/terraform.tf",
    
    ".github/workflows/ci-cd-pipeline.yaml",
    
    "dvc.yaml",
    
    "requirements.txt",
    "environment.yaml",
    "setup.py",
    "README.md",
    "MLproject",
    ".gitignore",
    "LICENSE",
    "Notebook/exp1.ipynb"
]



for filepath in list_of_files:
    path = Path(filepath)
    filedir, filename = os.path.split(path)
    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        #logging.info(f"Created directory: {filedir} for file: {filename}")
    try:
        if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
            with open(filepath, 'w') as f:
                pass # created empty file
    except Exception as e:
        print(f"Error creating file {filepath}: {e}")