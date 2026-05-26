# Final Video output

```bash
yolo detect predict \
model=Training/weights/best.pt \
source=Data_Extraction/traffic.mp4 \
conf=0.05 \
show_labels=True \
show_conf=True \
save=True
```