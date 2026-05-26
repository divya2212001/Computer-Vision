Scale Train Images

```bash
mkdir -p images/train_scaled
for img in ../Data_Extraction/images/train/*.jpg; do
    ffmpeg -i "$img" -vf scale=384:-1 "images/train_scaled/$(basename "$img")"
done
```

Scale Validation Images

```bash
mkdir -p images/val_scaled
for img in ../Data_Extraction/images/val/*.jpg; do
    ffmpeg -i "$img" -vf scale=384:-1 "images/val_scaled/$(basename "$img")"
done
```

Scale Test Images

```bash
mkdir -p images/test_scaled
for img in ../Data_Extraction/images/test/*.jpg; do
    ffmpeg -i "$img" -vf scale=384:-1 "images/test_scaled/$(basename "$img")"
done
```