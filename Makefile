ifeq ($(OS),Windows_NT)
	pathsep = ;
	options = --onefile --windowed
else
	pathsep = :
	UNAME := $(shell uname)
	ifeq ($(UNAME),Darwin)
		options = --windowed --name 'Study and Repeat'
	else
		options = --onefile
	endif
endif

dist/study_and_repeat : src/**/*.py
	pyinstaller $(options) --icon src/img/favicon.ico \
	  --add-data 'src/img/fugue-icons-3.5.6/icons-shadowless/*.png$(pathsep)src/img/fugue-icons-3.5.6/icons-shadowless' \
	  --add-data 'src/img/favicon.ico$(pathsep)src/img' \
	  src/study_and_repeat.py

.PHONY : clean
clean :
ifeq ($(OS),Windows_NT)
	-rmdir /s /q build dist
	-erase .\*.spec
else
	rm --recursive --force build dist ./*.spec
endif
