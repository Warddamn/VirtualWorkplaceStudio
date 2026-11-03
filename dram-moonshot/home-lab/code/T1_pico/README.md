# T1 bench-electronics code (Raspberry Pi Pico / Pico 2)

Code for the three first-weekend experiments:
- [E1 "A bit on the bench"](../../E1_bit_on_the_bench.md)
- [E2 "A gain cell without a capacitor"](../../E2_gain_cell_no_capacitor.md)
- [E3 "The price of distance"](../../E3_price_of_distance.md)

**All MicroPython here is reference code, untested on hardware.** It passes `python3 -m py_compile`. Every mode also ran in CPython against stub `machine`/`onewire` modules with a virtual clock, which catches crashes but not wiring or timing problems. Expect to debug on the bench.

## Files

| File | Runs on | What it does |
|---|---|---|
| `bench_calcs.py` | PC (Python 3 + numpy) | Every expected number in the three guides, with the arithmetic. `--selftest` checks the formulas, including a numeric RC-energy integral and a replay of the hot-side model's 0.37 / 3.95 pJ/bit. |
| `analyze_t1.py` | PC (Python 3 + numpy) | Turns the Pico's CSV logs into results: fitted strays, leakage from decay curves, the 16-cell retention distribution, Arrhenius fit, C from current-vs-frequency, 2-bit error rates, read-transistor calibration. `--selftest` runs every analysis on synthetic data. |
| `t1_common.py` | Pico | Helpers: ADC averaging, tri-state pins, CSV logger, DS18B20, heater thermostat with a 55 °C hard cut-off. |
| `hamming16.py` | Pico and PC | Extended Hamming (16,11) code that corrects one error and detects two, for the ECC demo in E1. |
| `e1_single_cell.py` | Pico | One 1T1C cell. Modes `share`, `destructive`, `retention`, `peek`. |
| `e1_array_4x4.py` | Pico | 16-bit array. Modes `pattern`, `refresh`, `retmap`, `ecc`. |
| `e2_gain_cell.py` | Pico | Three 2T0C cells side by side. Modes `transfer`, `retention`, `fast`, `readmany`, `mlc`. |
| `e3_energy.py` | Pico | `sweep` measures supply current vs frequency for each load. `spi` runs the qualitative SPI-vs-SRAM phases. |

## How to run

1. Install MicroPython on the Pico. Hold BOOTSEL, plug in USB, and drag the `.uf2` file for your board (Pico or Pico 2) from micropython.org onto the drive that appears.
2. Copy `t1_common.py`, `hamming16.py` and the experiment script to the Pico. In Thonny, use "Save as… → Raspberry Pi Pico". From a terminal, use `mpremote cp t1_common.py :`.
3. Edit `MODE` and the configuration block at the top of the script.
4. Run it, depending on the mode:
   - **Modes that ask you questions** (`share`, `destructive`, E3 `sweep`): run from Thonny, whose shell accepts typed answers. Set `LOGFILE = "name.csv"` so the data also lands on the Pico. Copy the file back afterwards with Thonny's Files pane or `mpremote cp :name.csv .`
   - **Unattended modes**: on a PC, `mpremote run e1_array_4x4.py > e1_retmap.csv` captures the CSV directly. Whether `mpremote run` forwards typed input to `input()` is unverified, so use Thonny for the question-asking modes.
5. Analyze on the PC, for example `python3 analyze_t1.py retmap e1_retmap.csv`. Run `python3 analyze_t1.py -h` for every command.

## Board choice

- **Use a Raspberry Pi Pico (RP2040) for E1 and E2.**
- **Avoid early Pico 2 boards for E1 and E2.** Early Pico 2 boards use the RP2350 A2 stepping, which has erratum E9: extra leakage on a GPIO pad whose input buffer is on while the pin sits between logic levels. A floating bitline sits there by design. The A4 stepping reportedly fixes E9, but shops still sell mixed stock.
- **E3 works on either board.**
