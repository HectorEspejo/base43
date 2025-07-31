#!/usr/bin/env python3
"""
Base43 Setup Script
Quick initialization script for new projects based on Base43 template.
"""

import os
import sys
import subprocess
import shutil
import secrets
import string
from pathlib import Path


class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_header():
    """Print welcome header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}╔══════════════════════════════════════╗{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}║      Base43 Project Setup Script     ║{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}╚══════════════════════════════════════╝{Colors.END}\n")


def print_success(message):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {message}{Colors.END}")


def print_error(message):
    """Print error message"""
    print(f"{Colors.RED}✗ {message}{Colors.END}")


def print_info(message):
    """Print info message"""
    print(f"{Colors.BLUE}→ {message}{Colors.END}")


def print_warning(message):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠ {message}{Colors.END}")


def generate_secret_key(length=50):
    """Generate a Django secret key"""
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(chars) for _ in range(length))


def check_requirements():
    """Check if required software is installed"""
    print_info("Checking requirements...")
    
    requirements = {
        'Python 3.8+': check_python_version,
        'Node.js 16+': check_node_version,
        'PostgreSQL': check_postgres,
        'Redis': check_redis
    }
    
    all_ok = True
    for req, check_func in requirements.items():
        if check_func():
            print_success(f"{req} is installed")
        else:
            print_error(f"{req} is NOT installed")
            all_ok = False
    
    return all_ok


def check_python_version():
    """Check if Python version is 3.8+"""
    return sys.version_info >= (3, 8)


def check_node_version():
    """Check if Node.js is installed and version is 16+"""
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        version = result.stdout.strip()
        major_version = int(version.split('.')[0].replace('v', ''))
        return major_version >= 16
    except:
        return False


def check_postgres():
    """Check if PostgreSQL is installed"""
    try:
        subprocess.run(['psql', '--version'], capture_output=True)
        return True
    except:
        return False


def check_redis():
    """Check if Redis is installed"""
    try:
        subprocess.run(['redis-cli', '--version'], capture_output=True)
        return True
    except:
        return False


def get_project_info():
    """Get project information from user"""
    print_info("\nProject Configuration")
    print("=" * 40)
    
    project_name = input(f"\n{Colors.BOLD}Project name:{Colors.END} ").strip()
    while not project_name or ' ' in project_name:
        print_error("Project name cannot be empty or contain spaces")
        project_name = input(f"{Colors.BOLD}Project name:{Colors.END} ").strip()
    
    project_description = input(f"{Colors.BOLD}Project description:{Colors.END} ").strip()
    
    domain = input(f"{Colors.BOLD}Domain (e.g., example.com):{Colors.END} ").strip()
    
    db_name = input(f"{Colors.BOLD}Database name [{project_name.lower()}_db]:{Colors.END} ").strip()
    if not db_name:
        db_name = f"{project_name.lower()}_db"
    
    db_user = input(f"{Colors.BOLD}Database user [{project_name.lower()}_user]:{Colors.END} ").strip()
    if not db_user:
        db_user = f"{project_name.lower()}_user"
    
    db_password = input(f"{Colors.BOLD}Database password [auto-generate]:{Colors.END} ").strip()
    if not db_password:
        db_password = generate_secret_key(20)
        print_info(f"Generated password: {db_password}")
    
    return {
        'project_name': project_name,
        'project_description': project_description,
        'domain': domain,
        'db_name': db_name,
        'db_user': db_user,
        'db_password': db_password,
        'secret_key': generate_secret_key()
    }


def replace_in_file(filepath, replacements):
    """Replace multiple strings in a file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        for old, new in replacements.items():
            content = content.replace(old, new)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    except Exception as e:
        print_error(f"Error updating {filepath}: {e}")
        return False


def update_project_files(project_info):
    """Update project files with new information"""
    print_info("\nUpdating project files...")
    
    replacements = {
        'Base43': project_info['project_name'],
        'base43': project_info['project_name'].lower(),
        'Your site description here': project_info['project_description'],
        'yourdomain.com': project_info['domain'] or 'localhost',
        'change_this_secure_password': project_info['db_password'],
        'generate_a_very_long_random_secret_key_here': project_info['secret_key'],
    }
    
    # Files to update
    files_to_update = [
        'README.md',
        'TEMPLATE_GUIDE.md',
        'frontend/package.json',
        'frontend/index.html',
        'backend/core/settings.py',
        '.env.example',
        'backend/.env.example'
    ]
    
    for file_path in files_to_update:
        if os.path.exists(file_path):
            if replace_in_file(file_path, replacements):
                print_success(f"Updated {file_path}")
            else:
                print_warning(f"Failed to update {file_path}")


def create_env_files(project_info):
    """Create .env files from examples"""
    print_info("\nCreating environment files...")
    
    # Backend .env
    backend_env_example = 'backend/.env.example'
    backend_env = 'backend/.env'
    
    if os.path.exists(backend_env_example):
        shutil.copy(backend_env_example, backend_env)
        
        # Update with actual values
        replace_in_file(backend_env, {
            'base43_db': project_info['db_name'],
            'base43_user': project_info['db_user'],
            'change-this-password': project_info['db_password'],
            'your-secret-key-here-change-in-production': project_info['secret_key'],
        })
        
        print_success("Created backend/.env")
    
    # Frontend .env
    frontend_env = 'frontend/.env.development'
    with open(frontend_env, 'w') as f:
        f.write("VITE_API_URL=http://localhost:8000\n")
        f.write("VITE_WS_URL=ws://localhost:8000\n")
    
    print_success("Created frontend/.env.development")


def setup_database(project_info):
    """Setup PostgreSQL database"""
    print_info("\nSetting up database...")
    
    try:
        # Create database and user
        commands = [
            f"CREATE DATABASE {project_info['db_name']};",
            f"CREATE USER {project_info['db_user']} WITH PASSWORD '{project_info['db_password']}';",
            f"GRANT ALL PRIVILEGES ON DATABASE {project_info['db_name']} TO {project_info['db_user']};"
        ]
        
        for cmd in commands:
            subprocess.run(
                ['psql', '-U', 'postgres', '-c', cmd],
                capture_output=True
            )
        
        print_success("Database created successfully")
        return True
    except Exception as e:
        print_warning(f"Could not create database automatically: {e}")
        print_info("Please create the database manually with:")
        print(f"\n  CREATE DATABASE {project_info['db_name']};")
        print(f"  CREATE USER {project_info['db_user']} WITH PASSWORD '{project_info['db_password']}';")
        print(f"  GRANT ALL PRIVILEGES ON DATABASE {project_info['db_name']} TO {project_info['db_user']};\n")
        return False


def install_dependencies():
    """Install Python and Node.js dependencies"""
    print_info("\nInstalling dependencies...")
    
    # Backend dependencies
    print_info("Installing Python dependencies...")
    os.chdir('backend')
    subprocess.run([sys.executable, '-m', 'venv', 'venv'])
    
    if os.name == 'nt':  # Windows
        pip_path = 'venv\\Scripts\\pip'
        python_path = 'venv\\Scripts\\python'
    else:  # Unix/Linux
        pip_path = 'venv/bin/pip'
        python_path = 'venv/bin/python'
    
    subprocess.run([pip_path, 'install', '-r', 'requirements.txt'])
    print_success("Python dependencies installed")
    
    # Frontend dependencies
    print_info("Installing Node.js dependencies...")
    os.chdir('../frontend')
    subprocess.run(['npm', 'install'])
    print_success("Node.js dependencies installed")
    
    os.chdir('..')


def run_migrations():
    """Run Django migrations"""
    print_info("\nRunning database migrations...")
    
    os.chdir('backend')
    if os.name == 'nt':  # Windows
        python_path = 'venv\\Scripts\\python'
    else:  # Unix/Linux
        python_path = 'venv/bin/python'
    
    subprocess.run([python_path, 'manage.py', 'migrate'])
    print_success("Migrations completed")
    
    os.chdir('..')


def create_superuser():
    """Prompt to create Django superuser"""
    print_info("\nWould you like to create a superuser account?")
    response = input("Create superuser? [Y/n]: ").strip().lower()
    
    if response != 'n':
        os.chdir('backend')
        if os.name == 'nt':  # Windows
            python_path = 'venv\\Scripts\\python'
        else:  # Unix/Linux
            python_path = 'venv/bin/python'
        
        subprocess.run([python_path, 'manage.py', 'createsuperuser'])
        os.chdir('..')


def print_next_steps(project_info):
    """Print next steps for the user"""
    print(f"\n{Colors.BOLD}{Colors.GREEN}✨ Setup Complete! ✨{Colors.END}\n")
    
    print(f"{Colors.BOLD}Next steps:{Colors.END}")
    print("\n1. Start the backend server:")
    print("   cd backend")
    print("   source venv/bin/activate  # On Windows: venv\\Scripts\\activate")
    print("   python manage.py runserver")
    
    print("\n2. Start the frontend server (in a new terminal):")
    print("   cd frontend")
    print("   npm run dev")
    
    print("\n3. Access your application:")
    print("   Frontend: http://localhost:5173")
    print("   Backend API: http://localhost:8000/api/")
    print("   Admin Panel: http://localhost:8000/admin/")
    
    print(f"\n{Colors.BOLD}Project Information:{Colors.END}")
    print(f"   Name: {project_info['project_name']}")
    print(f"   Database: {project_info['db_name']}")
    print(f"   Database User: {project_info['db_user']}")
    
    print(f"\n{Colors.YELLOW}Remember to:{Colors.END}")
    print("   - Update your logo (frontend/public/logo.png)")
    print("   - Customize the theme colors in frontend/tailwind.config.js")
    print("   - Review and update the README.md file")
    print("   - Set up your Git repository")
    
    print(f"\n{Colors.BLUE}Happy coding! 🚀{Colors.END}\n")


def main():
    """Main setup function"""
    print_header()
    
    # Check requirements
    if not check_requirements():
        print_error("\nPlease install all requirements before continuing.")
        sys.exit(1)
    
    # Get project information
    project_info = get_project_info()
    
    # Update project files
    update_project_files(project_info)
    
    # Create environment files
    create_env_files(project_info)
    
    # Install dependencies
    response = input(f"\n{Colors.BOLD}Install dependencies now? [Y/n]:{Colors.END} ").strip().lower()
    if response != 'n':
        install_dependencies()
    
    # Setup database
    response = input(f"\n{Colors.BOLD}Setup database now? [Y/n]:{Colors.END} ").strip().lower()
    if response != 'n':
        if setup_database(project_info):
            run_migrations()
            create_superuser()
    
    # Print next steps
    print_next_steps(project_info)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Setup cancelled by user.{Colors.END}")
        sys.exit(0)
    except Exception as e:
        print_error(f"\nAn error occurred: {e}")
        sys.exit(1)