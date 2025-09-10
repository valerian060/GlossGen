# GlossGen

**GlossGen** is an Image-to-Text Glossary Generator that leverages OCR and advanced AI summarization to help users extract, summarize, and organize vocabulary from images and PDFs. With a modern PyQt5-based graphical interface, GlossGen is designed for students, educators, and language learners who want to turn reading materials into interactive word lists and glossaries.

## Features

- **Image Text Extraction:** Uses Tesseract OCR to extract text from images or selected regions of images.
- **AI Summarization:** Integrates Gemini (Google Generative AI) to summarize and elaborate on the content of images.
- **PDF Support:** Extracts text from PDF images for glossary generation.
- **Glossary Creation:** Filters, counts, and analyzes words to generate detailed glossaries with definitions and difficulty levels.
- **Bookmarking:** Save interesting words for future reference; bookmarks are stored locally.
- **Web Lookup:** Instantly search for words on Wiktionary.
- **Mini-Games:** Includes interactive vocabulary mini-games for learning and retention.
- **Dark Themed UI:** Beautiful, accessible PyQt5 interface with custom dark styling.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/valerian060/GlossGen.git
   cd GlossGen
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   - Make sure [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) is installed and its path is set in `extract_text.py`.
   - For AI summarization, set up your Gemini API key in `gemini.py`.

3. Run the application:
   ```bash
   python main_ui.py
   ```

## Usage

1. **Start the App:** Launch via `python main_ui.py`. The welcome screen lets you choose to extract from PDF, summarize text, or play a mini-game.
2. **Extract Text:** Import an image or PDF. Select regions for OCR extraction.
3. **Summarize Content:** Use Gemini-powered summarization to get explanations for complex images.
4. **Glossary Generation:** View, filter, and analyze words. Bookmark new vocabulary and look up definitions.
5. **Mini-Games:** Reinforce learning with built-in vocabulary mini-games.

## Directory Structure

- `main_ui.py` – Main PyQt5 GUI and application logic
- `extract_text.py` – OCR text extraction functions
- `gemini.py` – Gemini AI summarization integration
- `process_text.py` – Glossary and vocabulary processing
- `menu.py`, `welcome.py`, `mini.py` – UI modules and mini-game logic

## Requirements

- Python 3.7+
- PyQt5
- pytesseract (and Tesseract OCR installed)
- pdf2image
- Pillow
- google-generativeai (for Gemini integration)

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License

This project currently does not specify a license.

## Acknowledgments

- Tesseract OCR
- Google Generative AI (Gemini)
- PyQt5

---

**GlossGen** turns images and PDFs into interactive wordlists, making vocabulary learning simple and fun!