"""
Claude Code Alternative - Async Processor (Phase 3)
Asynchronous processing for improved performance
"""

import asyncio
import concurrent.futures
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass
import time
import threading


@dataclass
class TaskResult:
    """Result of an async task"""
    success: bool
    result: Any
    error: Optional[str] = None
    execution_time: float = 0.0


class AsyncProcessor:
    """Asynchronous task processor with thread pool and asyncio support"""
    
    def __init__(self, max_workers: int = 4, use_asyncio: bool = True):
        """
        Initialize async processor

        Args:
            max_workers: Maximum number of worker threads
            use_asyncio: Use asyncio for async/await support
        """
        self.max_workers = max_workers
        self.use_asyncio = use_asyncio
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
        self.stats = {
            'tasks_submitted': 0,
            'tasks_completed': 0,
            'tasks_failed': 0,
            'total_execution_time': 0.0
        }
    
    async def process_async(self, func: Callable, *args, **kwargs) -> TaskResult:
        """
        Process function asynchronously

        Args:
            func: Function to execute
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            TaskResult with outcome
        """
        self.stats['tasks_submitted'] += 1
        start_time = time.time()
        
        try:
            if asyncio.iscoroutinefunction(func):
                # Async function - await it
                result = await func(*args, **kwargs)
            else:
                # Sync function - run in thread pool
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(
                    self.executor,
                    lambda: func(*args, **kwargs)
                )
            
            execution_time = time.time() - start_time
            self.stats['tasks_completed'] += 1
            self.stats['total_execution_time'] += execution_time
            
            return TaskResult(
                success=True,
                result=result,
                execution_time=execution_time
            )
        
        except Exception as e:
            execution_time = time.time() - start_time
            self.stats['tasks_failed'] += 1
            self.stats['total_execution_time'] += execution_time
            
            return TaskResult(
                success=False,
                result=None,
                error=str(e),
                execution_time=execution_time
            )
    
    async def process_batch_async(
        self,
        func: Callable,
        items: List[Any],
        batch_size: Optional[int] = None,
        **kwargs
    ) -> List[TaskResult]:
        """
        Process multiple items asynchronously in batches

        Args:
            func: Function to apply to each item
            items: List of items to process
            batch_size: Process in batches of this size (None for all at once)
            **kwargs: Additional keyword arguments for function

        Returns:
            List of TaskResults
        """
        if batch_size is None:
            batch_size = len(items)
        
        results = []
        
        for i in range(0, len(items), batch_size):
            batch = items[i:i + batch_size]
            tasks = [
                self.process_async(func, item, **kwargs)
                for item in batch
            ]
            batch_results = await asyncio.gather(*tasks)
            results.extend(batch_results)
        
        return results
    
    def process_sync(self, func: Callable, *args, **kwargs) -> TaskResult:
        """
        Process function synchronously (wrapper for consistency)

        Args:
            func: Function to execute
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            TaskResult with outcome
        """
        if self.use_asyncio and asyncio.iscoroutinefunction(func):
            # Run async function in new event loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                result = loop.run_until_complete(self.process_async(func, *args, **kwargs))
                return result
            finally:
                loop.close()
        else:
            # Run sync function directly
            self.stats['tasks_submitted'] += 1
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                self.stats['tasks_completed'] += 1
                self.stats['total_execution_time'] += execution_time
                
                return TaskResult(
                    success=True,
                    result=result,
                    execution_time=execution_time
                )
            
            except Exception as e:
                execution_time = time.time() - start_time
                self.stats['tasks_failed'] += 1
                self.stats['total_execution_time'] += execution_time
                
                return TaskResult(
                    success=False,
                    result=None,
                    error=str(e),
                    execution_time=execution_time
                )
    
    def process_batch_sync(
        self,
        func: Callable,
        items: List[Any],
        batch_size: Optional[int] = None,
        **kwargs
    ) -> List[TaskResult]:
        """
        Process multiple items synchronously in parallel using thread pool

        Args:
            func: Function to apply to each item
            items: List of items to process
            batch_size: Process in batches of this size (None for all at once)
            **kwargs: Additional keyword arguments for function

        Returns:
            List of TaskResults
        """
        if batch_size is None:
            batch_size = len(items)
        
        results = []
        
        for i in range(0, len(items), batch_size):
            batch = items[i:i + batch_size]
            
            # Use thread pool for parallel execution
            future_to_item = {
                self.executor.submit(func, item, **kwargs): item
                for item in batch
            }
            
            for future in concurrent.futures.as_completed(future_to_item):
                item = future_to_item[future]
                start_time = time.time()
                
                try:
                    result = future.result()
                    execution_time = time.time() - start_time
                    self.stats['tasks_completed'] += 1
                    self.stats['total_execution_time'] += execution_time
                    
                    results.append(TaskResult(
                        success=True,
                        result=result,
                        execution_time=execution_time
                    ))
                except Exception as e:
                    execution_time = time.time() - start_time
                    self.stats['tasks_failed'] += 1
                    self.stats['total_execution_time'] += execution_time
                    
                    results.append(TaskResult(
                        success=False,
                        result=None,
                        error=str(e),
                        execution_time=execution_time
                    ))
        
        self.stats['tasks_submitted'] += len(items)
        return results
    
    def get_stats(self) -> Dict[str, Any]:
        """Get processor statistics"""
        avg_time = (
            self.stats['total_execution_time'] / self.stats['tasks_completed']
            if self.stats['tasks_completed'] > 0
            else 0.0
        )
        
        return {
            **self.stats,
            'success_rate': (
                self.stats['tasks_completed'] / self.stats['tasks_submitted']
                if self.stats['tasks_submitted'] > 0
                else 0.0
            ),
            'average_execution_time': avg_time,
            'max_workers': self.max_workers
        }
    
    def shutdown(self) -> None:
        """Shutdown the executor"""
        self.executor.shutdown(wait=True)


class CodeAnalysisBatchProcessor:
    """Specialized batch processor for code analysis"""
    
    def __init__(self, analyzer: Any, max_workers: int = 4):
        """
        Initialize batch processor for code analysis

        Args:
            analyzer: Code analyzer instance
            max_workers: Maximum number of parallel analyses
        """
        self.analyzer = analyzer
        self.processor = AsyncProcessor(max_workers=max_workers)
    
    async def analyze_batch_async(
        self,
        code_snippets: List[Dict[str, str]],
        batch_size: Optional[int] = 10
    ) -> List[TaskResult]:
        """
        Analyze multiple code snippets asynchronously

        Args:
            code_snippets: List of {'code': str, 'language': str} dicts
            batch_size: Process in batches of this size

        Returns:
            List of TaskResults with analysis metrics
        """
        async def analyze_single(snippet: Dict[str, str]) -> Dict[str, Any]:
            return self.analyzer.analyze_code(
                snippet['code'],
                snippet['language']
            ).__dict__
        
        results = await self.processor.process_batch_async(
            analyze_single,
            code_snippets,
            batch_size=batch_size
        )
        
        return results
    
    def analyze_batch_sync(
        self,
        code_snippets: List[Dict[str, str]],
        batch_size: Optional[int] = 10
    ) -> List[TaskResult]:
        """
        Analyze multiple code snippets synchronously in parallel

        Args:
            code_snippets: List of {'code': str, 'language': str} dicts
            batch_size: Process in batches of this size

        Returns:
            List of TaskResults with analysis metrics
        """
        def analyze_single(snippet: Dict[str, str]) -> Dict[str, Any]:
            return self.analyzer.analyze_code(
                snippet['code'],
                snippet['language']
            ).__dict__
        
        results = self.processor.process_batch_sync(
            analyze_single,
            code_snippets,
            batch_size=batch_size
        )
        
        return results
    
    def get_stats(self) -> Dict[str, Any]:
        """Get batch processor statistics"""
        return self.processor.get_stats()
    
    def shutdown(self) -> None:
        """Shutdown the processor"""
        self.processor.shutdown()


# Example usage
if __name__ == "__main__":
    import sys
    sys.path.append('..')
    from code_analysis.enhanced_analyzer import EnhancedCodeAnalyzer
    
    # Example 1: Async processing
    async def example_async():
        """Example of async processing"""
        processor = AsyncProcessor(max_workers=2)
        
        async def slow_task(n: int) -> int:
            await asyncio.sleep(0.1)
            return n * 2
        
        # Process tasks in parallel
        tasks = list(range(5))
        results = await processor.process_batch_async(slow_task, tasks)
        
        print("Async processing results:")
        for i, result in enumerate(results):
            print(f"  Task {i}: success={result.success}, result={result.result}, time={result.execution_time:.3f}s")
        
        print(f"\nStats: {processor.get_stats()}")
        processor.shutdown()
    
    # Example 2: Code analysis batch processing
    def example_code_analysis():
        """Example of batch code analysis"""
        analyzer = EnhancedCodeAnalyzer()
        batch_processor = CodeAnalysisBatchProcessor(analyzer, max_workers=4)
        
        code_snippets = [
            {'code': 'def hello():\n    print("Hello")', 'language': 'python'},
            {'code': 'function add(a, b) { return a + b; }', 'language': 'javascript'},
            {'code': 'public class Test { }', 'language': 'java'},
            {'code': '#include <iostream>\nint main() { return 0; }', 'language': 'c++'},
        ]
        
        print("\nCode analysis batch processing:")
        start = time.time()
        results = batch_processor.analyze_batch_sync(code_snippets)
        elapsed = time.time() - start
        
        print(f"Analyzed {len(code_snippets)} snippets in {elapsed:.3f}s")
        
        for i, result in enumerate(results):
            if result.success:
                print(f"\n  Snippet {i} ({code_snippets[i]['language']}):")
                print(f"    Lines: {result.result['lines_of_code']}")
                print(f"    Complexity: {result.result['complexity_score']}")
                print(f"    Functions: {result.result['functions_count']}")
                print(f"    Execution time: {result.execution_time:.3f}s")
            else:
                print(f"\n  Snippet {i} failed: {result.error}")
        
        print(f"\nBatch processor stats: {batch_processor.get_stats()}")
        batch_processor.shutdown()
    
    # Run examples
    if len(sys.argv) > 1 and sys.argv[1] == 'async':
        asyncio.run(example_async())
    else:
        example_code_analysis()
