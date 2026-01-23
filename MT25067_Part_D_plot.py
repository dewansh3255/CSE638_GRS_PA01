#!/usr/bin/env python3
"""
Part D: Plot Generation Script
Roll Number: MT25067
Generates visualizations for Parts C and D
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys

# Set style for better-looking plots
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 100
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 10

def load_data():
    """Load CSV data files"""
    try:
        df_c = pd.read_csv('MT25067_Part_C_CSV.csv')
        df_d = pd.read_csv('MT25067_Part_D_CSV.csv')
        print("✓ CSV files loaded successfully")
        return df_c, df_d
    except FileNotFoundError as e:
        print(f"Error: Could not find CSV files.")
        print(f"Make sure you ran both shell scripts first.")
        print(f"Details: {e}")
        sys.exit(1)

def plot_part_c_time(df_c):
    """Plot 1: Part C Execution Time Comparison"""
    plt.figure(figsize=(10, 6))
    
    ax = sns.barplot(x="Task", y="Execution_Time_Sec", hue="Program", data=df_c)
    
    plt.title("Part C: Execution Time Comparison\n(Processes vs Threads)", 
              fontsize=14, fontweight='bold')
    plt.xlabel("Task Type", fontsize=12)
    plt.ylabel("Execution Time (seconds)", fontsize=12)
    plt.legend(title="Implementation", fontsize=10)
    
    # Add value labels on bars
    for container in ax.containers:
        ax.bar_label(container, fmt='%.2f', padding=3)
    
    plt.tight_layout()
    plt.savefig("MT25067_Part_C_Time_Plot.png", bbox_inches='tight')
    plt.close()
    print("✓ Generated: MT25067_Part_C_Time_Plot.png")

def plot_part_c_cpu(df_c):
    """Plot 2: Part C CPU Usage Comparison"""
    plt.figure(figsize=(10, 6))
    
    ax = sns.barplot(x="Task", y="Avg_CPU_Usage", hue="Program", data=df_c)
    
    # UPDATED TITLE
    plt.title("Part C: Average CPU Usage\n(Processes vs Threads - 3 Cores)", 
              fontsize=14, fontweight='bold')
    plt.xlabel("Task Type", fontsize=12)
    plt.ylabel("CPU Usage (%)", fontsize=12)
    
    # UPDATED LIMIT: Increased to 310 to accommodate 300% usage
    plt.ylim(0, 310)  
    plt.legend(title="Implementation", fontsize=10)
    
    # Add value labels on bars
    for container in ax.containers:
        ax.bar_label(container, fmt='%.1f%%', padding=3)
    
    # Add reference line at 300% (Max Capacity)
    plt.axhline(y=300, color='red', linestyle='--', alpha=0.3, label='300% (Max Capacity)')
    
    plt.tight_layout()
    plt.savefig("MT25067_Part_C_CPU_Plot.png", bbox_inches='tight')
    plt.close()
    print("✓ Generated: MT25067_Part_C_CPU_Plot.png")

def plot_part_c_disk(df_c):
    """Plot 3: Part C Disk I/O Comparison (Bonus)"""
    plt.figure(figsize=(10, 6))
    
    ax = sns.barplot(x="Task", y="Avg_Disk_Write_KB", hue="Program", data=df_c)
    
    plt.title("Part C: Average Disk Write I/O\n(Processes vs Threads)", 
              fontsize=14, fontweight='bold')
    plt.xlabel("Task Type", fontsize=12)
    plt.ylabel("Disk Write Throughput (KB/s)", fontsize=12)
    plt.legend(title="Implementation", fontsize=10)
    
    # Add value labels on bars
    for container in ax.containers:
        ax.bar_label(container, fmt='%.2f', padding=3)
    
    plt.tight_layout()
    plt.savefig("MT25067_Part_C_Disk_Plot.png", bbox_inches='tight')
    plt.close()
    print("✓ Generated: MT25067_Part_C_Disk_Plot.png")

def plot_part_d_scalability(df_d):
    """Plot 4: Part D Scalability Analysis"""
    plt.figure(figsize=(12, 7))
    
    # Filter for CPU task (primary scalability test)
    data_a = df_d[(df_d['Program'] == 'Program_A') & (df_d['Task'] == 'cpu')]
    data_b = df_d[(df_d['Program'] == 'Program_B') & (df_d['Task'] == 'cpu')]
    
    # Plot both lines
    plt.plot(data_a['Count'], data_a['Execution_Time_Sec'], 
             marker='o', markersize=8, linewidth=2.5, 
             label='Program A (Processes)', color='#1f77b4')
    
    plt.plot(data_b['Count'], data_b['Execution_Time_Sec'], 
             marker='s', markersize=8, linewidth=2.5, linestyle='--',
             label='Program B (Threads)', color='#ff7f0e')
    
    # UPDATED TITLE
    plt.title("Part D: Scalability Analysis - CPU Task\n(Workers pinned to 3 CPU cores)", 
              fontsize=14, fontweight='bold')
    plt.xlabel("Number of Workers (Processes/Threads)", fontsize=12)
    plt.ylabel("Execution Time (seconds)", fontsize=12)
    plt.legend(fontsize=11, loc='upper left')
    plt.grid(True, alpha=0.3)
    
    # Add data point labels
    for i, row in data_a.iterrows():
        plt.annotate(f"{row['Execution_Time_Sec']:.1f}s", 
                    (row['Count'], row['Execution_Time_Sec']),
                    textcoords="offset points", xytext=(0,10), 
                    ha='center', fontsize=8)
    
    for i, row in data_b.iterrows():
        plt.annotate(f"{row['Execution_Time_Sec']:.1f}s", 
                    (row['Count'], row['Execution_Time_Sec']),
                    textcoords="offset points", xytext=(0,-15), 
                    ha='center', fontsize=8)
    
    plt.tight_layout()
    plt.savefig("MT25067_Part_D_Scalability_Plot.png", bbox_inches='tight')
    plt.close()
    print("✓ Generated: MT25067_Part_D_Scalability_Plot.png")

def plot_part_d_cpu_trend(df_d):
    """Plot 5: Part D CPU Usage Trend (Bonus)"""
    plt.figure(figsize=(12, 7))
    
    # Filter for CPU task
    data_a = df_d[(df_d['Program'] == 'Program_A') & (df_d['Task'] == 'cpu')]
    data_b = df_d[(df_d['Program'] == 'Program_B') & (df_d['Task'] == 'cpu')]
    
    # Plot CPU usage trends
    plt.plot(data_a['Count'], data_a['Avg_CPU_Usage'], 
             marker='o', markersize=8, linewidth=2.5,
             label='Program A (Processes)', color='#2ca02c')
    
    plt.plot(data_b['Count'], data_b['Avg_CPU_Usage'], 
             marker='s', markersize=8, linewidth=2.5, linestyle='--',
             label='Program B (Threads)', color='#d62728')
    
    # UPDATED TITLE
    plt.title("Part D: CPU Usage vs Worker Count\n(CPU-intensive task on 3 cores)", 
              fontsize=14, fontweight='bold')
    plt.xlabel("Number of Workers (Processes/Threads)", fontsize=12)
    plt.ylabel("Average CPU Usage (%)", fontsize=12)
    
    # UPDATED LIMIT
    plt.ylim(0, 310)
    plt.legend(fontsize=11, loc='lower right')
    plt.grid(True, alpha=0.3)
    
    # Add reference line at 300%
    plt.axhline(y=300, color='red', linestyle=':', alpha=0.5, label='300% (3 Cores Max)')
    
    plt.tight_layout()
    plt.savefig("MT25067_Part_D_CPU_Trend_Plot.png", bbox_inches='tight')
    plt.close()
    print("✓ Generated: MT25067_Part_D_CPU_Trend_Plot.png")

def main():
    """Main execution"""
    print("="*50)
    print("PA01 Plot Generation Script")
    print("Roll Number: MT25067")
    print("="*50)
    print()
    
    # Load data
    df_c, df_d = load_data()
    
    print()
    print("Generating plots...")
    print("-"*50)
    
    # Generate all plots
    plot_part_c_time(df_c)
    plot_part_c_cpu(df_c)
    plot_part_c_disk(df_c)
    plot_part_d_scalability(df_d)
    plot_part_d_cpu_trend(df_d)
    
    print("-"*50)
    print()
    print("✓ All plots generated successfully!")
    print()
    print("Generated files:")
    print("  1. MT25067_Part_C_Time_Plot.png")
    print("  2. MT25067_Part_C_CPU_Plot.png")
    print("  3. MT25067_Part_C_Disk_Plot.png")
    print("  4. MT25067_Part_D_Scalability_Plot.png")
    print("  5. MT25067_Part_D_CPU_Trend_Plot.png")
    print()
    print("These plots are ready to include in your report!")
    print("="*50)

if __name__ == "__main__":
    main()