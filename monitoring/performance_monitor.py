"""
Zeal Code - Performance Monitoring (Phase 4)
Performance tracking and monitoring for production deployment
"""

import time
import json
import threading
from typing import Dict, List, Optional, Any, Callable, Tuple
from dataclasses import dataclass, field
from collections import deque, defaultdict
import statistics


@dataclass
class MetricData:
    """Single metric data point"""
    timestamp: float
    value: float
    labels: Dict[str, str] = field(default_factory=dict)


@dataclass
class PerformanceStats:
    """Aggregated performance statistics"""
    min: float
    max: float
    avg: float
    median: float
    p95: float
    p99: float
    count: int


class PerformanceMonitor:
    """Monitor and track performance metrics"""

    def __init__(self, max_history: int = 1000):
        """
        Initialize performance monitor

        Args:
            max_history: Maximum number of data points to keep per metric
        """
        self.max_history = max_history
        self.metrics: Dict[str, deque] = defaultdict(lambda: deque(maxlen=max_history))
        self.counters: Dict[str, int] = defaultdict(int)
        self.gauges: Dict[str, float] = {}
        self.timers: Dict[str, List[float]] = defaultdict(list)
        self.lock = threading.Lock()

    def record_metric(self, name: str, value: float, labels: Optional[Dict[str, str]] = None) -> None:
        """
        Record a metric value

        Args:
            name: Metric name
            value: Metric value
            labels: Optional labels for the metric
        """
        with self.lock:
            self.metrics[name].append(MetricData(
                timestamp=time.time(),
                value=value,
                labels=labels or {}
            ))

    def increment_counter(self, name: str, value: int = 1, labels: Optional[Dict[str, str]] = None) -> None:
        """
        Increment a counter

        Args:
            name: Counter name
            value: Amount to increment (default: 1)
            labels: Optional labels for the counter
        """
        with self.lock:
            counter_key = self._make_key(name, labels)
            self.counters[counter_key] += value

    def set_gauge(self, name: str, value: float, labels: Optional[Dict[str, str]] = None) -> None:
        """
        Set a gauge value

        Args:
            name: Gauge name
            value: Gauge value
            labels: Optional labels for the gauge
        """
        with self.lock:
            gauge_key = self._make_key(name, labels)
            self.gauges[gauge_key] = value

    def start_timer(self, name: str, labels: Optional[Dict[str, str]] = None) -> float:
        """
        Start a timer and return start time

        Args:
            name: Timer name
            labels: Optional labels for the timer

        Returns:
            Start timestamp
        """
        return time.time()

    def stop_timer(self, name: str, start_time: float, labels: Optional[Dict[str, str]] = None) -> None:
        """
        Stop a timer and record the duration

        Args:
            name: Timer name
            start_time: Start time from start_timer()
            labels: Optional labels for the timer
        """
        duration = time.time() - start_time
        with self.lock:
            timer_key = self._make_key(name, labels)
            self.timers[timer_key].append(duration)
            self.metrics[f"{name}_duration"].append(MetricData(
                timestamp=time.time(),
                value=duration,
                labels=labels or {}
            ))

    def get_metric_stats(self, name: str) -> Optional[PerformanceStats]:
        """
        Get statistics for a metric

        Args:
            name: Metric name

        Returns:
            PerformanceStats or None if no data
        """
        with self.lock:
            data = list(self.metrics[name])

        if not data:
            return None

        values = [d.value for d in data]

        return PerformanceStats(
            min=min(values),
            max=max(values),
            avg=statistics.mean(values),
            median=statistics.median(values),
            p95=self._percentile(values, 95),
            p99=self._percentile(values, 99),
            count=len(values)
        )

    def _percentile(self, values: List[float], percentile: float) -> float:
        """Calculate percentile"""
        sorted_values = sorted(values)
        index = int(len(sorted_values) * percentile / 100)
        return sorted_values[min(index, len(sorted_values) - 1)]

    def _make_key(self, name: str, labels: Optional[Dict[str, str]]) -> str:
        """Create a key with labels"""
        if not labels:
            return name

        label_str = ','.join(f"{k}={v}" for k, v in sorted(labels.items()))
        return f"{name}{{{label_str}}}"

    def get_counter_value(self, name: str, labels: Optional[Dict[str, str]] = None) -> int:
        """Get counter value"""
        with self.lock:
            counter_key = self._make_key(name, labels)
            return self.counters.get(counter_key, 0)

    def get_gauge_value(self, name: str, labels: Optional[Dict[str, str]] = None) -> Optional[float]:
        """Get gauge value"""
        with self.lock:
            gauge_key = self._make_key(name, labels)
            return self.gauges.get(gauge_key)

    def get_timer_stats(self, name: str, labels: Optional[Dict[str, str]] = None) -> Optional[PerformanceStats]:
        """Get timer statistics"""
        with self.lock:
            timer_key = self._make_key(name, labels)
            values = self.timers.get(timer_key, [])

        if not values:
            return None

        return PerformanceStats(
            min=min(values),
            max=max(values),
            avg=statistics.mean(values),
            median=statistics.median(values),
            p95=self._percentile(values, 95),
            p99=self._percentile(values, 99),
            count=len(values)
        )

    def reset_metric(self, name: str) -> None:
        """Reset a specific metric"""
        with self.lock:
            if name in self.metrics:
                self.metrics[name].clear()

    def reset_counter(self, name: str, labels: Optional[Dict[str, str]] = None) -> None:
        """Reset a specific counter"""
        with self.lock:
            counter_key = self._make_key(name, labels)
            if counter_key in self.counters:
                del self.counters[counter_key]

    def reset_gauge(self, name: str, labels: Optional[Dict[str, str]] = None) -> None:
        """Reset a specific gauge"""
        with self.lock:
            gauge_key = self._make_key(name, labels)
            if gauge_key in self.gauges:
                del self.gauges[gauge_key]

    def reset_timer(self, name: str, labels: Optional[Dict[str, str]] = None) -> None:
        """Reset a specific timer"""
        with self.lock:
            timer_key = self._make_key(name, labels)
            if timer_key in self.timers:
                del self.timers[timer_key]

    def get_all_metrics(self) -> Dict[str, Any]:
        """Get all current metric values"""
        with self.lock:
            return {
                'metrics': {
                    name: [d.value for d in data]
                    for name, data in self.metrics.items()
                },
                'counters': dict(self.counters),
                'gauges': dict(self.gauges),
                'timers': {name: stats.__dict__ for name, stats in {
                    name: self.get_timer_stats(name)
                    for name in list(self.timers.keys())
                }.items() if stats is not None}
            }

    def export_metrics(self, filepath: str) -> Tuple[bool, str]:
        """
        Export all metrics to a JSON file

        Args:
            filepath: Path to output file

        Returns:
            (success, message)
        """
        try:
            data = self.get_all_metrics()
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            return True, f"Metrics exported to {filepath}"
        except Exception as e:
            return False, f"Export failed: {str(e)}"

    def reset_all(self) -> None:
        """Reset all metrics"""
        with self.lock:
            self.metrics.clear()
            self.counters.clear()
            self.gauges.clear()
            self.timers.clear()


class PerformanceProfiler:
    """Context manager for profiling code execution"""

    def __init__(self, monitor: PerformanceMonitor, metric_name: str, labels: Optional[Dict[str, str]] = None):
        """
        Initialize profiler

        Args:
            monitor: PerformanceMonitor instance
            metric_name: Name for the timing metric
            labels: Optional labels
        """
        self.monitor = monitor
        self.metric_name = metric_name
        self.labels = labels
        self.start_time = None

    def __enter__(self):
        """Start profiling"""
        self.start_time = self.monitor.start_timer(self.metric_name, self.labels)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stop profiling"""
        if self.start_time:
            self.monitor.stop_timer(self.metric_name, self.start_time, self.labels)


# Example usage
if __name__ == "__main__":
    monitor = PerformanceMonitor(max_history=100)

    # Record metrics
    monitor.record_metric("response_time", 0.123, labels={"endpoint": "/api/analyze"})
    monitor.record_metric("response_time", 0.456, labels={"endpoint": "/api/analyze"})
    monitor.record_metric("response_time", 0.234, labels={"endpoint": "/api/generate"})

    # Increment counters
    monitor.increment_counter("api_requests", labels={"endpoint": "/api/analyze"})
    monitor.increment_counter("api_requests", labels={"endpoint": "/api/generate"})

    # Set gauges
    monitor.set_gauge("active_connections", 42)
    monitor.set_gauge("memory_usage_mb", 512.5)

    # Use timers
    start = monitor.start_timer("code_analysis")
    time.sleep(0.05)  # Simulate work
    monitor.stop_timer("code_analysis", start)

    # Use profiler context manager
    with PerformanceProfiler(monitor, "batch_processing", labels={"batch_size": "10"}):
        time.sleep(0.1)  # Simulate batch processing

    # Get statistics
    print("Response Time Stats (/api/analyze):")
    stats = monitor.get_metric_stats("response_time")
    if stats:
        print(f"  Min: {stats.min:.3f}s")
        print(f"  Max: {stats.max:.3f}s")
        print(f"  Avg: {stats.avg:.3f}s")
        print(f"  P95: {stats.p95:.3f}s")
        print(f"  P99: {stats.p99:.3f}s")

    print("\nCode Analysis Timer Stats:")
    timer_stats = monitor.get_timer_stats("code_analysis")
    if timer_stats:
        print(f"  Min: {timer_stats.min:.3f}s")
        print(f"  Max: {timer_stats.max:.3f}s")
        print(f"  Avg: {timer_stats.avg:.3f}s")
        print(f"  Count: {timer_stats.count}")

    print("\nBatch Processing Timer Stats:")
    batch_stats = monitor.get_timer_stats("batch_processing", labels={"batch_size": "10"})
    if batch_stats:
        print(f"  Min: {batch_stats.min:.3f}s")
        print(f"  Max: {batch_stats.max:.3f}s")
        print(f"  Avg: {batch_stats.avg:.3f}s")

    print("\nCounters:")
    print(f"  API requests (/api/analyze): {monitor.get_counter_value('api_requests', labels={'endpoint': '/api/analyze'})}")
    print(f"  API requests (/api/generate): {monitor.get_counter_value('api_requests', labels={'endpoint': '/api/generate'})}")

    print("\nGauges:")
    print(f"  Active connections: {monitor.get_gauge_value('active_connections')}")
    print(f"  Memory usage: {monitor.get_gauge_value('memory_usage_mb')} MB")

    # Export metrics
    success, message = monitor.export_metrics('/tmp/performance_metrics.json')
    print(f"\nExport: {success}, {message}")

    # Display all metrics
    print("\nAll Metrics:")
    all_metrics = monitor.get_all_metrics()
    print(json.dumps(all_metrics, indent=2))
