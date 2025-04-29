TARGETS:=$(shell find . -type f -name "*.c" -exec basename -s .c -a {} \;)

all: ${TARGETS}

%: %.c
	clang -emit-llvm -S -fno-discard-value-names -c -o $@.ll $< -g
	opt -load ../build/InstrumentPass.so -Instrument -S $@.ll -o $@.instrumented.ll
	opt -load ../build/CBIInstrumentPass.so -CBIInstrument -S $@.instrumented.ll -o $@.cbi.instrumented.ll
	clang -o $@ -L${PWD}/../build -lruntime -lm $@.cbi.instrumented.ll

fuzz-%: %
	@./test.sh $< 100s

fuzz-all:
	@mkdir -p reports
	@for t in ${TARGETS}; do \
		echo "== Fuzzing $$t =="; \
		$(MAKE) fuzz-$$t; \
	done

analyze-all:
	@mkdir -p reports
	@for t in ${TARGETS}; do \
		echo "== Running CBI on $$t =="; \
		cbi ./$$t fuzz_output_$$t || echo "CBI failed on $$t"; \
	done

clean:
	rm -rf *.ll *.instrumented.ll *.cbi.instrumented.ll \
	       fuzz_output_* \
	       *.report.json \
	       ${TARGETS} \
	       reports \
	       core.* \
	       *.cov *.jsonl *.json *.txt
