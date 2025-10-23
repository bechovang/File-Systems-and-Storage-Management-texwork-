# APA7_OSG — LaTeX Template (APA 7th)

## Overview
This repository contains a LaTeX template configured for APA 7th edition formatting. It uses `biblatex` with `biber` for bibliography management and includes example figures and a sample bibliography.

### Features
- APA 7th edition structure and formatting
- `biblatex` + `biber` workflow
- Example figures (`sampleFig.png`, `placeholder.png`)
- Ready-to-edit main file: `main.tex`
- Windows build script: `build_and_run.bat`

## Requirements
- TeX distribution: MiKTeX (Windows) or TeX Live
- TeX editor: TeXworks (bundled with MiKTeX, or install separately)
- Biber (usually included; ensure it’s installed and up to date)

## Install TeXworks (Windows)
You have two easy options:
1) Install MiKTeX (recommended on Windows). It includes TeXworks by default.
   - Download MiKTeX: `https://miktex.org/download`
   - During install, allow package-on-the-fly installation.
2) Install TeX Live and TeXworks separately if preferred.
   - TeX Live: `https://tug.org/texlive/`
   - TeXworks: `https://www.tug.org/texworks/`

After installation, update packages:
- MiKTeX Console → Updates → Check for updates → Install all
- Ensure `biber` is installed and on PATH (MiKTeX/TeX Live typically handles this)

## Build in TeXworks
1. Open `main.tex` in TeXworks.
2. In the typeset dropdown, select `pdfLaTeX` (or `XeLaTeX` if you need full Unicode/font support).
3. Build sequence for bibliography:
   - Run LaTeX: pdfLaTeX
   - Run Biber: Tools → Biber
   - Run LaTeX twice more: pdfLaTeX, pdfLaTeX
4. Output should be `main.pdf` in the project root.

Tip: If TeXworks doesn’t show “Biber” in Tools, ensure `biber` is installed, then restart TeXworks.

## Build via Command Line (Windows)
- Double-click `build_and_run.bat` or run in PowerShell:
  ```powershell
  ./build_and_run.bat
  ```
This script runs the typical LaTeX → Biber → LaTeX → LaTeX sequence and opens the resulting PDF.

## LaTeX metrics tool
`tex_metrics.py` đếm số chữ (tổng và theo chương/mục), số lần trích dẫn và so sánh khóa trích dẫn với `bibliography.bib`, kèm bộ đếm môi trường (figure/table/equation).

### Sử dụng (Windows PowerShell)
```powershell
python .\tex_metrics.py --tex .\main.tex --bib .\bibliography.bib --output text
```

Tùy chọn:
- `--output json` để xuất JSON
- `--no-follow-includes` để không theo `\input{}`/`\include{}`
- `--encoding utf-8` đặt encoding (mặc định `utf-8`)

Ví dụ:
```powershell
# Báo cáo dạng text
python .\tex_metrics.py --tex .\main.tex --bib .\bibliography.bib

# Xuất JSON
python .\tex_metrics.py --tex .\main.tex --bib .\bibliography.bib --output json > metrics.json
```

## Project Files
- `main.tex`: Main document
- `bibliography.bib`: References database
- `sampleFig.png`, `placeholder.png`: Example figures
- `build_and_run.bat`: Windows build helper

## Troubleshooting
- Missing references or citation warnings: run Biber, then run LaTeX twice
- “biber not found”: update MiKTeX/TeX Live; ensure `biber` is installed
- Package missing: allow MiKTeX to install on-the-fly or update packages

---

# APA7_OSG — Mẫu LaTeX (APA 7)

## Giới thiệu
Kho này cung cấp mẫu LaTeX cấu hình theo chuẩn APA phiên bản 7. Mẫu sử dụng `biblatex` với `biber` để quản lý tài liệu tham khảo, kèm ví dụ hình ảnh và thư mục mẫu.

### Tính năng
- Cấu trúc và định dạng theo APA 7
- Quy trình `biblatex` + `biber`
- Hình minh họa mẫu (`sampleFig.png`, `placeholder.png`)
- Tệp chính sẵn sàng chỉnh sửa: `main.tex`
- Script build cho Windows: `build_and_run.bat`

## Yêu cầu
- Bộ TeX: MiKTeX (Windows) hoặc TeX Live
- Trình soạn thảo TeX: TeXworks (đi kèm MiKTeX, hoặc cài riêng)
- Biber (thường có sẵn; đảm bảo đã cài và cập nhật)

## Cài đặt TeXworks (Windows)
Có hai cách đơn giản:
1) Cài MiKTeX (khuyến nghị trên Windows). MiKTeX bao gồm TeXworks.
   - Tải MiKTeX: `https://miktex.org/download`
   - Trong quá trình cài, bật chế độ tự cài gói khi cần.
2) Cài TeX Live và TeXworks riêng nếu muốn.
   - TeX Live: `https://tug.org/texlive/`
   - TeXworks: `https://www.tug.org/texworks/`

Sau khi cài, hãy cập nhật gói:
- MiKTeX Console → Updates → Check for updates → Install all
- Đảm bảo `biber` đã cài và có trong PATH (MiKTeX/TeX Live thường cấu hình sẵn)

## Biên dịch trong TeXworks
1. Mở `main.tex` bằng TeXworks.
2. Ở hộp chọn trình biên dịch, chọn `pdfLaTeX` (hoặc `XeLaTeX` nếu cần hỗ trợ Unicode/phông chữ).
3. Thứ tự biên dịch khi có tài liệu tham khảo:
   - Chạy LaTeX: pdfLaTeX
   - Chạy Biber: Tools → Biber
   - Chạy LaTeX hai lần nữa: pdfLaTeX, pdfLaTeX
4. Kết quả là `main.pdf` trong thư mục gốc của dự án.

Gợi ý: Nếu không thấy “Biber” trong Tools, hãy đảm bảo `biber` đã được cài, rồi khởi động lại TeXworks.

## Biên dịch qua dòng lệnh (Windows)
- Nhấp đúp `build_and_run.bat` hoặc chạy trong PowerShell:
  ```powershell
  ./build_and_run.bat
  ```
Script này chạy chuỗi LaTeX → Biber → LaTeX → LaTeX và mở tệp PDF.

## Công cụ thống kê LaTeX
`tex_metrics.py` đếm số chữ (tổng và theo chương/mục), số trích dẫn và so sánh khóa trích dẫn với `bibliography.bib`, cùng bộ đếm môi trường (figure/table/equation).

### Cách dùng (Windows PowerShell)
```powershell
python .\tex_metrics.py --tex .\main.tex --bib .\bibliography.bib --output text
```

Tùy chọn:
- `--output json` để xuất JSON
- `--no-follow-includes` để không theo `\input{}`/`\include{}`
- `--encoding utf-8` đặt encoding (mặc định `utf-8`)

Ví dụ:
```powershell
# Báo cáo dạng text
python .\tex_metrics.py --tex .\main.tex --bib .\bibliography.bib

# Xuất JSON
python .\tex_metrics.py --tex .\main.tex --bib .\bibliography.bib --output json > metrics.json
```

## Tệp trong dự án
- `main.tex`: Tài liệu chính
- `bibliography.bib`: CSDL tài liệu tham khảo
- `sampleFig.png`, `placeholder.png`: Hình minh họa
- `build_and_run.bat`: Script build cho Windows

## Xử lý sự cố
- Thiếu trích dẫn/tài liệu tham khảo: chạy Biber, sau đó chạy LaTeX hai lần
- “Không tìm thấy biber”: cập nhật MiKTeX/TeX Live; đảm bảo đã cài `biber`
- Thiếu gói: cho phép MiKTeX tự cài gói hoặc cập nhật gói
