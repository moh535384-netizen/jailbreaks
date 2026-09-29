# RunPod Qwen Chat

واجهة محادثة بسيطة لـ Qwen3-8B على RunPod.

## التشغيل

1. ثبّت المتطلبات: `pip install -r requirements.txt`
2. اضبط متغير البيئة `RUNPOD_API_KEY` بمفتاح RunPod الخاص بك.
3. الـ Endpoint ID مضبوط مسبقًا على `1qo88t036ztsye`.
4. شغّل: `python app.py`
5. افتح `http://localhost:8080`

مهم: لا تضع API Key داخل HTML أو ترفعه إلى GitHub. احتفظ به كمتغير بيئة/Secret.

الملف `deepseek-4-1.md` المرفق بالمشروع هو نسخة مباشرة من الملف الذي رفعته، ويُقرأ كـ system prompt عند كل طلب.
