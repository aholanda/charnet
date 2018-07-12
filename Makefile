all: __main__.py
	./$< -a

__main__.py: books.py  draw.py  formatting.py  graphs.py  lobby.py  plot.py

help: __main__.py
	./$< -h

clean:
	$(RM) *.bak *.csv *.dot *.log *.pdf *.pyc centr.tex global.tex legomenas.tex

.PHONY: all clean help
