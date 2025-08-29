# Performance Guide

Optimization techniques and best practices for high-performance image processing with Puhu.

## 🚀 Performance Overview

Puhu is designed for high performance with a Rust backend that provides:

- **Memory Safety**: No memory leaks or buffer overflows
- **Zero-Cost Abstractions**: Rust's performance without overhead
- **Parallel Processing**: Multi-threaded operations where beneficial
- **Efficient Memory Management**: Optimized memory allocation and deallocation
- **SIMD Optimizations**: Vectorized operations for supported CPUs

## ⚡ Core Performance Principles

### 1. Method Chaining Efficiency

Puhu's immutable design allows for efficient method chaining:

```python
import puhu

# ✅ Efficient: Chain operations to minimize intermediate allocations
efficient = (img.resize((800, 600))
                .blur(1.0)
                .brightness(20)
                .contrast(1.2)
                .saturate(1.1))

# ❌ Less efficient: Multiple intermediate variables
temp1 = img.resize((800, 600))
temp2 = temp1.blur(1.0)
temp3 = temp2.brightness(20)
temp4 = temp3.contrast(1.2)
result = temp4.saturate(1.1)
```

### 2. Lazy Loading

Images are loaded lazily when first accessed:

```python
# Image metadata is available immediately
img = puhu.open("large_image.jpg")
print(f"Size: {img.size}")  # Fast - no pixel data loaded yet

# Pixel data is loaded on first operation
resized = img.resize((400, 300))  # Now pixel data is loaded and processed
```

### 3. Memory-Efficient Operations

Operations are designed to minimize memory usage:

```python
# Memory usage is optimized internally
large_img = puhu.open("10MP_image.jpg")

# Each operation reuses memory efficiently
processed = (large_img
             .resize((2000, 1500))  # Efficient resizing
             .blur(2.0)             # In-place-style processing
             .sharpen(1.2))         # Optimized memory usage
```

## 📊 Performance Benchmarks

### Operation Speed Comparison

Here are typical performance characteristics (times will vary by hardware):

```python
import time
import puhu

def benchmark_operations(img, iterations=10):
    """Benchmark common operations."""
    operations = {
        "resize": lambda x: x.resize((800, 600)),
        "blur": lambda x: x.blur(2.0),
        "sharpen": lambda x: x.sharpen(1.5),
        "brightness": lambda x: x.brightness(20),
        "contrast": lambda x: x.contrast(1.2),
        "saturate": lambda x: x.saturate(1.1),
        "edge_detect": lambda x: x.edge_detect(),
        "sepia": lambda x: x.sepia(0.8),
    }
    
    results = {}
    
    for op_name, op_func in operations.items():
        times = []
        
        for _ in range(iterations):
            start = time.time()
            result = op_func(img)
            end = time.time()
            times.append(end - start)
        
        avg_time = sum(times) / len(times)
        results[op_name] = avg_time
        print(f"{op_name:12}: {avg_time:.4f}s avg")
    
    return results

# Run benchmark
img = puhu.open("test_image.jpg")
benchmark_results = benchmark_operations(img)
```

### Memory Usage Patterns

```python
import psutil
import os

def monitor_memory_usage(func, *args, **kwargs):
    """Monitor memory usage during function execution."""
    process = psutil.Process(os.getpid())
    
    # Memory before
    mem_before = process.memory_info().rss / 1024 / 1024  # MB
    
    # Execute function
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    
    # Memory after
    mem_after = process.memory_info().rss / 1024 / 1024  # MB
    
    print(f"Execution time: {end_time - start_time:.4f}s")
    print(f"Memory before: {mem_before:.1f} MB")
    print(f"Memory after: {mem_after:.1f} MB")
    print(f"Memory delta: {mem_after - mem_before:.1f} MB")
    
    return result

# Monitor memory usage
def heavy_processing(img):
    return (img.resize((1920, 1080))
              .blur(3.0)
              .sharpen(2.0)
              .brightness(30)
              .contrast(1.3))

img = puhu.open("large_image.jpg")
result = monitor_memory_usage(heavy_processing, img)
```

## 🔧 Optimization Techniques

### 1. Batch Processing

Process multiple images efficiently:

```python
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import time

def process_single_image(args):
    """Process a single image with error handling."""
    input_path, output_path, operations = args
    
    try:
        img = puhu.open(input_path)
        
        # Apply operations in sequence
        result = img
        for op_name, op_args in operations:
            if op_name == "resize":
                result = result.resize(op_args)
            elif op_name == "enhance":
                brightness, contrast, saturation = op_args
                result = (result.brightness(brightness)
                               .contrast(contrast)
                               .saturate(saturation))
            elif op_name == "filter":
                filter_type, strength = op_args
                if filter_type == "blur":
                    result = result.blur(strength)
                elif filter_type == "sharpen":
                    result = result.sharpen(strength)
        
        result.save(output_path)
        return f"✓ {input_path}"
        
    except Exception as e:
        return f"✗ {input_path}: {e}"

def batch_process_threaded(input_dir, output_dir, operations, max_workers=4):
    """Process images using thread pool for I/O bound operations."""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Prepare arguments
    tasks = []
    for img_file in input_path.glob("*.jpg"):
        output_file = output_path / img_file.name
        tasks.append((str(img_file), str(output_file), operations))
    
    # Process with thread pool
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(process_single_image, tasks))
    
    end_time = time.time()
    
    # Report results
    successful = sum(1 for r in results if r.startswith("✓"))
    total_time = end_time - start_time
    
    print(f"Processed {successful}/{len(tasks)} images in {total_time:.2f}s")
    print(f"Average: {total_time/len(tasks):.3f}s per image")
    
    return results

# Usage
operations = [
    ("resize", (800, 600)),
    ("enhance", (10, 1.1, 1.05)),  # brightness, contrast, saturation
    ("filter", ("sharpen", 1.1)),
]

results = batch_process_threaded("input", "output", operations, max_workers=6)
```

### 2. Memory-Conscious Processing

Handle large images efficiently:

```python
def process_large_image_efficiently(image_path, max_dimension=2048):
    """Process large images with memory optimization."""
    img = puhu.open(image_path)
    original_size = img.size
    
    print(f"Original size: {original_size}")
    
    # Step 1: Resize if too large (reduces memory for subsequent operations)
    if max(img.width, img.height) > max_dimension:
        # Calculate new size maintaining aspect ratio
        if img.width > img.height:
            new_width = max_dimension
            new_height = int(img.height * (max_dimension / img.width))
        else:
            new_height = max_dimension
            new_width = int(img.width * (max_dimension / img.height))
        
        print(f"Resizing to: ({new_width}, {new_height})")
        img = img.resize((new_width, new_height))
    
    # Step 2: Apply processing operations
    processed = (img
                 .brightness(15)
                 .contrast(1.1)
                 .saturate(1.05)
                 .sharpen(1.1))
    
    # Step 3: Resize back up if needed (for final output)
    if max(original_size) > max_dimension:
        # Scale back up, but not necessarily to original size
        target_size = (min(original_size[0], max_dimension * 2),
                      min(original_size[1], max_dimension * 2))
        processed = processed.resize(target_size)
        print(f"Final size: {target_size}")
    
    return processed

# Process very large image efficiently
large_result = process_large_image_efficiently("huge_image.jpg", 1500)
large_result.save("processed_huge_image.jpg")
```

### 3. Progressive Processing

Process images progressively for better user experience:

```python
def progressive_enhancement(img, steps=5):
    """Apply enhancements progressively with intermediate results."""
    results = {"original": img}
    current = img
    
    # Define progressive steps
    enhancement_steps = [
        ("brightness", lambda x: x.brightness(5)),
        ("contrast", lambda x: x.contrast(1.05)),
        ("saturation", lambda x: x.saturate(1.03)),
        ("sharpening", lambda x: x.sharpen(1.05)),
        ("final_polish", lambda x: x.brightness(3).contrast(1.02)),
    ]
    
    for i, (step_name, enhancement) in enumerate(enhancement_steps[:steps]):
        current = enhancement(current)
        results[f"step_{i+1}_{step_name}"] = current
        print(f"Completed step {i+1}: {step_name}")
    
    return results

# Create progressive enhancement
img = puhu.open("photo.jpg")
progressive_results = progressive_enhancement(img, 4)

# Save intermediate results
for step_name, step_img in progressive_results.items():
    step_img.save(f"progressive_{step_name}.jpg")
```

### 4. Caching and Memoization

Cache expensive operations:

```python
from functools import lru_cache
import hashlib

class ImageProcessor:
    """Image processor with caching capabilities."""
    
    def __init__(self, cache_size=128):
        self.cache_size = cache_size
        self._setup_cache()
    
    def _setup_cache(self):
        """Setup LRU cache for expensive operations."""
        self._cached_resize = lru_cache(maxsize=self.cache_size)(self._resize_impl)
        self._cached_filter = lru_cache(maxsize=self.cache_size)(self._filter_impl)
    
    def _get_image_hash(self, img):
        """Generate hash for image caching."""
        # Simple hash based on image properties
        return hash((img.size, img.mode, str(img.to_bytes()[:1000])))
    
    def _resize_impl(self, img_hash, size, resample):
        """Cached resize implementation."""
        # This would need the actual image, but demonstrates the concept
        print(f"Cache miss: resizing to {size}")
        return img_hash  # Placeholder
    
    def _filter_impl(self, img_hash, filter_type, strength):
        """Cached filter implementation."""
        print(f"Cache miss: applying {filter_type} with strength {strength}")
        return img_hash  # Placeholder
    
    def process_with_cache(self, img, operations):
        """Process image with caching."""
        img_hash = self._get_image_hash(img)
        result = img
        
        for op_type, params in operations:
            if op_type == "resize":
                # Use cached resize
                self._cached_resize(img_hash, params[0], params[1])
                result = result.resize(params[0])
            elif op_type == "filter":
                # Use cached filter
                self._cached_filter(img_hash, params[0], params[1])
                if params[0] == "blur":
                    result = result.blur(params[1])
                elif params[0] == "sharpen":
                    result = result.sharpen(params[1])
        
        return result

# Usage
processor = ImageProcessor(cache_size=64)
img = puhu.open("photo.jpg")

operations = [
    ("resize", ((800, 600), "BILINEAR")),
    ("filter", ("blur", 1.5)),
    ("filter", ("sharpen", 1.2)),
]

# First call - cache misses
result1 = processor.process_with_cache(img, operations)

# Second call with same operations - cache hits
result2 = processor.process_with_cache(img, operations)
```

## 🎯 Specific Optimization Strategies

### 1. Image Format Optimization

Choose the right format for your use case:

```python
def optimize_image_format(img, use_case="web"):
    """Optimize image format based on use case."""
    
    if use_case == "web":
        # For web: balance quality and file size
        if img.mode == "RGBA" or "transparency" in str(img.format).lower():
            # Use PNG for images with transparency
            return img, "PNG"
        else:
            # Use JPEG for photos without transparency
            return img.convert("RGB"), "JPEG"
    
    elif use_case == "print":
        # For print: maximum quality
        return img.convert("RGB"), "TIFF"
    
    elif use_case == "thumbnail":
        # For thumbnails: small file size
        thumbnail = img.copy()
        thumbnail.thumbnail((200, 200))
        return thumbnail.convert("RGB"), "JPEG"
    
    elif use_case == "archive":
        # For archival: lossless compression
        return img, "PNG"
    
    return img, "PNG"  # Default

def batch_optimize_formats(input_dir, output_dir):
    """Optimize image formats for different use cases."""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    for use_case in ["web", "thumbnail", "print"]:
        case_dir = output_path / use_case
        case_dir.mkdir(parents=True, exist_ok=True)
        
        for img_file in input_path.glob("*.jpg"):
            img = puhu.open(img_file)
            optimized_img, format_ext = optimize_image_format(img, use_case)
            
            output_file = case_dir / f"{img_file.stem}.{format_ext.lower()}"
            optimized_img.save(output_file, format=format_ext)
            
            print(f"{use_case}: {img_file.name} -> {output_file.name}")

# Optimize images for different use cases
batch_optimize_formats("source_images", "optimized_images")
```

### 2. Parallel Processing Strategies

Choose the right parallelization approach:

```python
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

def cpu_intensive_processing(img):
    """CPU-intensive image processing."""
    return (img
            .blur(3.0)           # CPU intensive
            .edge_detect()       # CPU intensive
            .sharpen(2.0)        # CPU intensive
            .contrast(1.5))      # CPU intensive

def io_intensive_processing(image_path):
    """I/O-intensive image processing."""
    img = puhu.open(image_path)      # I/O intensive
    processed = img.brightness(20).saturate(1.1)
    processed.save(f"processed_{Path(image_path).name}")  # I/O intensive
    return f"Processed {image_path}"

def choose_parallelization_strategy(task_type, image_paths, max_workers=None):
    """Choose optimal parallelization strategy based on task type."""
    
    if max_workers is None:
        max_workers = mp.cpu_count()
    
    if task_type == "cpu_intensive":
        # Use ProcessPoolExecutor for CPU-bound tasks
        print(f"Using ProcessPoolExecutor with {max_workers} workers")
        
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            # Load images first (can't pickle Puhu images across processes easily)
            images = [puhu.open(path) for path in image_paths]
            results = list(executor.map(cpu_intensive_processing, images))
        
        return results
    
    elif task_type == "io_intensive":
        # Use ThreadPoolExecutor for I/O-bound tasks
        print(f"Using ThreadPoolExecutor with {max_workers * 2} workers")
        
        with ThreadPoolExecutor(max_workers=max_workers * 2) as executor:
            results = list(executor.map(io_intensive_processing, image_paths))
        
        return results
    
    else:
        # Sequential processing
        print("Using sequential processing")
        return [io_intensive_processing(path) for path in image_paths]

# Example usage
image_files = ["img1.jpg", "img2.jpg", "img3.jpg", "img4.jpg"]

# For CPU-intensive tasks
cpu_results = choose_parallelization_strategy("cpu_intensive", image_files, 4)

# For I/O-intensive tasks
io_results = choose_parallelization_strategy("io_intensive", image_files, 4)
```

### 3. Memory Pool Management

Manage memory efficiently for batch processing:

```python
class ImageMemoryPool:
    """Memory pool for efficient image processing."""
    
    def __init__(self, max_memory_mb=1024):
        self.max_memory_mb = max_memory_mb
        self.current_memory_mb = 0
        self.processed_count = 0
    
    def estimate_image_memory(self, img):
        """Estimate memory usage for an image."""
        # Rough estimate: width * height * channels * bytes_per_channel
        channels = len(img.mode)
        return (img.width * img.height * channels) / (1024 * 1024)  # MB
    
    def can_process_image(self, img):
        """Check if image can be processed within memory limits."""
        estimated_memory = self.estimate_image_memory(img)
        return (self.current_memory_mb + estimated_memory) <= self.max_memory_mb
    
    def process_with_memory_management(self, image_paths, processing_func):
        """Process images with memory management."""
        results = []
        batch = []
        batch_memory = 0
        
        for image_path in image_paths:
            try:
                img = puhu.open(image_path)
                img_memory = self.estimate_image_memory(img)
                
                # Check if we need to process current batch
                if batch and (batch_memory + img_memory > self.max_memory_mb):
                    # Process current batch
                    print(f"Processing batch of {len(batch)} images ({batch_memory:.1f} MB)")
                    batch_results = self._process_batch(batch, processing_func)
                    results.extend(batch_results)
                    
                    # Reset batch
                    batch = []
                    batch_memory = 0
                
                # Add to current batch
                batch.append((image_path, img))
                batch_memory += img_memory
                
            except Exception as e:
                print(f"Error loading {image_path}: {e}")
        
        # Process final batch
        if batch:
            print(f"Processing final batch of {len(batch)} images ({batch_memory:.1f} MB)")
            batch_results = self._process_batch(batch, processing_func)
            results.extend(batch_results)
        
        return results
    
    def _process_batch(self, batch, processing_func):
        """Process a batch of images."""
        batch_results = []
        
        for image_path, img in batch:
            try:
                result = processing_func(img)
                output_path = f"processed_{Path(image_path).name}"
                result.save(output_path)
                batch_results.append(output_path)
                self.processed_count += 1
                
            except Exception as e:
                print(f"Error processing {image_path}: {e}")
        
        return batch_results

# Usage
def enhancement_processing(img):
    """Standard enhancement processing."""
    return (img
            .resize((1200, 800))
            .brightness(10)
            .contrast(1.1)
            .saturate(1.05)
            .sharpen(1.1))

# Process with memory management
memory_pool = ImageMemoryPool(max_memory_mb=512)  # 512 MB limit
image_files = [f"image_{i}.jpg" for i in range(1, 21)]  # 20 images

results = memory_pool.process_with_memory_management(image_files, enhancement_processing)
print(f"Processed {memory_pool.processed_count} images successfully")
```

## 📈 Performance Monitoring

### 1. Real-time Performance Tracking

```python
import time
import psutil
import threading
from collections import deque

class PerformanceMonitor:
    """Real-time performance monitoring for image processing."""
    
    def __init__(self, window_size=10):
        self.window_size = window_size
        self.processing_times = deque(maxlen=window_size)
        self.memory_usage = deque(maxlen=window_size)
        self.start_time = None
        self.monitoring = False
        self.monitor_thread = None
    
    def start_monitoring(self):
        """Start performance monitoring."""
        self.monitoring = True
        self.start_time = time.time()
        self.monitor_thread = threading.Thread(target=self._monitor_loop)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop performance monitoring."""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join()
    
    def _monitor_loop(self):
        """Monitoring loop running in separate thread."""
        process = psutil.Process()
        
        while self.monitoring:
            memory_mb = process.memory_info().rss / 1024 / 1024
            self.memory_usage.append(memory_mb)
            time.sleep(0.1)  # Monitor every 100ms
    
    def record_processing_time(self, processing_time):
        """Record processing time for an operation."""
        self.processing_times.append(processing_time)
    
    def get_stats(self):
        """Get current performance statistics."""
        if not self.processing_times:
            return None
        
        avg_processing_time = sum(self.processing_times) / len(self.processing_times)
        max_processing_time = max(self.processing_times)
        min_processing_time = min(self.processing_times)
        
        if self.memory_usage:
            avg_memory = sum(self.memory_usage) / len(self.memory_usage)
            max_memory = max(self.memory_usage)
        else:
            avg_memory = max_memory = 0
        
        total_time = time.time() - self.start_time if self.start_time else 0
        
        return {
            "avg_processing_time": avg_processing_time,
            "max_processing_time": max_processing_time,
            "min_processing_time": min_processing_time,
            "avg_memory_mb": avg_memory,
            "max_memory_mb": max_memory,
            "total_time": total_time,
            "operations_count": len(self.processing_times),
        }
    
    def print_stats(self):
        """Print current performance statistics."""
        stats = self.get_stats()
        if not stats:
            print("No performance data available")
            return
        
        print("\n" + "="*50)
        print("PERFORMANCE STATISTICS")
        print("="*50)
        print(f"Operations processed: {stats['operations_count']}")
        print(f"Total time: {stats['total_time']:.2f}s")
        print(f"Avg processing time: {stats['avg_processing_time']:.4f}s")
        print(f"Min processing time: {stats['min_processing_time']:.4f}s")
        print(f"Max processing time: {stats['max_processing_time']:.4f}s")
        print(f"Avg memory usage: {stats['avg_memory_mb']:.1f} MB")
        print(f"Max memory usage: {stats['max_memory_mb']:.1f} MB")
        print(f"Throughput: {stats['operations_count'] / stats['total_time']:.2f} ops/sec")
        print("="*50)

def monitored_processing(image_paths, processing_func):
    """Process images with performance monitoring."""
    monitor = PerformanceMonitor(window_size=20)
    monitor.start_monitoring()
    
    results = []
    
    try:
        for image_path in image_paths:
            start_time = time.time()
            
            # Process image
            img = puhu.open(image_path)
            result = processing_func(img)
            output_path = f"monitored_{Path(image_path).name}"
            result.save(output_path)
            
            # Record timing
            processing_time = time.time() - start_time
            monitor.record_processing_time(processing_time)
            
            results.append(output_path)
            
            # Print progress every 10 images
            if len(results) % 10 == 0:
                monitor.print_stats()
    
    finally:
        monitor.stop_monitoring()
        monitor.print_stats()
    
    return results

# Usage
def standard_processing(img):
    return (img
            .resize((800, 600))
            .brightness(15)
            .contrast(1.1)
            .sharpen(1.1))

image_files = [f"test_image_{i}.jpg" for i in range(1, 51)]  # 50 images
monitored_results = monitored_processing(image_files, standard_processing)
```

### 2. Profiling and Bottleneck Detection

```python
import cProfile
import pstats
from functools import wraps

def profile_function(func):
    """Decorator to profile function performance."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        profiler = cProfile.Profile()
        profiler.enable()
        
        try:
            result = func(*args, **kwargs)
        finally:
            profiler.disable()
            
            # Print profiling results
            stats = pstats.Stats(profiler)
            stats.sort_stats('cumulative')
            print(f"\nProfiling results for {func.__name__}:")
            stats.print_stats(10)  # Top 10 functions
        
        return result
    
    return wrapper

@profile_function
def complex_image_processing(img):
    """Complex processing pipeline for profiling."""
    # Step 1: Resize
    resized = img.resize((1200, 800))
    
    # Step 2: Multiple filters
    filtered = (resized
                .blur(2.0)
                .sharpen(1.5)
                .edge_detect()
                .brightness(20)
                .contrast(1.3)
                .saturate(1.2))
    
    # Step 3: Color effects
    colored = (filtered
               .sepia(0.3)
               .hue_rotate(15)
               .invert(0.1))
    
    # Step 4: Final adjustments
    final = (colored
             .brightness(-10)
             .contrast(0.9)
             .blur(0.5))
    
    return final

# Profile the complex processing
img = puhu.open("test_image.jpg")
profiled_result = complex_image_processing(img)
```

## 🎯 Best Practices Summary

### ✅ Do's

1. **Chain Operations**: Use method chaining for efficiency
2. **Batch Process**: Process multiple images together
3. **Choose Right Parallelization**: Threads for I/O, processes for CPU
4. **Monitor Memory**: Keep track of memory usage for large batches
5. **Optimize Image Sizes**: Resize large images before heavy processing
6. **Use Appropriate Formats**: Choose formats based on use case
7. **Profile Performance**: Identify bottlenecks in your processing pipeline

### ❌ Don'ts

1. **Don't Create Unnecessary Intermediates**: Avoid storing every step
2. **Don't Process Oversized Images**: Resize first if possible
3. **Don't Ignore Memory Limits**: Monitor and manage memory usage
4. **Don't Use Wrong Parallelization**: Match strategy to workload type
5. **Don't Skip Error Handling**: Always handle processing errors gracefully
6. **Don't Forget to Profile**: Measure before optimizing

### 🔧 Quick Optimization Checklist

```python
def optimized_image_processing_template(image_paths, max_workers=4):
    """Template for optimized image processing."""
    
    def process_single_image(image_path):
        try:
            # 1. Load image
            img = puhu.open(image_path)
            
            # 2. Check size and resize if too large
            if max(img.width, img.height) > 2048:
                scale = 2048 / max(img.width, img.height)
                new_size = (int(img.width * scale), int(img.height * scale))
                img = img.resize(new_size)
            
            # 3. Chain operations efficiently
            result = (img
                     .brightness(10)      # Fast operation
                     .contrast(1.1)       # Fast operation
                     .saturate(1.05)      # Fast operation
                     .sharpen(1.1))       # Moderate operation
            
            # 4. Save with appropriate format
            output_path = f"optimized_{Path(image_path).name}"
            if result.mode == "RGBA":
                result.save(output_path.replace('.jpg', '.png'), format="PNG")
            else:
                result.save(output_path, format="JPEG")
            
            return output_path
            
        except Exception as e:
            return f"Error: {image_path} - {e}"
    
    # 5. Use appropriate parallelization
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(process_single_image, image_paths))
    
    return results

# Usage
image_files = ["img1.jpg", "img2.jpg", "img3.jpg"]
optimized_results = optimized_image_processing_template(image_files, max_workers=6)
```

## 🔗 Next Steps

- **[Examples](examples.md)** - Real-world performance examples
- **[API Reference](api-reference.md)** - Complete method documentation
- **[Migration Guide](migration.md)** - Migrating from Pillow efficiently
- **[Contributing](contributing.md)** - Contributing performance improvements