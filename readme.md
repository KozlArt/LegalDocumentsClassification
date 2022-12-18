# Решение хакатона по классификации докуменетов

Команда: [KozlArt](https://github.com/KozlArt), [OZheRelieV](https://github.com/OZheRelieV)
### Описание решения
Создан классификатор юридических документов с помощью эмбеддингов предобученных языковых моделей с интерпретацией результатов в виде ключевых пунктов документа и цветовой разметкой документа. Для демонастрации решения был создан веб интерфейс streamlit.

### Метрики

| Metric        | Value|
|:-------------:|:-----:|
| ACC      |  0.975   |
| f1 macro      |  0.964   |


### Веб интерфейс и разметка

<p align="center">
<img height=300 src="https://github.com/KozlArt/LegalDocumentsClassification/blob/main/img/img1.png?raw=true"/>

</p>

<p align="center">
<img height=600 src="https://github.com/KozlArt/LegalDocumentsClassification/blob/main/img/img3.png?raw=true"/>
<img height=600 src="https://github.com/KozlArt/LegalDocumentsClassification/blob/main/img/img2.png?raw=true"/>
</p>


### Запуск решения
Решение тестировалось на ubuntu 18.04 с 128 гб RAM и 24 гб VRAM GPU
#### Подготовка пакетов

0. (Если нет conda)
```
wget https://repo.continuum.io/archive/Anaconda3-2022.10-Linux-x86_64.sh
bash Anaconda3-2022.10-Linux-x86_64.sh
```

1. Создать окружение conda из файла xmas.yml
```
conda create -f xmas.yml -n xmas python=3.8
conda activate xmas
```

или если не устанавливаются библиотеки

```
conda create -n xmas python=3.8
conda activate xmas
conda install pip
python -m pip install -r requirements.txt
```

2. Установить Java (для tika) + spacy nlp

```
sudo add-apt-repository ppa:linuxuprising/java
sudo apt update
sudo apt install oracle-java17-installer
```

```
python -m spacy download ru_core_news_sm
```

3. Скачать модель файлы и ноутбуки
  - [Скачать модель с облака](https://drive.google.com/file/d/1L6C6xWkQAqBsZMgXMQz4V9Gu6AL4fj5R/view?usp=sharing)
  - [Скачать датасет](https://drive.google.com/file/d/16ov3v-zpms35439N4EGsxR1X5BbjXIIk/view?usp=sharing)
  - Скачать model.py, web_interface.py, solutuion.ipynb, example_of_use.ipynb из репозитория
  - Все файлы должны находиться в одной директории

#### Пример питоновского интерфейса модели
Пример использования модуля доступен в example_of_use.ipynb
```
cl.get_dict(path) - > dict, модель принимает путь документа и выдает dict - результат классификации
cl.pdf_viz(path) - > None, модель принимает путь документа и создает в своей папке разметку ./output.pdf
```

#### Обучение и метрики модели
Весь процесс обучения описан в solutuion.ipynb

#### Запуск веб приложения
```
streamlit run web_interface.py
```
