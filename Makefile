runable:
	chmod u+x ./run_mcmc.py

BAA:
	export PYTHONHASHSEED=0
	./run_mcmc.py -l ES -a BAA -i 3 -d lcps
	export PYTHONHASHSEED=0
	./run_mcmc.py -l MS -a BAA -i 3 -d lcps
	export PYTHONHASHSEED=0
	./run_mcmc.py -l HS -a BAA -i 3 -d lcps
	export PYTHONHASHSEED=0
	./run_mcmc.py -l ES -a BAA -i 3 -d fcps
	export PYTHONHASHSEED=0
	./run_mcmc.py -l MS -a BAA -i 3 -d fcps
	export PYTHONHASHSEED=0
	./run_mcmc.py -l HS -a BAA -i 3 -d fcps

BCAA:
	export PYTHONHASHSEED=0
	./run_mcmc.py -l ES -a BCAA -i 3 -d lcps
	export PYTHONHASHSEED=0
	./run_mcmc.py -l MS -a BCAA -i 3 -d lcps
	export PYTHONHASHSEED=0
	./run_mcmc.py -l HS -a BCAA -i 3 -d lcps
	export PYTHONHASHSEED=0
	./run_mcmc.py -l ES -a BCAA -i 3 -d fcps
	export PYTHONHASHSEED=0
	./run_mcmc.py -l MS -a BCAA -i 3 -d fcps
	export PYTHONHASHSEED=0
	./run_mcmc.py -l HS -a BCAA -i 3 -d fcps

AIO:
	export PYTHONHASHSEED=0
	./run_mcmc.py -l ES -a AIO -i 3 -d lcps
	export PYTHONHASHSEED=0
	./run_mcmc.py -l MS -a AIO -i 3 -d lcps
	export PYTHONHASHSEED=0
	./run_mcmc.py -l HS -a AIO -i 3 -d lcps
	export PYTHONHASHSEED=0
	./run_mcmc.py -l ES -a AIO -i 3 -d fcps
	export PYTHONHASHSEED=0
	./run_mcmc.py -l MS -a AIO -i 3 -d fcps
	export PYTHONHASHSEED=0
	./run_mcmc.py -l HS -a AIO -i 3 -d fcps
