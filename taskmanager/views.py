from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Job, Task
from .task import scrape_coin_data

class StartScraping(APIView):
    def post(self, request):
        coins = request.data
        if not all(isinstance(coin, str) for coin in coins):
            return Response({"error": "Invalid input"}, status=status.HTTP_400_BAD_REQUEST)
        
        job = Job.objects.create()
        for coin in coins:
            scrape_coin_data.delay(job.job_id, coin)
        
        return Response({"job_id": job.job_id}, status=status.HTTP_202_ACCEPTED)

class ScrapingStatus(APIView):
    def get(self, request, job_id):
        job = Job.objects.get(pk=job_id)
        tasks = job.tasks.all()
        task_data = []
        
        for task in tasks:
            task_data.append({
                'coin': task.coin,
                'output': task.get_data()  # Use get_data to deserialize
            })
        
        return Response({
            'job_id': job.job_id,
            'tasks': task_data
        })
