UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Darwin)
    LINK_FLAGS := -fno-common -flat_namespace -bundle -undefined suppress
else
    LINK_FLAGS := -shared -fpic
endif

all: enc_c.so

%.so:%.o
	$(CC) $(LINK_FLAGS) -lprofanity -o $@ $^

%.o:%.c
	$(CC) $(INCLUDE) -D_GNU_SOURCE -D_BSD_SOURCE -fpic -g3 -O0 -std=c99 \
        -Wextra -pedantic -c -o $@ $<

clean:
	$(RM) enc_c.so
