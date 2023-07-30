import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import json
import os
import pandas as pd
from reportlab.lib.pagesizes import portrait
from reportlab.pdfgen import canvas
from tkinter import PhotoImage
from PIL import Image, ImageTk

# Nama file JSON yang akan digunakan
FILENAME = "data.json"

def load_data():
    try:
        with open(FILENAME, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []
    return data

def save_data(data):
    with open(FILENAME, 'w') as file:
        json.dump(data, file, indent=4)

def create_record():
    global data, name_entry, kerusakan_entry, status_entry, kwitansi_entry
    record = {}
    record['nama'] = name_entry.get()
    record['kerusakan'] = kerusakan_entry.get()
    record['status'] = status_entry.get()
    record['no_kwitansi'] = kwitansi_entry.get()
    data.append(record)
    save_data(data)
    messagebox.showinfo("Info", "Data telah ditambahkan.")

def read_records():
    global data
    records_text.delete(1.0, tk.END)
    for idx, record in enumerate(data, 1):
        if 'no_kwitansi' in record:
            records_text.insert(tk.END, f"No Kwitansi: {record['no_kwitansi']}\n")
        if 'nama' in record:
            records_text.insert(tk.END, f"Nama: {record['nama']}\n")
        if 'kerusakan' in record:
            records_text.insert(tk.END, f"Kerusakan: {record['kerusakan']}\n")
        if 'status' in record:
            records_text.insert(tk.END, f"Status: {record['status']}\n\n")

def update_record():
    global data, name_entry, kerusakan_entry, status_entry, kwitansi_entry
    kwitansi_no = kwitansi_entry.get()
    for record in data:
        if record.get('no_kwitansi') == kwitansi_no:
            record['nama'] = name_entry.get()
            record['kerusakan'] = kerusakan_entry.get()
            record['status'] = status_entry.get()
            save_data(data)
            messagebox.showinfo("Info", "Data telah diupdate.")
            break
    else:
        messagebox.showerror("Error", "No Kwitansi tidak ditemukan.")

def delete_record():
    global data, kwitansi_entry
    kwitansi_no = kwitansi_entry.get()
    for record in data:
        if record.get('no_kwitansi') == kwitansi_no:
            data.remove(record)
            save_data(data)
            messagebox.showinfo("Info", "Data telah dihapus.")
            break
    else:
        messagebox.showerror("Error", "No Kwitansi tidak ditemukan.")

def delete_all_data():
    global data
    if messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus seluruh data?"):
        data = []
        save_data(data)
        read_records()  # Update tampilan setelah menghapus data
        messagebox.showinfo("Info", "Seluruh data telah dihapus.")

def clear_entries():
    global name_entry, kerusakan_entry, status_entry, kwitansi_entry
    name_entry.delete(0, tk.END)
    kerusakan_entry.delete(0, tk.END)
    status_entry.delete(0, tk.END)
    kwitansi_entry.delete(0, tk.END)

def download_excel():
    global data
    df = pd.DataFrame(data)
    try:
        df.to_excel("data.xlsx", index=False)
        messagebox.showinfo("Info", "Data berhasil diunduh sebagai file Excel (data.xlsx).")
    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan saat menyimpan data sebagai Excel: {str(e)}")

def print_kwitansi():
    global data
    kwitansi_no = kwitansi_entry.get()
    for konter in data:
        if 'nama_konter' in konter:
            konter_nama = konter['nama_konter']
            konter_alamat = konter['alamat_konter']
            konter_telepon = konter['telepon_konter']
            break
    else:
        konter_nama = "Nama Konter"
        konter_alamat = "Alamat Konter"
        konter_telepon = "Telepon Konter"

    for record in data:
        if record.get('no_kwitansi') == kwitansi_no:
            pdf_filename = f"kwitansi_{kwitansi_no}.pdf"
            c = canvas.Canvas(pdf_filename, pagesize=portrait((3 * 72, 5 * 72)))
            c.setFont("Times-Roman", 11)

            # Ukuran halaman kwitansi
            page_width, page_height = portrait((3 * 72, 5 * 72))

            # Bagian kop dengan informasi konter
            kop_height = 1 + 7  # Tinggi bagian kop
            c.setFont("Courier-Bold", 12)
            # Membuat bagian kop menjadi rata tengah
            c.drawCentredString(page_width / 2, page_height - 0.5 * 82, konter_nama)
            c.setFont("Courier", 9)
            c.drawCentredString(page_width / 2, page_height - 1.4 * 39, konter_alamat)
            c.drawCentredString(page_width / 2, page_height - 2 * 35 ,konter_telepon)

            # Garis pemisah bagian kop dan data
            c.line(0.5 * 30, page_height - kop_height - 10 * 7, page_width - 0.5 * 30, page_height - kop_height - 10 * 7)


            # Bagian data kwitansi
            c.setFont("Courier", 10)
            c.drawString(0.5 * 72, page_height - kop_height - 2 * 60, f"No Kwitansi: {kwitansi_no}")
            c.drawString(0.5 * 72, page_height - kop_height - 2.5 * 60, f"Nama: {record.get('nama')}")
            c.drawString(0.5 * 72, page_height - kop_height - 3 * 60, f"Kerusakan: {record.get('kerusakan')}")
            c.drawString(0.5 * 72, page_height - kop_height - 3.5 * 60, f"Status (%) : {record.get('status')}")

            # Bagian data kwitansi
            c.setFont("Courier", 10)
            text_1 = "Terima Kasih"
            text_2 = "Atas Kepercayaan Anda"
            line_height = 55

            c.drawCentredString(page_width / 2, page_height - kop_height - 5 * line_height, text_1)
            c.drawCentredString(page_width / 2, page_height - kop_height - 5.6 * line_height, text_2)

            
            c.save()
            messagebox.showinfo("Info", f"Kwitansi dengan No Kwitansi {kwitansi_no} telah disimpan sebagai {pdf_filename}.")
            break
    else:
        messagebox.showerror("Error", "No Kwitansi tidak ditemukan.")

def input_konter():
    global data
    konter_nama = simpledialog.askstring("Input Konter", "Masukkan Nama Konter:")
    konter_alamat = simpledialog.askstring("Input Konter", "Masukkan Alamat Konter:")
    konter_telepon = simpledialog.askstring("Input Konter", "Masukkan Nomor Telepon Konter:")

    if konter_nama and konter_alamat and konter_telepon:
        konter_data = {
            'nama_konter': konter_nama,
            'alamat_konter': konter_alamat,
            'telepon_konter': konter_telepon
        }
        data.append(konter_data)
        save_data(data)
        messagebox.showinfo("Info", "Data konter telah ditambahkan.")

def main():
    global data, name_entry, kerusakan_entry, status_entry, records_text, kwitansi_entry
    data = load_data()

    root = tk.Tk()
    root.title("E-Konter Service")

    #set icon
    icon_path = "C:\\Users\\faisal hanafi\\Downloads\\kasir.png"
    if os.path.exists(icon_path):
        icon_img = Image.open(icon_path)
        icon_photo = ImageTk.PhotoImage(icon_img)
        root.iconphoto(True, icon_photo)


    # Label dan Entry untuk input data
    kwitansi_label = tk.Label(root, text="No Kwitansi:")
    kwitansi_label.grid(row=0, column=0, padx=10, pady=5)
    kwitansi_entry = tk.Entry(root)
    kwitansi_entry.grid(row=0, column=1, padx=10, pady=5)

    name_label = tk.Label(root, text="Nama:")
    name_label.grid(row=1, column=0, padx=10, pady=5)
    name_entry = tk.Entry(root)
    name_entry.grid(row=1, column=1, padx=10, pady=5)

    kerusakan_label = tk.Label(root, text="Kerusakan:")
    kerusakan_label.grid(row=2, column=0, padx=10, pady=5)
    kerusakan_entry = tk.Entry(root)
    kerusakan_entry.grid(row=2, column=1, padx=10, pady=5)

    status_label = tk.Label(root, text="Status Perbaikan:")
    status_label.grid(row=3, column=0, padx=10, pady=5)
    status_entry = tk.Entry(root)
    status_entry.grid(row=3, column=1, padx=10, pady=5)

    # Tombol untuk melakukan CRUD
    create_btn = tk.Button(root, text="Tambah Data", command=create_record)
    create_btn.grid(row=4, column=0, padx=10, pady=5)

    read_btn = tk.Button(root, text="Tampilkan Data", command=read_records)
    read_btn.grid(row=4, column=1, padx=10, pady=5)

    update_btn = tk.Button(root, text="Update Data", command=update_record)
    update_btn.grid(row=5, column=0, padx=10, pady=5)

    delete_btn = tk.Button(root, text="Hapus Data", command=delete_record)
    delete_btn.grid(row=5, column=1, padx=10, pady=5)

    clear_btn = tk.Button(root, text="Bersihkan", command=clear_entries)
    clear_btn.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

    # Text widget untuk menampilkan data
    records_text = tk.Text(root, width=40, height=10)
    records_text.grid(row=7, column=0, columnspan=2, padx=10, pady=5)

    # Tombol untuk menghapus seluruh data
    delete_all_btn = tk.Button(root, text="Hapus Seluruh Data", command=delete_all_data)
    delete_all_btn.grid(row=8, column=1, padx=10, pady=5)

    # Tombol untuk mengunduh data sebagai Excel
    download_excel_btn = tk.Button(root, text="Download Excel", command=download_excel)
    download_excel_btn.grid(row=8, column=0, padx=10, pady=5)

    # Tombol untuk mencetak kwitansi
    print_kwitansi_btn = tk.Button(root, text="Print Kwitansi", command=print_kwitansi)
    print_kwitansi_btn.grid(row=9, column=1, padx=10, pady=5)

    # Tombol untuk input konter
    input_konter_btn = tk.Button(root, text="Input Konter", command=input_konter)
    input_konter_btn.grid(row=9, column=0, padx=10, pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
