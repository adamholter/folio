Benchmark assets for the Folio speed-tier pull request (not part of the PR diff).

- `folio_cuda_bench.ipynb`: Colab notebook that installs the runtime, builds the public test take and runs `tools/benchmark_studio.py` against v0.3 on a Tesla T4.
- `results/bench60.json`, `results/bench600.json`: its output for 60 s and ten-minute takes.
- `results/*.mps.distance.json`: tier distances for two speakers, model run on Apple MPS in float32.
- `charts/`: the two PR charts and the script that draws them.
- `dnsmos_colab.py`: DNSMOS P.835 scoring used for the no-reference check.
