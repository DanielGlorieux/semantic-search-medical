import time
from typing import List, Dict
import numpy as np

class MetricsCollector:
    def __init__(self):
        self.queries = []
        self.latencies = []
        self.timestamps = []
    
    def add_query(self, query: str, latency: float):
        """Record a query and its latency"""
        self.queries.append(query)
        self.latencies.append(latency)
        self.timestamps.append(time.time())
    
    def get_summary(self) -> Dict:
        """Get summary statistics"""
        if not self.latencies:
            return {
                'total_queries': 0,
                'avg_latency': 0,
                'min_latency': 0,
                'max_latency': 0
            }
        
        return {
            'total_queries': len(self.queries),
            'avg_latency': np.mean(self.latencies),
            'min_latency': np.min(self.latencies),
            'max_latency': np.max(self.latencies),
            'median_latency': np.median(self.latencies)
        }
    
    def reset(self):
        """Reset all metrics"""
        self.queries = []
        self.latencies = []
        self.timestamps = []
