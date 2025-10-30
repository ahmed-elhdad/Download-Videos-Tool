import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import yt_dlp
import os

# متغير لتخزين مسار الحفظ
save_path = ""

# دالة لاختيار مجلد الحفظ
def choose_folder():
    global save_path
    folder = filedialog.askdirectory()
    if folder:
        save_path = folder
        folder_label.config(text=f"📁 مجلد الحفظ: {folder}", fg="lightgreen")
    else:
        folder_label.config(text="⚠️ لم يتم اختيار مجلد بعد", fg="red")


# دالة التحميل
def download_video():
    url = url_entry.get().strip()
    site = site_var.get()

    if not url:
        messagebox.showwarning("تحذير", "من فضلك أدخل رابط الفيديو.")
        return
    if not save_path:
        messagebox.showwarning("تحذير", "من فضلك اختر مجلد الحفظ أولاً.")
        return

    status_label.config(text=f"📡 جاري التحميل من {site}...", fg="yellow")
    progress_bar['value'] = 0
    progress_label.config(text="جاري التحضير...")
    root.update_idletasks()

    def run_download():
        try:
            ydl_opts = {
                'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
                'progress_hooks': [hook_progress],
                'quiet': True
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            status_label.config(text="✅ تم التحميل بنجاح!", fg="lightgreen")
        except Exception as e:
            status_label.config(text="❌ فشل التحميل", fg="red")
            messagebox.showerror("خطأ", f"حدث خطأ أثناء التحميل:\n{e}")

    threading.Thread(target=run_download).start()


# دالة لتحديث حالة التحميل
def hook_progress(d):
    if d['status'] == 'downloading':
        total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
        downloaded_bytes = d.get('downloaded_bytes', 0)

        if total_bytes:
            percent = downloaded_bytes / total_bytes * 100
            mb_done = downloaded_bytes / (1024 * 1024)
            mb_total = total_bytes / (1024 * 1024)
            progress_bar['value'] = percent
            progress_label.config(
                text=f"تم تحميل {mb_done:.2f} / {mb_total:.2f} ميجابايت ({percent:.1f}%)"
            )
            root.update_idletasks()

    elif d['status'] == 'finished':
        progress_label.config(text="✅ التحميل اكتمل 100%")
        progress_bar['value'] = 100
        root.update_idletasks()


# واجهة المستخدم
root = tk.Tk()
root.title("🎬 أداة تحميل الفيديوهات - yt_dlp GUI")
root.geometry("500x420")
root.resizable(False, False)
root.config(bg="#222")

# العنوان
title_label = tk.Label(root, text="🎥 أداة تحميل الفيديوهات", font=("Arial", 16, "bold"), fg="gold", bg="#222")
title_label.pack(pady=15)

# قائمة المواقع
sites = [
    "YouTube",
    "Facebook",
    "Instagram",
    "TikTok",
    "Twitter (X)",
    "Vimeo",
]

site_var = tk.StringVar(value=sites[0])
site_label = tk.Label(root, text="اختر الموقع:", bg="#222", fg="white", font=("Arial", 12))
site_label.pack()
site_menu = ttk.Combobox(root, textvariable=site_var, values=sites, state="readonly", width=40)
site_menu.pack(pady=5)

# إدخال الرابط
url_label = tk.Label(root, text="أدخل رابط الفيديو:", bg="#222", fg="white", font=("Arial", 12))
url_label.pack(pady=5)
url_entry = tk.Entry(root, width=55)
url_entry.pack(pady=5)

# اختيار مجلد الحفظ
folder_btn = tk.Button(root, text="📁 اختر مجلد الحفظ", bg="#444", fg="white", font=("Arial", 11), command=choose_folder)
folder_btn.pack(pady=5)

folder_label = tk.Label(root, text="⚠️ لم يتم اختيار مجلد بعد", bg="#222", fg="red", font=("Arial", 10))
folder_label.pack(pady=5)

# زر التحميل
download_btn = tk.Button(root, text="⬇️ تحميل الفيديو", bg="gold", fg="black", font=("Arial", 12, "bold"), command=download_video)
download_btn.pack(pady=10)

# شريط التقدم
progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress_bar.pack(pady=10)

# نسبة التحميل
progress_label = tk.Label(root, text="في انتظار البدء...", bg="#222", fg="white", font=("Arial", 11))
progress_label.pack(pady=5)

# حالة التحميل
status_label = tk.Label(root, text="", bg="#222", fg="white", font=("Arial", 11, "bold"))
status_label.pack(pady=5)

# زر الخروج
exit_btn = tk.Button(root, text="❌ خروج", bg="#444", fg="white", font=("Arial", 10), command=root.destroy)
exit_btn.pack(pady=10)

root.mainloop()
