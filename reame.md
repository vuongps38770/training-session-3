.
├── best.pt                  # Mô hình YOLOv8 đã huấn luyện (weights)
├── change-label-names.py    # Script đổi tên nhãn (label) sau khi huấn luyện
├── datasets/                # Chứa dữ liệu huấn luyện/validation
├── generate.ipynb           # Notebook sinh dữ liệu hoặc xử lý nào đó trước huấn luyện
├── image.png                # Ảnh test/dùng cho trực quan
├── img.jpg                  # Ảnh test khác
├── predict.py               # Script dùng để dự đoán với ảnh đầu vào
├── reame.md                 # (Lỗi chính tả) Đáng ra là README.md
├── requirements.txt         # Các thư viện cần cài đặt
├── train.ipynb              # Notebook huấn luyện mô hình YOLOv8
├── visual.py                # Script vẽ/hiển thị kết quả dự đoán

Cài đặt:
pip install -r requirements.txt

Cách sử dụng:
# Dự đoán trên ảnh:
python predict.py --source image.jpg --weights best.pt

# Dự đoán trên webcam:
python predict.py --source 0 --weights best.pt

# Huấn luyện:
- Chạy file train.ipynb trên Jupyter Notebook


 ___      ___ ___  ___  ________  ________   ________          ________  ________     
|\  \    /  /|\  \|\  \|\   __  \|\   ___  \|\   ____\        |\   ___ \|\_____  \    
\ \  \  /  / | \  \\\  \ \  \|\  \ \  \\ \  \ \  \___|        \ \  \_|\ \\|___/  /|   
 \ \  \/  / / \ \  \\\  \ \  \\\  \ \  \\ \  \ \  \  ___       \ \  \ \\ \   /  / /   
  \ \    / /   \ \  \\\  \ \  \\\  \ \  \\ \  \ \  \|\  \       \ \  \_\\ \ /  /_/__  
   \ \__/ /     \ \_______\ \_______\ \__\\ \__\ \_______\       \ \_______\\________\
    \|__|/       \|_______|\|_______|\|__| \|__|\|_______|        \|_______|\|_______|
