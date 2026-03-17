import os
import shutil
import sys
import subprocess
import threading
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import re

# 1. AUTO-INSTALL TOOLS
try:
    from bs4 import BeautifulSoup, Comment
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "beautifulsoup4"])
    from bs4 import BeautifulSoup, Comment

import chardet

# ==========================================
# 2. CONFIGURATION
# ==========================================
# We assume the DWT is in the standard location relative to the root
# The script will calculate the ../../ part automatically
DWT_FILENAME = "Dynamic Web Templates/Academic-Content-DWT.dwt"

# THE TARGET: Your existing English Portal
INDEX_FILENAME = "English/Mishnah Portal.htm"

NEW_PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <title>Structured Mishnah: {TRACTATE_ENG} {CHAPTER} | {TRACTATE_HEB}</title>
    <meta name="description" content="Visual literary analysis of the Mishnah text. {TRACTATE_ENG} Chapter {CHAPTER}." />
    <style type="text/css">
    /* Basic Page Reset */
    body { margin: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #fff; }
    
    /* Main Container */
    main.content-wrapper { max-width: 1000px; margin: 0 auto; padding: 20px; }

    /* The Hybrid Header (Gray Box) */
    .hybrid-header {
        background: #f8f9fa; border-left: 5px solid #5B6526; 
        padding: 20px; margin-bottom: 30px;
        display: flex; justify-content: space-between; align-items: center;
        direction: ltr;
    }
    .hybrid-header a { text-decoration: none; color: #5B6526; font-weight: bold; font-size: 0.9rem; }
    .hybrid-header a:hover { text-decoration: underline; }

    /* HEBREW CONTENT STYLES (Centered) */
    .hebrew-content { 
        direction: rtl; 
        text-align: center; 
        font-family: 'David', 'Frank Ruehl CLM', serif; 
        font-size: 1.25em; 
        line-height: 1.6;
    }
    
    /* ALIGNMENT FIXES */
    .hebrew-content table { width: 100% !important; margin: 0 auto; border-collapse: collapse; }
    .hebrew-content p { text-align: center; margin-bottom: 10px; }
    
    /* Perfect Header Alignment Trick */
    tr:has(.logo) td { width: 33.33% !important; vertical-align: top; }
    .logo { text-align: center !important; width: 100%; display: block; }
    .Mesechet { text-align: right !important; display: block; }
    .Perek { text-align: left !important; display: block; }

    /* Footer */
    footer { text-align: center; padding: 40px; color: #999; font-size: 12px; border-top: 1px solid #eee; margin-top: 50px; }

    @media (max-width: 768px) {
        .hybrid-header { flex-direction: column; text-align: center; }
        .hebrew-content { overflow-x: auto; }
    }
    </style>
</head>
<body>

    <main class="content-wrapper">
        <div class="hybrid-header">
            <div>
                <h1 style="color: #333; margin: 0; font-size: 1.5rem;">Structured Mishnah: {TRACTATE_ENG}</h1>
                <p style="margin: 5px 0 0; color: #666;">Chapter {CHAPTER} (Visual Analysis)</p>
            </div>
            <div style="text-align: right;">
                <h2 style="margin: 0; color: #5B6526;">{TRACTATE_HEB}</h2>
                <p style="margin: 5px 0 0;"><a href="{INDEX_PATH}">&larr; Back to Index</a></p>
            </div>
        </div>

        <div class="hebrew-content" lang="he" dir="rtl">
            {OLD_CONTENT}
        </div>
        
        </main>

    <footer>
        <p>&copy; 2025 Chaver.com | <a href="{INDEX_PATH}" style="color:#999;">Mishnah Index</a></p>
    </footer>

</body>
</html>
"""

HEBREW_MAP = {
    "Berakhot": "ברכות", "Brachot": "ברכות", "Peah": "פאה", "Demai": "דמאי", 
    "Kilayim": "כלאים", "Sheviit": "שביעית", "Shviit": "שביעית",
    "Terumot": "תרומות", "Trumot": "תרומות", "Maaserot": "מעשרות", "Maasrot": "מעשרות",
    "Maaser Sheni": "מעשר שני", "Challah": "חלה", "Hallah": "חלה",
    "Orlah": "ערלה", "Bikkurim": "ביכורים", "Bichorim": "ביכורים",
    "Shabbat": "שבת", "Eruvin": "ערובין", "Pesachim": "פסחים", "Shekalim": "שקלים", 
    "Yoma": "יומא", "Sukkah": "סוכה", "Beitzah": "ביצה", "Yom Tov (Betzah)": "ביצה", 
    "Betzeh": "ביצה", "Rosh Hashanah": "ראש השנה", "Taanit": "תענית", 
    "Megillah": "מגילה", "Moed Katan": "מועד קטן", "Chagigah": "חגיגה",
    "Yevamot": "יבמות", "Ketubot": "כתובות", "Nedarim": "נדרים", "Nazir": "נזיר", 
    "Sotah": "סוטה", "Gittin": "גיטין", "Kiddushin": "קידושין",
    "Bava Kamma": "בבא קמא", "Baba Kama": "בבא קמא",
    "Bava Metzia": "בבא מציעא", "Baba Metzia": "בבא מציעא",
    "Bava Batra": "בבא בתרא", "Baba Batra": "בבא בתרא",
    "Sanhedrin": "סנהדרין", "Makkot": "מכות", "Shevuot": "שבועות", 
    "Eduyot": "עדיות", "Avodah Zarah": "עבודה זרה", "Avot": "אבות", "Horayot": "הוריות",
    "Zevachim": "זבחים", "Menachot": "מנחות", "Chullin": "חולין", "Hullin": "חולין",
    "Bekhorot": "בכורות", "Arakhin": "ערכין", "Temurah": "תמורה", 
    "Keritot": "כריתות", "Kritot": "כריתות", "Meilah": "מעילה", 
    "Tamid": "תמיד", "Middot": "מידות", "Midot": "מידות", "Kinnim": "קנים",
    "Kelim": "כלים", "Oholot": "אהלות", "Negaim": "נגעים", "Parah": "פרה", 
    "Tohorot": "טהרות", "Mikvaot": "מקואות", "Niddah": "נידה", "Nidah": "נידה",
    "Makhshirin": "מכשירים", "Zavim": "זבים", "Tevul Yom": "טבול יום", 
    "Yadayim": "ידים", "Uktzim": "עוקצים"
}

def get_names(filename):
    clean = filename.replace(".htm", "").replace(".html", "")
    eng_name = "Mishnah"
    heb_name = "משנה"
    chapter = "?"
    if "Perek" in clean:
        try:
            parts = clean.split("Perek")
            raw_name = parts[0].replace("Masechet", "").strip("_ ").strip()
            chapter = parts[1].strip()
            eng_name = raw_name.replace("_", " ")
            if eng_name in HEBREW_MAP:
                heb_name = "מסכת " + HEBREW_MAP[eng_name]
            elif eng_name.replace("Mashechet ", "") in HEBREW_MAP:
                 heb_name = "מסכת " + HEBREW_MAP[eng_name.replace("Mashechet ", "")]
            else:
                heb_name = "מסכת " + eng_name
        except:
            pass
    return eng_name, heb_name, chapter

class ModernizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mishnah Page Updater (Links to Portal)")
        self.root.geometry("700x600")
        
        tk.Label(root, text="Mishnah Page Updater", font=("Arial", 16, "bold"), fg="#5B6526").pack(pady=10)
        tk.Label(root, text="Updates 524 pages -> Links to 'English/Mishnah Portal.htm'", font=("Arial", 10)).pack(pady=5)

        self.folder_path = tk.StringVar()
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="1. Select Folder", command=self.select_folder, width=20, height=2, bg="#ddd").pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="2. RUN UPDATE", command=self.start_thread, width=20, height=2, bg="#5B6526", fg="white").pack(side=tk.LEFT, padx=10)

        tk.Label(root, textvariable=self.folder_path, fg="blue").pack()
        self.log_area = scrolledtext.ScrolledText(root, width=80, height=20)
        self.log_area.pack(pady=10, padx=10)
        
    def log(self, message):
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)
            self.log(f"Selected: {folder}")

    def start_thread(self):
        if not self.folder_path.get():
            messagebox.showerror("Error", "Please select a folder first!")
            return
        threading.Thread(target=self.run_process, daemon=True).start()

    def run_process(self):
        root_dir = self.folder_path.get()
        backup_dir = os.path.join(root_dir, "BACKUP_PAGES_ONLY")
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
            self.log(f"Backup folder: {backup_dir}")

        count = 0
        IGNORE_FOLDERS = {'_vti_cnf', '_vti_pvt', '_vti_log', '_private', 'backup', 'BACKUP', 'backup_originals'}

        self.log("--- STARTING UPDATE ---")

        for root, dirs, files in os.walk(root_dir):
            dirs[:] = [d for d in dirs if d not in IGNORE_FOLDERS and not d.lower().startswith('backup') and not d.startswith('_')]
            
            for filename in files:
                if "Index" in filename or "Portal" in filename: continue 

                if filename.lower().endswith((".htm", ".html")) and "Perek" in filename:
                    
                    file_path = os.path.join(root, filename)
                    eng_name, heb_name, chapter = get_names(filename)

                    # --- CALCULATE SMART LINKS ---
                    # Calculate path from current file back to the root "Mishnah-New" folder
                    rel_path_to_root = os.path.relpath(root_dir, root) 
                    
                    # Construct link to the Portal
                    # e.g. "../../../English/Mishnah Portal.htm"
                    index_link = os.path.join(rel_path_to_root, INDEX_FILENAME).replace("\\", "/")
                    
                    # Construct link to the DWT
                    dwt_link = os.path.join(rel_path_to_root, DWT_FILENAME).replace("\\", "/")
                    # -----------------------------

                    # Backup
                    backup_path = os.path.join(backup_dir, f"{filename}.bak")
                    if not os.path.exists(backup_path):
                        shutil.copy2(file_path, backup_path)

                    # READ & DETECT
                    try:
                        with open(file_path, 'rb') as f:
                            raw_data = f.read()
                        result = chardet.detect(raw_data)
                        encoding = result['encoding']
                        if not encoding or result['confidence'] < 0.6: encoding = 'windows-1255'
                        if encoding == 'Windows-1252': encoding = 'windows-1255'
                        soup = BeautifulSoup(raw_data, 'html.parser', from_encoding=encoding)
                    except Exception as e:
                        self.log(f"Error reading {filename}: {e}")
                        continue

                    content_html = ""
                    
                    # EXTRACT
                    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
                    for c in comments:
                        if "#BeginEditable" in c:
                            region_name = c.replace("#BeginEditable", "").strip().strip('"')
                            if region_name in ["start", "Body", "Content", "writehere", "main"]:
                                parent = c.parent
                                if parent:
                                    try:
                                        content_html = parent.decode_contents()
                                        content_html = re.sub(r'', '', content_html)
                                        content_html = re.sub(r'', '', content_html)
                                        break
                                    except: pass

                    if not content_html:
                        section1 = soup.find('div', class_='Section1')
                        if section1:
                            for h in section1.find_all(['h1', 'h2', 'h3']): h.decompose()
                            content_html = str(section1)

                    if not content_html and soup.find('table'):
                        tables = soup.find_all('table')
                        content_html = "".join([str(t) for t in tables])

                    # SAVE
                    if content_html:
                        new_page = NEW_PAGE_TEMPLATE.replace("{DWT_PATH}", dwt_link)
                        new_page = new_page.replace("{INDEX_PATH}", index_link)
                        new_page = new_page.replace("{TRACTATE_ENG}", eng_name)
                        new_page = new_page.replace("{TRACTATE_HEB}", heb_name)
                        new_page = new_page.replace("{CHAPTER}", chapter)
                        new_page = new_page.replace("{OLD_CONTENT}", content_html)

                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_page)
                        
                        self.log(f" Updated -> {filename}")
                        count += 1

        self.log(f"\nDONE! Updated {count} pages.")
        messagebox.showinfo("Success", "All pages modernized.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernizerApp(root)
    root.mainloop()