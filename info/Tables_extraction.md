Извлечение таблиц
=====================

Для работы по извлечению большинства таблиц из PDF-документов используется инструмент с открытым исходным кодом [PDFPlumber](https://github.com/jsvine/pdfplumber). Этот инструмент позволяет извлечь таблицы, показывает подробную информацию о каждом текстовом символе в ней, прямоугольнике и строке. Также визуально отображает таблицы. Лучше всего работает с автоматически сгенерированными, а не отсканированными файлами PDF. 

Пример работы PDFPlumber по нахождению таблицы:

![PDFPlumber example](https://github.com/owls-nlp/pdf_tools_bot_ICQ/blob/master/info/images/tables_extraction_example.jpg)

Для использования данного инструмента в системе была создана функция **pdfplumber_extractor** класса Document. Данная функция на вход получает путь до PDF-документа. Предполагалось, что поиск и извлечение таблиц будет происходить по координатам блоков с классом «таблица», полученным от [SegmentationModel](Blocks_detection.md), но, во время экспериментов выяснилось, что модель возвращает границы слишком близко к самой таблице и PDFPlumber не всегда такую таблицу способен распознать. Поэтому было решено искать таблицы на всей странице, а не на области, а затем оставлять только те, которые имеют пересечение с блоками с классом «таблица». 

Для удобного сохранения всех извлеченных с помощью PDFplumber таблиц используется структура Pandas DataFrame языка Python. Каждая строка содержит информацию об одной извлеченной таблице: номер страницы, координаты в разрешении для jpg-файла (лево, верх, право, низ) и саму извлеченную таблицу в виде Pandas DataFrame. Т. к. разрешение у PDF-страницы и jpg-файлов, с которыми работает Detectron2, не совпадает, используется свойство пропорции для перехода от одних координат к другим. После выполнения функция возвращает данную структуру.

Для сопоставления извлеченных с помощью PDFPlumber таблиц и блоков с классом «таблица», полученных в результате работы SegmantationModel, используются функции **match_pdfplumber_data** и **calc_iou** класса Document. В функции calc_iou реализовано вычисление [Intersection over Union](https://www.pyimagesearch.com/2016/11/07/intersection-over-union-iou-for-object-detection/). Это метрика оценки, используемая для измерения точности детекции объекта в наборе данных. Происходит вычисление отношения площади пересечения блоков к площади объединения блоков. По этой метрике выбираются только те таблицы, которые максимально близки к области блока с классом «таблица». 