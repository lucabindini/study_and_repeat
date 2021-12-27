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

ifeq ($(OS),Windows_NT)
study_and_repeat_windows.exe : dist/study_and_repeat inno_setup.iss
	iscc inno_setup.iss
endif

dist/study_and_repeat : src/*.py src/*/*.py
	pyinstaller $(options) --icon src/img/favicon.ico \
	  --add-data 'src/img/fugue-icons-3.5.6/icons-shadowless/*.png$(pathsep)src/img/fugue-icons-3.5.6/icons-shadowless' \
	  --add-data 'src/img/favicon.ico$(pathsep)src/img' \
	  src/study_and_repeat.py

.PHONY : clean
clean :
ifeq ($(OS),Windows_NT)
	-rmdir /s /q build dist
	-erase .\*.spec .\*.exe
else
	rm -rf build dist ./*.spec
endif
