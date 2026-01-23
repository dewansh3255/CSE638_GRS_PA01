# PA01: Processes and Threads Analysis

**Roll Number:** MT25067  
**Course:** Graduate Systems (CSE638)  
**Assignment:** Programming Assignment 01 - Processes and Threads

---

## 📋 Table of Contents
- [Overview](#overview)
- [Implementation Details](#implementation-details)
- [Prerequisites](#prerequisites)
- [Compilation and Execution](#compilation-and-execution)
- [File Structure](#file-structure)
- [Results and Analysis](#results-and-analysis)
- [AI Usage Declaration](#ai-usage-declaration)
- [Author](#author)

---

## 🎯 Overview

This assignment explores the performance characteristics of **processes** (fork-based) versus **threads** (pthread-based) implementations across three types of workloads:

1. **CPU-intensive**: Mathematical calculations (Pi computation using Leibniz formula)
2. **Memory-intensive**: Large-scale memory allocation and manipulation
3. **I/O-intensive**: File read/write operations

The project measures and compares:
- CPU usage patterns
- Execution time
- Disk I/O throughput
- Scalability with increasing worker count

---

## 🔧 Implementation Details

### Part A: Process and Thread Creation
- **Program A** (`MT25067_Part_A_Program_A.c`): Creates N child processes using `fork()`
- **Program B** (`MT25067_Part_A_Program_B.c`): Creates N threads using `pthread`

### Part B: Worker Functions
All worker functions are implemented in `MT25067_Part_B_workers.c`:

1. **`run_cpu_intensive()`**
   - Performs 7000 iterations of Pi calculation (3M terms per iteration)
   - Designed to maximize CPU utilization
   - Uses Leibniz formula for Pi approximation

2. **`run_mem_intensive()`**
   - Allocates 10MB buffer per iteration
   - Performs 7000 iterations of memory operations
   - Uses `memset()` for memory writes

3. **`run_io_intensive()`**
   - Performs 7000 iterations of file I/O
   - Creates, writes, reads, and deletes temporary files
   - Tests disk subsystem performance

**Note:** Iteration count = last digit of roll number (7) × 1000 = 7000

### Part C: Measurement Automation
Bash script (`MT25067_Part_C_shell.sh`) automates:
- Execution of all 6 program+task combinations
- CPU monitoring using `top`
- Disk I/O monitoring using `iostat`
- Process pinning to CPU cores 0-2 using `taskset -c 0-2`
- Execution time measurement
- CSV data generation

### Part D: Scalability Analysis
Extended analysis (`MT25067_Part_D_shell.sh`) testing:
- **Program A**: 2, 3, 4, 5 processes
- **Program B**: 2, 3, 4, 5, 6, 7, 8 threads
- Focus on CPU-intensive task for clearest scalability insights
- All workers pinned to 3 CPU cores

---

## 🛠️ Prerequisites

### System Requirements
- Linux environment (Ubuntu 22.04 or similar)
- GCC compiler
- Make utility
- Monitoring tools: `top`, `iostat`, `taskset`
- Python 3.x (for plot generation)

### Required Packages
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install build-essential sysstat procps bc

# Python dependencies
pip3 install pandas matplotlib seaborn
```

### Docker Alternative
A `Dockerfile` is provided for consistent execution environment:
```bash
docker build -t pa01-env .
docker run -it --rm -v $(pwd):/app pa01-env
```

---

## ⚙️ Compilation and Execution

### 1. Compile Programs
```bash
make clean
make
```

This generates two executables:
- `Program_A` (process-based)
- `Program_B` (thread-based)

### 2. Run Individual Programs
```bash
# Run with default 2 workers
./Program_A cpu
./Program_B mem

# Run with custom worker count
./Program_A cpu 4      # 4 processes
./Program_B io 6       # 6 threads
```

### 3. Run Part C Measurements
```bash
./MT25067_Part_C_shell.sh
```
**Output:** `MT25067_Part_C_CSV.csv`

### 4. Run Part D Scalability Tests
```bash
./MT25067_Part_D_shell.sh
```
**Output:** `MT25067_Part_D_CSV.csv`

### 5. Generate Plots
```bash
python3 MT25067_Part_D_plot.py
```
**Outputs:**
- `MT25067_Part_C_Time_Plot.png`
- `MT25067_Part_C_CPU_Plot.png`
- `MT25067_Part_C_Disk_Plot.png`
- `MT25067_Part_D_Scalability_Plot.png`
- `MT25067_Part_D_CPU_Trend_Plot.png`

---

## 📁 File Structure

```
MT25067_PA01/
├── MT25067_Part_A_Program_A.c       # Process-based implementation
├── MT25067_Part_A_Program_B.c       # Thread-based implementation
├── MT25067_Part_B_workers.c         # Worker function implementations
├── MT25067_Part_B_workers.h         # Worker function headers
├── MT25067_Part_C_shell.sh          # Part C automation script
├── MT25067_Part_D_shell.sh          # Part D scalability script
├── MT25067_Part_D_plot.py           # Plot generation script
├── MT25067_Part_C_CSV.csv           # Part C measurement data
├── MT25067_Part_D_CSV.csv           # Part D measurement data
├── MT25067_Part_C_Time_Plot.png     # Generated plots
├── MT25067_Part_C_CPU_Plot.png
├── MT25067_Part_C_Disk_Plot.png
├── MT25067_Part_D_Scalability_Plot.png
├── MT25067_Part_D_CPU_Trend_Plot.png
├── MT25067_Report.pdf               # Comprehensive analysis report
├── Makefile                         # Build automation
├── README.md                        # This file
├── Dockerfile                       # Container environment
└── .gitignore                       # Git ignore rules
```

---

## 📊 Results and Analysis

### Part C: Measurement Data

#### Raw Data Table
| Program | Task | Execution Time (s) | Avg CPU Usage (%) | Avg Disk Write (KB/s) |
|---------|------|-------------------|-------------------|----------------------|
| Program_A | cpu | 42.38 | 67.0 | 2.22 |
| Program_A | mem | 2.36 | 73.3 | 1.12 |
| Program_A | io | 1.90 | 9.1 | 1.68 |
| Program_B | cpu | 36.39 | 195.3 | 0.63 |
| Program_B | mem | 2.04 | 196.7 | 1.11 |
| Program_B | io | 1.83 | 21.5 | 1.67 |

### Key Findings from Part C

#### 1. CPU Usage Patterns
- **Threads (Program B)** achieve ~195% CPU usage on CPU tasks (near 2× core utilization)
- **Processes (Program A)** achieve ~67% CPU usage (limited parallelism)
- **3-core limit**: Maximum theoretical CPU = 300%

#### 2. Execution Time
- **CPU Task**: Threads (36.4s) outperform processes (42.4s) by ~14%
- **MEM Task**: Both implementations similar (~2s)
- **I/O Task**: Both implementations similar (~1.9s)

#### 3. Disk I/O Characteristics
- **CPU tasks** show minimal disk activity (<2.5 KB/s)
- **I/O tasks** show highest disk throughput (~1.7 KB/s)
- **Processes vs Threads**: Similar I/O patterns for MEM and I/O tasks

### Key Findings from Part D

#### Part D: Scalability Data

##### Program A (Processes) - CPU Task
| Worker Count | Execution Time (s) | Avg CPU Usage (%) | Avg Disk Write (KB/s) |
|--------------|-------------------|-------------------|----------------------|
| 2 | 42.70 | 67.0 | 2.96 |
| 3 | 43.14 | 75.2 | 0.53 |
| 4 | 63.70 | 61.4 | 0.36 |
| 5 | 72.93 | 57.5 | 0.32 |

##### Program B (Threads) - CPU Task
| Worker Count | Execution Time (s) | Avg CPU Usage (%) | Avg Disk Write (KB/s) |
|--------------|-------------------|-------------------|----------------------|
| 2 | 36.95 | 199.8 | 1.82 |
| 3 | 40.31 | 296.9 | 0.57 |
| 4 | 56.61 | 269.7 | 0.41 |
| 5 | 66.20 | 287.3 | 0.35 |
| 6 | 79.93 | 289.2 | 0.29 |
| 7 | 91.50 | 299.6 | 0.25 |
| 8 | 110.83 | 291.3 | 0.21 |

### Key Findings from Part D

#### 1. Scalability (CPU Task)
- **Processes**: Execution time increases nearly linearly with worker count
  - 2 workers: 42.7s
  - 5 workers: 72.9s
  - Limited by inter-process overhead

- **Threads**: Better initial scaling, then degradation
  - 2 workers: 36.9s
  - 8 workers: 110.8s
  - Benefits from shared memory, but suffers from contention beyond 3 cores

#### 2. CPU Utilization Trends
- **Threads** consistently achieve ~290-300% CPU usage (saturating 3 cores)
- **Processes** achieve ~60-75% CPU usage (underutilizing available cores)
- **Bottleneck**: Only 3 cores available via taskset, causing worker contention

### Theoretical Insights

**Visual Reference**: See generated plots for detailed comparisons
- `MT25067_Part_C_CPU_Plot.png` - CPU usage comparison across task types
- `MT25067_Part_C_Time_Plot.png` - Execution time comparison
- `MT25067_Part_C_Disk_Plot.png` - Disk I/O patterns
- `MT25067_Part_D_Scalability_Plot.png` - Execution time vs worker count
- `MT25067_Part_D_CPU_Trend_Plot.png` - CPU utilization scaling

1. **Thread Advantages**:
   - Lower context-switch overhead
   - Shared memory space (no IPC needed)
   - Better CPU utilization for compute-bound tasks

2. **Process Limitations**:
   - Higher memory overhead (separate address spaces)
   - Expensive context switches
   - No shared memory benefits

3. **Resource Contention**:
   - Beyond 3 workers, both implementations suffer from core saturation
   - Threads show more severe degradation due to synchronization overhead

---

## 🤖 AI Usage Declaration

### Components Using AI Assistance
The following components were developed with AI assistance (ChatGPT/Claude):

1. **Worker Function Optimization**
   - Initial Pi calculation implementation (Leibniz formula)
   - Memory allocation patterns for memory-intensive task
   - I/O buffering strategy

2. **Bash Scripting**
   - `top` and `iostat` parsing logic
   - Background process management
   - CSV formatting automation

3. **Plot Generation**
   - Matplotlib/Seaborn visualization code
   - Data aggregation and labeling
   - Multi-plot layout design

4. **Makefile Structure**
   - Dependency management
   - Compilation flags optimization

### Components Written Independently
- Core program structure (fork/pthread creation logic)
- Worker function calibration and tuning
- Analysis and interpretation of results
- Report documentation

**Declaration**: All AI-generated code has been thoroughly reviewed, tested, and understood. 

---