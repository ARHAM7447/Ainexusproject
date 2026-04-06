# Import necessary modules
from flask import Blueprint, render_template, request
from langdetect import detect
from deep_translator import GoogleTranslator

# Create Blueprint
tool4_bp = Blueprint("tool4", __name__, url_prefix="/tool4", template_folder="templates")

# Custom language dictionary (since deep-translator doesn't provide LANGUAGES)
LANGUAGES = {
    "en": "English",
    "hi": "Hindi",
    "fr": "French",
    "es": "Spanish",
    "de": "German",
    "ar": "Arabic",
    "ru": "Russian",
    "zh-cn": "Chinese",
    "ja": "Japanese"
}

# Function to detect language and translate text
def detect_and_translate(text, target_lang):
    # Detect language
    result_lang = detect(text)

    try:
        # Translate using deep-translator
        translate_text = GoogleTranslator(
            source='auto',
            target=target_lang
        ).translate(text)
    except Exception as e:
        translate_text = f"Translation Error: {str(e)}"

    return result_lang, translate_text

# Route: Show page
@tool4_bp.route('/')
def index():
    return render_template('tool4.html', languages=LANGUAGES)

# Route: Handle translation
@tool4_bp.route('/trans', methods=['POST'])
def trans():
    translation = ""
    detected_lang = ""

    if request.method == 'POST':
        text = request.form.get('text')
        target_lang = request.form.get('target_lang')

        if text and target_lang:
            detected_lang, translation = detect_and_translate(text, target_lang)

    return render_template(
        'tool4.html',
        translation=translation,
        detected_lang=detected_lang,
        languages=LANGUAGES
    )