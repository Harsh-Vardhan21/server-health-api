from fastapi import APIRouter
import psutil

router = APIRouter()

@router.get("/metrics")
def get_all_metrics():
    return {
        "cpu": get_cpu(),
        "memory": get_memory(),
        "disk": get_disk()
    }

@router.get("/metrics/cpu")
def get_cpu_metrics():
    return get_cpu()

@router.get("/metrics/memory")
def get_memory_metrics():
    return get_memory()

@router.get("/metrics/disk")
def get_disk_metrics():
    return get_disk()

def get_cpu():
    return {
        "usage_percent": psutil.cpu_percent(interval=1),
        "core_count": psutil.cpu_count(),
        "frequency_mhz": round(psutil.cpu_freq().current, 2) if psutil.cpu_freq() else None
    }

def get_memory():
    mem = psutil.virtual_memory()
    return {
        "total_gb": round(mem.total / (1024**3), 2),
        "used_gb": round(mem.used / (1024**3), 2),
        "available_gb": round(mem.available / (1024**3), 2),
        "usage_percent": mem.percent
    }

def get_disk():
    disk = psutil.disk_usage('/')
    return {
        "total_gb": round(disk.total / (1024**3), 2),
        "used_gb": round(disk.used / (1024**3), 2),
        "free_gb": round(disk.free / (1024**3), 2),
        "usage_percent": disk.percent
    }