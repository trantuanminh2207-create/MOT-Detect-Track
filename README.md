Library: pip install ultralytics opencv-python torch torchvision --extra-index-url https://download.pytorch.org/whl/cu121z
Run: python detect_track.py
Video test and demo: https://drive.google.com/drive/folders/11EmGQstP6qkNjHaWbdS0_4oB3MURvH7M?usp=sharing

Mô tả về điều kiện test:
Vì code được viết để có thể sử dụng trên cả 2 nền tảng 
Cấu hình 1: gtx 1660 supper
            intel i5 11400f
Cấu hình 2: Intel i3 10005g1

Độ phân giải video test 1920x1080
phiên bản python: Python 3.11.9
Yolov11

NHẬN XÉT: 
Trường hợp 1 - Yolov11n:
Tốc độ xử lý đạt tốc độ nhanh nhất, tuy nhiên yêu cầu cần có video độ phân giải cao và config giá trị imgsz cao để có thể đạt độ chính xác. Tuy nhiên imgsz càng cao, tốc độ xử lý càng chậm, vì vậy loại bỏ trường hợp 1

Trường hợp 2 - Yolov11s:
Mô hình này có cải thiện về độ chính xác so với Trường hợp 1, không cần sử dụng độ phân giải quá cao cũng có thể đạt được độ chính xác tương đương với mô hình Yolov11n, tuy nhiên, tốc độ xử lý bị giảm đi 1 phần để đạt
được bằng việc sử dụng cấu hình có GPU nhiều nhân CUDA hơn.

Trường hợp 3 - Yolov11m:
Đây là mô hình tầm trung của Yolo, mang lại độ chính xác tốt hơn hẳn so với 2 mô hình trước đó, tuy nhiên, tốc độ xử lý lại chậm hơn rất nhiều, không phù hợp trong đề tài nghiên cứu cần có cả độ chính xác và đặc biệt là
tốc độ xử lý nhanh

--> kết luận: Em lựa chọn Yolov11s làm mô hình cho dự án này.
