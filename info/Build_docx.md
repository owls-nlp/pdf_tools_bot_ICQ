Сбор docx-документа
=====================

Для сбора всей извлеченной информации в итоговый docx-документ используется библиотека с открытым исходным кодом [python-docx](https://python-docx.readthedocs.io/en/latest/). Python-docx – это библиотека Python для создания и обновления файлов Microsoft Word. 

Для использования данной библиотеки в системе была создана функция **build_docx_document** класса **Document**, которая получает на вход имя docx-файла. Для работы с таблицами любого формата была создана функция **add_table_to_docx**, которая получает на вход объект класса **DocumentDocx** и таблицу в виде структуры Pandas DataFrame. Возвращает измененный экземпляр класса DocumentDocx, в который была добавлена таблица. 

Демонстрация собранного docx-документа: 

![Demo](https://github.com/owls-nlp/pdf_tools_bot_ICQ/blob/master/info/images/build_docx_demo.jpg)