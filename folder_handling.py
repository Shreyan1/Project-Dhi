import os

# List of top-level directories
TOP_LEVEL_DIRECTORIES = ['/home', '/root', '/bin', '/dev', '/etc', '/lib', '/lib64', 
                         '/media', '/mnt', '/opt', '/var', '/proc', '/run', '/sbin', 
                         '/sys', '/tmp', '/usr', '/srv']

def get_absolute_path(foldername):
    # If the input is a top-level directory, use it as-is
    if foldername in TOP_LEVEL_DIRECTORIES:
        return foldername
    # If not a top-level directory, convert to absolute path based on current directory
    if not foldername.startswith('/'):
        foldername = os.path.abspath(foldername)
    return foldername

def check_access(foldername):
    if os.path.exists(foldername) and os.access(foldername, os.R_OK):
        return True
    return False

def list_files_in_folder(foldername):
    foldername = get_absolute_path(foldername)
    
    if check_access(foldername):
        os.system(f'cd {foldername} && ls -l')
    else:
        print(f"Permission denied or folder does not exist: {foldername}")

def handle_directories(foldername):
    if foldername == "/root" and os.geteuid() != 0:
        print("Permission denied: run as root to access /root")
        return
    elif foldername == "/home":
        foldername = os.path.expanduser("~")
    
    list_files_in_folder(foldername)

# Example usage
# foldername = "home"
# handle_directories(foldername)
