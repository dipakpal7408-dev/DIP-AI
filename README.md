---
title: DIP AI V-01
emoji: 🖼️
colorFrom: indigo
colorTo: pink
sdk: gradio
sdk_version: 4.44.0
app_file: app.py
pinned: false
license: mit
---

# DIP AI V-01

High quality, ultra-resolution image generation demo built with Gradio.

## Kaise use karo (local)

```bash
pip install -r requirements.txt
python app.py
```

## Space par deploy (GitHub se live karna)

1. Hugging Face par ek naya Space banao: https://huggingface.co/new-space (SDK: **Gradio** select karo).
2. Is folder ke saare files (`app.py`, `requirements.txt`, `README.md`, aur apna model code/weights) us Space ke git repo me push kar do:
   ```bash
   git clone https://huggingface.co/spaces/<your-username>/<space-name>
   cp app.py requirements.txt README.md <your-username>/<space-name>/
   cd <your-username>/<space-name>
   git add .
   git commit -m "Initial DIP AI V-01 demo"
   git push
   ```
3. Space automatically build ho kar live ho jayega — kuch minutes lagenge (especially GPU hardware select karne par).
4. Agar model bada hai (GPU chahiye), Space settings me free CPU se paid GPU hardware me switch karo, warna ultra-high-res generation slow/timeout ho sakta hai.

## Apna model wire karna

`app.py` me `load_model()` aur `generate()` functions abhi ek placeholder Stable Diffusion XL pipeline use kar rahe hain taaki Space turant chal jaaye. Apna DIP AI V-01 code (jo GitHub repo me hai) yahan replace karo:

- Apna model package (jaise `dip_ai/`) is folder ke andar copy karo.
- `app.py` ke top par usse import karo, aur `load_model()` / `generate()` ke andar apne actual inference calls daalo.
- `requirements.txt` me apne model ki dependencies add/update karo.
