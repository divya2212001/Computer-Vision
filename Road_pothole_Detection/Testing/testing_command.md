```bash
yolo detect predict \
model=../Training/train/weights/best.pt \
source=../Data_Extraction/images/test \
conf=0.10 \
save=True
```