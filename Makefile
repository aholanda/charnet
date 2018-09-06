all: __main__.py
	./$< -a

FIGS := Figure-Assortativity.pdf  Figure-Betweenness.pdf  Figure-Closeness.pdf  Figure-Degree.pdf  Figure-Density_versus_CC.pdf

__main__.py: books.py  draw.py  formatting.py  graphs.py  lobby.py  plot.py

$(FIGS): __main__.py
	./$< -p

plot: $(FIGS)

sync: $(FIGS)
	cp $^ ../charnet-paper.git

help: __main__.py
	./$< -h

clean:
	$(RM) *.bak *.csv *.dot *.log *.pdf g-*.png *.pyc centr.tex global.tex legomenas.tex

.PHONY: all clean help plot
