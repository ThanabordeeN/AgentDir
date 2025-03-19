import os
import shutil
import glob
from datetime import datetime
from pathlib import Path


def create_dir(dir_path)-> str:
    """
    Create a directory if it doesn't exist.
    
    Args:
        dir_path (str): Path of the directory to create. Can be relative or absolute path.
                        Will create parent directories as needed.
    
    Returns:
        str: Success message indicating the directory was created.
    
    Example:
        create_dir('data/processed')
    """
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return f"Directory '{dir_path}' created"


def remove_dir(dir_path, recursive=False)-> str:
    """
    Remove a directory, with option to delete recursively.
    
    Args:
        dir_path (str): Path of the directory to remove.
        recursive (bool, optional): If True, removes directory and all contents.
                                   If False, directory must be empty. Defaults to False.
    
    Returns:
        str: Message indicating success or that the directory doesn't exist.
        
    Raises:
        OSError: If directory is not empty and recursive=False.
    """
    if os.path.exists(dir_path):
        if recursive:
            shutil.rmtree(dir_path)
        else:
            os.rmdir(dir_path)
        return f"Directory '{dir_path}' removed"
    return f"Directory '{dir_path}' doesn't exist"


def list_dir(dir_path='.')-> str:
    """
    List contents of a directory with detailed information.
    
    Args:
        dir_path (str, optional): Path of the directory to list. Defaults to current directory.
    
    Returns:
        list: List of dictionaries, each containing file/directory details:
            - name: Name of the file/directory
            - type: 'File' or 'Directory'
            - size: Size in bytes
            - modified: Last modification timestamp in 'YYYY-MM-DD HH:MM:SS' format
        str: Error message if directory doesn't exist.
    """
    if not os.path.exists(dir_path):
        return f"Directory '{dir_path}' doesn't exist"
    
    items = []
    for item in os.listdir(dir_path):
        full_path = os.path.join(dir_path, item)
        size = os.path.getsize(full_path)
        mod_time = datetime.fromtimestamp(os.path.getmtime(full_path)).strftime('%Y-%m-%d %H:%M:%S')
        item_type = 'Directory' if os.path.isdir(full_path) else 'File'
        items.append({
            'name': item,
            'type': item_type,
            'size': size,
            'modified': mod_time
        })
    return items


def get_current_dir()-> str:
    """
    Get the current working directory.
    
    Returns:
        str: Absolute path of the current working directory.
    """
    return os.getcwd()


def copy_file(src:str, dest:str)-> str:
    """
    Copy a file or directory from source to destination.
    
    Args:
        src (str): Source path of file or directory to copy.
        dest (str): Destination path where file or directory will be copied.
                   For directories, this should be the new directory name.
    
    Returns:
        str: Success message indicating what was copied and where.
        
    Raises:
        FileNotFoundError: If source doesn't exist.
        shutil.Error: If copying fails for any reason.
    """
    if os.path.isdir(src):
        shutil.copytree(src, dest)
        return f"Directory '{src}' copied to '{dest}'"
    else:
        shutil.copy2(src, dest)
        return f"File '{src}' copied to '{dest}'"


def move_file(src:str, dest:str)-> str:
    """
    Move a file or directory from source to destination.
    
    Args:
        src (str): Source path of file or directory to move.
        dest (str): Destination path where file or directory will be moved.
                   Can be a new filename or directory location.
    
    Returns:
        str: Success message indicating what was moved and where.
        
    Raises:
        FileNotFoundError: If source doesn't exist.
        OSError: If destination exists or other OS-related errors occur.
    """
    shutil.move(src, dest)
    return f"'{src}' moved to '{dest}'"


def remove_file(file_path:str)->str:
    """
    Remove a file from the filesystem.
    
    Args:
        file_path (str): Path of the file to remove.
    
    Returns:
        str: Success message or notification that file doesn't exist.
        
    Raises:
        OSError: If file exists but cannot be removed (e.g., permission issues).
    """
    if os.path.exists(file_path):
        os.remove(file_path)
        return f"File '{file_path}' removed"
    return f"File '{file_path}' doesn't exist"


def rename(old_path:str, new_path:str) -> str:
    """
    Rename a file or directory.
    
    Args:
        old_path (str): Current path of the file or directory.
        new_path (str): New path/name for the file or directory.
    
    Returns:
        str: Success message indicating the rename operation.
        
    Raises:
        FileNotFoundError: If old_path doesn't exist.
        FileExistsError: If new_path already exists.
    """
    os.rename(old_path, new_path)
    return f"'{old_path}' renamed to '{new_path}'"

def get_function_list()->list:
    """
    List of functions in the module.
    
    Returns:
        list: Names of functions in the module.
    """
    return [create_dir, remove_dir, list_dir, get_current_dir, copy_file, move_file, remove_file, rename]
