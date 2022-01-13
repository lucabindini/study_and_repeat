ifeq ($(OS),Windows_NT)
	pathsep = ;
	options = --windowed
	wget = Invoke-WebRequest -OutFile
	unzip = Expand-Archive -DestinationPath
else
	pathsep = :
	UNAME := $(shell uname)
	unzip = unzip -d
	ifeq ($(UNAME),Darwin)
		options = --windowed --name 'Study and Repeat'
		wget = curl --output
	else
		options = --onefile
		wget = wget --output-document
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

requirements.txt : FORCE
	python -m pip freeze >requirements.txt
FORCE :

install :
	python -m pip install --requirement requirements.txt
	$(wget) fugue-icons-3.5.6.zip https://p.yusukekamiyamane.com/icons/downloads/fugue-icons-3.5.6.zip
	$(unzip) src/img/fugue-icons-3.5.6 fugue-icons-3.5.6.zip
	rm fugue-icons-3.5.6.zip

clean :
ifeq ($(OS),Windows_NT)
	-rmdir /s /q build dist
	-erase .\*.spec .\*.exe
else
	rm -rf build dist ./*.spec
endif

.PHONY : clean install
