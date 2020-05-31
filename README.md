pdf_tools_bot_ICQ
=====================

Имя бота в ICQ: @pdf_tools_bot

**ICQ-бот pdf_tools_bot** создан для быстрого и удобного извлечения информации из PDF документов. Бот поддерживает PDF-формат как отсканированных, так и сгенерированных документов. В боте реализованы следующие функции извлечения информации:  

1) Извлечение изображений. Пользователю предоставляется zip-архив с извлеченными изображениями в формате jpg.

2) Извлечение таблиц. Пользователю предоставляется zip-архив с извлеченными таблицами, сохраненными в документы формата xlsx.

3) Извлечение текста. Пользователь должен выбрать к какому типу относится PDF-документ (отсканированный или сгенерированный) и формат иерархии. Пользователю предоставляется docx-документ.

4) Извлечение всей информации. Пользователь должен выбрать к какому типу относится PDF-документ (отсканированный или сгенерированный) и формат иерархии. Пользователю предоставляется docx-документ. 

Алгоритм работы в зависимости от выбранной функции
-----------------------------------

1. Для извлечения только изображений используется результат [поиска информационных блоков](info/Blocks_detection.md) с классом «фигура».

2. Для извлечения только таблиц используется [PDFPlumber](info/Tables_extraction.md).

3. Для извлечения только текста используется результат [поиска информационных блоков](info/Blocks_detection.md) с классами «заголовок», «текст», «список». В зависимости от типа PDF-документа (отсканированный или сгенерированный) и [формата иерархии](info/Format.md) выбирается способ сортировки информационных блоков и [извлечения текста](info/Text_extraction.md): Tesseract OCR для отсканированных документов и pdftotext для сгенерированных документов. 

4. Для извлечения всей информации и сбора docx-документа используется следующий алгоритм: 

- осуществляется [поиск информационных блоков](info/Blocks_detection.md);

- сортировка блоков по выбранному [формату иерархии](info/Format.md);

- извлечение таблиц с помощью [PDFPlumber](info/Tables_extraction.md) и сравнение с блоками класса «таблица»;

- [извлечение текста](info/Text_extraction.md);

- [сбор docx-документа](info/Build_docx.md).

Сбор Docker-контейнера
-----------------------------------
1. Необходимо добавить папку models и скачать в нее модели. Ссылка на скачивание: https://drive.google.com/drive/folders/1BnG8JieuJk_nnx_fFLJH1hGnowmSc2KV?usp=sharing
2. В папку tesseract_data необходимо добавить файлы модели (rus, eng, lat) Tesseract OCR. Ссылка на скачивание: https://github.com/tesseract-ocr/tessdata 