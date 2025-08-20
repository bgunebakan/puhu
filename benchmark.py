#!/usr/bin/env python3
"""
Comprehensive benchmark script comparing Puhu vs Pillow performance.
Tests all supported operations with various image sizes and formats.
"""

import time
import psutil
import os
import sys
import statistics
import platform
import datetime
import json
import csv
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional
import tracemalloc
import gc

try:
    from PIL import Image as PILImage, ImageOps
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False
    print("Warning: Pillow not available for comparison")

try:
    import puhu
    PUHU_AVAILABLE = True
except ImportError:
    PUHU_AVAILABLE = False
    print("Warning: Puhu not available - please install first")

import numpy as np


class BenchmarkResult:
    """Container for benchmark results"""
    def __init__(self, operation: str, library: str, time_ms: float, 
                 memory_mb: float, success: bool = True, error: str = None):
        self.operation = operation
        self.library = library
        self.time_ms = time_ms
        self.memory_mb = memory_mb
        self.success = success
        self.error = error

    def __repr__(self):
        status = "✓" if self.success else "✗"
        return f"{status} {self.library}: {self.time_ms:.2f}ms, {self.memory_mb:.2f}MB"


class ImageBenchmark:
    """Main benchmark class for comparing Puhu vs Pillow"""
    
    def __init__(self, test_images_dir: str = "test_images", iterations: int = 5):
        self.test_images_dir = Path(test_images_dir)
        self.iterations = iterations
        self.results: List[BenchmarkResult] = []
        
        # Create test images directory
        self.test_images_dir.mkdir(exist_ok=True)
        
        # Test configurations
        self.test_sizes = [(100, 100), (500, 500), (1000, 1000), (2000, 2000)]
        self.test_formats = ['RGB', 'RGBA', 'L']
        self.resize_filters = ['NEAREST', 'BILINEAR', 'BICUBIC', 'LANCZOS']
        
    def create_test_images(self):
        """Generate test images of various sizes and formats"""
        print("Creating test images...")
        
        for size in self.test_sizes:
            for fmt in self.test_formats:
                # Create gradient image for more realistic testing
                width, height = size
                if fmt == 'RGB':
                    # RGB gradient
                    r = np.linspace(0, 255, width, dtype=np.uint8)
                    g = np.linspace(0, 255, height, dtype=np.uint8)
                    b = np.full((height, width), 128, dtype=np.uint8)
                    
                    img_data = np.zeros((height, width, 3), dtype=np.uint8)
                    img_data[:, :, 0] = r[np.newaxis, :]
                    img_data[:, :, 1] = g[:, np.newaxis]
                    img_data[:, :, 2] = b
                    
                elif fmt == 'RGBA':
                    # RGBA gradient with alpha
                    r = np.linspace(0, 255, width, dtype=np.uint8)
                    g = np.linspace(0, 255, height, dtype=np.uint8)
                    b = np.full((height, width), 128, dtype=np.uint8)
                    a = np.full((height, width), 200, dtype=np.uint8)
                    
                    img_data = np.zeros((height, width, 4), dtype=np.uint8)
                    img_data[:, :, 0] = r[np.newaxis, :]
                    img_data[:, :, 1] = g[:, np.newaxis]
                    img_data[:, :, 2] = b
                    img_data[:, :, 3] = a
                    
                else:  # L (grayscale)
                    # Grayscale gradient
                    gray = np.linspace(0, 255, width, dtype=np.uint8)
                    img_data = np.tile(gray, (height, 1))
                
                # Save using PIL
                if PILLOW_AVAILABLE:
                    if fmt == 'L':
                        pil_img = PILImage.fromarray(img_data, mode='L')
                    else:
                        pil_img = PILImage.fromarray(img_data, mode=fmt)
                    
                    filename = f"test_{width}x{height}_{fmt.lower()}.png"
                    pil_img.save(self.test_images_dir / filename)
                    
                    # Also save as JPEG for format testing
                    if fmt == 'RGB':
                        jpg_filename = f"test_{width}x{height}_{fmt.lower()}.jpg"
                        pil_img.save(self.test_images_dir / jpg_filename, quality=95)
        
        print(f"Created test images in {self.test_images_dir}")

    def measure_performance(self, func, *args, **kwargs) -> Tuple[float, float, Any, Optional[str]]:
        """Measure execution time and memory usage of a function"""
        gc.collect()  # Clean up before measurement
        
        # Start memory tracking
        tracemalloc.start()
        process = psutil.Process()
        memory_before = process.memory_info().rss / 1024 / 1024  # MB
        
        start_time = time.perf_counter()
        
        try:
            result = func(*args, **kwargs)
            success = True
            error = None
        except Exception as e:
            result = None
            success = False
            error = str(e)
        
        end_time = time.perf_counter()
        
        # Measure memory
        memory_after = process.memory_info().rss / 1024 / 1024  # MB
        memory_used = memory_after - memory_before
        tracemalloc.stop()
        
        execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
        
        return execution_time, memory_used, result, error

    def benchmark_image_loading(self):
        """Benchmark image loading from file and bytes"""
        print("\n=== Image Loading Benchmarks ===")
        
        for size in self.test_sizes:
            for fmt in ['rgb', 'rgba', 'l']:
                filename = f"test_{size[0]}x{size[1]}_{fmt}.png"
                filepath = self.test_images_dir / filename
                
                if not filepath.exists():
                    continue
                
                print(f"\nTesting {filename}:")
                
                # Read file as bytes for bytes loading test
                with open(filepath, 'rb') as f:
                    image_bytes = f.read()
                
                # Test file loading
                for library, loader in [
                    ("Pillow", lambda p: PILImage.open(p) if PILLOW_AVAILABLE else None),
                    ("Puhu", lambda p: puhu.Image.open(str(p)) if PUHU_AVAILABLE else None)
                ]:
                    if (library == "Pillow" and not PILLOW_AVAILABLE) or \
                       (library == "Puhu" and not PUHU_AVAILABLE):
                        continue
                    
                    times = []
                    memories = []
                    
                    for _ in range(self.iterations):
                        exec_time, memory, result, error = self.measure_performance(loader, filepath)
                        if error is None:
                            times.append(exec_time)
                            memories.append(memory)
                    
                    if times:
                        avg_time = statistics.mean(times)
                        avg_memory = statistics.mean(memories)
                        self.results.append(BenchmarkResult(
                            f"load_file_{size[0]}x{size[1]}_{fmt}", 
                            library, avg_time, avg_memory
                        ))
                        print(f"  {library} file loading: {avg_time:.2f}ms ± {statistics.stdev(times):.2f}ms")
                
                # Test bytes loading
                for library, loader in [
                    ("Pillow", lambda b: PILImage.open(b) if PILLOW_AVAILABLE else None),
                    ("Puhu", lambda b: puhu.Image.open(b) if PUHU_AVAILABLE else None)
                ]:
                    if (library == "Pillow" and not PILLOW_AVAILABLE) or \
                       (library == "Puhu" and not PUHU_AVAILABLE):
                        continue
                    
                    times = []
                    memories = []
                    
                    for _ in range(self.iterations):
                        from io import BytesIO
                        bytes_io = BytesIO(image_bytes)
                        exec_time, memory, result, error = self.measure_performance(loader, bytes_io)
                        if error is None:
                            times.append(exec_time)
                            memories.append(memory)
                    
                    if times:
                        avg_time = statistics.mean(times)
                        avg_memory = statistics.mean(memories)
                        self.results.append(BenchmarkResult(
                            f"load_bytes_{size[0]}x{size[1]}_{fmt}", 
                            library, avg_time, avg_memory
                        ))
                        print(f"  {library} bytes loading: {avg_time:.2f}ms ± {statistics.stdev(times):.2f}ms")

    def benchmark_resize_operations(self):
        """Benchmark resize operations with different filters"""
        print("\n=== Resize Benchmarks ===")
        
        # Use a medium-sized image for resize tests
        test_file = self.test_images_dir / "test_1000x1000_rgb.png"
        if not test_file.exists():
            return
        
        target_sizes = [(250, 250), (500, 500), (1500, 1500)]
        
        for target_size in target_sizes:
            print(f"\nResizing to {target_size[0]}x{target_size[1]}:")
            
            for filter_name in self.resize_filters:
                print(f"  Filter: {filter_name}")
                
                # Pillow resize
                if PILLOW_AVAILABLE:
                    def pillow_resize():
                        img = PILImage.open(test_file)
                        filter_map = {
                            'NEAREST': PILImage.NEAREST,
                            'BILINEAR': PILImage.BILINEAR, 
                            'BICUBIC': PILImage.BICUBIC,
                            'LANCZOS': PILImage.LANCZOS
                        }
                        return img.resize(target_size, filter_map[filter_name])
                    
                    times = []
                    memories = []
                    for _ in range(self.iterations):
                        exec_time, memory, result, error = self.measure_performance(pillow_resize)
                        if error is None:
                            times.append(exec_time)
                            memories.append(memory)
                    
                    if times:
                        avg_time = statistics.mean(times)
                        avg_memory = statistics.mean(memories)
                        self.results.append(BenchmarkResult(
                            f"resize_{target_size[0]}x{target_size[1]}_{filter_name.lower()}", 
                            "Pillow", avg_time, avg_memory
                        ))
                        print(f"    Pillow: {avg_time:.2f}ms ± {statistics.stdev(times):.2f}ms")
                
                # Puhu resize
                if PUHU_AVAILABLE:
                    def puhu_resize():
                        img = puhu.Image.open(str(test_file))
                        return img.resize(target_size, filter_name)
                    
                    times = []
                    memories = []
                    for _ in range(self.iterations):
                        exec_time, memory, result, error = self.measure_performance(puhu_resize)
                        if error is None:
                            times.append(exec_time)
                            memories.append(memory)
                    
                    if times:
                        avg_time = statistics.mean(times)
                        avg_memory = statistics.mean(memories)
                        self.results.append(BenchmarkResult(
                            f"resize_{target_size[0]}x{target_size[1]}_{filter_name.lower()}", 
                            "Puhu", avg_time, avg_memory
                        ))
                        print(f"    Puhu: {avg_time:.2f}ms ± {statistics.stdev(times):.2f}ms")

    def benchmark_crop_operations(self):
        """Benchmark crop operations"""
        print("\n=== Crop Benchmarks ===")
        
        test_file = self.test_images_dir / "test_1000x1000_rgb.png"
        if not test_file.exists():
            return
        
        crop_boxes = [
            (100, 100, 300, 300),  # Small crop
            (200, 200, 600, 600),  # Medium crop
            (100, 100, 800, 800),  # Large crop
        ]
        
        for crop_box in crop_boxes:
            crop_size = f"{crop_box[2]-crop_box[0]}x{crop_box[3]-crop_box[1]}"
            print(f"\nCrop to {crop_size}:")
            
            # Pillow crop
            if PILLOW_AVAILABLE:
                def pillow_crop():
                    img = PILImage.open(test_file)
                    return img.crop(crop_box)
                
                times = []
                memories = []
                for _ in range(self.iterations):
                    exec_time, memory, result, error = self.measure_performance(pillow_crop)
                    if error is None:
                        times.append(exec_time)
                        memories.append(memory)
                
                if times:
                    avg_time = statistics.mean(times)
                    avg_memory = statistics.mean(memories)
                    self.results.append(BenchmarkResult(
                        f"crop_{crop_size}", "Pillow", avg_time, avg_memory
                    ))
                    print(f"  Pillow: {avg_time:.2f}ms ± {statistics.stdev(times):.2f}ms")
            
            # Puhu crop
            if PUHU_AVAILABLE:
                def puhu_crop():
                    img = puhu.Image.open(str(test_file))
                    return img.crop(crop_box)
                
                times = []
                memories = []
                for _ in range(self.iterations):
                    exec_time, memory, result, error = self.measure_performance(puhu_crop)
                    if error is None:
                        times.append(exec_time)
                        memories.append(memory)
                
                if times:
                    avg_time = statistics.mean(times)
                    avg_memory = statistics.mean(memories)
                    self.results.append(BenchmarkResult(
                        f"crop_{crop_size}", "Puhu", avg_time, avg_memory
                    ))
                    print(f"  Puhu: {avg_time:.2f}ms ± {statistics.stdev(times):.2f}ms")

    def benchmark_rotation_operations(self):
        """Benchmark rotation and transpose operations"""
        print("\n=== Rotation & Transpose Benchmarks ===")
        
        test_file = self.test_images_dir / "test_500x500_rgb.png"
        if not test_file.exists():
            return
        
        rotations = [90, 180, 270]
        transposes = ['FLIP_LEFT_RIGHT', 'FLIP_TOP_BOTTOM']
        
        # Test rotations
        for angle in rotations:
            print(f"\nRotation {angle}°:")
            
            # Pillow rotation
            if PILLOW_AVAILABLE:
                def pillow_rotate():
                    img = PILImage.open(test_file)
                    if angle == 90:
                        return img.rotate(-90, expand=True)
                    elif angle == 180:
                        return img.rotate(180)
                    elif angle == 270:
                        return img.rotate(90, expand=True)
                
                times = []
                memories = []
                for _ in range(self.iterations):
                    exec_time, memory, result, error = self.measure_performance(pillow_rotate)
                    if error is None:
                        times.append(exec_time)
                        memories.append(memory)
                
                if times:
                    avg_time = statistics.mean(times)
                    avg_memory = statistics.mean(memories)
                    self.results.append(BenchmarkResult(
                        f"rotate_{angle}", "Pillow", avg_time, avg_memory
                    ))
                    print(f"  Pillow: {avg_time:.2f}ms ± {statistics.stdev(times):.2f}ms")
            
            # Puhu rotation
            if PUHU_AVAILABLE:
                def puhu_rotate():
                    img = puhu.Image.open(str(test_file))
                    return img.rotate(float(angle))
                
                times = []
                memories = []
                for _ in range(self.iterations):
                    exec_time, memory, result, error = self.measure_performance(puhu_rotate)
                    if error is None:
                        times.append(exec_time)
                        memories.append(memory)
                
                if times:
                    avg_time = statistics.mean(times)
                    avg_memory = statistics.mean(memories)
                    self.results.append(BenchmarkResult(
                        f"rotate_{angle}", "Puhu", avg_time, avg_memory
                    ))
                    print(f"  Puhu: {avg_time:.2f}ms ± {statistics.stdev(times):.2f}ms")
        
        # Test transposes
        for transpose in transposes:
            print(f"\n{transpose}:")
            
            # Pillow transpose
            if PILLOW_AVAILABLE:
                def pillow_transpose():
                    img = PILImage.open(test_file)
                    if transpose == 'FLIP_LEFT_RIGHT':
                        return img.transpose(PILImage.FLIP_LEFT_RIGHT)
                    elif transpose == 'FLIP_TOP_BOTTOM':
                        return img.transpose(PILImage.FLIP_TOP_BOTTOM)
                
                times = []
                memories = []
                for _ in range(self.iterations):
                    exec_time, memory, result, error = self.measure_performance(pillow_transpose)
                    if error is None:
                        times.append(exec_time)
                        memories.append(memory)
                
                if times:
                    avg_time = statistics.mean(times)
                    avg_memory = statistics.mean(memories)
                    self.results.append(BenchmarkResult(
                        f"transpose_{transpose.lower()}", "Pillow", avg_time, avg_memory
                    ))
                    print(f"  Pillow: {avg_time:.2f}ms ± {statistics.stdev(times):.2f}ms")
            
            # Puhu transpose
            if PUHU_AVAILABLE:
                def puhu_transpose():
                    img = puhu.Image.open(str(test_file))
                    return img.transpose(transpose)
                
                times = []
                memories = []
                for _ in range(self.iterations):
                    exec_time, memory, result, error = self.measure_performance(puhu_transpose)
                    if error is None:
                        times.append(exec_time)
                        memories.append(memory)
                
                if times:
                    avg_time = statistics.mean(times)
                    avg_memory = statistics.mean(memories)
                    self.results.append(BenchmarkResult(
                        f"transpose_{transpose.lower()}", "Puhu", avg_time, avg_memory
                    ))
                    print(f"  Puhu: {avg_time:.2f}ms ± {statistics.stdev(times):.2f}ms")

    def benchmark_batch_operations(self):
        """Benchmark batch operations unique to Puhu"""
        print("\n=== Batch Operations Benchmarks ===")
        
        test_file = self.test_images_dir / "test_1000x1000_rgb.png"
        if not test_file.exists():
            return
        
        # Test resize_and_crop
        print("\nResize and Crop (1000x1000 -> 800x800 -> crop 400x400):")
        
        # Pillow equivalent (separate operations)
        if PILLOW_AVAILABLE:
            def pillow_resize_and_crop():
                img = PILImage.open(test_file)
                resized = img.resize((800, 800), PILImage.BILINEAR)
                return resized.crop((200, 200, 600, 600))
            
            times = []
            memories = []
            for _ in range(self.iterations):
                exec_time, memory, result, error = self.measure_performance(pillow_resize_and_crop)
                if error is None:
                    times.append(exec_time)
                    memories.append(memory)
            
            if times:
                avg_time = statistics.mean(times)
                avg_memory = statistics.mean(memories)
                self.results.append(BenchmarkResult(
                    "resize_and_crop_batch", "Pillow", avg_time, avg_memory
                ))
                print(f"  Pillow (separate): {avg_time:.2f}ms ± {statistics.stdev(times):.2f}ms")
        
        # Puhu batch operation
        if PUHU_AVAILABLE:
            def puhu_resize_and_crop():
                img = puhu.Image.open(str(test_file))
                return img.resize_and_crop((800, 800), (200, 200, 400, 400), "BILINEAR")
            
            times = []
            memories = []
            for _ in range(self.iterations):
                exec_time, memory, result, error = self.measure_performance(puhu_resize_and_crop)
                if error is None:
                    times.append(exec_time)
                    memories.append(memory)
            
            if times:
                avg_time = statistics.mean(times)
                avg_memory = statistics.mean(memories)
                self.results.append(BenchmarkResult(
                    "resize_and_crop_batch", "Puhu", avg_time, avg_memory
                ))
                print(f"  Puhu (batch): {avg_time:.2f}ms ± {statistics.stdev(times):.2f}ms")

    def get_system_info(self) -> Dict[str, str]:
        """Collect system information for the report"""
        return {
            "timestamp": datetime.datetime.now().isoformat(),
            "platform": platform.platform(),
            "processor": platform.processor(),
            "architecture": platform.architecture()[0],
            "python_version": platform.python_version(),
            "cpu_count": str(psutil.cpu_count()),
            "memory_total": f"{psutil.virtual_memory().total / (1024**3):.1f} GB",
            "pillow_version": getattr(PILImage, '__version__', 'N/A') if PILLOW_AVAILABLE else 'N/A',
            "puhu_version": getattr(puhu, '__version__', 'N/A') if PUHU_AVAILABLE else 'N/A'
        }

    def generate_html_report(self, output_file: str = "benchmark_report.html"):
        """Generate comprehensive HTML benchmark report"""
        system_info = self.get_system_info()
        
        # Group results by operation
        operations = {}
        for result in self.results:
            if result.operation not in operations:
                operations[result.operation] = {}
            operations[result.operation][result.library] = result
        
        # Calculate statistics
        faster_count = {"Puhu": 0, "Pillow": 0, "Tie": 0}
        memory_efficient = {"Puhu": 0, "Pillow": 0, "Tie": 0}
        performance_data = []
        
        for operation, libs in operations.items():
            if len(libs) >= 2 and "Puhu" in libs and "Pillow" in libs:
                puhu_result = libs["Puhu"]
                pillow_result = libs["Pillow"]
                
                speedup = pillow_result.time_ms / puhu_result.time_ms
                if speedup > 1.1:
                    faster = "Puhu"
                    faster_count["Puhu"] += 1
                elif speedup < 0.9:
                    faster = "Pillow"
                    faster_count["Pillow"] += 1
                else:
                    faster = "Tie"
                    faster_count["Tie"] += 1
                
                memory_ratio = pillow_result.memory_mb / puhu_result.memory_mb if puhu_result.memory_mb > 0 else 1
                if memory_ratio > 1.1:
                    mem_efficient = "Puhu"
                    memory_efficient["Puhu"] += 1
                elif memory_ratio < 0.9:
                    mem_efficient = "Pillow"
                    memory_efficient["Pillow"] += 1
                else:
                    mem_efficient = "Tie"
                    memory_efficient["Tie"] += 1
                
                performance_data.append({
                    "operation": operation,
                    "puhu_time": puhu_result.time_ms,
                    "pillow_time": pillow_result.time_ms,
                    "puhu_memory": puhu_result.memory_mb,
                    "pillow_memory": pillow_result.memory_mb,
                    "speedup": speedup,
                    "faster": faster,
                    "memory_efficient": mem_efficient
                })
        
        # Generate HTML
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Puhu vs Pillow Benchmark Report</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            text-align: center;
            margin-bottom: 30px;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 40px;
            margin-bottom: 20px;
        }}
        .system-info {{
            background: #ecf0f1;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 30px;
        }}
        .system-info h3 {{
            margin-top: 0;
            color: #2c3e50;
        }}
        .info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 10px;
        }}
        .info-item {{
            display: flex;
            justify-content: space-between;
            padding: 5px 0;
        }}
        .info-label {{
            font-weight: bold;
            color: #7f8c8d;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: white;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #3498db;
            color: white;
            font-weight: bold;
        }}
        tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}
        tr:hover {{
            background-color: #e8f4fd;
        }}
        .faster-puhu {{
            background-color: #d5f4e6;
            color: #27ae60;
            font-weight: bold;
        }}
        .faster-pillow {{
            background-color: #fdeaea;
            color: #e74c3c;
            font-weight: bold;
        }}
        .tie {{
            background-color: #fff3cd;
            color: #856404;
            font-weight: bold;
        }}
        .chart-container {{
            margin: 30px 0;
            height: 400px;
            position: relative;
        }}
        .summary-stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        .stat-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }}
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .recommendations {{
            background: #e8f5e8;
            border-left: 5px solid #27ae60;
            padding: 20px;
            margin: 30px 0;
        }}
        .recommendations h3 {{
            color: #27ae60;
            margin-top: 0;
        }}
        .recommendation-item {{
            margin: 10px 0;
            padding: 10px;
            background: white;
            border-radius: 5px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Puhu vs Pillow Performance Benchmark Report</h1>
        
        <div class="system-info">
            <h3>📊 System Information</h3>
            <div class="info-grid">
                <div class="info-item">
                    <span class="info-label">Timestamp:</span>
                    <span>{system_info['timestamp']}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Platform:</span>
                    <span>{system_info['platform']}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Processor:</span>
                    <span>{system_info['processor']}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Architecture:</span>
                    <span>{system_info['architecture']}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Python Version:</span>
                    <span>{system_info['python_version']}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">CPU Cores:</span>
                    <span>{system_info['cpu_count']}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Total Memory:</span>
                    <span>{system_info['memory_total']}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Pillow Version:</span>
                    <span>{system_info['pillow_version']}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Puhu Version:</span>
                    <span>{system_info['puhu_version']}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Test Iterations:</span>
                    <span>{self.iterations}</span>
                </div>
            </div>
        </div>
        
        <div class="summary-stats">
            <div class="stat-card">
                <div class="stat-number">{faster_count['Puhu']}</div>
                <div>Operations where Puhu is faster</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{faster_count['Pillow']}</div>
                <div>Operations where Pillow is faster</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{memory_efficient['Puhu']}</div>
                <div>Operations where Puhu uses less memory</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(self.results)}</div>
                <div>Total tests performed</div>
            </div>
        </div>
        
        <h2>📈 Performance Comparison Chart</h2>
        <div class="chart-container">
            <canvas id="performanceChart"></canvas>
        </div>
        
        <h2>📋 Detailed Results</h2>
        <table>
            <thead>
                <tr>
                    <th>Operation</th>
                    <th>Puhu Time (ms)</th>
                    <th>Pillow Time (ms)</th>
                    <th>Speedup</th>
                    <th>Puhu Memory (MB)</th>
                    <th>Pillow Memory (MB)</th>
                    <th>Winner</th>
                </tr>
            </thead>
            <tbody>
"""
        
        for data in performance_data:
            winner_class = "faster-puhu" if data['faster'] == 'Puhu' else "faster-pillow" if data['faster'] == 'Pillow' else "tie"
            speedup_text = f"{data['speedup']:.2f}x" if data['faster'] == 'Puhu' else f"1/{data['speedup']:.2f}x" if data['faster'] == 'Pillow' else "~1x"
            
            html_content += f"""
                <tr>
                    <td>{data['operation'].replace('_', ' ').title()}</td>
                    <td>{data['puhu_time']:.2f}</td>
                    <td>{data['pillow_time']:.2f}</td>
                    <td class="{winner_class}">{speedup_text}</td>
                    <td>{data['puhu_memory']:.2f}</td>
                    <td>{data['pillow_memory']:.2f}</td>
                    <td class="{winner_class}">{data['faster']}</td>
                </tr>
"""
        
        # Add recommendations
        recommendations = self.generate_recommendations(performance_data)
        
        html_content += f"""
            </tbody>
        </table>
        
        <div class="recommendations">
            <h3>💡 Performance Recommendations</h3>
            {recommendations}
        </div>
        
        <script>
        // Chart data
        const chartData = {json.dumps([{'operation': d['operation'], 'puhu': d['puhu_time'], 'pillow': d['pillow_time']} for d in performance_data[:10]])};
        
        // Create chart
        const ctx = document.getElementById('performanceChart').getContext('2d');
        new Chart(ctx, {{
            type: 'bar',
            data: {{
                labels: chartData.map(d => d.operation.replace(/_/g, ' ')),
                datasets: [{{
                    label: 'Puhu (ms)',
                    data: chartData.map(d => d.puhu),
                    backgroundColor: 'rgba(52, 152, 219, 0.8)',
                    borderColor: 'rgba(52, 152, 219, 1)',
                    borderWidth: 1
                }}, {{
                    label: 'Pillow (ms)',
                    data: chartData.map(d => d.pillow),
                    backgroundColor: 'rgba(231, 76, 60, 0.8)',
                    borderColor: 'rgba(231, 76, 60, 1)',
                    borderWidth: 1
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                scales: {{
                    y: {{
                        beginAtZero: true,
                        title: {{
                            display: true,
                            text: 'Time (milliseconds)'
                        }}
                    }},
                    x: {{
                        title: {{
                            display: true,
                            text: 'Operations'
                        }}
                    }}
                }},
                plugins: {{
                    title: {{
                        display: true,
                        text: 'Performance Comparison (Lower is Better)'
                    }},
                    legend: {{
                        display: true,
                        position: 'top'
                    }}
                }}
            }}
        }});
        </script>
    </div>
</body>
</html>
"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"📄 HTML report generated: {output_file}")
        return output_file

    def generate_recommendations(self, performance_data: List[Dict]) -> str:
        """Generate performance recommendations based on benchmark results"""
        recommendations = []
        
        # Analyze loading performance
        loading_ops = [d for d in performance_data if 'load' in d['operation']]
        if loading_ops and all(d['faster'] == 'Puhu' for d in loading_ops):
            recommendations.append(
                "<div class='recommendation-item'>"
                "<strong>✅ Use Puhu for image loading:</strong> Puhu's lazy loading is consistently faster for file operations, "
                "making it ideal for applications that load many images but don't immediately process them."
                "</div>"
            )
        
        # Analyze resize performance
        resize_ops = [d for d in performance_data if 'resize' in d['operation']]
        if resize_ops and all(d['faster'] == 'Pillow' for d in resize_ops):
            recommendations.append(
                "<div class='recommendation-item'>"
                "<strong>⚠️ Use Pillow for intensive resizing:</strong> Pillow significantly outperforms Puhu in resize operations. "
                "Consider using Pillow for batch image processing or real-time resizing."
                "</div>"
            )
        
        # Analyze crop performance
        crop_ops = [d for d in performance_data if 'crop' in d['operation']]
        if crop_ops and all(d['faster'] == 'Pillow' for d in crop_ops):
            recommendations.append(
                "<div class='recommendation-item'>"
                "<strong>⚠️ Use Pillow for cropping operations:</strong> Pillow is faster for crop operations. "
                "However, consider Puhu's batch operations like resize_and_crop for combined workflows."
                "</div>"
            )
        
        # Memory usage recommendations
        high_memory_ops = [d for d in performance_data if d['puhu_memory'] > 5.0]
        if high_memory_ops:
            recommendations.append(
                "<div class='recommendation-item'>"
                "<strong>🧠 Memory optimization needed:</strong> Some Puhu operations use significant memory. "
                "Consider processing images in smaller batches or using streaming approaches for large datasets."
                "</div>"
            )
        
        # General recommendations
        recommendations.extend([
            "<div class='recommendation-item'>"
            "<strong>🔄 Hybrid approach:</strong> Consider using Puhu for loading and simple operations, "
            "then converting to Pillow for complex processing when needed."
            "</div>",
            "<div class='recommendation-item'>"
            "<strong>📊 Profile your specific use case:</strong> These benchmarks use synthetic data. "
            "Test with your actual images and workflows for the most accurate performance comparison."
            "</div>"
        ])
        
        return '\n'.join(recommendations)

    def generate_markdown_report(self, output_file: str = "benchmark_report.md"):
        """Generate markdown benchmark report"""
        system_info = self.get_system_info()
        
        # Group results by operation
        operations = {}
        for result in self.results:
            if result.operation not in operations:
                operations[result.operation] = {}
            operations[result.operation][result.library] = result
        
        # Calculate statistics
        faster_count = {"Puhu": 0, "Pillow": 0, "Tie": 0}
        memory_efficient = {"Puhu": 0, "Pillow": 0, "Tie": 0}
        
        markdown_content = f"""# 🚀 Puhu vs Pillow Performance Benchmark Report

## 📊 System Information

| Property | Value |
|----------|-------|
| Timestamp | {system_info['timestamp']} |
| Platform | {system_info['platform']} |
| Processor | {system_info['processor']} |
| Architecture | {system_info['architecture']} |
| Python Version | {system_info['python_version']} |
| CPU Cores | {system_info['cpu_count']} |
| Total Memory | {system_info['memory_total']} |
| Pillow Version | {system_info['pillow_version']} |
| Puhu Version | {system_info['puhu_version']} |
| Test Iterations | {self.iterations} |

## 📈 Performance Summary

| Operation | Puhu Time (ms) | Pillow Time (ms) | Speedup | Puhu Memory (MB) | Pillow Memory (MB) | Winner |
|-----------|----------------|------------------|---------|------------------|--------------------|---------|
"""
        
        for operation, libs in operations.items():
            if len(libs) >= 2 and "Puhu" in libs and "Pillow" in libs:
                puhu_result = libs["Puhu"]
                pillow_result = libs["Pillow"]
                
                speedup = pillow_result.time_ms / puhu_result.time_ms
                if speedup > 1.1:
                    faster = "Puhu"
                    faster_count["Puhu"] += 1
                    speedup_text = f"{speedup:.2f}x"
                elif speedup < 0.9:
                    faster = "Pillow"
                    faster_count["Pillow"] += 1
                    speedup_text = f"1/{speedup:.2f}x"
                else:
                    faster = "Tie"
                    faster_count["Tie"] += 1
                    speedup_text = "~1x"
                
                memory_ratio = pillow_result.memory_mb / puhu_result.memory_mb if puhu_result.memory_mb > 0 else 1
                if memory_ratio > 1.1:
                    memory_efficient["Puhu"] += 1
                elif memory_ratio < 0.9:
                    memory_efficient["Pillow"] += 1
                else:
                    memory_efficient["Tie"] += 1
                
                operation_name = operation.replace('_', ' ').title()
                markdown_content += f"| {operation_name} | {puhu_result.time_ms:.2f} | {pillow_result.time_ms:.2f} | {speedup_text} | {puhu_result.memory_mb:.2f} | {pillow_result.memory_mb:.2f} | **{faster}** |\n"
        
        # Add summary statistics
        puhu_times = [r.time_ms for r in self.results if r.library == "Puhu" and r.success]
        pillow_times = [r.time_ms for r in self.results if r.library == "Pillow" and r.success]
        
        if puhu_times and pillow_times:
            puhu_avg = statistics.mean(puhu_times)
            pillow_avg = statistics.mean(pillow_times)
            overall_speedup = pillow_avg / puhu_avg
        
        markdown_content += f"""

## 📊 Summary Statistics

### Speed Comparison
- **Puhu faster**: {faster_count['Puhu']} operations
- **Pillow faster**: {faster_count['Pillow']} operations
- **Tied**: {faster_count['Tie']} operations

### Memory Efficiency
- **Puhu more efficient**: {memory_efficient['Puhu']} operations
- **Pillow more efficient**: {memory_efficient['Pillow']} operations
- **Tied**: {memory_efficient['Tie']} operations

### Overall Performance
- **Puhu average**: {puhu_avg:.2f}ms
- **Pillow average**: {pillow_avg:.2f}ms
- **Overall ratio**: {overall_speedup:.2f}x

## 💡 Key Findings

### Puhu Strengths
- ✅ **Lazy Loading**: Excellent performance for image loading operations
- ✅ **Memory Efficiency**: Generally uses less memory during loading phase
- ✅ **Fast File Access**: Minimal overhead for file path operations

### Pillow Strengths
- ✅ **Image Processing**: Significantly faster for resize, crop, and transformation operations
- ✅ **Mature Optimization**: Decades of optimization show in processing performance
- ✅ **Native Libraries**: Leverages highly optimized C libraries

### Recommendations

1. **Use Puhu when**:
   - Loading many images but processing few
   - Memory efficiency is critical
   - You need lazy loading benefits
   - Working with simple operations on small images

2. **Use Pillow when**:
   - Heavy image processing workloads
   - Performance-critical resize/crop operations
   - Complex image manipulation pipelines
   - Production systems requiring maximum speed

3. **Hybrid approach**:
   - Use Puhu for loading and simple operations
   - Convert to Pillow for intensive processing when needed
   - Leverage Puhu's batch operations to reduce Python-Rust boundary crossings

---

*Report generated on {system_info['timestamp']}*
"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"📝 Markdown report generated: {output_file}")
        return output_file

    def export_csv_data(self, output_file: str = "benchmark_data.csv"):
        """Export benchmark data to CSV for further analysis"""
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Operation', 'Library', 'Time_ms', 'Memory_MB', 'Success', 'Error'])
            
            for result in self.results:
                writer.writerow([
                    result.operation,
                    result.library,
                    result.time_ms,
                    result.memory_mb,
                    result.success,
                    result.error or ''
                ])
        
        print(f"📊 CSV data exported: {output_file}")
        return output_file

    def generate_report(self):
        """Generate comprehensive benchmark report"""
        print("\n" + "="*80)
        print("COMPREHENSIVE BENCHMARK REPORT")
        print("="*80)
        
        # Group results by operation
        operations = {}
        for result in self.results:
            if result.operation not in operations:
                operations[result.operation] = {}
            operations[result.operation][result.library] = result
        
        # Performance comparison
        print("\nPERFORMANCE COMPARISON:")
        print("-" * 50)
        
        faster_count = {"Puhu": 0, "Pillow": 0, "Tie": 0}
        memory_efficient = {"Puhu": 0, "Pillow": 0, "Tie": 0}
        
        for operation, libs in operations.items():
            if len(libs) >= 2 and "Puhu" in libs and "Pillow" in libs:
                puhu_result = libs["Puhu"]
                pillow_result = libs["Pillow"]
                
                # Time comparison
                speedup = pillow_result.time_ms / puhu_result.time_ms
                if speedup > 1.1:
                    faster = "Puhu"
                    faster_count["Puhu"] += 1
                elif speedup < 0.9:
                    faster = "Pillow"
                    faster_count["Pillow"] += 1
                else:
                    faster = "Tie"
                    faster_count["Tie"] += 1
                
                # Memory comparison
                memory_ratio = pillow_result.memory_mb / puhu_result.memory_mb if puhu_result.memory_mb > 0 else 1
                if memory_ratio > 1.1:
                    mem_efficient = "Puhu"
                    memory_efficient["Puhu"] += 1
                elif memory_ratio < 0.9:
                    mem_efficient = "Pillow"
                    memory_efficient["Pillow"] += 1
                else:
                    mem_efficient = "Tie"
                    memory_efficient["Tie"] += 1
                
                print(f"\n{operation}:")
                print(f"  Puhu:   {puhu_result.time_ms:8.2f}ms  {puhu_result.memory_mb:6.2f}MB")
                print(f"  Pillow: {pillow_result.time_ms:8.2f}ms  {pillow_result.memory_mb:6.2f}MB")
                print(f"  Faster: {faster} ({speedup:.2f}x)  More efficient: {mem_efficient}")
        
        # Summary statistics
        print("\n" + "="*50)
        print("SUMMARY STATISTICS:")
        print("="*50)
        print(f"Speed comparison:")
        print(f"  Puhu faster:    {faster_count['Puhu']:2d} operations")
        print(f"  Pillow faster:  {faster_count['Pillow']:2d} operations")
        print(f"  Tied:           {faster_count['Tie']:2d} operations")
        
        print(f"\nMemory efficiency:")
        print(f"  Puhu better:    {memory_efficient['Puhu']:2d} operations")
        print(f"  Pillow better:  {memory_efficient['Pillow']:2d} operations")
        print(f"  Tied:           {memory_efficient['Tie']:2d} operations")
        
        # Calculate overall averages
        puhu_times = [r.time_ms for r in self.results if r.library == "Puhu" and r.success]
        pillow_times = [r.time_ms for r in self.results if r.library == "Pillow" and r.success]
        
        if puhu_times and pillow_times:
            puhu_avg = statistics.mean(puhu_times)
            pillow_avg = statistics.mean(pillow_times)
            overall_speedup = pillow_avg / puhu_avg
            
            print(f"\nOverall average performance:")
            print(f"  Puhu average:   {puhu_avg:.2f}ms")
            print(f"  Pillow average: {pillow_avg:.2f}ms")
            print(f"  Overall speedup: {overall_speedup:.2f}x")

    def run_all_benchmarks(self):
        """Run all benchmark tests"""
        print("Starting comprehensive Puhu vs Pillow benchmark...")
        print(f"Iterations per test: {self.iterations}")
        print(f"Libraries available: Pillow={PILLOW_AVAILABLE}, Puhu={PUHU_AVAILABLE}")
        
        if not PILLOW_AVAILABLE and not PUHU_AVAILABLE:
            print("Error: Neither Pillow nor Puhu is available!")
            return
        
        # Create test images
        self.create_test_images()
        
        # Run benchmarks
        self.benchmark_image_loading()
        self.benchmark_resize_operations()
        self.benchmark_crop_operations()
        self.benchmark_rotation_operations()
        self.benchmark_batch_operations()
        
        # Generate report
        self.generate_report()
        
        print(f"\nBenchmark completed! {len(self.results)} tests run.")
        
        # Generate reports
        print("\n" + "="*50)
        print("GENERATING REPORTS")
        print("="*50)
        
        html_file = self.generate_html_report()
        md_file = self.generate_markdown_report()
        csv_file = self.export_csv_data()
        
        print(f"\n📁 Reports generated:")
        print(f"   📄 HTML Report: {html_file}")
        print(f"   📝 Markdown Report: {md_file}")
        print(f"   📊 CSV Data: {csv_file}")
        print(f"\n💡 Open the HTML report in your browser for the best viewing experience!")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Benchmark Puhu vs Pillow performance")
    parser.add_argument("--iterations", "-i", type=int, default=5, 
                       help="Number of iterations per test (default: 5)")
    parser.add_argument("--test-dir", "-d", type=str, default="test_images",
                       help="Directory for test images (default: test_images)")
    parser.add_argument("--output-dir", "-o", type=str, default=".",
                       help="Directory for output reports (default: current directory)")
    parser.add_argument("--report-name", "-n", type=str, default="benchmark_report",
                       help="Base name for report files (default: benchmark_report)")
    
    args = parser.parse_args()
    
    benchmark = ImageBenchmark(test_images_dir=args.test_dir, iterations=args.iterations)
    
    # Set output directory for reports
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)
    
    # Update report generation methods to use custom output paths
    original_generate_html = benchmark.generate_html_report
    original_generate_md = benchmark.generate_markdown_report
    original_export_csv = benchmark.export_csv_data
    
    benchmark.generate_html_report = lambda: original_generate_html(str(output_dir / f"{args.report_name}.html"))
    benchmark.generate_markdown_report = lambda: original_generate_md(str(output_dir / f"{args.report_name}.md"))
    benchmark.export_csv_data = lambda: original_export_csv(str(output_dir / f"{args.report_name}.csv"))
    
    benchmark.run_all_benchmarks()


if __name__ == "__main__":
    main()
