class File:
    def __init__(self, name, content=""):
        self.type = "file"
        self.name = name
        self.content = content
    
    def __repr__(self):
        return f"File({self.name})"

class Folder:
    def __init__(self, name):
        self.type = "folder"
        self.name = name
        self.children = {}  # dict of name -> File or Folder
    
    def __repr__(self):
        return f"Folder({self.name})"

# Create /etc folder
etc = Folder("etc")

# Create /etc/hostname file with content
hostname_file = File("hostname", "my-computer")

# Add the file to the folder
etc.children["hostname"] = hostname_file

print(etc)
print(etc.children["hostname"].content)

class VirtualFilesystem:
    def __init__(self):
        self.root = Folder("/")

    def navigate(self, path):
        parts = path.split("/")
        parts = [p for p in parts if p]  # Remove empty strings
        
        current = self.root
        
        for part in parts[:-1]:  # Navigate through all folders
            current = current.children[part]
        
        return current.children[parts[-1]]  # Return the final file/folder

    def cat(self, path):
        """Read a file's content. Returns content or error message."""
        try:
            result = self.navigate(path)
            if result.type == "file":
                return result.content
            else:
                return f"Error: {path} is a directory"
        except KeyError:
            return f"Error: {path} not found"
    
    def ls(self, path):
        """List contents of a folder."""
        try:
            result = self.navigate(path)
            if result.type == 'folder':
                result = list(result.children.keys())
                return "\n".join(result)
            else:
                return f"Error: {path} is not a directory"
        except:
            return f"Error: {path} is not found"
    
    def mkdir(self, path):
        """Create a folder at the given path."""
        parts = path.split("/")
        parts = [p for p in parts if p]
        
        current = self.root
        
        for part in parts:
            if part not in current.children:
                current.children[part] = Folder(part)
            elif current.children[part].type != "folder":
                return f"Error: File exists with {part} name in {path}, choose another name."
            current = current.children[part]
        return f"{path}"
    
    def touch(self, path):
        """Create a file at the given path."""
        parts = path.split("/")
        parts = [p for p in parts if p]
        
        current = self.root
        
        for part in parts[:-1]:
            if part not in current.children:
                current.children[part] = Folder(part)
            elif current.children[part].type != "folder":
                return f"Error: File exists with {part} name in {path}, choose another name."
            current = current.children[part]
        if parts[-1] not in current.children:
            current.children[parts[-1]] = File(parts[-1])
        return f"{path}"

fs = VirtualFilesystem()

# Build /etc/hostname
etc = Folder("etc")
hostname_file = File("hostname", "my-computer")
etc.children["hostname"] = hostname_file
fs.root.children["etc"] = etc

# Now use navigate
result = fs.navigate("/etc/hostname")
print(result.content)  # Should print: my-computer


print(fs.cat("/etc/doesnotexist/hostname"))
print(fs.cat("/etc/"))

port_file = File("port", "8080")
etc.children["port"] = port_file

superuser_file = File("superuser", "shreya")
etc.children["superuser"] = superuser_file

print(fs.ls("/etc/"))
print(fs.ls("/etc"))
print(fs.cat("/etc/hostname"))

print(fs.mkdir("/etc/hostname"))
print(fs.mkdir("/etc/hosts"))
print(fs.mkdir("/home/dev/projects"))
print(fs.ls("/home/dev"))
print(fs.ls("/home"))

print(fs.touch("/home/dev/file"))
print(fs.touch("/home/file_home"))