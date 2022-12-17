# Решение хакатона по классификации докуменетов

### Запуск решения
Решение тестировалось на ubuntu 18.04 с 128 гб RAM и 24 гб VRAM
#### Подготовка пакетов

0. (Если нет conda)
```
wget https://repo.continuum.io/archive/Anaconda3-2022.10-Linux-x86_64.sh
bash Anaconda3-2022.10-Linux-x86_64.sh
```

1. Создать окружение conda из xmas.yml
```
conda env create -f xmas.yml -n xmas
```

2. Установить Java (для tika)

```
sudo add-apt-repository ppa:linuxuprising/java
sudo apt update
sudo apt install oracle-java17-installer
```

3. Скачать модель с облака и запустить
