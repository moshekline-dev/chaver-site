import os
import shutil
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox

class RestoreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("EMERGENCY RESTORE TOOL")
        self.root.geometry("600x500")
        
        tk.Label(root, text="Emergency Restore", font=("Arial", 16, "bold"), fg="red").pack(pady=10)
        tk.Label(root, text="This will undo changes and restore files from the backup.", font=("Arial", 10)).pack(pady=5)

        self.folder_path = tk.StringVar()
        
        tk.Button(root, text="1. Select 'Mishnah-New' Folder", command=self.select_folder, width=30, height=2, bg="#ddd").pack(pady=10)
        tk.Button(root, text="2. RESTORE ORIGINAL FILES", command=self.run_restore, width=30, height=2, bg="red", fg="white").pack(pady=10)

        self.log_area = scrolledtext.ScrolledText(root, width=70, height=20)
        self.log_area.pack(pady=10, padx=10)

    def log(self, message):
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)
            self.log(f"Target: {folder}")

    def run_restore(self):
        root_dir = self.folder_path.get()
        if not root_dir:
            messagebox.showerror("Error", "Select folder first.")
            return

        # Check for backup folders
        backup_dirs = ["BACKUP_ORIGINALS", "BACKUP_ORIGINALS_V2"]
        found_backup = None
        for b in backup_dirs:
            path = os.path.join(root_dir, b)
            if os.path.exists(path):
                found_backup = path
                break
        
        if not found_backup:
            messagebox.showerror("Error", "Could not find BACKUP_ORIGINALS folder!")
            return

        self.log(f"Found Backup at: {found_backup}")
        self.log("Starting Restoration...")

        restored_count = 0
        
        # Walk through the DESTROYED/BROKEN site structure
        for current_root, dirs, files in os.walk(root_dir):
            # Don't look inside the backup folder itself
            if "BACKUP" in current_root:
                continue

            for filename in files:
                if filename.endswith(".htm") or filename.endswith(".html"):
                    # This is a broken file in a folder (e.g. Seder Zeraim/...)
                    # Let's look for its healthy twin in the backup folder
                    
                    original_file_path = os.path.join(current_root, filename)
                    
                    # The backup file is likely named "filename.htm.bak"
                    backup_filename = filename + ".bak"
                    backup_source = os.path.join(found_backup, backup_filename)

                    if os.path.exists(backup_source):
                        # RESTORE: Copy backup OVER the broken file
                        try:
                            shutil.copy2(backup_source, original_file_path)
                            self.log(f"Restored: {filename}")
                            restored_count += 1
                        except Exception as e:
                            self.log(f"Error restoring {filename}: {e}")
                    else:
                        # Try without .bak extension just in case
                        backup_source_alt = os.path.join(found_backup, filename)
                        if os.path.exists(backup_source_alt):
                            shutil.copy2(backup_source_alt, original_file_path)
                            self.log(f"Restored: {filename}")
                            restored_count += 1

        self.log(f"--- COMPLETE ---")
        self.log(f"Restored {restored_count} files to their original folders.")
        messagebox.showinfo("Done", "Restoration Complete. Your site should be back to normal.")

if __name__ == "__main__":
    root = tk.Tk()
    app = RestoreApp(root)
    root.mainloop()