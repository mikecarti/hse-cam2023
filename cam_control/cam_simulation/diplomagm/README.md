# Разработка модели для панорамной камеры высокого разрешения.

## Назначение

Данное приложение предназначено для предварительного моделирования панорамных систем при их проектировании и разработке, а также для предварительного моделирования процесса съёмки с подбором для неё оптимальных параметров (время экспозиции, размер диафрагмы).

## Предыстория

Необходимость обеспечения контроля и безопасности на крупных инфраструктурных объектах (аэропорты, стадионы и т.д.) требует наличия панорамных камер высокого разрешения. При разработке системы подобной сложности требуется учёт и анализ значительного количества различных параметров и факторов. Во избежание значительных материальных и временных затрат в ходе реализации панорамных систем необходимо их предварительное моделирование.

## Мотивация

Панорамная съемка -- вид съемки, позволяющий формировать изображение с большим углом обзора по горизонтали. Данное приложение предназначено для моделирование панорамных систем и процесса панорамной съемки. Панорамная система может включать в себя от одной до нескольких камер, каждая из которых, в свою очередь, обладает собственными характеристиками в зависимости от размера матрицы, фокусного расстояния объектива и расположения относительно других камер. На основании вышеперечисленных характеристик данное приложение формирует 2D-проекцию сверху области видимости панорамной системы. Помимо прочего, на основании характеристик панорамной системы данная модель позволяет вычислять оптимальные параметры съемки (время экспозиции, размер диафрагмы) для повышения качества съемки.

## Установка

### Предусловия

Наличие среды разработки, поддерживающей язык программирования Python версии 3.10.0 и выше; система контроля версий git; библиотеки PySide6 для работы фреймворка Qt 6.0+.

### Развёртывание

Для установки языка программирования Python необходимой версии необходимо перейти по ссылке https://www.python.org/downloads/ на официальный сайт разработчиков, выбрать необходимую версию, а затем установить согласно инструкциям на сайте.

Для установки локальной копии репозитория необходимо выполнить в терминале следующую команду.

```
git clone https://gitlab.car.cos.ru/mgantsev/diplomagm

```

Для установки библиотеки PySide6 необходимо выполнить в терминале следующую команду.

```
pip install PySide6

```

Для запуска приложения необходимо выполнить следующую команду.

```
python main.py

```

### Проверка готовности

Данный пункт будет заполнен после реализации всплывающего окна или иного уведомления о готовности приложения.

## Пользователю

### Пользовательская инструкция

Пользовательская инструкция будет добавлена позже в папку /documents в формате PDF.

## Разработчику

### Архитектура ПО

Список папок:

* .vscode -- содержит JSON-файл с настроками для автогенерации документации;

* dump -- содержит JSON-файл с информацией о текущих несохранённых изменениях в параметрах панорамной системы;

* fields -- содержит JSON-файлы с информацией о параметрах сохранённых областей интереса (например, футбольных полей);

* lists of panoramic systems -- содержит JSON-файлы с информацией о параметрах сохранённых панорамных систем;

* documents -- содержит HTML-файлы автоматически сгенерированной документации;

* figures -- содержит JPG и ESP-файлы с результатами моделирования областей видимости и резкости.

Список файлов:

* app.py -- содержит интерфейсы для взаимодействия модели панорамной системы с грацическим интерфейсом;

* basis.py -- содержит классы и их методы для базовых понятий, которые используются в качестве параметров панорамных систем и камер;

* camera.py -- содержит класс камеры и его методы;

* camera_dialog.py -- содержит автоматически сгенерированные параметры диалогового окна для работы с камерами;

* field.py -- содержит класс поля и его методы;

* field_dialog.py -- содержит автоматически сгенерированные параметры диалогового окна для работы с полями;

* json_reader.py -- содержит функции для работы с данными и файлами в JSON-формате;

* main.py -- содержит функцию main для запуска приложения;

* pano_dialog -- содержит автоматически сгенерированные параметры диалогового окна для работы с панорамными камерами;

* panoramic_sysytem.py -- содержит классы списка панорамных камер, панорамных камер и их методы;

* rotation_matrix.py -- содержит функции для вычисления матриц поворота;

* scheme.py -- содержит функции для визуализации областей видимости и резкости панорамных камер;

* ui_main.py -- содержит автоматически сгенерированные параметры главного окна приложения.


### Вычисление и визуализация области видимости

Область видимости (FOV) -- пространство, наблюдаемое оптической системой.

Вычисление области видимости происходит с помощью функции calculatePanoramicSystemFOV, являющейся методом класса PanoramicSystem. Для вычисления области видимости используются следующие параметры панорамной системы (объект класса PanoramicSystem): положение панорамной системы в пространстве (координаты x, y, z), ориентация панорамной системы в пространстве (углы pitch, yaw, roll), список камер, составляющих панорамную систему (list_of_cameras). Также для вычисления области видимости используются следующие параметры каждой камеры (объект класса Camera) в отдельности: фокусное расстояние объектива камеры (focal_length), размеры матрицы камеры (width, height). После вычисления координат четырёхугольника проекции области видимости (объект класса Tetragon) на поверхность интересующей нас сцены вычисленный четырёхугольник сохраняется в список list_of_cameras_fov. 

Визуализация области видимости панорамной системы осуществляется с помощью функции showFOV, получающей на вход список панорамных систем (объект класса ListOfPanoramicSystems) и интересующее нас поле (объект класса Field). Для визуализации используются параметры интересующего нас поля: размеры поля (width, length), положение поля в пространстве (координаты x, y, z). Также для визуализации используется список областей видимости (list_of_cameras_fov), вычисленный с помощью функции calculatePanoramicSystemFOV для каждой панорамной системы, входящей в список панорамных систем.

### Вычисление и визуализация области резкости

Область резкости (FOS) -- пространство, наблюдаемое оптической системой и обладающее приемлемой резкостью на изображении, снятом с помощью оптической системы.

Вычисление области области резкости происходит с помощью функции calculatePanoramicSystemFOS, являющейся методом класса PanoramicSystem. Для вычисления области видимости используются следующие параметры панорамной системы (объект класса PanoramicSystem): положение панорамной системы в пространстве (координаты x, y, z), ориентация панорамной системы в пространстве (углы pitch, yaw, roll), список камер, составляющих панорамную систему (list_of_cameras). Также для вычисления области видимости используются следующие параметры каждой камеры (объект класса Camera) в отдельности: диафрагменное число (f_number), размеры пикселей матрицы камеры (pixel_size). После вычисления координат многоугольника проекции области резкости (массив np.array) на поверхность интересующей нас сцены вычисленный многоугольник сохраняется в список list_of_cameras_fos. 

Визуализация области видимости панорамной системы осуществляется с помощью функции showFOS, получающей на вход список панорамных систем (объект класса ListOfPanoramicSystems) и интересующее нас поле (объект класса Field). Для визуализации используются параметры интересующего нас поля: размеры поля (width, length), положение поля в пространстве (координаты x, y, z). Также для визуализации используется список областей видимости (list_of_cameras_fos), вычисленный с помощью функции calculatePanoramicSystemFOS для каждой панорамной системы, входящей в список панорамных систем.

### Документация

[Документация](https://argoneon.github.io/diplomagm/) проекта.