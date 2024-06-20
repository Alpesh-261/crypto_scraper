from celery import shared_task
from .models import Job, Task
from .coinmarket import CoinMarketCap

@shared_task
def scrape_coin_data(job_id, coin):
    job = Job.objects.get(pk=job_id)
    task = Task.objects.create(job=job, coin=coin)
    
    cmc = CoinMarketCap()
    try:
        data = cmc.get_coin_data(coin)
        task.set_data(data)
        task.status = 'completed'
    except Exception as e:
        task.set_data({'error': str(e)})
        task.status = 'failed'
    
    task.save()
    return task.id
