from pyinstrument import Profiler
from app import generate_scored_string

profiler = Profiler()
profiler.start()

for _ in range(100_000):
    generate_scored_string(8)

profiler.stop()
print(profiler.output_text(unicode=True, color=True))
