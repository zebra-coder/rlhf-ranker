import ast
import time
import psutil
import os
import matplotlib.pyplot as plt

# --- 1. The Core Logic ---
def analyze_complexity(code):
    """Statically analyzes code to detect loops (Big O indicator)."""
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return f"Syntax Error: {e}"
        
    loops = 0
    for node in ast.walk(tree):
        if isinstance(node, (ast.For, ast.While)):
            loops += 1
    return f"O(n^{loops})" if loops > 0 else "O(1)"

def measure_runtime(code_func, *args):
    """Measures actual execution metrics."""
    process = psutil.Process(os.getpid())
    start_mem = process.memory_info().rss
    start_time = time.perf_counter()
    
    result = code_func(*args)
    
    end_time = time.perf_counter()
    end_mem = process.memory_info().rss
    
    return {
        "result": result,
        "time": f"{end_time - start_time:.6f}s",
        "raw_time": end_time - start_time,
        "memory": f"{(end_mem - start_mem) / 1024:.2f} KB"
    }

# --- 2. The Visual Proof (The Graph) ---
def generate_complexity_graph(func, input_sizes=[10, 100, 500, 1000]):
    """Runs the function with different inputs and plots the time curve."""
    times = []
    print("\n--- Generating Visual Proof ---")
    
    for n in input_sizes:
        metrics = measure_runtime(func, n)
        exec_time = metrics['raw_time']
        times.append(exec_time)
        print(f"Input: {n} -> Time: {exec_time:.6f}s")

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(input_sizes, times, marker='o', linestyle='-', color='b', label='Your Code')
    
    # Add Reference Line (O(n^2))
    ref_y = [x**2 for x in input_sizes]
    scale_factor = times[-1] / (input_sizes[-1]**2) if times[-1] > 0 else 0
    ref_y_scaled = [y * scale_factor for y in ref_y]
    
    plt.plot(input_sizes, ref_y_scaled, 'r--', alpha=0.5, label='O(n^2) Reference')
    
    plt.title(f"Performance Analysis: {func.__name__}")
    plt.xlabel("Input Size (n)")
    plt.ylabel("Time (seconds)")
    plt.legend()
    plt.grid(True)
    
    # Save and Open
    filename = "complexity_proof.png"
    plt.savefig(filename)
    print(f"Graph saved as {filename}")
    
    if os.name == 'nt': # Windows specific command
        os.startfile(filename)

# --- 3. The Execution Block ---
if __name__ == "__main__":
    # The code we are testing
    def sample_algo(n): 
        # A simple O(n^2) task to prove the graph works
        return [i*j for i in range(n) for j in range(n)]

    # 1. Static Analysis
    print("Analyzing Code Structure...")
    # (We pass the source code of the function as a string for AST)
    code_str = """
def sample_algo(n):
    return [i*j for i in range(n) for j in range(n)]
    """
    print(f"Complexity Grade: {analyze_complexity(code_str)}")

    # 2. Dynamic Analysis (The Graph)
    # THIS is the line you were missing:
    generate_complexity_graph(sample_algo)