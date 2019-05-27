NOW := $(shell date +%Y-%m-%d_%H-%M)

push: notes.org.gpg
	git commit -m "notes up to $(NOW)" $< \
	&& git push

notes.org.gpg:
	-if [ -f $@ ]; then rm -i $@; fi
	-gpg -c notes.org \
	&& cp -v  notes.org /tmp/$(NOW)-notes.org \
	&& git commit -m "notes up to $(NOW)" $@ \
	&& git push && rm -i notes.org

notes.org:
	gpg notes.org.pgp
