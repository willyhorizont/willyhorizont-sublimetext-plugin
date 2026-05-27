import sublime
import sublime_plugin

class SublimeTextSelectLinesCommand(sublime_plugin.TextCommand):
    def run(self, edit, forward=True):
        print("\n" * 100)

        settings = self.view.settings()
        # settings.set("target_prev_col", 0)
        # target_prev_col = settings.get("target_prev_col", 0)

        current_selections = list(self.view.sel())
        print(f"current_selections: {current_selections}")

        print(f"current_selections_text: \"{self.view.substr(current_selections[0])}\"")
        current_selections_length = len(current_selections[0])
        print(f"current_selections_length: {current_selections_length}")

        target_selection = current_selections[-1] if forward else current_selections[0]
        print(f"target_selection: {target_selection}")
        print(f"target_selection.a: {target_selection.a}")
        print(f"target_selection.b: {target_selection.b}")

        current_row, current_col = self.view.rowcol(target_selection.b)
        current_row += 1
        current_col += 1
        print(f"current_row: {current_row}")
        print(f"current_col: {current_col}")

        target_row = current_row + (1 if forward else -1)
        print(f"target_row: {target_row}")
        target_col = current_col
        settings.set("target_prev_col", target_col)
        print(f"target_col: {current_col}")

        target_line_region = self.view.line(self.view.text_point((target_row - 1), 0))
        print(f"target_line_region: {target_line_region}")
        print(f"target_line_region_text: \"{self.view.substr(target_line_region)}\"")
        target_line_length = target_line_region.size()
        print(f"target_line_length: {target_line_length}")

        if (target_col > target_line_length):
            target_col = target_line_length
        if (settings.get("target_prev_col", 0) > target_line_length):
            target_col = target_line_length
        else:
            target_col = settings.get("target_prev_col", 0)

        settings.set("target_prev_col", target_col)

        print(f"target_col: {target_col}")
        print(f"target_prev_col: {settings.get('target_prev_col', 0)}")
        # target_point = self.view.text_point((target_row - 1), (settings.get("target_prev_col", 0) + 1))
        # print(f"target_point: {target_point}")
        # new_region = sublime.Region(target_point, target_selection.a)
        # print(f"(({target_col} - 1) + (({target_line_length} + 1) - {target_col}))")
        new_region = sublime.Region((target_selection.b - (((target_col - 1) + ((target_line_length + 1) - target_col)) + 1)), target_selection.a)
        print(f"new_region: {new_region}")

        self.view.sel().clear()

        self.view.sel().add(new_region)

        # self.view.show(new_region)

        for region in current_selections:
            self.view.sel().add(region)

        return

        self.view.sel().clear()

        self.view.sel().add(new_region)

        # self.view.show(new_region)

        for region in current_selections:
            self.view.sel().add(region)

        return
        
        # Pengecekan batas: pastikan baris tujuan tidak minus atau melebihi total baris dokumen
        total_lines = (self.view.rowcol(self.view.size())[0] + 1)
        print(f"total_lines: {total_lines}")
        if ((target_row < 0) or (target_row > total_lines)):
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
