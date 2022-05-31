from main.models import TaskResult


def searchbar_list(request):
    latest_result = TaskResult.objects.latest('pubDateTime')
    return {"currentDevices": latest_result.IPPort}
