# Final Video output

```bash
yolo detect predict \
model=../Training/train/weights/best.pt \
source=../Data_Extraction/output_road.mp4 \
conf=0.10 \
show_labels=True \
show_conf=True \
save=True
```