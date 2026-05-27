import sublime
import sublime_plugin

class SublimeTextSelectLinesCommand(sublime_plugin.TextCommand):
    def run(self, edit, forward=True):
        # 1. Ambil semua kursor (selections) yang aktif saat ini
        current_selections = list(self.view.sel())
        print(current_selections)
        
        # 2. Tentukan kursor mana yang paling ujung untuk dijadikan acuan baris baru
        # Jika forward (ke bawah), acuannya kursor paling terakhir. Jika ke atas, kursor paling pertama.
        target_selection = current_selections[-1] if forward else current_selections[0]
        
        # 3. Ambil posisi baris saat ini (menggunakan text point)
        current_row, current_col = self.view.rowcol(target_selection.b)
        print(f"current_row: {current_row}")
        print(f"current_col: {current_col}")
        
        # 4. Hitung target baris berikutnya
        target_row = current_row + (1 if forward else -1)
        
        # Pengecekan batas: pastikan baris tujuan tidak minus atau melebihi total baris dokumen
        total_lines = self.view.rowcol(self.view.size())[0]
        if target_row < 0 or target_row > total_lines:
            return # Keluar jika sudah mentok di paling atas atau paling bawah
            
        # 5. Konversi kembali koordinat (row, col) target menjadi text point posisi kursor baru
        target_point = self.view.text_point(target_row, current_col)
        
        # Pengecekan layout: Jika baris tujuan lebih pendek dari kolom kursor saat ini,
        # kursor baru otomatis ditaruh di akhir baris tersebut (ujung kanan baris).
        line_region = self.view.line(target_point)
        if target_point > line_region.b:
            target_point = line_region.b
            
        # 6. Buat objek Region baru (kursor baru) dan tambahkan ke layar
        new_cursor = sublime.Region(target_point, target_point)
        self.view.sel().add(new_cursor)
        
        # 7. Otomatis gulir layar (scroll) agar kursor baru tetap terlihat
        self.view.show(new_cursor, False)
        
        # # Log untuk debugging di konsol (Ctrl + `)
        # direction = "bawah" if forward else "atas"
        # print(f"[Custom Plugin] Kursor berhasil ditambahkan ke {direction} di baris ke-{target_row + 1}")
