#!/usr/bin/env python3
"""
API Retry Wrapper
Wraps API calls with automatic retry logic
"""

import time
import json
import subprocess
from functools import wraps

class APIRetryWrapper:
    """Wrapper for API calls with retry logic."""
    
    def __init__(self, max_retries=3, backoff_seconds=[1, 5, 15]):
        self.max_retries = max_retries
        self.backoff_seconds = backoff_seconds
        self.call_history = []
    
    def call(self, method, url, **kwargs):
        """
        Make API call with automatic retry.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            url: API endpoint URL
            **kwargs: Additional arguments for requests
            
        Returns:
            dict: Response data or error info
        """
        import requests
        
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                response = requests.request(method, url, timeout=10, **kwargs)
                
                # Log attempt
                self.call_history.append({
                    'url': url,
                    'attempt': attempt + 1,
                    'status': response.status_code,
                    'timestamp': time.time()
                })
                
                # Success
                if response.status_code == 200:
                    return {
                        'success': True,
                        'status': response.status_code,
                        'data': response.json() if response.text else None,
                        'attempts': attempt + 1
                    }
                
                # Server error - retry
                if response.status_code >= 500:
                    last_error = f"Server error {response.status_code}"
                    if attempt < self.max_retries - 1:
                        wait = self.backoff_seconds[min(attempt, len(self.backoff_seconds)-1)]
                        time.sleep(wait)
                        continue
                
                # Client error - don't retry
                if response.status_code >= 400:
                    return {
                        'success': False,
                        'status': response.status_code,
                        'error': f"Client error: {response.status_code}",
                        'attempts': attempt + 1
                    }
                    
            except requests.exceptions.Timeout:
                last_error = "Timeout"
                if attempt < self.max_retries - 1:
                    wait = self.backoff_seconds[min(attempt, len(self.backoff_seconds)-1)]
                    time.sleep(wait)
                    
            except requests.exceptions.ConnectionError:
                last_error = "Connection error"
                if attempt < self.max_retries - 1:
                    wait = self.backoff_seconds[min(attempt, len(self.backoff_seconds)-1)]
                    time.sleep(wait)
                    
            except Exception as e:
                last_error = str(e)
                if attempt < self.max_retries - 1:
                    wait = self.backoff_seconds[min(attempt, len(self.backoff_seconds)-1)]
                    time.sleep(wait)
        
        # All retries failed
        return {
            'success': False,
            'error': last_error or "Unknown error",
            'attempts': self.max_retries,
            'max_retries_reached': True
        }
    
    def get(self, url, **kwargs):
        """Convenience method for GET requests."""
        return self.call('GET', url, **kwargs)
    
    def post(self, url, **kwargs):
        """Convenience method for POST requests."""
        return self.call('POST', url, **kwargs)

# Global instance for agents to use
api_client = APIRetryWrapper()

# Example usage for agents:
if __name__ == "__main__":
    # Test the wrapper
    result = api_client.get('http://localhost:8001/api/v32/or_data')
    print(json.dumps(result, indent=2))
