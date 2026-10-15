import csv
import platform
import time
import cv2
import torch
from ultralytics import YOLO

# tự động phát hiện phần cứng sử dụng
if torch.cuda.is_available():
    device_type = 0
  #lấy tên GPU của hệ thống
    device_name = f"GPU: {torch.cuda.get_device_name(0)}"
    use_half = True  # Ép GPU dùng FP16 để tăng tốc
else:
    device_type = "cpu"
    # Lấy tên CPU của hệ thống
    device_name = f"CPU: {platform.processor() or 'Standard CPU'}"
    use_half = False

print(f"---- Hệ thống đang chạy trên: {device_name}")

# Khởi động mô hình YOLO
model = YOLO("yolo11s.pt")

input_video_path = "test_video.mp4"
tracker_type = "bytetrack.yaml"  # Đổi thành 'botsort.yaml' ở lượt chạy 2
output_video_path = f"output_{tracker_type.split('.')[0]}.mp4"
log_csv_path = f"tracking_log_{tracker_type.split('.')[0]}.csv"

cap = cv2.VideoCapture(input_video_path)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps_input = cap.get(cv2.CAP_PROP_FPS)

out = cv2.VideoWriter(
    output_video_path,
    cv2.VideoWriter_fourcc(*"mp4v"),
    fps_input,
    (width, height),
)

# Mở file CSV log dữ liệu 
csv_file = open(log_csv_path, mode="w", newline="", encoding="utf-8")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(
    ["Frame", "Track_ID", "Class_Name", "X1", "Y1", "X2", "Y2"]
)

print(f"--> Đang tiến hành Benchmark với {tracker_type}...")
start_time = time.time()
frame_count = 0

# cấu hình cho yolo
results = model.track(
    source=input_video_path,
    tracker=tracker_type,
    classes=[0, 1, 2, 3, 5, 7],  
    conf=0.35,
    imgsz=960,
    device=device_type,
    half=use_half,
    stream=True,
    persist=True,
    rect=True,  
)

for r in results:
    frame_count += 1

    
    annotated_frame = r.plot(line_width=1, font_size=8, conf=False)
    out.write(annotated_frame)
  
    if r.boxes is not None and r.boxes.id is not None:
        boxes = r.boxes.xyxy.cpu().numpy()
        track_ids = r.boxes.id.int().cpu().numpy()
        cls_ids = r.boxes.cls.int().cpu().numpy()

        for box, track_id, cls_id in zip(boxes, track_ids, cls_ids):
            x1, y1, x2, y2 = box
            class_name = model.names[cls_id]
            csv_writer.writerow(
                [
                    frame_count,
                    track_id,
                    class_name,
                    int(x1),
                    int(y1),
                    int(x2),
                    int(y2),
                ]
            )

end_time = time.time()
total_time = end_time - start_time
avg_fps = frame_count / total_time if total_time > 0 else 0

cap.release()
out.release()
csv_file.close()

# Trả kết quả
print("\n=== KẾT QUẢ ===")
print(f"Thiết bị thử nghiệm: {device_name}")
print(f"Thuật toán Tracker:  {tracker_type}")
print(f"Tốc độ xử lý (FPS):  {avg_fps:.2f} FPS")
print(f"File video kết quả:  {output_video_path}")
print(f"File dữ liệu Log:    {log_csv_path}")