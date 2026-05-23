"""
Health check utilities for the AutoFilterBot.

Provides endpoints and functions for monitoring bot health,
database connectivity, and system resources.
"""

import asyncio
import logging
import time
from datetime import datetime
from typing import Dict, Any, Optional

import psutil
from motor.motor_asyncio import AsyncIOMotorClient

logger = logging.getLogger(__name__)


class HealthCheck:
    """Health check manager for monitoring bot status."""
    
    def __init__(self):
        self.start_time = datetime.now()
        self._last_check: Optional[Dict[str, Any]] = None
        self._check_interval = 60  # seconds
    
    @property
    def uptime(self) -> float:
        """Return bot uptime in seconds."""
        return (datetime.now() - self.start_time).total_seconds()
    
    @property
    def uptime_str(self) -> str:
        """Return formatted uptime string."""
        seconds = int(self.uptime)
        days, remainder = divmod(seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        parts = []
        if days:
            parts.append(f"{days}d")
        if hours:
            parts.append(f"{hours}h")
        if minutes:
            parts.append(f"{minutes}m")
        parts.append(f"{seconds}s")
        
        return " ".join(parts)
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get current system resource usage."""
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return {
            "cpu_percent": cpu_percent,
            "memory": {
                "total": memory.total,
                "available": memory.available,
                "percent": memory.percent,
                "used": memory.used,
            },
            "disk": {
                "total": disk.total,
                "used": disk.used,
                "free": disk.free,
                "percent": disk.percent,
            },
        }
    
    async def check_database(self, db_client: AsyncIOMotorClient) -> Dict[str, Any]:
        """Check database connectivity and latency."""
        start = time.time()
        try:
            # Ping the database
            await db_client.admin.command('ping')
            latency = (time.time() - start) * 1000  # Convert to ms
            
            return {
                "status": "healthy",
                "latency_ms": round(latency, 2),
            }
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return {
                "status": "unhealthy",
                "error": str(e),
            }
    
    async def get_full_status(self, db_client: Optional[AsyncIOMotorClient] = None) -> Dict[str, Any]:
        """Get comprehensive health status."""
        status = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "uptime": self.uptime_str,
            "uptime_seconds": self.uptime,
            "system": self.get_system_stats(),
        }
        
        if db_client:
            status["database"] = await self.check_database(db_client)
            if status["database"]["status"] == "unhealthy":
                status["status"] = "degraded"
        
        self._last_check = status
        return status


# Global health check instance
health_checker = HealthCheck()


def format_bytes(size: int) -> str:
    """Format bytes to human readable string."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} PB"


def get_readable_time(seconds: int) -> str:
    """Convert seconds to readable time format."""
    days, remainder = divmod(seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    result = ""
    if days:
        result += f"{days} day{'s' if days > 1 else ''}, "
    if hours:
        result += f"{hours} hour{'s' if hours > 1 else ''}, "
    if minutes:
        result += f"{minutes} minute{'s' if minutes > 1 else ''}, "
    result += f"{seconds} second{'s' if seconds > 1 else ''}"
    
    return result
