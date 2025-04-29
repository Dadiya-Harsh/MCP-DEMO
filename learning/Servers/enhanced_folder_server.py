import difflib
import fnmatch
import json
import os
import shutil
import zipfile
from pathlib import Path
from typing import Dict, List, Optional

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP, Context
from mcp.server.fastmcp.exceptions import ResourceError
from mcp.types import TextContent
from pydantic import BaseModel, Field

# Load environment variables from .env file
load_dotenv()

# Configuration
ALLOWED_BASE_PATH = os.getenv("ALLOWED_BASE_PATH", "E:\\Test")  # Default to E:\Test if not set
# Normalize path for cross-platform compatibility
ALLOWED_BASE_PATH = str(Path(ALLOWED_BASE_PATH).resolve())
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB limit for file operations

mcp = FastMCP(
    name="folder_server",
    host="localhost",
    port=8004,
    log_level="INFO",
)

# Input models for validation
class FileOperation(BaseModel):
    path: str = Field(..., description="Relative path to the file")
    content: Optional[str] = Field(None, description="Content to write to the file")

class FileCopyMoveOperation(BaseModel):
    source_path: str = Field(..., description="Relative path to the source file")
    target_path: str = Field(..., description="Relative path to the target file")

class FolderOperation(BaseModel):
    path: str = Field(..., description="Relative path to the folder")

class FileSearchOperation(BaseModel):
    path: str = Field(..., description="Relative path to the directory to search in")
    pattern: str = Field(..., description="Search pattern (supports wildcards)")
    recursive: bool = Field(True, description="Whether to search recursively")

class FileDiffOperation(BaseModel):
    path1: str = Field(..., description="Relative path to the first file")
    path2: str = Field(..., description="Relative path to the second file")

class FileCompressOperation(BaseModel):
    action: str = Field(..., description="Operation: 'create' or 'extract'")
    path: str = Field(..., description="Relative path to the folder or zip file")
    zip_path: str = Field(..., description="Relative path to the zip file to create or extract")

# Security check for file paths
def sanitize_path(path: str) -> str:
    """Ensure path is safe and within allowed directory."""
    # Normalize input path and remove leading slashes
    full_path = os.path.abspath(os.path.join(ALLOWED_BASE_PATH, path.lstrip("/").lstrip("\\")))
    if not full_path.startswith(ALLOWED_BASE_PATH):
        raise ValueError("Access outside allowed directory")
    return full_path

@mcp.resource(
    name="folder_server",
    description="Provides access to a folder on the server.",
    uri="resource://folder-server",
    mime_type="application/json"
)
def folder_server() -> str:
    """
    Provides metadata about the folder server resource.

    Returns:
        str: JSON-encoded information about the folder server resource
    """
    return json.dumps({
        "status": "ready",
        "message": "Folder server resource is ready",
        "base_path": ALLOWED_BASE_PATH
    })

@mcp.tool(
    name="file_read",
    description="Read content from a specified file in the allowed folder."
)
async def file_read(op: FileOperation, ctx: Context) -> List[TextContent]:
    """
    Read content from a specified file.

    Args:
        op: FileOperation model containing the file path
        ctx: Context for logging and progress reporting

    Returns:
        List[TextContent]: File content and status
    """
    await ctx.info(f"Attempting to read file: {op.path}")
    try:
        safe_path = sanitize_path(op.path)
        if not os.path.exists(safe_path):
            await ctx.error(f"File not found: {op.path}")
            return [TextContent(type="text", text=json.dumps({"status": "error", "message": "File not found"}))]
        if not os.path.isfile(safe_path):
            await ctx.error(f"Path is not a file: {op.path}")
            return [TextContent(type="text", text=json.dumps({"status": "error", "message": "Path is not a file"}))]

        file_size = os.path.getsize(safe_path)
        if file_size > MAX_FILE_SIZE:
            await ctx.error(f"File too large: {file_size} bytes")
            return [TextContent(type="text", text=json.dumps({"status": "error", "message": "File too large"}))]

        await ctx.report_progress(50, 100)
        with open(safe_path, 'r', encoding='utf-8') as f:
            content = f.read()
        await ctx.report_progress(100, 100)

        return [TextContent(type="text", text=json.dumps({
            "status": "success",
            "path": op.path,
            "content": content
        }))]
    except Exception as e:
        await ctx.error(f"Error reading file {op.path}: {str(e)}")
        return [TextContent(type="text", text=json.dumps({"status": "error", "message": str(e)}))]

@mcp.tool(
    name="file_write",
    description="Write content to a specified file in the allowed folder."
)
async def file_write(op: FileOperation, ctx: Context) -> List[TextContent]:
    """
    Write content to a specified file.

    Args:
        op: FileOperation model containing path and content
        ctx: Context for logging and progress reporting

    Returns:
        List[TextContent]: Operation status
    """
    await ctx.info(f"Attempting to write file: {op.path}")
    try:
        if not op.content:
            await ctx.error("Content is required for file write")
            return [TextContent(type="text", text=json.dumps({"status": "error", "message": "Content is required"}))]

        safe_path = sanitize_path(op.path)
        os.makedirs(os.path.dirname(safe_path), exist_ok=True)

        await ctx.report_progress(50, 100)
        with open(safe_path, 'w', encoding='utf-8') as f:
            f.write(op.content)
        await ctx.report_progress(100, 100)

        return [TextContent(type="text", text=json.dumps({
            "status": "success",
            "path": op.path,
            "message": "File written successfully"
        }))]
    except Exception as e:
        await ctx.error(f"Error writing file {op.path}: {str(e)}")
        return [TextContent(type="text", text=json.dumps({"status": "error", "message": str(e)}))]

@mcp.tool(
    name="file_delete",
    description="Delete a specified file in the allowed folder."
)
async def file_delete(op: FileOperation, ctx: Context) -> List[TextContent]:
    """
    Delete a specified file.

    Args:
        op: FileOperation model containing the file path
        ctx: Context for logging and progress reporting

    Returns:
        List[TextContent]: Operation status
    """
    await ctx.info(f"Attempting to delete file: {op.path}")
    try:
        safe_path = sanitize_path(op.path)
        if not os.path.exists(safe_path):
            await ctx.error(f"File not found: {op.path}")
            return [TextContent(type="text", text=json.dumps({"status": "error", "message": "File not found"}))]
        if not os.path.isfile(safe_path):
            await ctx.error(f"Path is not a file: {op.path}")
            return [TextContent(type="text", text=json.dumps({"status": "error", "message": "Path is not a file"}))]

        await ctx.report_progress(50, 100)
        os.remove(safe_path)
        await ctx.report_progress(100, 100)

        return [TextContent(type="text", text=json.dumps({
            "status": "success",
            "path": op.path,
            "message": "File deleted successfully"
        }))]
    except Exception as e:
        await ctx.error(f"Error deleting file {op.path}: {str(e)}")
        return [TextContent(type="text", text=json.dumps({"status": "error", "message": str(e)}))]

@mcp.tool(
    name="folder_analysis",
    description="Analyze a folder to provide context about its contents."
)
async def folder_analysis(folder: FolderOperation, ctx: Context) -> List[TextContent]:
    """
    Analyze a folder's contents.

    Args:
        folder: FolderOperation model containing the folder path
        ctx: Context for logging and progress reporting

    Returns:
        List[TextContent]: Folder analysis results
    """
    await ctx.info(f"Analyzing folder: {folder.path}")
    try:
        safe_path = sanitize_path(folder.path)
        if not os.path.exists(safe_path):
            await ctx.error(f"Folder not found: {folder.path}")
            return [TextContent(type="text", text=json.dumps({"status": "error", "message": "Folder not found"}))]
        if not os.path.isdir(safe_path):
            await ctx.error(f"Path is not a directory: {folder.path}")
            return [TextContent(type="text", text=json.dumps({"status": "error", "message": "Path is not a directory"}))]

        files = []
        total_size = 0
        file_count = 0
        await ctx.report_progress(0, 100)

        for root, _, filenames in os.walk(safe_path):
            for i, filename in enumerate(filenames):
                file_path = os.path.join(root, filename)
                file_size = os.path.getsize(file_path)
                total_size += file_size
                file_count += 1
                files.append({
                    "name": filename,
                    "path": os.path.relpath(file_path, ALLOWED_BASE_PATH),
                    "size": file_size,
                    "modified": os.path.getmtime(file_path)
                })
                # Report progress every 10 files
                if (i + 1) % 10 == 0:
                    await ctx.report_progress(min(90, (i + 1) * 90 // len(filenames)), 100)

        await ctx.report_progress(100, 100)

        return [TextContent(type="text", text=json.dumps({
            "status": "success",
            "path": folder.path,
            "file_count": file_count,
            "total_size": total_size,
            "files": files[:50],  # Limit to 50 files for brevity
            "message": "Folder analysis completed"
        }))]
    except Exception as e:
        await ctx.error(f"Error analyzing folder {folder.path}: {str(e)}")
        return [TextContent(type="text", text=json.dumps({"status": "error", "message": str(e)}))]

# New file operations

@mcp.tool(
    name="file_copy",
    description="Copy a file to a new location within the allowed folder."
)
async def file_copy(op: FileCopyMoveOperation, ctx: Context) -> List[TextContent]:
    """
    Copy a file to a new location.

    Args:
        op: FileCopyMoveOperation model containing source and target paths
        ctx: Context for logging and progress reporting

    Returns:
        List[TextContent]: Operation status
    """
    await ctx.info(f"Copying file from {op.source_path} to {op.target_path}")
    try:
        safe_source_path = sanitize_path(op.source_path)
        safe_target_path = sanitize_path(op.target_path)

        if not os.path.exists(safe_source_path):
            await ctx.error(f"Source file not found: {op.source_path}")
            return [TextContent(type="text", text=json.dumps({"status": "error", "message": "Source file not found"}))]
        if not os.path.isfile(safe_source_path):
            await ctx.error(f"Source path is not a file: {op.source_path}")
            return [TextContent(type="text", text=json.dumps({"status": "error", "message": "Source path is not a file"}))]

        file_size = os.path.getsize(safe_source_path)
        if file_size > MAX_FILE_SIZE:
            await ctx.error(f"File too large: {file_size} bytes")
            return [TextContent(type="text", text=json.dumps({"status": "error", "message": "File too large"}))]

        # Create target directory if it doesn't exist
        os.makedirs(os.path.dirname(safe_target_path), exist_ok=True)

        await ctx.report_progress(50, 100)
        shutil.copy2(safe_source_path, safe_target_path)
        await ctx.report_progress(100, 100)

        return [TextContent(type="text", text=json.dumps({
            "status": "success",
            "source_path": op.source_path,
            "target_path": op.target_path,
            "message": "File copied successfully"
        }))]
    except Exception as e:
        await ctx.error(f"Error copying file {op.source_path}: {str(e)}")
        return [TextContent(type="text", text=json.dumps({"status": "error", "message": str(e)}))]

@mcp.tool(
    name="file_move",
    description="Move or rename a file within the allowed folder."
)
async def file_move(op: FileCopyMoveOperation, ctx: Context) -> List[TextContent]:
    """
    Move or rename a file.

    Args:
        op: FileCopyMoveOperation model containing source and target paths
        ctx: Context for logging and progress reporting

    Returns:
        List[TextContent]: Operation status
    """
    await ctx.info(f"Moving file from {op.source_path} to {op.target_path}")
    try:
        safe_source_path = sanitize_path(op.source_path)
        safe_target_path = sanitize_path(op.target_path)

        if not os.path.exists(safe_source_path):
            await ctx.error(f"Source file not found: {op.source_path}")
            return [TextContent(type="text", text=json.dumps({"status": "error", "message": "Source file not found"}))]
        if not os.path.isfile(safe_source_path):
            await ctx.error(f"Source path is not a file: {op.source_path}")
            return [TextContent(type="text", text=json.dumps({"status": "error", "message": "Source path is not a file"}))]

        # Create target directory if it doesn't exist
        os.makedirs(os.path.dirname(safe_target_path), exist_ok=True)

        await ctx.report_progress(50, 100)
        shutil.move(safe_source_path, safe_target_path)
        await ctx.report_progress(100, 100)

        return [TextContent(type="text", text=json.dumps({
            "status": "success",
            "source_path": op.source_path,
            "target_path": op.target_path,
            "message": "File moved successfully"
        }))]
    except Exception as e:
        await ctx.error(f"Error moving file {op.source_path}: {str(e)}")
        return [TextContent(type="text", text=json.dumps({"status": "error", "message": str(e)}))]

@mcp.tool(
    name="file_info",
    description="Get detailed metadata about a specific file."
)
async def file_info(op: FileOperation, ctx: Context) -> List[TextContent]:
    """
    Get detailed information about a file.

    Args:
        op: FileOperation model containing the file path
        ctx: Context for logging and progress reporting

    Returns:
        List[TextContent]: File metadata
    """
    await ctx.info(f"Getting file info: {op.path}")
    try:
        safe_path = sanitize_path(op.path)
        if not os.path.exists(safe_path):
            await ctx.error(f"File not found: {op.path}")
            return [TextContent(type="text", text=json.dumps({"status": "error", "message": "File not found"}))]
        if not os.path.isfile(safe_path):
            await ctx.error(f"Path is not a file: {op.path}")
            return [TextContent(type="text", text=json.dumps({"status": "error", "message": "Path is not a file"}))]

        stats = os.stat(safe_path)
        file_info = {
            "name": os.path.basename(safe_path),
            "path": op.path,
            "size": stats.st_size,
            "created": stats.st_ctime,
            "modified": stats.st_mtime,
            "accessed": stats.st_atime,
            "extension": os.path.splitext(safe_path)[1],
            "is_hidden": os.path.basename(safe_path).startswith('.')
        }

        await ctx.report_progress(100, 100)

        return [TextContent(type="text", text=json.dumps({
            "status": "success",
            "file_info": file_info
        }))]
    except Exception as e:
        await ctx.error(f"Error getting file info {op.path}: {str(e)}")
        return [TextContent(type="text", text=json.dumps({"status": "error", "message": str(e)}))]

# New folder operations

@mcp.tool(
    name="folder_create",
    description="Create a new directory within the allowed folder."
)
async def folder_create(folder: FolderOperation, ctx: Context) -> List[TextContent]:
    """
    Create a new directory.

    Args:
        folder: FolderOperation model containing the folder path
        ctx: Context for logging and progress reporting

    Returns:
        List[TextContent]: Operation status
    """
    await ctx.info(f"Creating folder: {folder.path}")
    try:
        safe_path = sanitize_path(folder.path)

        if os.path.exists(safe_path):
            if os.path.isdir(safe_path):
                await ctx.info(f"Folder already exists: {folder.path}")
                return [TextContent(type="text", text=json.dumps({
                    "status": "info",
                    "message": "Folder already exists"
                }))]
            else:
                await ctx.error(f"A file with that name already exists: {folder.path}")
                return [TextContent(type="text", text=json.dumps({
                    "status": "error",
                    "message": "A file with that name already exists"
                }))]

        await ctx.report_progress(50, 100)
        os.makedirs(safe_path, exist_ok=True)
        await ctx.report_progress(100, 100)

        return [TextContent(type="text", text=json.dumps({
            "status": "success",
            "path": folder.path,
            "message": "Folder created successfully"
        }))]
    except Exception as e:
        await ctx.error(f"Error creating folder {folder.path}: {str(e)}")
        return [TextContent(type="text", text=json.dumps({"status": "error", "message": str(e)}))]

@mcp.tool(
    name="folder_delete",
    description="Delete an empty directory within the allowed folder."
)
async def folder_delete(folder: FolderOperation, ctx: Context) -> List[TextContent]:
    """
    Delete an empty directory.

    Args:
        folder: FolderOperation model containing the folder path
        ctx: Context for logging and progress reporting

    Returns:
        List[TextContent]: Operation status
    """
    await ctx.info(f"Deleting folder: {folder.path}")
    try:
        safe_path = sanitize_path(folder.path)

        if not os.path.exists(safe_path):
            await ctx.error(f"Folder not found: {folder.path}")
            return [TextContent(type="text", text=json.dumps({"status": "error", "message": "Folder not found"}))]
        if not os.path.isdir(safe_path):
            await ctx.error(f"Path is not a directory: {folder.path}")
            return [TextContent(type="text", text=json.dumps({"status": "error", "message": "Path is not a directory"}))]

        await ctx.report_progress(50, 100)
        try:
            os.rmdir(safe_path)  # Only removes empty directories
            await ctx.report_progress(100, 100)
            return [TextContent(type="text", text=json.dumps({
                "status": "success",
                "path": folder.path,
                "message": "Folder deleted successfully"
            }))]
        except OSError:
            await ctx.error(f"Directory not empty: {folder.path}")
            return [TextContent(type="text", text=json.dumps({
                "status": "error",
                "message": "Directory not empty. Use folder_analysis to view contents."
            }))]
    except Exception as e:
        await ctx.error(f"Error deleting folder {folder.path}: {str(e)}")
        return [TextContent(type="text", text=json.dumps({"status": "error", "message": str(e)}))]

@mcp.tool(
    name="folder_list",
    description="List contents of a directory (simplified version of folder_analysis)."
)
async def folder_list(folder: FolderOperation, ctx: Context) -> List[TextContent]:
    """
    List contents of a directory.

    Args:
        folder: FolderOperation model containing the folder path
        ctx: Context for logging and progress reporting

    Returns:
        List[TextContent]: Directory listing
    """
    await ctx.info(f"Listing folder contents: {folder.path}")
    try:
        safe_path = sanitize_path(folder.path)

        if not os.path.exists(safe_path):
            await ctx.error(f"Folder not found: {folder.path}")
            return [TextContent(type="text", text=json.dumps({"status": "error", "message": "Folder not found"}))]
        if not os.path.isdir(safe_path):
            await ctx.error(f"Path is not a directory: {folder.path}")
            return [TextContent(type="text", text=json.dumps({"status": "error", "message": "Path is not a directory"}))]

        await ctx.report_progress(50, 100)

        items = []
        for item in os.listdir(safe_path):
            item_path = os.path.join(safe_path, item)
            is_dir = os.path.isdir(item_path)
            items.append({
                "name": item,
                "is_directory": is_dir,
                "size": os.path.getsize(item_path) if not is_dir else None
            })

        await ctx.report_progress(100, 100)

        return [TextContent(type="text", text=json.dumps({
            "status": "success",
            "path": folder.path,
            "items": items,
            "count": len(items)
        }))]
    except Exception as e:
        await ctx.error(f"Error listing folder {folder.path}: {str(e)}")
        return [TextContent(type="text", text=json.dumps({"status": "error", "message": str(e)}))]

# Advanced features

@mcp.tool(
    name="file_search",
    description="Search for files matching patterns within a directory."
)
async def file_search(op: FileSearchOperation, ctx: Context) -> List[TextContent]:
    """
    Search for files matching patterns.

    Args:
        op: FileSearchOperation model containing search parameters
        ctx: Context for logging and progress reporting

    Returns:
        List[TextContent]: Search results
    """
    await ctx.info(f"Searching for files matching pattern '{op.pattern}' in: {op.path}")
    try:
        safe_path = sanitize_path(op.path)

        if not os.path.exists(safe_path):
            await ctx.error(f"Directory not found: {op.path}")
            return [TextContent(type="text", text=json.dumps({"status": "error", "message": "Directory not found"}))]
        if not os.path.isdir(safe_path):
            await ctx.error(f"Path is not a directory: {op.path}")
            return [TextContent(type="text", text=json.dumps({"status": "error", "message": "Path is not a directory"}))]

        await ctx.report_progress(0, 100)
        matches = []

        if op.recursive:
            for root, dirnames, filenames in os.walk(safe_path):
                for filename in fnmatch.filter(filenames, op.pattern):
                    file_path = os.path.join(root, filename)
                    matches.append({
                        "name": filename,
                        "path": os.path.relpath(file_path, ALLOWED_BASE_PATH),
                        "size": os.path.getsize(file_path)
                    })
                await ctx.report_progress(min(90, len(matches)), 100)
        else:
            for filename in fnmatch.filter(os.listdir(safe_path), op.pattern):
                file_path = os.path.join(safe_path, filename)
                if os.path.isfile(file_path):
                    matches.append({
                        "name": filename,
                        "path": os.path.relpath(file_path, ALLOWED_BASE_PATH),
                        "size": os.path.getsize(file_path)
                    })
            await ctx.report_progress(90, 100)

        await ctx.report_progress(100, 100)

        return [TextContent(type="text", text=json.dumps({
            "status": "success",
            "search_path": op.path,
            "pattern": op.pattern,
            "matches": matches,
            "count": len(matches)
        }))]
    except Exception as e:
        await ctx.error(f"Error searching in folder {op.path}: {str(e)}")
        return [TextContent(type="text", text=json.dumps({"status": "error", "message": str(e)}))]

@mcp.tool(
    name="file_diff",
    description="Compare the contents of two text files."
)
async def file_diff(op: FileDiffOperation, ctx: Context) -> List[TextContent]:
    """
    Compare the contents of two text files.

    Args:
        op: FileDiffOperation model containing paths to files to compare
        ctx: Context for logging and progress reporting

    Returns:
        List[TextContent]: Diff results
    """
    await ctx.info(f"Comparing files: {op.path1} and {op.path2}")
    try:
        safe_path1 = sanitize_path(op.path1)
        safe_path2 = sanitize_path(op.path2)

        for path, label in [(safe_path1, op.path1), (safe_path2, op.path2)]:
            if not os.path.exists(path):
                await ctx.error(f"File not found: {label}")
                return [TextContent(type="text", text=json.dumps({"status": "error", "message": f"File not found: {label}"}))]
            if not os.path.isfile(path):
                await ctx.error(f"Path is not a file: {label}")
                return [TextContent(type="text", text=json.dumps({"status": "error", "message": f"Path is not a file: {label}"}))]
            if os.path.getsize(path) > MAX_FILE_SIZE:
                await ctx.error(f"File too large: {label}")
                return [TextContent(type="text", text=json.dumps({"status": "error", "message": f"File too large: {label}"}))]

        await ctx.report_progress(30, 100)

        # Read both files
        with open(safe_path1, 'r', encoding='utf-8') as f1:
            content1 = f1.readlines()

        with open(safe_path2, 'r', encoding='utf-8') as f2:
            content2 = f2.readlines()

        await ctx.report_progress(60, 100)

        # Generate diff
        diff = list(difflib.unified_diff(
            content1, content2,
            fromfile=op.path1, tofile=op.path2,
            lineterm=''
        ))

        await ctx.report_progress(100, 100)

        return [TextContent(type="text", text=json.dumps({
            "status": "success",
            "path1": op.path1,
            "path2": op.path2,
            "diff": diff,
            "is_identical": len(diff) == 0
        }))]
    except Exception as e:
        await ctx.error(f"Error comparing files: {str(e)}")
        return [TextContent(type="text", text=json.dumps({"status": "error", "message": str(e)}))]

@mcp.tool(
    name="file_compress",
    description="Create or extract zip archives."
)
async def file_compress(op: FileCompressOperation, ctx: Context) -> List[TextContent]:
    """
    Create or extract zip archives.

    Args:
        op: FileCompressOperation model containing compression parameters
        ctx: Context for logging and progress reporting

    Returns:
        List[TextContent]: Operation status
    """
    await ctx.info(f"Compression operation '{op.action}' for path: {op.path}")
    try:
        safe_path = sanitize_path(op.path)
        safe_zip_path = sanitize_path(op.zip_path)

        if op.action == "create":
            if not os.path.exists(safe_path):
                await ctx.error(f"Source path not found: {op.path}")
                return [TextContent(type="text", text=json.dumps({"status": "error", "message": f"Source path not found: {op.path}"}))]

            # Create directory for zip file if needed
            os.makedirs(os.path.dirname(safe_zip_path), exist_ok=True)

            # Create a new zip file
            with zipfile.ZipFile(safe_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Handle directory vs file
                if os.path.isdir(safe_path):
                    base_dir = os.path.basename(safe_path.rstrip('/\\'))
                    total_files = sum([len(files) for _, _, files in os.walk(safe_path)])
                    processed = 0

                    for root, _, files in os.walk(safe_path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            if os.path.getsize(file_path) <= MAX_FILE_SIZE:
                                # Add file to zip with relative path
                                rel_path = os.path.join(base_dir, os.path.relpath(file_path, safe_path))
                                zipf.write(file_path, rel_path)
                                processed += 1
                                await ctx.report_progress(min(90, processed * 90 // total_files), 100)
                            else:
                                # Add single file to zip
                                zipf.write(safe_path, os.path.basename(safe_path))
                                await ctx.report_progress(90, 100)

                                await ctx.report_progress(100, 100)
            return [TextContent(type="text", text=json.dumps({
                "status": "success",
                "action": "create",
                "source_path": op.path,
                "zip_path": op.zip_path,
                "message": "Archive created successfully"
            }))]

        elif op.action == "extract":
            if not os.path.exists(safe_zip_path):
                await ctx.error(f"Zip file not found: {op.zip_path}")
                return [TextContent(type="text", text=json.dumps({"status": "error", "message": f"Zip file not found: {op.zip_path}"}))]
            if not zipfile.is_zipfile(safe_zip_path):
                await ctx.error(f"Not a valid zip file: {op.zip_path}")
                return [TextContent(type="text", text=json.dumps({"status": "error", "message": f"Not a valid zip file: {op.zip_path}"}))]

            # Create extraction directory if needed
            os.makedirs(safe_path, exist_ok=True)

            # Extract the zip file
            with zipfile.ZipFile(safe_zip_path, 'r') as zipf:
                # Get total files for progress reporting
                total_files = len(zipf.infolist())

                for i, file_info in enumerate(zipf.infolist()):
                    zipf.extract(file_info, safe_path)
                    await ctx.report_progress(min(90, (i + 1) * 90 // total_files), 100)

            await ctx.report_progress(100, 100)
            return [TextContent(type="text", text=json.dumps({
                "status": "success",
                "action": "extract",
                "zip_path": op.zip_path,
                "target_path": op.path,
                "message": "Archive extracted successfully"
            }))]

        else:
            await ctx.error(f"Invalid action: {op.action}")
            return [TextContent(type="text", text=json.dumps({
                "status": "error",
                "message": "Invalid action. Use 'create' or 'extract'."
            }))]
    except Exception as e:
        await ctx.error(f"Error in compression operation: {str(e)}")
        return [TextContent(type="text", text=json.dumps({"status": "error", "message": str(e)}))]

@mcp.resource(
    name="folder_content",
    description="Read content of a specific file as a resource.",
    uri="resource://folder-content/{path}",
    mime_type="text/plain"
)
async def folder_content(path: str) -> str:
    """
    Read content of a specific file as a resource.

    Args:
        path: Relative path to the file

    Returns:
        str: File content
    """
    ctx = Context(fastmcp=mcp)  # Create context manually for logging
    await ctx.info(f"Reading file content as resource: {path}")
    try:
        safe_path = sanitize_path(path)
        if not os.path.exists(safe_path):
            await ctx.error(f"File not found: {path}")
            raise ResourceError(f"File not found: {path}")
        if not os.path.isfile(safe_path):
            await ctx.error(f"Path is not a file: {path}")
            raise ResourceError(f"Path is not a file: {path}")

        file_size = os.path.getsize(safe_path)
        if file_size > MAX_FILE_SIZE:
            await ctx.error(f"File too large: {file_size} bytes")
            raise ResourceError(f"File too large: {file_size} bytes")

        with open(safe_path, 'r', encoding='utf-8') as f:
            content = f.read()

        return content
    except Exception as e:
        await ctx.error(f"Error reading file resource {path}: {str(e)}")
        raise ResourceError(str(e))

# Additional specialized prompts

@mcp.prompt(
    name="folder_server_prompt",
    description="Prompt for performing operations in the folder server."
)
def folder_server_prompt() -> List[Dict]:
    """
    Provides guidance and context for performing operations in the folder server.

    Returns:
        List[Dict]: A list of chat messages for the AI to consider
    """
    return [
        {
            "role": "system",
            "content": f"You are a folder server assistant. All operations must be performed within {ALLOWED_BASE_PATH}. "
                       f"Available tools include file operations (read, write, delete, copy, move, info), "
                       f"folder operations (analysis, create, delete, list), and advanced features "
                       f"(search, diff, compress). Use these tools to perform file and folder operations safely."
        },
        {
            "role": "user",
            "content": "I need help managing files and folders on the server. What operations can I perform?"
        }
    ]

@mcp.prompt(
    name="file_management_prompt",
    description="Prompt for organizing files and folders efficiently."
)
def file_management_prompt() -> List[Dict]:
    """
    Provides guidance for file and folder organization tasks.

    Returns:
        List[Dict]: A list of chat messages for the AI to consider
    """
    return [
        {
            "role": "system",
            "content": f"You are a file organization assistant. You help users organize their files and folders efficiently "
                       f"within {ALLOWED_BASE_PATH}. You can suggest best practices for file organization, "
                       f"help identify duplicate files, create logical folder structures, and perform batch operations. "
                       f"Available tools include file_copy, file_move, folder_create, folder_list, folder_analysis, and file_search."
        },
        {
            "role": "user",
            "content": "I need help organizing my files into a more logical structure. Can you show me how to analyze my current files and create a better organization system?"
        }
    ]

@mcp.prompt(
    name="text_editing_prompt",
    description="Prompt for text file editing workflows."
)
def text_editing_prompt() -> List[Dict]:
    """
    Provides guidance for text file editing workflows.

    Returns:
        List[Dict]: A list of chat messages for the AI to consider
    """
    return [
        {
            "role": "system",
            "content": f"You are a text editing assistant. You help users read, modify, and create text files "
                       f"within {ALLOWED_BASE_PATH}. You can suggest edits, help format text, and guide users "
                       f"through common text editing workflows. Available tools include file_read, file_write, "
                       f"file_diff, and file_info. You can help with tasks like updating configuration files, "
                       f"editing documents, and creating new text-based content."
        },
        {
            "role": "user",
            "content": "I need to modify a text file to update some configuration settings. Can you show me how to read, modify, and save changes to the file?"
        }
    ]

@mcp.prompt(
    name="file_search_prompt",
    description="Prompt for finding specific files and content."
)
def file_search_prompt() -> List[Dict]:
    """
    Provides guidance for finding specific files and content.

    Returns:
        List[Dict]: A list of chat messages for the AI to consider
    """
    return [
        {
            "role": "system",
            "content": f"You are a file search assistant. You help users find specific files and content "
                       f"within {ALLOWED_BASE_PATH}. You can guide users on how to search for files by name pattern, "
                       f"analyze folder contents, and locate specific content. Available tools include file_search, "
                       f"folder_list, folder_analysis, and file_read. You can help with tasks like finding files "
                       f"matching certain patterns, locating files with specific content, and organizing search results."
        },
        {
            "role": "user",
            "content": "I need to find all text files that contain specific information. How can I search through files efficiently?"
        }
    ]

if __name__ == "__main__":
    # Ensure the base path exists
    os.makedirs(ALLOWED_BASE_PATH, exist_ok=True)
    mcp.run(transport="stdio")  # Use SSE transport for HTTP compatibility