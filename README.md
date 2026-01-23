# Graduate Systems (CSE638) - PA01: Processes and Threads

**Roll Number:** MT25067  
**Assignment:** PA01 - Processes and Threads  
**Deadline:** January 23, 2026

---

## Table of Contents
- [Overview](#overview)
- [Repository Structure](#repository-structure)
- [Implementation Details](#implementation-details)
- [Building the Project](#building-the-project)
- [Running the Programs](#running-the-programs)
- [Measurements and Analysis](#measurements-and-analysis)
- [AI Usage Declaration](#ai-usage-declaration)
- [Results Summary](#results-summary)

---

## Overview

This assignment explores the behavior of processes vs. threads when executing CPU-intensive, memory-intensive, and I/O-intensive workloads. The project consists of:

- **Program A**: Multi-process implementation using `fork()`
- **Program B**: Multi-threaded implementation using `pthread`
- **Worker Functions**: Three workload types (CPU, Memory, I/O)
- **Automated Measurement**: Bash scripts to collect performance metrics
- **Scalability Analysis**: Testing with varying numbers of processes/threads

---

## Repository Structure

```
GRS_PA01/
├── MT25067_Part_A_Program_A.c       # Multi-process program
├── MT25067_Part_A_Program_B.c       # Multi-threaded program
├── MT25067_Part_B_workers.c         # Worker function implementations
├── MT25067_Part_B_workers.h         # Worker function headers
├── MT25067_Part_C_shell.sh          # Automation script for Part C
├── MT25067_Part_D_shell.sh          # Automation script for Part D
├── MT25067_Part_C_CSV.csv           # Part C measurement results
├── MT25067_Part_D_CSV.csv           # Part D scalability results
├── MT25067_Part_D_plot.py           # Python script for generating plots
├── MT25067_Part_C_Time_Plot.png     # Part C execution time plot
├── MT25067_Part_C_CPU_Plot.png      # Part C CPU usage plot
├── MT25067_Part_D_Scalability_Plot.png  # Part D scalability plot
├── Makefile                         # Build automation
├── Dockerfile                       # Docker environment setup
├── .gitignore                       # Git ignore rules
└── README.md                        # This file
```

---

## Implementation Details

### Part A: Process and Thread Creation

**Program A (Processes)**
- Creates N child processes using `fork()` (default N=2)
- Each child executes the specified worker function independently
- Parent waits for all children to complete using `wait()`

**Program B (Threads)**
- Creates N threads using `pthread_create()` (default N=2)
- Each thread executes the worker function concurrently
- Main thread joins all worker threads before exiting

### Part B: Worker Functions

All worker functions execute for `ROLL_LAST_DIGIT × 10³` iterations (7 × 1000 = 7000 iterations):

1. **CPU-Intensive (`run_cpu_intensive`)**
   - Calculates Pi using Leibniz series to 3,000,000 terms
   - Performs 7000 iterations of this calculation
   - Maximizes CPU utilization with mathematical operations

2. **Memory-Intensive (`run_mem_intensive`)**
   - Allocates 1 MB buffer
   - Performs `memset()` operations on the buffer
   - Tests memory bandwidth and cache performance

3. **I/O-Intensive (`run_io_intensive`)**
   - Creates temporary files with unique names
   - Writes and reads data in a loop
   - Measures disk I/O performance

### Part C: Measurement Automation

The `MT25067_Part_C_shell.sh` script:
- Compiles all programs using the Makefile
- Runs 6 combinations (Program A/B × CPU/Memory/I/O)
- Monitors processes using `top` for CPU usage
- Monitors disk activity using `iostat`
- Pins processes to CPU 0 using `taskset -c 0`
- Records execution time, average CPU%, and disk I/O
- Outputs results to CSV format

### Part D: Scalability Analysis

The `MT25067_Part_D_shell.sh` script extends Part C to test:
- **Program A**: 2, 3, 4, 5 processes
- **Program B**: 2, 3, 4, 5, 6, 7, 8 threads
- Uses CPU-intensive task to highlight parallelism behavior
- Generates data for scalability plots

---

## Building the Project

### Prerequisites
- GCC compiler with pthread support
- `make` utility
- `sysstat` package (for `iostat`)
- `procps` package (for `top`)
- Python 3 with pandas, matplotlib, seaborn (for plotting)

### Compilation

```bash
make clean  # Remove old binaries
make        # Compile both programs
```

This generates two executables:
- `Program_A` (multi-process)
- `Program_B` (multi-threaded)

### Docker Environment (Optional)

```bash
docker build -t pa01-env .
docker run -it -v $(pwd):/app pa01-env
```

---

## Running the Programs

### Manual Execution

**Program A (Processes):**
```bash
./Program_A <cpu|mem|io> [num_processes]

# Examples:
./Program_A cpu           # 2 processes (default), CPU task
./Program_A mem 4         # 4 processes, Memory task
```

**Program B (Threads):**
```bash
./Program_B <cpu|mem|io> [num_threads]

# Examples:
./Program_B io            # 2 threads (default), I/O task
./Program_B cpu 8         # 8 threads, CPU task
```

### Automated Measurements

**Part C - Basic Comparison:**
```bash
chmod +x MT25067_Part_C_shell.sh
./MT25067_Part_C_shell.sh
# Output: MT25067_Part_C_CSV.csv
```

**Part D - Scalability Analysis:**
```bash
chmod +x MT25067_Part_D_shell.sh
./MT25067_Part_D_shell.sh
# Output: MT25067_Part_D_CSV.csv
```

**Generate Plots:**
```bash
python3 MT25067_Part_D_plot.py
# Generates PNG plot files
```

---

## Measurements and Analysis

### Part C Results

| Program | Task | Execution Time (s) | Avg CPU% | Avg Disk I/O (KB/s) |
|---------|------|-------------------|----------|---------------------|
| Program_A | CPU | 77.35 | 33.42 | 3.03 |
| Program_A | Memory | 0.21 | 46.70 | 103.99 |
| Program_A | I/O | 1.41 | 7.08 | 51.99 |
| Program_B | CPU | 70.29 | 99.85 | 1.74 |
| Program_B | Memory | 0.21 | 87.50 | 103.48 |
| Program_B | I/O | 1.62 | 19.50 | 51.74 |

**Key Observations:**
- **CPU Task**: Threads (Program B) achieve ~99.8% CPU utilization vs. ~33.4% for processes, demonstrating better core utilization when pinned
- **Memory Task**: Both complete in similar time (~0.21s), but threads show higher CPU% (87.5% vs 46.7%)
- **I/O Task**: Processes are slightly faster (1.41s vs 1.62s), but threads show higher CPU utilization during I/O waits

### Part D Results (Scalability)

When pinned to a single CPU core:
- **Processes**: Execution time scales linearly (2→5 processes: 79s→200s)
- **Threads**: Execution time scales linearly (2→8 threads: 71s→278s)
- Both show minimal parallelism benefit when constrained to one core
- Context switching overhead becomes apparent with more workers

---

## AI Usage Declaration

### Components Generated with AI Assistance:
1. **Bash scripts** (`MT25067_Part_C_shell.sh`, `MT25067_Part_D_shell.sh`)
   - AI assisted with `top` and `iostat` parsing logic
   - AI provided suggestions for background process monitoring
   
2. **Python plotting script** (`MT25067_Part_D_plot.py`)
   - AI generated matplotlib/seaborn boilerplate
   - Plot styling and layout suggestions from AI

3. **Worker function calibration**
   - AI helped optimize iteration counts for measurable execution times
   - Suggestions for preventing compiler optimization

### Components Written Manually:
- Core program logic (fork, pthread implementations)
- Worker function algorithms
- Makefile structure
- Final analysis and interpretation of results

**Note:** All AI-generated code has been reviewed, understood, and tested to ensure correctness and compliance with assignment requirements.

---

## Results Summary

The assignment successfully demonstrates:
1. **Process vs Thread Creation**: Both mechanisms work correctly for parallel task execution
2. **Workload Characterization**: CPU, memory, and I/O tasks show distinct performance profiles
3. **Measurement Infrastructure**: Automated scripts reliably capture CPU%, memory, and I/O metrics
4. **Scalability Insights**: When pinned to a single core, parallelism provides minimal benefit, and execution time scales linearly with worker count

---