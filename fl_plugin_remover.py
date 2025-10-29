import os
import sys
import ctypes
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import shutil
from typing import List, Dict, Tuple

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    if not is_admin():
        # Get the script path with proper escaping
        script = os.path.abspath(__file__).replace('\\', '\\\\')
        python_exe = sys.executable.replace('\\', '\\\\')
        
        # Create a temporary VBS script to run PowerShell hidden
        vbs_script = f"""
        Set UAC = CreateObject("Shell.Application")
        UAC.ShellExecute "{python_exe}", "\"{script}\"", "", "runas", 0
        """
        
        # Write the temporary VBS script
        temp_script = os.path.join(os.environ['TEMP'], 'elevate_script.vbs')
        with open(temp_script, 'w') as f:
            f.write(vbs_script)
        
        try:
            # Execute the VBS script which will run the Python script as admin
            # without showing any windows
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            
            subprocess.Popen(
                ['wscript.exe', '//B', temp_script],
                shell=True,
                startupinfo=startupinfo,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE
            )
            sys.exit(0)
        except Exception as e:
            try:
                # Fallback to PowerShell method if VBS fails
                ps_script = f"""
                $script = '{script}'
                $python = '{python_exe}'
                $psi = New-Object System.Diagnostics.ProcessStartInfo
                $psi.FileName = $python
                $psi.Arguments = "`"$script`""
                $psi.Verb = 'runas'
                $psi.WindowStyle = 'Hidden'
                $proc = [System.Diagnostics.Process]::Start($psi)
                $proc.WaitForExit()
                if ($proc.ExitCode -ne 0) {{
                    [System.Windows.Forms.MessageBox]::Show("Failed to run with admin rights", "Error", [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Error)
                }}
                """
                
                temp_ps_script = os.path.join(os.environ['TEMP'], 'elevate_script.ps1')
                with open(temp_ps_script, 'w') as f:
                    f.write(ps_script)
                
                subprocess.Popen(
                    ['powershell.exe', '-ExecutionPolicy', 'Bypass', '-WindowStyle', 'Hidden', '-File', temp_ps_script],
                    shell=True,
                    startupinfo=startupinfo,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    stdin=subprocess.PIPE
                )
                sys.exit(0)
            except Exception as e2:
                messagebox.showerror("Error", f"Failed to elevate privileges: {str(e2)}")
                sys.exit(1)

class FLPluginRemover:
    def __init__(self, root):
        self.root = root
        self.root.title("Easy")
<<<<<<< HEAD
        self.root.geometry("800x600")
        self.root.minsize(800, 600)
=======
        self.root.geometry("900x700")  # Slightly larger default window
        self.root.minsize(900, 700)
        
        # Set window icon
        try:
            self.root.iconbitmap('icon.ico')  # For Windows
        except:
            try:
                # Try alternative method if the above fails
                img = tk.PhotoImage(file='icon.ico')
                self.root.tk.call('wm', 'iconphoto', self.root._w, img)
            except:
                pass  # Icon setting is optional, continue if it fails
        
        # Set default font for the application
        default_font = ('Segoe UI', 9)  # Windows system font
        self.root.option_add('*Font', default_font)
        
        # Configure ttk style
        style = ttk.Style()
        style.configure('.', font=default_font)
        style.configure('TButton', font=default_font)
        style.configure('TLabel', font=default_font)
        style.configure('TEntry', font=default_font)
        style.configure('Treeview', font=default_font, rowheight=25)
        style.configure('Treeview.Heading', font=('Segoe UI', 9, 'bold'))
>>>>>>> e4200e3 (feat: Enhance UI with improved icon and file type filtering)
        
        # Common plugin directories for all plugin formats
        self.plugin_dirs = [
            # FL Studio specific
            os.path.join(os.environ.get('APPDATA', ''), 'FL Studio', 'Settings', 'Hardware'),
            os.path.join(os.environ.get('PROGRAMFILES', ''), 'Image-Line', 'FL Studio', 'Plugins'),
            
            # VST2/VST3 Directories
            os.path.join(os.environ.get('PROGRAMFILES', ''), 'VSTPlugins'),
            os.path.join(os.environ.get('PROGRAMFILES(x86)', ''), 'VSTPlugins'),
            os.path.join(os.environ.get('COMMONPROGRAMFILES', ''), 'VST2'),
            os.path.join(os.environ.get('COMMONPROGRAMFILES(x86)', ''), 'VST2'),
            os.path.join(os.environ.get('COMMONPROGRAMFILES', ''), 'VST3'),
            os.path.join(os.environ.get('COMMONPROGRAMFILES(x86)', ''), 'VST3'),
            
            # AAX Plugins (Pro Tools)
            os.path.join(os.environ.get('COMMONPROGRAMFILES', ''), 'Avid', 'Audio', 'Plug-Ins'),
            os.path.join(os.environ.get('COMMONPROGRAMFILES(x86)', ''), 'Avid', 'Audio', 'Plug-Ins'),
            os.path.join(os.environ.get('PROGRAMFILES', ''), 'Common Files', 'Avid', 'Audio', 'Plug-Ins'),
            
            # Common VST directories used by other DAWs
            os.path.join(os.environ.get('PROGRAMFILES', ''), 'Common Files', 'VST3'),
            os.path.join(os.environ.get('PROGRAMFILES(x86)', ''), 'Common Files', 'VST3'),
            os.path.join(os.environ.get('PROGRAMFILES', ''), 'Common Files', 'VST2'),
            os.path.join(os.environ.get('PROGRAMFILES(x86)', ''), 'Common Files', 'VST2'),
            
            # Steinberg VST directories
            os.path.join(os.environ.get('PROGRAMFILES', ''), 'Steinberg', 'VSTPlugins'),
            os.path.join(os.environ.get('PROGRAMFILES(x86)', ''), 'Steinberg', 'VSTPlugins'),
            
            # Custom user directories
            os.path.join(os.environ.get('USERPROFILE', ''), 'Documents', 'VST Plugins'),
            os.path.join(os.environ.get('USERPROFILE', ''), 'Documents', 'VST3'),
        ]
        
        # Plugin file extensions to look for
        self.plugin_extensions = [
            # VST
            '.dll',  # Windows VST
            '.vst',  # macOS VST
            '.vst3', # VST3
            
            # AAX
            '.aaxplugin',
            
            # Audio Units (macOS)
            '.component',
            
            # Other common plugin formats
            '.dpm',   # Pro Tools
            '.bundle', # macOS bundle
            '.vst',    # Linux VST
            '.so',     # Linux shared object
            
            # FL Studio specific
            '.fst',    # FL Studio preset
            '.fsc',    # FL Studio controller script
            
            # Additional formats
            '.dll.a',  # Sometimes used for plugin metadata
            '.vst.bak',# Backup files
            '.vst3.bak',
            '.aax.bak',
        ]
        
        self.plugins = []
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scan button
        scan_frame = ttk.Frame(main_frame)
        scan_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(
            scan_frame, 
            text="Scan for Plugins", 
            command=self.scan_plugins
        ).pack(side=tk.LEFT, padx=5)
        
<<<<<<< HEAD
        # Plugin list
        self.tree_frame = ttk.Frame(main_frame)
        self.tree_frame.pack(fill=tk.BOTH, expand=True, pady=10)
=======
        # Search and filter frame
        search_frame = ttk.Frame(main_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Left side - Search
        search_left = ttk.Frame(search_frame)
        search_left.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Label(search_left, text="Search:").pack(side=tk.LEFT, padx=(0, 5))
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_left, textvariable=self.search_var, width=30)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.search_entry.bind('<KeyRelease>', self.filter_plugins)
        
        # Right side - File Type Filter
        filter_frame = ttk.Frame(search_frame)
        filter_frame.pack(side=tk.RIGHT, fill=tk.X, padx=(10, 0))
        
        ttk.Label(filter_frame, text="File Type:").pack(side=tk.LEFT, padx=(0, 5))
        self.file_types = ['All Types'] + sorted(list(set(ext.upper() for ext in self.plugin_extensions)))
        self.file_type_var = tk.StringVar(value='All Types')
        self.file_type_menu = ttk.Combobox(
            filter_frame, 
            textvariable=self.file_type_var, 
            values=self.file_types,
            state='readonly',
            width=10
        )
        self.file_type_menu.pack(side=tk.LEFT, padx=(0, 5))
        self.file_type_menu.bind('<<ComboboxSelected>>', self.filter_plugins)
        
        # Clear filters button
        ttk.Button(
            search_frame, 
            text="Clear All", 
            command=self.clear_filters,
            style='TButton'
        ).pack(side=tk.LEFT, padx=(10, 0))
        
        # Plugin list
        self.tree_frame = ttk.Frame(main_frame)
        self.tree_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
>>>>>>> e4200e3 (feat: Enhance UI with improved icon and file type filtering)
        
        # Create scrollbar
        scrollbar = ttk.Scrollbar(self.tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create treeview
        self.tree = ttk.Treeview(
            self.tree_frame,
            columns=('Name', 'Type', 'Location'),
            show='headings',
<<<<<<< HEAD
            yscrollcommand=scrollbar.set
=======
            yscrollcommand=scrollbar.set,
            style='Treeview'
>>>>>>> e4200e3 (feat: Enhance UI with improved icon and file type filtering)
        )
        
        # Configure columns
        self.tree.heading('Name', text='Plugin Name', command=lambda: self.treeview_sort_column('Name', False))
        self.tree.heading('Type', text='Type', command=lambda: self.treeview_sort_column('Type', False))
        self.tree.heading('Location', text='Location', command=lambda: self.treeview_sort_column('Location', False))
        
        self.tree.column('Name', width=200)
        self.tree.column('Type', width=100)
        self.tree.column('Location', width=400)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.tree.yview)
        
<<<<<<< HEAD
=======
        # Store all items and types for filtering
        self.all_items = []
        self.plugin_types = set()
        
>>>>>>> e4200e3 (feat: Enhance UI with improved icon and file type filtering)
        # Add selection handler
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        
        # Action buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        self.remove_btn = ttk.Button(
            button_frame, 
            text="Remove Selected", 
            command=self.remove_selected,
            state=tk.DISABLED
        )
        self.remove_btn.pack(side=tk.LEFT, padx=5)
        
        self.refresh_btn = ttk.Button(
            button_frame,
            text="Refresh List",
            command=self.scan_plugins
        )
        self.refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(
            self.root, 
            textvariable=self.status_var,
            relief=tk.SUNKEN, 
<<<<<<< HEAD
            anchor=tk.W
=======
            anchor=tk.W,
            font=('Segoe UI', 8)
>>>>>>> e4200e3 (feat: Enhance UI with improved icon and file type filtering)
        )
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM, ipady=2)
        self.status_var.set("Ready. Click 'Scan for Plugins' to begin.")
    
<<<<<<< HEAD
=======
    def filter_plugins(self, event=None):
        """Filter the treeview based on search text and file type."""
        search_term = self.search_var.get().lower()
        file_type = self.file_type_var.get()
        
        # If both search and file type are empty, show all items
        if not search_term and file_type == "All Types":
            for item in self.all_items:
                self.tree.reattach(item, '', 'end')
            self.status_var.set(f"Showing all {len(self.all_items)} plugins")
            return
            
        visible_count = 0
        
        # First, hide all items
        for item in self.all_items:
            self.tree.detach(item)
            
        # Then show only matching items
        for item in self.all_items:
            values = self.tree.item(item, 'values')
            if not values:
                continue
                
            plugin_name = values[0].lower()
            plugin_type = values[1].lower()
            
            # Check if item matches file type (if specified) and search term (if specified)
            matches_type = (file_type == "All Types" or 
                          file_type.lower() == plugin_type.lower())
            matches_search = (not search_term or 
                            search_term in plugin_name)
            
            if matches_type and (not search_term or matches_search):
                self.tree.reattach(item, '', 'end')
                visible_count += 1
                
        self.status_var.set(f"Showing {visible_count} of {len(self.all_items)} plugins")
    
    def clear_filters(self):
        """Clear all filters and show all plugins."""
        self.search_var.set('')
        self.file_type_var.set('All Types')
        self.filter_plugins()
        self.search_entry.focus()
    
    def clear_search(self):
        """Clear the search box and update filters."""
        self.search_var.set('')
        self.filter_plugins()
        self.search_entry.focus()
    
>>>>>>> e4200e3 (feat: Enhance UI with improved icon and file type filtering)
    def treeview_sort_column(self, col, reverse):
        """Sort tree contents when a column header is clicked."""
        # Get all items from the tree
        items = [(self.tree.set(item, col), item) for item in self.tree.get_children('')]
        
        # Sort the items
        items.sort(reverse=reverse)
        
        # Rearrange items in sorted positions
        for index, (val, item) in enumerate(items):
            self.tree.move(item, '', index)
        
        # Reverse sort next time
        self.tree.heading(col, command=lambda: self.treeview_sort_column(col, not reverse))
    
    def scan_plugins(self):
        """Scan for FL Studio plugins in common directories."""
        self.plugins = []
<<<<<<< HEAD
        self.tree.delete(*self.tree.get_children())
=======
        self.all_items = []
        self.plugin_types = set()
        
        # Clear the tree
        for item in self.tree.get_children():
            self.tree.delete(item)
            
>>>>>>> e4200e3 (feat: Enhance UI with improved icon and file type filtering)
        self.status_var.set("Scanning for plugins...")
        self.root.update()
        
        found_any = False
        
<<<<<<< HEAD
        for plugin_dir in self.plugin_dirs:
            if os.path.exists(plugin_dir):
                found_any = True
                self.status_var.set(f"Scanning: {plugin_dir}")
                self.root.update()
                
                for root_dir, _, files in os.walk(plugin_dir):
                    for file in files:
                        # Check if the file has any of our target extensions (case-insensitive)
                        if any(file.lower().endswith(ext) for ext in self.plugin_extensions):
                            plugin_path = os.path.join(root_dir, file)
                            plugin_name = os.path.splitext(file)[0]
                            plugin_type = os.path.splitext(file)[1][1:].upper()
                            
                            # Skip certain system files
                            if any(skip in plugin_name.lower() for skip in ['unins', 'setup', 'install']):
                                continue
                                
                            self.plugins.append({
                                'name': plugin_name,
                                'type': plugin_type,
                                'path': plugin_path,
                                'directory': root_dir
                            })
                            
                            # Add to treeview
                            self.tree.insert('', 'end', values=(
                                plugin_name,
                                plugin_type,
                                root_dir
                            ))
=======
        for root_dir in self.plugin_dirs:
            if os.path.exists(root_dir):
                found_any = True
                for file in os.listdir(root_dir):
                    # Get the file extension in lowercase without the dot
                    file_ext = os.path.splitext(file)[1].lower()
                    
                    # Skip if not a plugin file
                    if not any(file.lower().endswith(ext) for ext in self.plugin_extensions):
                        continue
                        
                    plugin_path = os.path.join(root_dir, file)
                    plugin_name = os.path.splitext(file)[0]
                    plugin_type = file_ext.upper().lstrip('.')
                    
                    # Skip certain system files
                    if any(skip in plugin_name.lower() for skip in ['unins', 'setup', 'install']):
                        continue
                        
                    self.plugins.append({
                        'name': plugin_name,
                        'type': plugin_type,
                        'path': plugin_path,
                        'directory': root_dir
                    })
                    
                    # Add to treeview
                    item_id = self.tree.insert('', 'end', values=(
                        plugin_name,
                        plugin_type,
                        plugin_path
                    ))
                    self.all_items.append(item_id)  # Store the item ID
                    self.plugin_types.add(plugin_type)  # Track unique plugin types
        
        # Update the file type dropdown with found types
        if hasattr(self, 'file_type_menu'):
            current_type = self.file_type_var.get()
            file_types = ['All Types'] + sorted(list(self.plugin_types))
            self.file_type_menu['values'] = file_types
            
            # Reset to 'All Types' if the current selection is no longer valid
            if current_type not in file_types:
                self.file_type_var.set('All Types')
>>>>>>> e4200e3 (feat: Enhance UI with improved icon and file type filtering)
        
        if not found_any:
            self.status_var.set("No plugin directories found. You can manually add directories.")
            messagebox.showwarning("No Directories", "No standard FL Studio plugin directories were found. "
                                                  "You may need to manually add plugin directories.")
        else:
            self.status_var.set(f"Found {len(self.plugins)} plugins. Select one to remove.")
<<<<<<< HEAD
    
=======
            
        # Make sure all items are visible after scan
        self.filter_plugins()
>>>>>>> e4200e3 (feat: Enhance UI with improved icon and file type filtering)
    def on_select(self, event):
        """Handle selection of a plugin in the treeview."""
        selected = self.tree.selection()
        if selected:
            self.remove_btn.config(state=tk.NORMAL)
        else:
            self.remove_btn.config(state=tk.DISABLED)
    
    def remove_selected(self):
        """Remove the selected plugin(s)."""
        selected_items = self.tree.selection()
        if not selected_items:
            return
            
        # Get the plugin paths
        plugins_to_remove = []
        for item in selected_items:
            values = self.tree.item(item, 'values')
            plugin_name = values[0]
            plugin_path = ""
            
            # Find the full path in our plugins list
            for plugin in self.plugins:
                if plugin['name'] == plugin_name and plugin['directory'] == values[2]:
                    plugin_path = plugin['path']
                    break
            
            if plugin_path:
                plugins_to_remove.append((plugin_name, plugin_path, item))
        
        if not plugins_to_remove:
            messagebox.showerror("Error", "Could not find the selected plugins in the filesystem.")
            return
            
        # Confirm deletion
        plugin_list = "\n".join([name for name, _, _ in plugins_to_remove])
        if not messagebox.askyesno(
            "Confirm Removal",
            f"Are you sure you want to remove the following plugins?\n\n{plugin_list}"
        ):
            return
        
        # Remove the plugins
        success_count = 0
        for plugin_name, plugin_path, item in plugins_to_remove:
            try:
                if os.path.exists(plugin_path):
                    if os.path.isfile(plugin_path):
                        try:
                            # Try to change permissions first
                            os.chmod(plugin_path, 0o777)
                            # Then remove
                            os.remove(plugin_path)
                            
                            # Remove related files
                            base_path = os.path.splitext(plugin_path)[0]
                            for ext in ['.dll.a', '.json', '.ini', '.txt', '.dat']:
                                related_file = base_path + ext
                                if os.path.exists(related_file):
                                    try:
                                        os.chmod(related_file, 0o777)
                                        os.remove(related_file)
                                    except Exception as e:
                                        print(f"Could not remove {related_file}: {e}")
                        except PermissionError as pe:
                            error_msg = f"Failed to remove {plugin_name}: {str(pe)}\n\n" \
                                      f"Please make sure FL Studio and any other audio applications are closed " \
                                      f"and try again with administrator privileges."
                            messagebox.showerror("Permission Error", error_msg)
                            continue
                    # Remove from treeview
                    self.tree.delete(item)
                    success_count += 1
                else:
                    messagebox.showwarning("Warning", f"File not found: {plugin_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to remove {plugin_name}: {str(e)}")
        
        # Update status
        if success_count > 0:
            self.status_var.set(f"Successfully removed {success_count} plugin(s).")
            messagebox.showinfo("Success", f"Successfully removed {success_count} plugin(s).")
        else:
            self.status_var.set("No plugins were removed.")

def main():
    # Check and request admin rights if not already running as admin
    if not is_admin():
        try:
            run_as_admin()
            # If we get here, the user accepted the UAC prompt
            # but we need to exit this instance as the elevated one will start
            return
        except Exception as e:
            messagebox.showerror("Admin Rights Required", 
                              "This application requires administrator privileges to remove plugins.\n"
                              "Please run the application as administrator.")
            sys.exit(1)
    
    root = tk.Tk()
    app = FLPluginRemover(root)
    
    # Set window icon if available
    try:
        root.iconbitmap(default='fl_icon.ico')
    except:
        pass
    
    root.mainloop()

if __name__ == "__main__":
<<<<<<< HEAD
    main()
=======
    main()
>>>>>>> e4200e3 (feat: Enhance UI with improved icon and file type filtering)
