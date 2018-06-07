NOW := $(date +%Y-%m-%d_%H-%M)
notes.org.gpg: notes.org
	-rm -i $@
	-gpg -c $<
	-cp -v  $< /tmp/$(NOW)-$<
	-git commit -m "notes up to $(NOW)" $@
