all: bin/minfs

.PHONY: clean

bin/minfs: bin minfs_tool
	cp lindenis-v833-RTOS-melis-4.0/source/utility/host-tool/minfs_tool/minfs bin

minfs_tool:
	$(MAKE) -C lindenis-v833-RTOS-melis-4.0/source/utility/host-tool/minfs_tool

bin:
	mkdir bin

clean:
	rm -Rf bin
	$(MAKE) -C lindenis-v833-RTOS-melis-4.0/source/utility/host-tool/minfs_tool clean
