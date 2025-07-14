#!/usr/bin/env bash
# هذا الأمر بيوقف لو صار أي خطأ في النص البرمجي
set -e

# أول شي: ثبتي كل المكتبات اللي موجودة في ملف requirements.txt
pip install -r requirements.txt

# ثاني شي: طبّقي أي تغييرات على قاعدة البيانات
python manage.py migrate

# ثالث شي: اجمعي كل ملفات الستايل والصور الصغيرة في مكان واحد
python manage.py collectstatic --noinput --clear