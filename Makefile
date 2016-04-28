
all: data small big

data:
	python experiment/data.py

small:
	python experiment/train_core.py -e 2 -i 1

big: 
	python experiment/train_augmented.py -e 7 -i 1
