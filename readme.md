# Решение хакатона по классификации докуменетов

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
conda env create -f xmas.yml -n xmas
conda activate xmas
```

2. Установить Java (для tika)

```
sudo add-apt-repository ppa:linuxuprising/java
sudo apt update
sudo apt install oracle-java17-installer
```

3. Скачать модель файлы и ноутбуки
  - [Скачать модель с облака](https://drive.google.com/file/d/1L6C6xWkQAqBsZMgXMQz4V9Gu6AL4fj5R/view?usp=sharing)
  - 
  - Все файлы должны находиться в одной директории

#### Пример питоновского интерфейса модели

#### Обучение и метрики модели
Весь процесс обучения описан в 

#### Запуск веб приложения
```
streamlit run web_interface.py
```
