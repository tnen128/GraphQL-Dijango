# simulator/views.py
from django.shortcuts import render
from .models import KPIResult
import json

def results_dashboard(request):
    # Group results by simulator
    simulators_data = {}
    for result in KPIResult.objects.order_by('simulator_id', '-timestamp'):
        if result.simulator_id not in simulators_data:
            simulators_data[result.simulator_id] = {
                'inputs': [],
                'outputs': [],
                'timestamps': []
            }
        simulators_data[result.simulator_id]['inputs'].append(result.input_value)
        simulators_data[result.simulator_id]['outputs'].append(result.output_value)
        simulators_data[result.simulator_id]['timestamps'].append(
            result.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        )

    return render(request, 'simulator/dashboard.html', {
        'simulators_data': json.dumps(simulators_data)
    })